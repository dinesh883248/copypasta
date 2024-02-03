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
4. setup git
```sh
git config user.name dinesh
git config user.email dinesh883248@gmail.com
git add --all
git commit -m 'initial'
```
5. update settings
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
