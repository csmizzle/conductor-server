echo "[!] Starting Conductors Celery Server ..."
celery -A conductor_server worker -l INFO

exit 0
