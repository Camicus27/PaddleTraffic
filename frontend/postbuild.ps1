Remove-Item -Path "..\backend\django_project\django_project\static\*" -Force -Recurse
Copy-Item -Path "dist\*" -Destination "..\backend\django_project\django_project\static" -Recurse
Set-Location "..\backend\django_project\django_project"
Move-Item -Path "static\index.html" -Destination "templates\index.html" -Force

Write-Output "Moved Vue build to Django static and templates folders"