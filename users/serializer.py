from rest_framework import serializers
from users.models import *


class SignupSerializers(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.CharField() 
    password = serializers.CharField() 


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password=serializers.CharField()