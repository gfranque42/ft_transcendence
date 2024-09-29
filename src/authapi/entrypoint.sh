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

python manage.py makemigrations

python manage.py migrate

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
