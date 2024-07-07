#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST 5432; do
      sleep 0.1
    done

    echo "PostgreSQL started!"
fi

echo "Migrating database..."
python manage.py flush --no-input
python manage.py migrate
echo "Database migrated!"

echo "Restoring data from SQL dump..."
PGPASSWORD=$DATABASE_PASS psql -h $DATABASE_HOST -U $DATABASE_USER -d $DATABASE_NAME < "test_data.sql"
echo "SQL dump restored!"

exec "$@"
