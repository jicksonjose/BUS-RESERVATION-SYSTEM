from rest_framework import serializers
from  .models import *


class BusDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusDocument
        fields = ['busowner', 'busRc', 'owner_ID']


class BusDetailsSerializer(serializers.ModelSerializer):
    busnumber = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=BusNumber.objects.all(), required=False)

    class Meta:
        model = BusDetails
        fields = ['busowner', 'busname', 'thumbnail', 'busnumber', 'seats']