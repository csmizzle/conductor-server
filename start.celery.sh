echo "[!] Starting Conductor's Celery Server ..."
celery -A conductor_server worker -l INFO

exit 0
