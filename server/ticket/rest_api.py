from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

@api_view(['POST'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def flight_book(request: Request) -> Response:
    info_data = {
        "flight": ""
    }

    return Response(info_data)