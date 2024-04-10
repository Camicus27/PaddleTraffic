#! /bin/bash
export PATH="~/.local/bin:$PATH"
cd /opt/paddletraffic/backend/django_project
poetry run python manage.py runserver --noreload
