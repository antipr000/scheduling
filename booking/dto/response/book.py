from booking.dto.base import BaseDTO
from booking.models.bookings import Bookings


class BookingResponseDTO(BaseDTO):
    booking_id: str
    provider_name: str
    service_name: str
    user_id: str
    email: str
    start_time: int
    end_time: int
    date: str

    @staticmethod
    def from_booking(booking: Bookings) -> "BookingResponseDTO":
        return BookingResponseDTO(
            booking_id=booking.id,
            provider_name=booking.provider.name,
            service_name=booking.service.name,
            user_id=booking.user.id,
            email=booking.user.email,
            start_time=booking.start_time,
            end_time=booking.end_time,
            date=booking.date.strftime("%Y-%m-%d"),
        )
