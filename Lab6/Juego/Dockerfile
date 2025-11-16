# Imagen base de Python
FROM python:3.12-slim

# Evitar interacción con paquetes
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias necesarias para pygame y soporte gráfico
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    build-essential \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    libfreetype6-dev \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libsm6 \
    libxrandr2 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar pygame
RUN pip install --no-cache-dir pygame==2.6.1

# Habilitar conexión al servidor X11
ENV DISPLAY=:0

# Comando por defecto para correr tu juego
CMD ["python", "main.py"]
