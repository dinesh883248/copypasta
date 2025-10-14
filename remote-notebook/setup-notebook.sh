#!/bin/bash

USER=$1
REMOTE_IP=$2
PRIVATE_KEY_PATH=$3

if [ -z "$USER" ]; then
  echo "Usage: $0 <user> <remote_ip> [private_key_path]"
  exit 1
fi

if [ -z "$REMOTE_IP" ]; then
  echo "Usage: $0 <user> <remote_ip> [private_key_path]"
  exit 1
fi

if [ -z "$PRIVATE_KEY_PATH" ]; then
  PRIVATE_KEY_PATH="~/.ssh/id_rsa"
fi

rsync -azP -e "ssh -i $PRIVATE_KEY_PATH" run-notebook.sh $USER@$REMOTE_IP:/home/$USER/install-notebook.sh

ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -i $PRIVATE_KEY_PATH $USER@$REMOTE_IP "chmod +x /home/$USER/install-notebook.sh"

ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -i $PRIVATE_KEY_PATH $USER@$REMOTE_IP "/home/$USER/install-notebook.sh $USER"

echo "Run the following command in your local terminal to access the Jupyter Notebook:"
echo "ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -i $PRIVATE_KEY_PATH -L 8899:localhost:8899 $USER@$REMOTE_IP"
