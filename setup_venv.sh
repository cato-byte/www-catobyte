#!/bin/bash
sudo apt update
sudo apt install pkg-config
sudo apt install libxml2-dev
#create venv
python3 -m venv kunturvenv

# Activate the virtual environment
source ./kunturvenv/bin/activate

# Upgrade pip and setuptools
pip install --upgrade pip setuptools

# Install the dependencies from requirements.txt
pip install -r requirements.txt