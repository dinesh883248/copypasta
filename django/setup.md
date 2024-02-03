# django setup
1. setup user
```sh
set -e
read -p "Enter the project name: " PROJECT_NAME
USERNAME="$PROJECT_NAME"
sudo useradd -ms /bin/bash $USERNAME
echo "User "$USERNAME" created successfully."
```
2. switch user
```sh
sudo su - "$USERNAME"
```
3. setup project
```sh
mkdir "$PROJECT_NAME"
cd "$PROJECT_NAME"
python3 -m venv venv
. venv/bin/activate
pip install -U pip
pip install django
django-admin startproject "$PROJECT_NAME"
cd "$PROJECT_NAME"
django-admin startapp common
echo "export DJANGO_ENVIRONMENT=prod" >> .env
```
4. setup pre-commit
```sh
. ../venv/bin/activate
pip install pre-commit
tee .pre-commit-config.yaml <<EOF
repos:
-   repo: https://github.com/ambv/black
    rev: 23.12.1
    hooks:
    - id: black
      language_version: python3.
EOF
pre-commit install
```
5. setup git
```sh
git init
git config user.name dinesh
git config user.email dinesh883248@gmail.com
tee .gitignore <<EOF
*.pyc
__pycache__/
*.swo
*.swp
sqlite3.db
EOF
pip freeze > requirements.txt
git add --all
git commit -m 'initial'
```
6. update settings
- change debug from true to false.
- add common to apps.
- more updates below..
```sh
tee -a "$PROJECT_NAME" <<EOF
STATIC_ROOT = BASE_DIR / "static"

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
DJANGO_ENVIRONMENT = os.environ["DJANGO_ENVIRONMENT"]
print("DJANGO_ENVIRONMENT: ", DJANGO_ENVIRONMENT)
APPEND_SLASH = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        }
    },
}
EOF
```
