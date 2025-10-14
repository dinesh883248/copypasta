#!/bin/bash

USER=$1
PORT=8899

python3 -m venv /home/$USER/.venv
source /home/$USER/.venv/bin/activate
pip install --upgrade pip uv
uv pip install notebook

cd /home/$USER
jupyter-notebook --port=$PORT --no-browser
