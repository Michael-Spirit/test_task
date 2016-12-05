Local deployment
================================

### Install project requirements
    $ pip install -r requirements.txt

### Create local settings file
    $ cp test_task/local_settings test_task/local_settings.py

### Run migrations
    $ python manage.py migrate

### Run tests
    $ python manage.py test

### Run server
    $ python manage.py runserver
