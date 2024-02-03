# django setup
1. setup user
```sh
read -p "Enter the project name: " PROJECT_NAME
USERNAME=${PROJECT_NAME}
sudo useradd -ms /bin/bash $USERNAME
echo "User $USERNAME created successfully."
```
2. setup project
```sh
sudo su - $USERNAME
```
