test:
	coverage run manage.py test -v 2

serve:
	python manage.py runserver 8002

tunnel:
	python ./scripts/dev_tunnel.py -l 8002 -d discuss


celery-beat:
	celery -A server beat -l INFO  --scheduler django_celery_beat.schedulers:DatabaseScheduler

celery-worker:
	celery -A server worker -l INFO
