param(
    [switch]$Migrate,
    [switch]$Clean,
    [switch]$Host_
)

Set-Location "./backend/django_project/"

function MakeAndMigrate { # do we also need makemigrations paddle_traffic and migrate paddle_traffic?
    poetry run python manage.py makemigrations
    poetry run python manage.py makemigrations paddle_traffic
    poetry run python manage.py migrate
}

if($Migrate) {
    MakeAndMigrate
    Set-Location "../../"
} elseif ($Clean) {
    Remove-Item db.sqlite3 -Force
    Remove-Item -Path "paddle_traffic/migrations" -Recurse -Force
    echo "Deleted db.sqlite3"
    MakeAndMigrate
    echo "MakeAndMigrate Finished"
    poetry run python manage.py seed
    Set-Location "../../"
 } elseif($Host_) {
    try {
        poetry run python manage.py runserver 0.0.0.0:8000
    } finally {
        Set-Location "../../"
    }
 } else {
    try {
        poetry run python manage.py runserver
    }
    finally {
        Set-Location "../../"
    }
}