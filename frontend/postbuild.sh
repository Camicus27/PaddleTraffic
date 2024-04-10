#!/bin/sh

mkdir -p /opt/paddletraffic/backend/django_project/django_project/static
rm -rf /opt/paddletraffic/backend/django_project/django_project/static/*
cp -r /opt/paddletraffic/frontend/dist/* /opt/paddletraffic/backend/django_project/django_project/static
mv /opt/paddletraffic/backend/django_project/django_project/static/index.html /opt/paddletraffic/backend/django_project/django_project/templates/index.html

echo "Moved Vue build to Django static and templates folders"

