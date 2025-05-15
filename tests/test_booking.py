from .base import BaseIntegrationTest
from django.urls import reverse
from rest_framework import status
from datetime import datetime
from booking.models.bookings import Bookings


class BookingCreateIntegrationTest(BaseIntegrationTest):
    """Integration tests for booking creation."""

    def test_create_booking_success(self):
        """Test creating a new booking."""

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
        self.assertEqual(response.data["user_id"], data["user_id"])

    def test_create_booking_fails_when_no_room_available(self):
        """Test creating a booking fails when no room is available."""

        # Set up the test data
        user_1 = self.users[0]

        user_2 = self.users[1]

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

        # Create a booking for user_1
        url = reverse(
            "availability_slots",
            kwargs={"service_id": service_id, "date": date},
        )
        data = {
            "provider_id": provider.id,
            "user_id": user_1.id,
            "start_time": 540,  # 9:00 AM
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create a booking for user_2
        url = reverse(
            "availability_slots",
            kwargs={"service_id": service_id, "date": date},
        )
        data = {
            "provider_id": provider.id,
            "user_id": user_2.id,
            "start_time": 540,  # 9:00 AM
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_booking_success_assigns_different_room(self):
        """Test creating a booking successfully assigns a different room when we book slot for same service,
        with same provider and same date and time"""

        # Set up the test data
        user_1 = self.users[0]

        user_2 = self.users[1]

        provider = next(
            (
                provider
                for provider in self.providers
                if provider.name == "Massage Therapy Center"
            ),
            None,
        )

        service = next(
            (service for service in self.services if service.name == "Swedish Massage"),
            None,
        )

        service_id = service.id
        date = datetime.now().strftime("%Y-%m-%d")

        # Create a booking for user_1
        url = reverse(
            "availability_slots",
            kwargs={"service_id": service_id, "date": date},
        )

        data = {
            "provider_id": provider.id,
            "user_id": user_1.id,
            "start_time": 540,  # 9:00 AM
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create a booking for user_2
        url = reverse(
            "availability_slots",
            kwargs={"service_id": service_id, "date": date},
        )
        data = {
            "provider_id": provider.id,
            "user_id": user_2.id,
            "start_time": 540,  # 9:00 AM
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Compare rooms are different
        booking_1 = Bookings.objects.filter(
            user_id=user_1.id, service_id=service_id
        ).first()
        booking_2 = Bookings.objects.filter(
            user_id=user_2.id, service_id=service_id
        ).first()
        self.assertNotEqual(booking_1.room.id, booking_2.room.id)


class BookingListIntegrationTest(BaseIntegrationTest):
    """Integration tests for booking list."""

    def test_list_bookings_success(self):
        """Test listing bookings successfully."""
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

        # List bookings
        url = reverse("bookings", kwargs={"user_id": user.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user_id"], user.id)
        self.assertEqual(response.data[0]["service_name"], service.name)
        self.assertEqual(response.data[0]["provider_name"], provider.name)
        self.assertEqual(response.data[0]["start_time"], 540)
        self.assertEqual(response.data[0]["end_time"], 630)
        self.assertEqual(response.data[0]["date"], date)
