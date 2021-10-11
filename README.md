# Todo-APP
A simple todo app with. Made with Django.

This project is available at https://obscure-crag-30514.herokuapp.com

## How to run project locally?

Make sure you have Python 3 and pip installed.
- Clone this repository.
- Create virtualenv with Python 3.
- Active the virtualenv.
- Install dependences.
- Run the migrations.
- Run the server.

### On Linux
```
git clone https://github.com/MarcusAldrey/Todo-APP.git
cd Todo-APP
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
### On Windows
```
git clone https://github.com/MarcusAldrey/Todo-APP.git
cd Todo-APP
python -m venv .venv
venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
