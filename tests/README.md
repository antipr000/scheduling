# Integration Tests

This directory contains integration tests for the scheduling application. The tests are written using Django's testing framework and Django REST framework's testing utilities.

## Structure

- `base.py`: Contains the base test class with common setup for all integration tests
- `test_*.py`: Individual test files for different components

## Running Tests

To run all tests:
```bash
DJANGO_SETTINGS_MODULE=scheduling.test_settings python manage.py test tests
```

To run a specific test file:
```bash
DJANGO_SETTINGS_MODULE=scheduling.test_settings python manage.py test tests.test_booking
```