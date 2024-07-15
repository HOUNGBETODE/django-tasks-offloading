#!/bin/ash

echo "Applying migrations to database"

python manage.py makemigrations
python manage.py migrate


exec "$@"