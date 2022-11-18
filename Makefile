mr:
	python manage.py makemigrations && python manage.py migrate && python manage.py runserver
r:
	python manage.py runserver
user:
	python manage.py createsuperuser