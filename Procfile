web: gunicorn restaurant_api.wsgi --log-file -
release: python manage.py migrate && python manage.py collectstatic --noinput
