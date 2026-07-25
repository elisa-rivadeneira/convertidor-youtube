from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import threading
import uuid
import logging
import time
from datetime import datetime

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
LOG_FILE = 'download_log.txt'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

download_status = {}

def log_download(ip, url, format_type, status, title=''):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] IP: {ip} | URL: {url} | Formato: {format_type} | Estado: {status} | Título: {title}"
    logger.info(log_entry)

def delete_file_after_delay(filepath, delay_minutes=15):
    def delete_task():
        time.sleep(delay_minutes * 60)
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Archivo eliminado automáticamente: {filepath}")
        except Exception as e:
            logger.error(f"Error al eliminar archivo {filepath}: {str(e)}")

    thread = threading.Thread(target=delete_task)
    thread.daemon = True
    thread.start()

def download_video(url, download_id, format_type='video', ip_address='unknown'):
    try:
        download_status[download_id] = {'status': 'downloading', 'progress': 0}

        def progress_hook(d):
            if d['status'] == 'downloading':
                try:
                    percent = d.get('_percent_str', '0%').strip()
                    download_status[download_id]['progress'] = percent
                except:
                    pass
            elif d['status'] == 'finished':
                download_status[download_id]['status'] = 'finished'
                download_status[download_id]['filename'] = d['filename']

        if format_type == 'audio':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [progress_hook],
            }
        else:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
                'progress_hooks': [progress_hook],
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if format_type == 'audio':
                filename = os.path.splitext(filename)[0] + '.mp3'
            title = info.get('title', 'video')
            download_status[download_id]['status'] = 'completed'
            download_status[download_id]['filename'] = filename
            download_status[download_id]['title'] = title
            log_download(ip_address, url, format_type, 'COMPLETADO', title)
            delete_file_after_delay(filename, 15)
    except Exception as e:
        download_status[download_id]['status'] = 'error'
        download_status[download_id]['error'] = str(e)
        log_download(ip_address, url, format_type, f'ERROR: {str(e)}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    format_type = data.get('format', 'video')

    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_address:
        ip_address = ip_address.split(',')[0].strip()
    else:
        ip_address = request.remote_addr

    if not url:
        return jsonify({'error': 'URL no proporcionada'}), 400

    log_download(ip_address, url, format_type, 'INICIADO')

    download_id = str(uuid.uuid4())
    thread = threading.Thread(target=download_video, args=(url, download_id, format_type, ip_address))
    thread.start()

    return jsonify({'download_id': download_id})

@app.route('/status/<download_id>')
def status(download_id):
    if download_id in download_status:
        return jsonify(download_status[download_id])
    return jsonify({'status': 'not_found'}), 404

@app.route('/download-file/<download_id>')
def download_file(download_id):
    if download_id in download_status and download_status[download_id]['status'] == 'completed':
        filename = download_status[download_id]['filename']
        return send_file(filename, as_attachment=True)
    return jsonify({'error': 'Archivo no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
