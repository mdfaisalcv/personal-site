#!/bin/sh
set -e

echo "Waiting for the database..."
python manage.py wait_for_db

echo "Applying migrations..."
python manage.py migrate --no-input

echo "Collecting static files..."
python manage.py collectstatic --no-input

# Load sample bio-data the first time only (won't duplicate on restarts,
# since Profile already exists after the first successful load).
python manage.py shell -c "
from portfolio.models import Profile
import sys
if not Profile.objects.exists():
    print('No profile found, loading sample fixture...')
    sys.exit(1)
" || python manage.py loaddata portfolio/fixtures/initial_data.json

echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
