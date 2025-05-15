from rest_framework.views import APIView
from rest_framework.response import Response
from booking.services.availability import AvailabilityService
from rest_framework.status import HTTP_200_OK
from booking.services.booking import BookingService
from booking.dto.request.book import BookingRequestDTO
from booking.dto.response.book import BookingResponseDTO
from booking.dto.response.availability import AvailabilitySlotDTO


class AvailabilityView(APIView):
    def get(self, request, service_id):
        availability_service = AvailabilityService()
        available_dates = availability_service.get_available_dates_for_service(
            service_id
        )
        return Response(data=available_dates, status=HTTP_200_OK)


class AvailabilitySlotsView(APIView):
    def get(self, request, service_id, date):
        availability_service = AvailabilityService()
        slots = availability_service.get_available_slots_for_date(service_id, date)
        slot_dicts = [slot.model_dump() for slot in slots]
        return Response(data=slot_dicts, status=HTTP_200_OK)

    def post(self, request, service_id, date):
        booking_service = BookingService()
        booking_request: BookingRequestDTO = BookingRequestDTO.from_dict(request.data)
        booking_response = booking_service.create_booking(
            service_id, date, booking_request
        )
        return Response(data=booking_response.model_dump(), status=HTTP_200_OK)
