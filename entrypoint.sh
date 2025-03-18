#!/bin/sh
# Ejecuta las migraciones si es necesario
echo "Microservice assistant"
echo "Running makemigrations and migrate..."
echo "Running makemigrations and migrate..."
echo "Running makemigrations and migrate..."
echo "Running makemigrations and migrate..."


python manage.py makemigrations assistant
python manage.py makemigrations message
python manage.py migrate
# Inicia el servidor con watchmedo
echo "Starting the server with watchmedo..."
watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- gunicorn -b 0.0.0.0:8080 app.wsgi:application
