# Installation

```
pipenv install
pipenv shell
pip install pytest
```

# Run

In `mysite`, edit environment variable in `.env` file

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