from django.db import models
import uuid
from rest_framework import serializers

class Flight(models.Model):
    objects = models.Manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    """Unique, anchor-generated id"""

    def __str__(self):
        return "flight " + self.id
    
class TicketBookRequest:
    _REQUIRED_FIELDS = {"iss", "sub", "iat", "exp"}

    username = ''
    usernumber= ''
    email = ''
    seat_count = 0

class TicketBookRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketBookRequest
        fields = (
            'username',
            'usernumber'
            'email',
            'seat_count',
        )