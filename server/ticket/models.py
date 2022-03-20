from django.db import models
import uuid
from rest_framework import serializers

###
# DTO Models
##
class TicketBookRequest:
    """
    User input the required fields
    """
    _REQUIRED_FIELDS = {"username", "telephone", "email", "seat_count", "idem_id"}

    username = ''
    telephone= ''
    email = ''
    seat_count = 0
    idem_id = ''

class TicketBookRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketBookRequest
        fields = (
            'username',
            'usernumber'
            'email',
            'seat_count',
        )

class FlightSeats:
    """
    Contains the state of all seats in the flight
    """
    seats = []
    
###
# DB Models
##
class Flight(models.Model):
    objects = models.Manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    """Unique, anchor-generated id"""

    #Destination = models.TextField(null=False, blank=False)


    def __str__(self):
        return "flight " + self.id
    
class User(models.Model):
    objects = models.Manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField(max_length=512)
    email = models.TextField()
    telephone = models.TextField()


class SeatReservation(models.Model):
    objects = models.Manager()

    flight = models.OneToOneField(
        Flight, primary_key=True, on_delete=models.CASCADE)
    )

    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)
    )
    """The user who booked this seat"""

    seatId = models.TextField()
    """The ID of seat """

    class Meta:
        unique_together = (("flight", "seatId"),)

    def __str__(self):
        return f"seatreservation: {self.flight.id} {self.seatId}"
