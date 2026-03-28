web: python manage.py collectstatic --noinput && python manage.py migrate && python create_superuser.py && gunicorn config.wsgi --log-file -
