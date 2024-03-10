from django.db import models
from users.models import *
from bus.models import *
from refferal.models import *


PAYMENT_STATUS = [
    ('SUCCESS', 'success'),
    ('FAILURE', 'failure')
]

class BusReservation(models.Model):
    bus = models.ForeignKey(BusDetails, on_delete=models.CASCADE, null=True, related_name='bus_reservations')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='user_reservations')
    date = models.DateField(auto_now_add=True, null=True)
    total = models.PositiveIntegerField()
    payment_status = models.CharField(max_length=255, choices=PAYMENT_STATUS)
    referral_code_used = models.CharField(max_length=100, null=True, blank=True, default='0')
    referred_user = models.CharField(max_length=100, null=True, blank=True, default='0')
   
    pickup = models.ForeignKey(BusPoints, on_delete=models.CASCADE, null=True, related_name='pickup_reservations')
    dropoff = models.ForeignKey(BusPoints, on_delete=models.CASCADE, null=True, related_name='dropoff_reservations')

    def __str__(self):
        return f"{self.user} - {self.pickup} to {self.dropoff}"



class BusReservationDetails(models.Model):
    reservation = models.ForeignKey(BusReservation, on_delete=models.CASCADE, null=True, related_name='bus_reservation')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    ticket_number = models.CharField(max_length=100)
    seat_number = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.reservation} - {self.name}"