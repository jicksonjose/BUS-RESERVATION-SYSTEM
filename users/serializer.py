from rest_framework import serializers
from users.models import *
from bus.models import *
from reservation.models import *

class BusOwnerSignupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['name', 'email', 'otp']



class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password=serializers.CharField()


class SearchBusDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusDetails
        fields = '__all__'

class BusPointsStopNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusPoints
        fields =  ['stop_name']

        
class BusReservationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusReservationDetails
        fields = '__all__'

class BusReservationSerializer(serializers.ModelSerializer):
    details = BusReservationDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = BusReservation
        fields = '__all__'


class UserSignupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = [ 'email', 'otp']


