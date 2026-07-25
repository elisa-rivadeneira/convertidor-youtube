#!/usr/bin/env python3

import yt_dlp
import sys

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Descargando: {url}")
            ydl.download([url])
            print("Descarga completada!")
    except Exception as e:
        print(f"Error al descargar: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python download_youtube.py <URL_DE_YOUTUBE>")
        sys.exit(1)

    video_url = sys.argv[1]
    download_video(video_url)
