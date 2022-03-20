from django.db import models
import uuid
from rest_framework import serializers
from django.core.validators import EmailValidator

###
# DTO Models
##
class TicketBookRequest(models.Model):
    """
    User input the required fields
    """
    # _REQUIRED_FIELDS = {"username", "telephone", "email", "seat_count", "idempotent_id"}

    username = models.TextField()
    telephone = models.TextField()
    email = models.TextField()
    seat_count = models.TextField()
    idempotent_id  = models.TextField()

class TicketBookRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketBookRequest
        fields = (
            'username',
            'telephone',
            'email',
            'seat_count',
            'idempotent_id',
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
    
class BookRequest(models.Model):
    objects = models.Manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField(max_length=512)
    email = models.TextField(validators=[EmailValidator])
    telephone = models.TextField()
    idempotent_id = models.TextField()
    pnr = models.TextField()

class SeatReservation(models.Model):
    objects = models.Manager()

    # flight = models.OneToOneField(
    #     Flight, primary_key=True, on_delete=models.CASCADE)
    # )
    flightId = models.TextField()

    request = models.OneToOneField(
        BookRequest, primary_key=True, on_delete=models.CASCADE
    )
    """The request which booked this seat"""

    seatId = models.TextField()
    """The ID of seat """

    class Meta:
        unique_together = (("flightId", "seatId"),)

    def __str__(self):
        return f"seatreservation: {self.flight.id} {self.seatId}"
