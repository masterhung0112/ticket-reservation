# Installation

```
pipenv install
pipenv shell

# On Ubuntu: sudo apt-get install libmysqlclient-dev
pip install mysqlclient
```

# Run

Go to `mysite/settings.py`, change the variable for DB in `DATABASES` variable

Run the following command in the first run
```
pipenv shell
python manage.py migrate --run-syncdb
```

Run the server
```
pipenv shell
python manage.py runserver
```

# Run Test

Go to `mysite/settings.py`, change the default DB in `DATABASES` variable to sqlite3

At folder `server`, run all tests
```
pipenv shell
python -m unittest
```

Test a specific test
```
pipenv shell

# Run unit test of a specific file
python -m unittest ticket.tests.test_seat_allocation
python manage.py test ticket.tests.rest_api
```