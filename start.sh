echo "[!] Starting Conductor Server ..."
echo "[!] Creating Conductor tables ..."

python manage.py makemigrations && \
python manage.py migrate

if [ -z "$DJANGO_SUPERUSER_USERNAME" ] || [ -z "$DJANGO_SUPERUSER_EMAIL" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ]
then
    echo "[!] Superuser credentials provided, starting admin role creation ..."
    python manage.py ensure_adminuser --noinput
else
    echo "[!] Superuser credentials not provided, skipping admin role creation ..."
fi

echo "[!] Starting Django Server ..."

gunicorn conductor_server.wsgi \
    --workers=4 \
    --bind=0.0.0.0:8000 \
    --log-level=info \
    --timeout=300

exit 0
