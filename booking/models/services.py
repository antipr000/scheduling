from booking.models.base import BaseModel
from django.db import models


class Services(BaseModel):
    name = models.CharField(max_length=255)
    duration = models.IntegerField()
    id_prefix = "svc"

    def __str__(self):
        return self.name

    class Meta:
        db_table = "services"
