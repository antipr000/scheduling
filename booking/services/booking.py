from booking.models.bookings import Bookings
from booking.models.providers import Providers
from booking.models.users import Users
from booking.models.rooms import Rooms
from booking.models.services import Services
from booking.models.room_supported_services import RoomSupportedServices
from booking.dto.request.book import BookingRequestDTO
from booking.dto.response.book import BookingResponseDTO
from datetime import datetime
from django.db.models import Q
from typing import List, Optional


class BookingService:
    def create_booking(
        self, service_id: str, date: str, booking_request: BookingRequestDTO
    ) -> BookingResponseDTO:
        service = Services.objects.get(id=service_id)
        provider = Providers.objects.get(id=booking_request.provider_id)
        user = Users.objects.get(id=booking_request.user_id)

        booking_date = datetime.strptime(date, "%Y-%m-%d")
        start_time = booking_request.start_time
        end_time = start_time + service.duration

        # Get rooms for the provider supported by services
        room_supported_services = RoomSupportedServices.objects.filter(
            room__provider=provider, service=service
        ).select_related("room")

        rooms = [
            room_supported_service.room
            for room_supported_service in room_supported_services
        ]

        # Check if the room is available for the given date and time
        # First fetch all bookings for these set of rooms
        # Check for overlap:
        # Case 1: Existing booking starts before and ends during/after our slot
        # Case 2: Existing booking starts during our slot
        existing_bookings: List[Bookings] = (
            Bookings.objects.filter(
                room__in=rooms,
                date=booking_date,
            )
            .filter(
                Q(start_time__lt=start_time, end_time__gt=start_time)
                | Q(start_time__lt=end_time, end_time__gt=end_time)
            )
            .select_related("room")
            .all()
        )

        room_to_use: Optional[Rooms] = None

        for room in rooms:
            existing_booking = next(
                (
                    booking
                    for booking in existing_bookings
                    if booking.room.id == room.id
                ),
                None,
            )
            if existing_booking:
                continue

            room_to_use = room
            break

        if room_to_use is None:
            raise ValueError("No room available for the requested time slot")

        inserted_booking = Bookings.objects.create(
            provider=provider,
            service=service,
            room=room_to_use,
            user=user,
            start_time=start_time,
            end_time=end_time,
            date=booking_date,
        )

        booking = Bookings.objects.select_related("provider", "service", "user").get(
            id=inserted_booking.id
        )

        return BookingResponseDTO.from_booking(booking)

    def get_bookings(self, user_id: str) -> List[BookingResponseDTO]:
        bookings = Bookings.objects.filter(user_id=user_id).select_related(
            "provider", "service", "user"
        )

        return [BookingResponseDTO.from_booking(booking) for booking in bookings]
