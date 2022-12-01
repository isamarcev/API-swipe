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
