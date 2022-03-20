from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.http import JsonResponse
import uuid
import random
import string

from .models import TicketBookRequestSerializer, BookRequest, SeatReservation
from .seat_allocation import NotEnoughSeatException, mapReservedSeatsToArray, findAvailableSeatsFor242, lotLocalIdx2SeatId

@api_view(["POST"])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def ticket_book(request: Request) -> Response:
    """
    POST /ticket/book

    Accept the number of seat
    """
    data = JSONParser().parse(request)
    ticket_book_request_serializer = TicketBookRequestSerializer(data=data)
    if not ticket_book_request_serializer.is_valid():
        return JsonResponse(ticket_book_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    flightId = "VNJ234"
    allSeatRowCount = 8
    seatFormat = [2, 4, 2]

    ticket_book_request = ticket_book_request_serializer.data
    # print('ticket_book_request', ticket_book_request)
    # try:
    #     print('ticket_book_request',ticket_book_request)
    #     BookRequest.objects.get(idempotent_id = ticket_book_request.idempotent_id)
    #     return Response(
    #         {"error": f"Duplicate idempotent ID {ticket_book_request.idempotent_id}"},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )
    # except (ObjectDoesNotExist):
    #     pass
    # Query all allocated seats for the flight

    try:
        # Find 
        book_request = BookRequest()
        book_request.id = str(uuid.uuid4())
        book_request.name = ticket_book_request.get('username')
        book_request.telephone = ticket_book_request.get('telephone')
        book_request.email = ticket_book_request.get('email')
        book_request.idempotent_id = ticket_book_request.get('idempotent_id')
        book_request.save()
        
        seat_count = int(ticket_book_request.get('seat_count'))

        if seat_count > 64:
            return Response(
                {"error": "Not enough seat"},
                status=status.HTTP_400_BAD_REQUEST
            )

        allSeatReservations = SeatReservation.objects.filter(
            flightId = flightId
        )

        allReservedSeats = []

        # Create a list of all reserved seats
        # Ex: ["1A", "2B"]
        for seatReservation in allSeatReservations:
            allReservedSeats.append(seatReservation.seatId)

        reservedSeatMap = mapReservedSeatsToArray(allSeatRowCount, allReservedSeats)

        # Find the free seats
        allocatedSeatRows = findAvailableSeatsFor242(seat_count, reservedSeatMap)

        allocatedSeatIds = []

        # There is enough seat, write the allocated seat to DB
        for rowIdx, allocatedSeatRow in enumerate(allocatedSeatRows):
            for slotIdx, allocatedSeatLot in enumerate(allocatedSeatRow):
                for allocatedSeatLocalIdx in allocatedSeatLot:
                    seatReservation = SeatReservation()
                    seatReservation.flightId = flightId
                    seatReservation.request = book_request
                    seatReservation.seatId = lotLocalIdx2SeatId(rowIdx, slotIdx, allocatedSeatLocalIdx, seatFormat)
                    seatReservation.save()
                    allocatedSeatIds.append(seatReservation.seatId)
        # print('allocatedSeatIds', allocatedSeatIds)

        # Generate PNR number after all processing is successful
        book_request.pnr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        book_request.save()

        return Response(
            {"allocated_seats": allocatedSeatIds, "request": { 
                    "pnr": book_request.pnr
                }
            },
            status=status.HTTP_200_OK
        )
        
    except NotEnoughSeatException:
        # Not enough seats
        return Response(
            {"error": "Not enough seat"},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )