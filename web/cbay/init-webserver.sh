#!/bin/bash

python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py loaddata /usr/src/app/fixtures/data.json


exec "$@"