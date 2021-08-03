#!/bin/bash
: "$(sed -i "s/TEMPLATE_CELERY_PW/$REDIS_CELERY_PW/g" /var/www/app/celeryconfig.py)"
celery -A app.app.celery worker --loglevel=INFO  --without-gossip --without-mingle --without-heartbeat -Ofair &
exec gunicorn --config gunicorn_config.py app.wsgi:app --preload