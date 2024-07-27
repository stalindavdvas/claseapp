# Usa una imagen base con Python
FROM python:3.9-slim

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos e instala las dependencias
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia el código fuente del servicio
COPY . .

# Expone el puerto en el que el servicio se ejecuta
EXPOSE 5001

# Comando para ejecutar el servicio
CMD ["python", "auth-service.py"]
