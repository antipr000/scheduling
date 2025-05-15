from booking.models.base import BaseModel
from django.db import models
from booking.models.providers import Providers


class Rooms(BaseModel):
    provider = models.ForeignKey(
        Providers, on_delete=models.CASCADE, db_column="providerId"
    )
    id_prefix = "room"

    def __str__(self):
        return f"Room {self.id} - {self.provider.name}"

    class Meta:
        db_table = "rooms"
