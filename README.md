# Convertidor de YouTube

Aplicación web para descargar videos de YouTube en formato MP4 o convertir a MP3.

## Características

- 📹 Descarga videos en alta calidad (MP4)
- 🎵 Extrae audio en formato MP3
- 📊 Registro de descargas con IP, fecha y hora
- 🗑️ Eliminación automática de archivos después de 15 minutos
- 🎨 Interfaz moderna y responsive

## Requisitos

- Python 3.8+
- FFmpeg (para conversión de audio)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/elisa-rivadeneira/convertidor-youtube.git
cd convertidor-youtube
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Instalar FFmpeg:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Descargar desde https://ffmpeg.org/download.html
```

## Uso

1. Iniciar el servidor:
```bash
python3 app.py
```

2. Abrir en el navegador:
```
http://localhost:5000
```

3. Pegar una URL de YouTube y seleccionar formato (Video MP4 o Audio MP3)

## Logs

Los registros de descargas se guardan en `download_log.txt` con:
- Fecha y hora
- IP del usuario
- URL descargada
- Formato seleccionado
- Estado de la descarga
- Título del video

## Advertencias

⚠️ **Uso Legal**: Esta herramienta es solo para uso educativo. Descargar contenido de YouTube puede violar sus Términos de Servicio. Usa bajo tu propia responsabilidad.

## Licencia

MIT
