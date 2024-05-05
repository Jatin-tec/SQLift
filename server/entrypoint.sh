!/bin/sh

# Apply database migrations
python manage.py db init
python manage.py db migrate

# Apply updates
python manage.py db upgrade

# Start Gunicorn server
gunicorn --bind 0.0.0.0:5000 wsgi:app