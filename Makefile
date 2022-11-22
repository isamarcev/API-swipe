mr:
	python manage.py makemigrations && python manage.py migrate && python manage.py runserver 9000
r:
	python manage.py runserver 9000
user:
	python manage.py createsuperuser