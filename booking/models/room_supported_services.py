from booking.models.base import BaseModel
from django.db import models
from booking.models.rooms import Rooms
from booking.models.services import Services


class RoomSupportedServices(BaseModel):
    room: models.ForeignKey[Rooms] = models.ForeignKey(
        Rooms, on_delete=models.CASCADE, db_column="roomId"
    )
    service: models.ForeignKey[Services] = models.ForeignKey(
        Services, on_delete=models.CASCADE, db_column="serviceId"
    )
    id_prefix = "rss"

    def __str__(self):
        return f"{self.room} - {self.service.name}"

    class Meta:
        db_table = "room_supported_services"
        unique_together = ("room", "service")
