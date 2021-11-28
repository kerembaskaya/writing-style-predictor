cd /applications || exit

gunicorn -k uvicorn.worker.UvicornWorker \
  --workers 4 \
  --bind "0.0.0.0:${APP_PORT:-8080}" \
  style.app:app \
  "$@"
