./manage.py migrate
./manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_NAME --email $DJANGO_SUPERUSER_EMAIL --password $DJANGO_SUPERUSER_PASSWORD
./manage.py runserver 0.0.0.0:8000
