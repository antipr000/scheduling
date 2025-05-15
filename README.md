# Scheduling Service
APIs for a scheduling service similar to calendly


## Data seeding
We have a data seeder defined under `deploy/data_seeder.py` that is responsible for loading some initial data to faciliate local testing and integration tests. The seeder script is automatically run when you start the server using `docker compose` or when running tests.
To run it explicitly, you can use `python seed.py`


## Starting server locally
Run `docker compose -f deploy/docker-compose.yaml up -d` to start the database container and server


## Integration Tests

This directory contains integration tests for the scheduling application. The tests are written using Django's testing framework and Django REST framework's testing utilities.

### Structure

- `base.py`: Contains the base test class with common setup for all integration tests
- `test_*.py`: Individual test files for different components

### Running Tests

To run all tests:
```bash
docker compose -f deploy/docker-compose-test.yaml up
```

To run all tests manually:
```bash
DJANGO_SETTINGS_MODULE=scheduling.test_settings python manage.py test tests
```

To run a specific test file:
```bash
DJANGO_SETTINGS_MODULE=scheduling.test_settings python manage.py test tests.test_booking
```