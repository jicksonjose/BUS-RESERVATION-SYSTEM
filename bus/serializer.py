from rest_framework import serializers
from  .models import *



class BusDetailSerializer(serializers.ModelSerializer):
    # Define fields including the file field
    busrc = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    thumbnail = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)

    class Meta:
        model = BusDetails
        fields = ['busowner', 'busname', 'busrc', 'registration_number', 'thumbnail', 'ac_nonac', 'wifi', 'food', 'drink']

class BusDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusDetails
        fields = '__all__'

class BusRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusRoute
        fields = '__all__'
