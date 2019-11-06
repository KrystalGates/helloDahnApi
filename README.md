# Hello DANH

Hello DANH (Distressed And Need Help) is an application designed for people who are disabled and need full time caregivers. It allows the user to create a network of chosen contacts to discretely alert through email when the user has become uncomfortable or alarmed with the services of the caregiver.

## Getting Hello DANH running

1. Clone down this repo

2. In the terminal:

`cd helloDanhApi`

`python -m venv helloDanhEnv`

Activate the enviroment. Use the `source ./helloDanhEnv/bin/activate` command on OSX, or run `activate.bat` for Windows.

`pip install -r requirements.txt`

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py loaddata alertplacement`

`python manage.py runserver`

You have the Hello DANH API up and running but WAIT you need to go to [HelloDANHClient](https://github.com/KrystalGates/helloDanhClient) and follow the instructions if you haven't already!

Created with [Django REST](https://www.django-rest-framework.org/)