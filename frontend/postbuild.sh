#!/bin/sh

mkdir -p ~/paddletraffic/backend/django_project/django_project/static
rm -rf ~/paddletraffic/backend/django_project/django_project/static/*
cp -r ~/paddletraffic/frontend/dist/* ~/paddletraffic/backend/django_project/django_project/static
mv ~/paddletraffic/backend/django_project/django_project/static/index.html ~/paddletraffic/backend/django_project/django_project/templates/index.html

echo "Moved Vue build to Django static and templates folders"

