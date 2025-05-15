from rest_framework.views import APIView
from rest_framework.response import Response
from booking.services.booking import BookingService
from rest_framework.status import HTTP_200_OK


class BookingView(APIView):
    def get(self, request, user_id: str):
        booking_service = BookingService()
        booking_response = booking_service.get_bookings(user_id)
        booking_dicts = [booking.model_dump() for booking in booking_response]
        return Response(data=booking_dicts, status=HTTP_200_OK)
