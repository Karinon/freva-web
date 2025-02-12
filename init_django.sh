#!/bin/bash
export DJANGO_SUPERUSER_PASSWORD=$1
export DJANGO_SUPERUSER_EMAIL=admin@freva.de
if [ -z $1 ];then
    echo "Usage: $0 django_passwd"
    exit 1
fi

python manage.py migrate --fake-initial --noinput
python manage.py createsuperuser \
    --noinput \
    --username freva-admin \
    --email $DJANGO_SUPERUSER_EMAIL
