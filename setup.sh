#!/bin/bash

sudo apt-get remove -y --purge man-db

sudo apt update

sudo apt-get install python3.9

sudo apt install python3-pip

python3 -m pip install --upgrade pip

pip3 install -r requirements.txt

sudo apt install tmux