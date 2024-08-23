#!/bin/bash


mkdir /run/postgresql
chown postgres:postgres /run/postgresql
echo "DATABASEUSER=$DATABASEUSER" > /user.sh
echo "DATABASEPWD=$DATABASEPWD" >> /user.sh
echo "MYDATABASE=$MYDATABASE" >> /user.sh
su - postgres -c bash << EOF
source /user.sh
export DATABASEUSER
export DATABASEPWD
export MYDATABASE
mkdir /var/lib/postgresql/data/
chmod /var/lib/postgresql/data/
initdb /var/lib/postgresql/data/
echo "host all all 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf
echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf
pg_ctl start -D /var/lib/postgresql/data/
createuser -e -s -d -R $DATABASEUSER
psql -c "ALTER USER $DATABASEUSER WITH PASSWORD '$DATABASEPWD';"
createdb -O $DATABASEUSER $MYDATABASE

EOF

cp ./pg_hba.conf /etc/postgresql/15/main

python manage.py collectstatic -y

echo "static files collected"

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell

python manage.py makemigrations

echo "makemigrations done"

python manage.py migrate

echo "migrate done"

redis-server --daemonize yes 

redis-cli ping

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0.0.0.0:8005
