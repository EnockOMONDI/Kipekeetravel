#!/bin/bash

# Build the project
set -o errexit  # exit on error
echo "Building the project JDA..."




pip install -r requirements.txt

python3 manage.py makemigrations 
python3 manage.py migrate 
