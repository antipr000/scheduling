from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from deploy.data_seeder import seed_data
from booking.models.users import Users
from booking.models.providers import Providers
from booking.models.services import Services
from booking.models.rooms import Rooms


class BaseIntegrationTest(TestCase):
    """Base class for all integration tests with common setup."""

    def setUp(self):
        """Set up test data and client."""
        self.client = APIClient()
        seed_data()
        self.users = list(Users.objects.all())
        self.providers = list(Providers.objects.all())
        self.services = list(Services.objects.all())
        self.rooms = list(Rooms.objects.all())

    def tearDown(self):
        """Clean up after tests."""
        pass
