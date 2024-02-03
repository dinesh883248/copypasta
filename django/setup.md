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
