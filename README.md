python manage.py runserver<br />
redis-server --port 6380<br />
celery -A tt worker -B -l INFO<br />
