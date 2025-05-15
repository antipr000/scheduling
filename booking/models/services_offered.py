from booking.models.base import BaseModel
from django.db import models
from booking.models.providers import Providers
from booking.models.services import Services


class ServicesOffered(BaseModel):
    provider: models.ForeignKey[Providers] = models.ForeignKey(
        Providers, on_delete=models.CASCADE, db_column="providerId"
    )
    service: models.ForeignKey[Services] = models.ForeignKey(
        Services, on_delete=models.CASCADE, db_column="serviceId"
    )
    id_prefix = "svo"

    def __str__(self):
        return f"{self.provider.name} - {self.service.name}"

    class Meta:
        db_table = "services_offered"
        unique_together = ("provider", "service")
