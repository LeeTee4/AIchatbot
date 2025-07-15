# Railway deployment configuration
web: gunicorn Lee_Chat.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate
