from booking.dto.base import BaseDTO


class BookingRequestDTO(BaseDTO):
    provider_id: str
    user_id: str
    start_time: int
