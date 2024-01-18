from django.db import models
from main.models import BaseModel

class BusOwner(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    

    class Meta:
        db_table = "bus_owner_table"
        verbose_name = 'Bus Owner '
        verbose_name_plural = 'Bus Owners '

    def __str__(self):
        return f"{self.first_name}-{self.last_name}"