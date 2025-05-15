from .base import BaseIntegrationTest
from django.urls import reverse
from rest_framework import status
from datetime import datetime, timedelta
from booking.models.bookings import Bookings


class AvailableDatesIntegrationTest(BaseIntegrationTest):
    """Integration tests for available dates functionality."""

    def test_availability_for_service_returns_all_available_dates(self):
        """Test availability for service returns all available dates"""

        # Set up the test data
        service = self.services[0]

        url = reverse(
            "availability",
            kwargs={"service_id": service.id},
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 30)
        date_tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        date_two_days_from_now = (datetime.now() + timedelta(days=2)).strftime(
            "%Y-%m-%d"
        )
        self.assertIn(date_tomorrow, response.data)
        self.assertIn(date_two_days_from_now, response.data)


class AvailableSlotsIntegrationTest(BaseIntegrationTest):
    """Integration tests for available slots functionality."""

    def test_availability_slots_returns_all_available_slots(self):
        """Test availability for service returns all available slots"""

        # Set up the test data
        service = next(
            (
                service
                for service in self.services
                if service.name == "Deep Tissue Massage"
            ),
            None,
        )
        date = datetime.now().strftime("%Y-%m-%d")

        url = reverse(
            "availability_slots",
            kwargs={"service_id": service.id, "date": date},
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        provider_names = [slot["provider_name"] for slot in response_data]

        # Assert on providers for the service
        self.assertIn("Spa & Wellness Center", provider_names)
        self.assertIn("Massage Therapy Center", provider_names)
        self.assertNotIn("Beauty Salon", provider_names)

        # Assert that Message Therapy Center has slot for 9 AM
        self.assertIn(
            "Massage Therapy Center",
            [
                slot["provider_name"]
                for slot in response_data
                if slot["start_time"] == 540
            ],
        )

    def test_availability_slots_returns_no_slots_for_9_am_when_booked(self):
        """Test availability slots returns no slots for 9 AM when booked"""

        # Set up the test data
        user = self.users[0]

        provider = next(
            (
                provider
                for provider in self.providers
                if provider.name == "Massage Therapy Center"
            ),
            None,
        )

        service = next(
            (
                service
                for service in self.services
                if service.name == "Deep Tissue Massage"
            ),
            None,
        )

        service_id = service.id
        date = datetime.now().strftime("%Y-%m-%d")

        url = reverse(
            "availability_slots",
            kwargs={"service_id": service_id, "date": date},
        )
        data = {
            "provider_id": provider.id,
            "user_id": user.id,
            "start_time": 540,  # 9:00 AM
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get availability slots again
        url = reverse(
            "availability_slots",
            kwargs={"service_id": service_id, "date": date},
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that there are no slots for 9 AM for Massage Therapy Center
        self.assertNotIn(
            "Massage Therapy Center",
            [
                slot["provider_name"]
                for slot in response.data
                if slot["start_time"] == 540
            ],
        )
