param(
    [switch]$Migrate,
    [switch]$Clean
)

Set-Location "./backend/django_project/"

function MakeAndMigrate { # do we also need makemigrations paddle_traffic and migrate paddle_traffic?
    poetry run python manage.py makemigrations
    poetry run python manage.py migrate
}

if($Migrate) {
    MakeAndMigrate
} elseif ($Clean) {
    Remove-Item db.sqlite3 -Force
    MakeAndMigrate
} else {
    try {
        poetry run python manage.py runserver
    }
    finally {
        Set-Location "../../"
    }
}