from booking.models.base import BaseModel
from django.db import models
import json


class Locks(BaseModel):
    name: str = models.CharField(max_length=255)
    params: str = models.JSONField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "locks"

    def get_params(self) -> dict:
        return json.loads(self.params)
