from rest_framework import serializers
from  .models import *
from reservation.models import *


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

class BusScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusSchedule
        fields = '__all__'


class BusRouteSerializerdata(serializers.ModelSerializer):
    class Meta:
        model = BusRoute
        fields = ('id','start', 'destination')

class BusDetailListSerializerdata(serializers.ModelSerializer):
    class Meta:
        model = BusDetails
        fields = ('busname',)



class BusScheduleSerializer(serializers.ModelSerializer):
    bus_name = serializers.CharField(source='route.bus.busname', read_only=True)
    route = BusRouteSerializerdata()
    class Meta:
        model = BusSchedule
        fields = ['id', 'bus_name', 'route', 'date', 'status']


class BusPointsSerializer(serializers.ModelSerializer):
    route = serializers.UUIDField(write_only=True)

    class Meta:
        model = BusPoints
        fields = ['route', 'stop_name', 'stop_order', 'arrival_time', 'price']


class ViewBusPointsSerializer(serializers.ModelSerializer):
    
    route = BusRouteSerializerdata()
    bus_name = serializers.CharField(source='route.bus', read_only=True)

    class Meta:
        model = BusPoints
        fields = ['route','bus_name', 'stop_name', 'stop_order', 'arrival_time', 'price']



class BusStaffSerializerList(serializers.ModelSerializer):
    class Meta:
        model = BusStaff
        fields ='__all__'

class BusStaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStaff
        fields ='__all__'

class BusStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStaff
        fields = ['id', 'first_name', 'last_name', 'phone', 'type']


class BusStaffScheduleSerializer(serializers.ModelSerializer):
    staff = BusStaffSerializer()
    bus_schedule = BusScheduleSerializer()

    class Meta:
        model = BusStaffSchedule
        fields = ['id', 'staff', 'bus_schedule']


#=========Bus Reservation Serializer =================================
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BusRoute
#         fields = ('id','first_name', 'last_name')
class BusReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.first_name')  # Access user's first name
    user_last_name = serializers.StringRelatedField(source='user.last_name')  # Access user's last name
    route_start = serializers.StringRelatedField(source='pickup.route.start')  # Access route's start
    route_destination = serializers.StringRelatedField(source='pickup.route.destination')  # Access route's destination
    bus_name = serializers.StringRelatedField(source='bus.busname')  # Access bus name
    bus_id = serializers.PrimaryKeyRelatedField(source='bus.id', read_only=True)  # Access bus ID
    route_id = serializers.PrimaryKeyRelatedField(source='pickup.route.id', read_only=True)  
    user_phone = serializers.StringRelatedField(source='user.phone', read_only=True)  
    user_email = serializers.StringRelatedField(source='user.email', read_only=True)  

    class Meta:
        model = BusReservation
        fields = ['id',
                   'pickup', 
                   'route_start',
                    'route_destination',
                    'user', 
                    'user_last_name', 
                    'date', 'total', 
                    'payment_status', 
                    'referral_code_used', 
                    'referred_user', 
                    'bus_name', 
                    'bus_id',
                    'route_id',
                    'user_phone',
                    'user_email',
                    'dropoff'
                    ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['pickup'] = BusPointsSerializer(instance.pickup).data
        return representation
    

class BusPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusPoints
        fields = ['id', 'route', 'stop_name', 'stop_order', 'arrival_time', 'price']

class BusReservationListSerializer(serializers.ListSerializer):
    child = BusReservationSerializer()     


class BusReservationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusReservationDetails
        fields = ['reservation', 'name', 'age', 'gender', 'ticket_number', 'seat_number', 'price']
