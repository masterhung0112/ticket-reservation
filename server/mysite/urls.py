from django.urls import path, include

urlpatterns = [
    path(r'ticket/', include('ticket.apps.ticket.urls'))
]