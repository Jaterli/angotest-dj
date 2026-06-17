FROM python:3.12-slim

WORKDIR /app

# Copiar dependencias primero (optimiza la caché de Docker)
COPY ./backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copiar el resto del código
COPY ./backend /app/

# Script de entrada para ejecutar Gunicorn
COPY ./docker/backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]