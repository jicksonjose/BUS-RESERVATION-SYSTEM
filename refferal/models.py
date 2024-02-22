from unittest import signals
from django.db import models
from users.models import *
from bus.models import *
from reservation.models import *
from django.db import models
from main.models import *
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta


class ReferralCode(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='referral_codes')
    code = models.CharField(max_length=20, unique=True)
    referred_bus = models.ForeignKey(BusDetails, on_delete=models.SET_NULL, null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code

    # def generate_referral_code():
    #     return get_random_string(length=10)

    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         expiration_date = datetime.now() + timedelta(days=30)  # Set an expiration date, e.g., 30 days from creation
    #         ReferralCode.objects.create(user=instance, code=generate_referral_code(), expiration_date=expiration_date)

    # signals.post_save.connect(create_user_profile, sender=User)

