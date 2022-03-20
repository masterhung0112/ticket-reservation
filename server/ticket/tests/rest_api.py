"""This module tests the `/ticket` endpoint."""
from rest_framework import status
from rest_framework.test import APITestCase
import uuid

from ..models import SeatReservation, BookRequest

# def _get_expected_response():
#     return """
#     {
#         "ticket": ""
#     }
#     """

# @pytest.mark.django_db
# def test_book_flight(client)
#     response = client.get(f"/ticket/book", follow=True)
#     content = json.loads(response.content)
#     expected_response = json.loads(_get_expected_response())
#     assert content == expected_response
#     assert response.status_code == 200

class TicketBookTests(APITestCase):
    def test_new_book(self):
        url = '/ticket/book'
        data = {
            'username': 'name 1',
            'telephone': '+8434345345',
            'email': 'test@gmail.com',
            'seat_count': '4',
            'idempotent_id': str(uuid.uuid4())
        }
        response = self.client.post(url, data, format='json')
        # self.assertIsNone(response.data['error'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BookRequest.objects.count(), 1)
        self.assertEqual(SeatReservation.objects.count(), 4)
