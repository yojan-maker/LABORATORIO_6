  GNU nano 7.2                                                                                   Dockerfile                                                                                             
# Imagen base
FROM python:3.10-slim

# Variable de entorno para Streamlit
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_PORT=8501

# Crear directorio de la app
WORKDIR /app

# Copiar archivos
COPY requirements.txt .
COPY app.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto de Streamlit
EXPOSE 8501

# Comando para ejecutar la app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
