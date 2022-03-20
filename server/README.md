# Installation

```
pipenv install
pipenv shell
pip install pytest
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
python -m unittest ticket.tests.test_seat_allocation
```