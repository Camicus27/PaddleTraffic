Set-Location "./backend/django_project/"
try {
    poetry run python manage.py runserver
}
finally {
    Set-Location "../../"
}