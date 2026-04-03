#!/bin/sh

echo "Waiting for MySQL to be ready..."

# 等待数据库就绪
max_retries=30
counter=0
while [ $counter -lt $max_retries ]; do
    python -c "import pymysql; pymysql.connect(host='$DB_HOST', port=int('$DB_PORT'), user='$DB_USER', password='$DB_PASSWORD')" 2>/dev/null && break
    counter=$((counter + 1))
    echo "MySQL is unavailable - attempt $counter/$max_retries - sleeping 2s"
    sleep 2
done

if [ $counter -eq $max_retries ]; then
    echo "Failed to connect to MySQL after $max_retries attempts"
    exit 1
fi

echo "MySQL is up - running migrations"
python manage.py migrate --noinput

echo "Initializing data"
python manage.py init_data

echo "Starting server"
exec gunicorn thesis_selection.wsgi:application --bind 0.0.0.0:8000 --workers 2 --access-logfile - --error-logfile -
