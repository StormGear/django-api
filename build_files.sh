#!/usr/bin/env bash

# Install python3 and pip
echo "Building the project"
python3 --version
echo "Use a virtual environment"
python3 -m venv venv
source venv/bin/activate

echo "Installing requirements"
python3 -m pip install -r requirements.txt

echo "Migrating database"
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collecting static files"
python3 manage.py collectstatic --noinput





# sudo apt update
# sudo apt install python3 python3-pip
# pip install -r requirements.txt
# python3.9 manage.py collectstatic --noinput