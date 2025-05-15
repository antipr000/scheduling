from django.urls import path
from booking.views.health import HealthView
from booking.views.service import AvailabilityView, AvailabilitySlotsView
from booking.views.booking import BookingView

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path(
        "service/<str:service_id>/availability",
        AvailabilityView.as_view(),
        name="availability",
    ),
    path(
        "service/<str:service_id>/availability/<str:date>",
        AvailabilitySlotsView.as_view(),
        name="availability_slots",
    ),
    path("booking/<str:user_id>", BookingView.as_view(), name="bookings"),
]
