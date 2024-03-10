from django.db import models
from users.models import BusOwner
from main.models import BaseModel
from users.models import *




class BusDetails(models.Model):
    busowner = models.ForeignKey(BusOwner, on_delete=models.CASCADE, null=True , related_name='bus_details',  db_column='busowner_id')
    busname = models.CharField(max_length=100)
    busrc = models.ImageField(upload_to="busrc")
    registration_number = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to="busthumbnail")
    ac_nonac = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    food = models.BooleanField(default=False)
    drink = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    

    def __str__(self):
        return self.busname 
    


class BusRoute(BaseModel):
    bus = models.ForeignKey(BusDetails, on_delete=models.CASCADE, null=True , related_name='bus_route')
    start = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    starting_time =  models.CharField(max_length=100)
    destination_time = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.start} to {self.destination}"

    
class BusSchedule(BaseModel): 

    ACTIVE = 'active'
    INACTIVE = 'In-active'
    TYPE_CHOICES = [
        (ACTIVE, 'active'),
        (INACTIVE, 'In-active'),
    ]
    
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, null=True , related_name='route')
    date = models.CharField(max_length=100)
    status = models.CharField(max_length=100,choices=TYPE_CHOICES, default=ACTIVE)

    def __str__(self):
        return f"{self.route}"


class BusPoints(BaseModel):
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE,null=True,  related_name='bus_points')
    stop_name = models.CharField(max_length=100)
    stop_order = models.CharField(max_length=100)
    arrival_time = models.CharField(max_length=100)
    price = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.route} to {self.stop_name} on {self.stop_order}"


class BusStaff(models.Model):
    DRIVER = 'driver'
    STAFF = 'staff'

    TYPE_CHOICES = [
        (DRIVER, 'Driver'),
        (STAFF, 'Staff'),
    ]
    busowner = models.ForeignKey(BusOwner, on_delete=models.CASCADE, null=True , related_name='bus_detail',  db_column='busowner')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.first_name} - {self.type}"


class BusStaffSchedule(models.Model):
    staff = models.ForeignKey(BusStaff, on_delete=models.CASCADE, null=True, related_name='bus_staff')
    bus_schedule = models.ForeignKey(BusSchedule, on_delete=models.CASCADE, null=True, related_name='bus_schedule')
    
    def __str__(self):
        return f"{self.staff} - {self.bus_schedule}"








    
    



    
