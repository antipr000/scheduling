from booking.models.base import BaseModel
from django.db import models


class Users(BaseModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    id_prefix = "usr"

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        db_table = "users"
