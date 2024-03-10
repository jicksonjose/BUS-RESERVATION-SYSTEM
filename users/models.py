from django.db import models
from main.models import BaseModel
from django.utils import timezone

class BusOwner(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.CharField(max_length=100)
    idproof = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


    class Meta:
        db_table = "bus_owner_table"
        verbose_name = 'Bus Owner '
        verbose_name_plural = 'Bus Owners '

    def __str__(self):
        return self.name
    
class Otp(models.Model):
    otp = models.CharField(max_length=6, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    attempt = models.PositiveIntegerField(default=0)
    expiration_time = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name

    def is_valid(self):
        """
        Check if the OTP is still valid based on the expiration time.
        """
        return not self.is_expired and (self.expiration_time is None or self.expiration_time > timezone.now())


class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email =models.CharField(max_length=100)
    password =models.CharField(max_length=100)
    refferalcode = models.CharField(max_length=100)
    refferalcode_status = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




    