#!/bin/sh

# Migrar base de datos
python manage.py migrate --noinput

# Recolectar archivos estáticos (incluye React build)
python manage.py collectstatic --noinput

# Iniciar Gunicorn
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120