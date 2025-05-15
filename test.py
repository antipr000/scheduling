import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scheduling.settings")

import django

django.setup()

from booking.models.services import Services

service = Services(
    name="Test Service",
    duration=10,
)

service.save()

print(Services.objects.first().__dict__)
