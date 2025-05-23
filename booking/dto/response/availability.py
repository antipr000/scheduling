from booking.dto.base import BaseDTO
from booking.models.rooms import Rooms
from booking.models.services import Services
from datetime import datetime


class AvailabilitySlotDTO(BaseDTO):
    date: str
    start_time: int
    end_time: int
    provider_name: str
    service_name: str

    @staticmethod
    def from_room_and_service(
        date: datetime, start_time: int, room: Rooms, service: Services
    ) -> "AvailabilitySlotDTO":
        return AvailabilitySlotDTO(
            date=date.strftime("%Y-%m-%d"),
            start_time=start_time,
            end_time=start_time + service.duration,
            provider_name=room.provider.name,
            service_name=service.name,
        )
