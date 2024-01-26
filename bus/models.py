from django.db import models
from users.models import BusOwner
from main.models import BaseModel

class BusDocument(BaseModel):
    busowner = models.ForeignKey(BusOwner, on_delete=models.CASCADE, null=True , related_name='bus_doc',  db_column='bus_doc_id')
    busRc = models.CharField(max_length=100)
    owner_ID = models.CharField(max_length=100)
    is_verified =  models.BooleanField(default=False)

    def __str__(self):
        return self.busowner.name
    

class BusNumber(models.Model):
    busowner = models.ForeignKey(BusOwner, on_delete=models.CASCADE, null=True , related_name='bus_number_details',  db_column='bus_number')
    busnumber = models.CharField(max_length=100)

    def __str__(self):
        return self.busnumber

class BusDetails(models.Model):
    busowner = models.ForeignKey(BusOwner, on_delete=models.CASCADE, null=True , related_name='bus_details',  db_column='busowner_id')
    busname = models.CharField(max_length=100)
    thumbnail = models.CharField(max_length=100)
    busnumber = models.ForeignKey(BusNumber, on_delete=models.CASCADE, null=True , related_name='bus_number',  db_column='bus_num_id')
    seats = models.IntegerField(default=0)

    def __str__(self):
        return self.busname 
    

class BusFeature(BaseModel):
    bus = models.ForeignKey(BusDetails, on_delete=models.CASCADE, null=True, related_name='bus_features')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.title  



    
class BusRoutes(BaseModel):
    bus = models.ForeignKey(BusDetails, on_delete=models.CASCADE, null=True , related_name='source_destination')
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return f"{self.source} to {self.destination}"

class BusPoints(BaseModel):
    busId = models.ForeignKey(BusDetails, on_delete=models.CASCADE, null=True , related_name='bus_point_id')
    route = models.ForeignKey(BusRoutes, on_delete=models.CASCADE,null=True,  related_name='bus_points')
    starting_point = models.CharField(max_length=100)
    destination_point = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return f"{self.starting_point} to {self.destination_point} on {self.route}"
