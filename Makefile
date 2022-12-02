mr:
	python manage.py makemigrations && python manage.py migrate && python manage.py runserver 9000
m:
	python manage.py makemigrations && python manage.py migrate
r:
	python manage.py runserver 9000
user:
	python manage.py createsuperuser

beat:
	celery -A APISwipe beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
celery:
	celery -A APISwipe worker -l info
celery-beat:
	celery -A APISwipe worker -l INFO && celery -A APISwipe beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
startapp:
	python manage.py migrate --no-input
	python manage.py collectstatic --no-input
	gunicorn APISwipe.wsgi:application --bind 0.0.0.0:8000
	python manage.py create_user
	python manage.py create_developers
	python manage.py create_ad
