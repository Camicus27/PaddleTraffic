
## Full Installation
First we need pipx. [Why use pipx?](https://python-poetry.org/docs/#installing-with-pipx)

`pip install pipx`

Start by installing poetry

`pipx install poetry`

[See More on Update / Uninstall](https://python-poetry.org/docs/#installing-with-pipx)

Add Environment Variables when prompted

`pipx ensurepath`

Create a folder where you want the backend to be.
CD into that folder.

For a projects you need to add a toml file. This is akin to a build.gradle, makefile, etc. We can auto generate the toml file. Navigate to your project folder and run the cmd. [See More](https://python-poetry.org/docs/basic-usage/).

`poetry init`

Don't use `new`, as it creates a new package, we'll use the django project to create a package and directory structure.

Make sure to name the project in the prompt the same as what you will name the Django Project. This can be changed in the .toml file.

Before moving on, virtual environments aren't set to be in the project folder by default so, let's set that to be true, it can be helpfulto see what's in the virtual environment sometimes.

`poetry config virtualenvs.in-project true`

Poetry also wants you to have a README file. So add a blank one.

Add Django as a dependency

`poetry add django`

From here we can use Django to create the rest of our project. Create a new Django project.

`poetry run python -m django startproject PROJECT_NAME`

Running install should ensure everything is correct.

`poetry install`

The folder structure should look like this

```
BACKEND_REPO
    .venv
        Lib
        Scripts
        .gitignore
        pyvenv.cfg
    DJANGO_PROJECT
        DJANGO_PROJECT
            __init__.py
            asgi.py
            settings.py
            urls.py
            wsgi.py
        manage.py
    poetry.lock
    pyproject.toml
    README.md
```

Test running the server (make sure you're in the django project directory, run from poetry)

`python manage.py runserver`

Create a .gitignore in the root directory and add the following
```
uploads/*
db.sqlite3
*.pyc
.DS_Store
autotester
.idea
```

## Useful Links
- https://python-poetry.org/
- https://python-poetry.org/docs/cli/

