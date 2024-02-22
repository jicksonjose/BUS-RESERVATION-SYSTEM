from rest_framework import serializers
from users.models import *
from bus.models import *


class BusOwnerSignupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['name', 'email', 'otp']



class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password=serializers.CharField()