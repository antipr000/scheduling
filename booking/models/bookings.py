from booking.models.base import BaseModel
from django.db import models
from booking.models.providers import Providers
from booking.models.services import Services
from booking.models.rooms import Rooms
from booking.models.users import Users


class Bookings(BaseModel):
    provider: models.ForeignKey[Providers] = models.ForeignKey(
        Providers, on_delete=models.CASCADE, db_column="providerId"
    )
    service: models.ForeignKey[Services] = models.ForeignKey(
        Services, on_delete=models.CASCADE, db_column="serviceId"
    )
    room: models.ForeignKey[Rooms] = models.ForeignKey(
        Rooms, on_delete=models.CASCADE, db_column="roomId"
    )
    user: models.ForeignKey[Users] = models.ForeignKey(
        Users, on_delete=models.CASCADE, db_column="userId"
    )
    start_time = models.IntegerField(db_column="startTime")
    end_time = models.IntegerField(db_column="endTime")
    date = models.DateTimeField()
    id_prefix = "book"

    def __str__(self):
        return f"Booking {self.id} - {self.user.name}"

    class Meta:
        db_table = "bookings"
