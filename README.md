# TARAPEUTIC ASSISTANT

## DEPENDENCES

- python 3.9.2 (32bit o 64bit)
- pip 21.0.1
- mysql==5.7

## Environment Variables

The .env.example file presents the environment variables that must be defined in a ".env" file in the root directory,
otherwise the default values in the "setting" file will be used.

## HOW TO INSTALL?

Once the dependencies are satisfied, whether you have a virtual environment (virtualenv, venv, or conda) or whether you don't need it, go to the root of this project and run:

```sh
# In your terminal 
pip install -r requirements.txt
```

Once this is done, the migrations need to be created:

```sh
# In your terminal
python manage.py makemigrations
```

Followed by this, they need to be run:

```sh
# In your terminal
python manage.py migrate
```

# HOW TO EXECUTE THE PROJECT?

By having the previous steps simply positions in the root of the project and run:

```sh
#  In your terminal
python manage.py runserver
```

## EXECUTE JSON FOR FILLING THE DATABASE (CATALOGS)

Being at the root of the project and run:

```bat
REM In your windows terminal
python manage.py loaddata data\fixtures\user_type.json
python manage.py loaddata data\fixtures\user.json
```bat

```bat
REM In your Linux terminal
python manage.py loaddata data/fixtures/user_type.json
python manage.py loaddata data/fixtures/user.json
```bat