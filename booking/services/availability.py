from booking.models.bookings import Bookings
from booking.models.providers import Providers
from booking.models.services import Services
from booking.models.rooms import Rooms
from booking.models.room_supported_services import RoomSupportedServices
from typing import List
from booking.dto.response.availability import AvailabilitySlotDTO
from datetime import datetime, timedelta


class AvailabilityService:
    def _check_if_room_available(
        self,
        bookings: List[Bookings],
        room: Rooms,
        date: datetime,
        start_time: int,
        end_time: int,
    ) -> bool:
        booking = next(
            (
                booking
                for booking in bookings
                if booking.room.id == room.id
                and booking.date.date() == date.date()
                and (
                    (
                        booking.start_time <= start_time
                        and booking.end_time >= start_time
                    )
                    or (booking.start_time <= end_time and booking.end_time >= end_time)
                )
            ),
            None,
        )

        return booking is None

    def get_available_dates_for_service(self, service_id: str) -> List[str]:
        service = Services.objects.get(id=service_id)

        # Look for next 30 days
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)

        bookings = (
            Bookings.objects.filter(service=service, date__range=(start_date, end_date))
            .select_related("room")
            .all()
        )

        duration = service.duration

        room_supported_services = (
            RoomSupportedServices.objects.filter(service=service)
            .select_related("room")
            .all()
        )

        rooms = [
            room_supported_service.room
            for room_supported_service in room_supported_services
        ]

        # Now we will loop through each day and check if there is any room available for that day
        available_dates = set()
        date = start_date
        while date < end_date:
            for room in rooms:
                for start_time in range(0, 24 * 60, duration):
                    end_time = start_time + duration

                    is_available = self._check_if_room_available(
                        bookings, room, date, start_time, end_time
                    )

                    if is_available:
                        available_dates.add(date.strftime("%Y-%m-%d"))

            date += timedelta(days=1)

        return list(available_dates)

    def get_available_slots_for_date(
        self, service_id: str, date: str
    ) -> List[AvailabilitySlotDTO]:
        service = Services.objects.get(id=service_id)
        date = datetime.strptime(date, "%Y-%m-%d")

        bookings = (
            Bookings.objects.filter(service=service, date=date)
            .select_related("room")
            .all()
        )

        room_supported_services = (
            RoomSupportedServices.objects.filter(service=service)
            .select_related("room", "room__provider")
            .all()
        )

        rooms = [
            room_supported_service.room
            for room_supported_service in room_supported_services
        ]

        slots = []
        for time in range(0, 24 * 60, service.duration):
            for room in rooms:
                # Check if the room is available for the given time
                is_available = self._check_if_room_available(
                    bookings, room, date, time, time + service.duration
                )

                if is_available:
                    slots.append(
                        AvailabilitySlotDTO.from_room_and_service(
                            date, time, room, service
                        )
                    )

        return slots
