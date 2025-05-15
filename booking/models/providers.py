from booking.models.base import BaseModel
from django.db import models


class Providers(BaseModel):
    name = models.CharField(max_length=255)
    id_prefix = "prv"

    def __str__(self):
        return self.name

    class Meta:
        db_table = "providers"
