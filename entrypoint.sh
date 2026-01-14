#!/bin/bash

set -e

cd /app/src

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Start consumer in background
echo "Starting consumer in background..."
python manage.py startconsumer &

# Execute the command passed to the container (runserver)
exec "$@"
