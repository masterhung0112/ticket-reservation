from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import TicketBookRequestSerializer
    
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
    
    return Response(
        {"isOK": True},
        status=status.HTTP_200_OK
    )