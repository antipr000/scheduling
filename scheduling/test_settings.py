from .settings import *
import os

# Use the same database for tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "scheduling",
        "USER": "scheduling",
        "PASSWORD": "scheduling",
        "HOST": os.getenv("MYSQL_HOST", "localhost"),
        "PORT": "3306",
        "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        "TEST": {
            "NAME": "scheduling",  # Use the same database for tests
            "MIRROR": "default",  # Use the same database as default
        },
    }
}


# Disable migrations during tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Disable test database creation
TEST_RUNNER = "django.test.runner.DiscoverRunner"
TEST_CREATE_DB = False
