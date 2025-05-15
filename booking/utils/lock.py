from booking.models.locks import Locks
from booking.models.services import Services
from booking.utils.enums import LockEntity
from django.db import transaction
from booking.dto.internal.provider_lock_params import ProviderLockParamsDTO
from booking.dto.request.book import BookingRequestDTO
from typing import List
import time


def check_if_lock_exists(
    params: List[ProviderLockParamsDTO],
    date: str,
    booking_request: BookingRequestDTO,
    service: Services,
) -> bool:
    end_time = booking_request.start_time + service.duration
    lock = next(
        (
            param
            for param in params
            if param.provider_id == booking_request.provider_id
            and param.date == date
            and (
                (
                    param.start_time <= booking_request.start_time
                    and param.end_time >= booking_request.start_time
                )
                or (param.start_time <= end_time and param.end_time >= end_time)
            )
        ),
        None,
    )
    return lock is not None


def with_lock(entity: LockEntity, max_wait_time: int = 30):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with transaction.atomic():
                locks = list(Locks.objects.filter(name=entity.value).all())
                params = [lock.get_params() for lock in locks]
                param_dtos = [
                    ProviderLockParamsDTO.from_dict(param) for param in params
                ]
                service_id = args[1]  # service_id is second parameter
                date = args[2]  # date is third parameter
                booking_request = args[3]  # booking_request is fourth parameter
                service = Services.objects.get(id=service_id)
                start_time = time.time()
                print(f"Checking if lock exists for {entity.value}")
                while check_if_lock_exists(param_dtos, date, booking_request, service):
                    if time.time() - start_time > max_wait_time:
                        raise Exception("Failed to acquire lock")
                    time.sleep(1)

                # Acquire lock
                print(f"Acquiring lock for {entity.value}")
                lock_params = ProviderLockParamsDTO(
                    provider_id=booking_request.provider_id,
                    date=date,
                    start_time=booking_request.start_time,
                    end_time=booking_request.start_time + service.duration,
                )
                lock = Locks.objects.create(
                    name=entity.value, params=lock_params.model_dump_json()
                )

                resp = func(*args, **kwargs)
                # Release lock
                print(f"Releasing lock for {entity.value}")
                lock.delete()
                return resp

        return wrapper

    return decorator
