#!/bin/bash

service postgresql start

su - postgres << EOF
psql -c "CREATE DATABASE mydatabase;"
psql -c "CREATE USER username WITH PASSWORD 'password';"
psql -c "ALTER ROLE username SET client_encoding TO 'utf8';"
psql -c "ALTER ROLE username SET default_transaction_isolation TO 'read committed';"
psql -c "ALTER ROLE username SET timezone TO 'UTC';"
psql -c "GRANT postgres TO username;"
psql -c "GRANT ALL PRIVILEGES ON DATABASE mydatabase TO username;"
psql -c "GRANT ALL PRIVILEGES ON SCHEMA public TO username;"
psql -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO username;"
psql -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO username;"
EOF

cp ./pg_hba.conf /etc/postgresql/15/main


python manage.py collectstatic -y

echo "static files collected"

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell


python manage.py makemigrations authapi

echo "makemigrations done"


python manage.py migrate 

python manage.py migrate --fake authapi 0002_alter_userprofile_otp_secret

python manage.py migrate 

echo "migrate done"

# python manage.py migrate --list


mkdir -p /project/media/images/

mv ../default_avatar.jpg ./media/images/default_avatar.jpg

python manage.py runserver 0.0.0.0:8000
