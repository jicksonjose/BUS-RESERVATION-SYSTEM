from rest_framework import serializers
from users.models import *


class SignupSerializers(serializers.ModelSerializer):
    class Meta:
        model = BusOwner
        fields = (
            'name',
            'phone',
            'email',
            'password'
        )