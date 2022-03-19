from django.urls import path
from .views import TicketView
from .book import ticket_book

urlpatterns = [
    # /ticket
    path(r'', TicketView.as_view()),
    path('book', ticket_book)
]