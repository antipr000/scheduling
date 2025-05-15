from booking.dto.base import BaseDTO


class ProviderLockParamsDTO(BaseDTO):
    provider_id: str
    date: str
    start_time: int
    end_time: int
