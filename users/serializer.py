from rest_framework import serializers
from users.models import *
from bus.models import *


class BusOwnerSignupSerializers(serializers.ModelSerializer):
    class Meta:
        model = BusOwner
        fields = ['name', 'email', 'phone', 'password']



class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password=serializers.CharField()