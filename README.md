# Polling Project
The Polling Project allows users to Create, Manage and Vote in multiple polls created by various users.
As a result, one can statistically analyze the trend by taking public opinion through these polls.

# Tech Stack
This application is purely build with the Django Framework of Python.
Requirements:
- Python 3
- python-pip
- [virtualenv](https://virtualenv.pypa.io/en/latest/)
- Django 3.2
- [django-crispy-form](https://django-crispy-forms.readthedocs.io/en/latest/install.html)
- [python-decouple](https://pypi.org/project/python-decouple/)
- Pillow
- sqlite3

# Installation
First, clone this respository with the following link:
```bash
git clone https://github.com/Parth-Shah-99/Polling-Project.git
```
Next, navigate in the following folder:
```bash
cd Polling-Project
```
Create a virtualenv for the following project and activate it:
```bash
virtualenv venv
source venv/bin/activate
```
Next, install the requirements from requirements.txt file:
```bash
pip install -r requirements.txt
```
Next, run migrations:
```bash
python manage.py migrate
```
Next, create a default superuser (entering username and password for admin):
```bash
python manage.py createsuperuser
```
Run the server:
```bash
python manage.py runserver
```
Finally, navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
