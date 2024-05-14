echo "[!] Creating Conductor tables ..."

python manage.py makemigrations && \
python manage.py migrate

if [ -z "$DJANGO_SUPERUSER_USERNAME" ] || [ -z "$DJANGO_SUPERUSER_EMAIL" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ]
then
    python manage.py ensure_adminuser --noinput
fi

echo "[!] Starting Conductors Celery Server ..."
celery -A conductor_server worker -l INFO

exit 0
