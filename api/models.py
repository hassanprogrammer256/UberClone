from django.db import models
import uuid
from accounts.models import DriverProfile,CustomerProfile



VEHICLE_STATUSES = [
    ('available','Available'),
    ('on_trip','On Trip'),
    ('mechanical_breakdown','Mechanical Breakdown')
]

class Location(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,unique=True,default=uuid.uuid4)
    name = models.CharField(max_length=50,unique=True)
    lat= models.CharField(max_length=15)
    long= models.CharField(max_length=15)

    class Meta:
        ordering = ['name']
        verbose_name = 'Destination'
        verbose_name_plural = 'Destinations'

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    driver = models.ForeignKey(DriverProfile,on_delete=models.CASCADE,null=True,blank=True)
    plate_number = models.CharField(max_length=15,unique=True)
    model = models.CharField(max_length=15)
    color = models.CharField(max_length=15)
    capacity= models.IntegerField(default=1)
    status  =  models.CharField(max_length=20,choices=VEHICLE_STATUSES,default='available')

    def __str__(self):
        return self.plate_number

class Trip(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True)
    driver = models.ForeignKey(DriverProfile,on_delete=models.CASCADE)
    trip_date = models.DateField(auto_created=True)
    origin = models.ForeignKey(Location,on_delete=models.CASCADE,verbose_name="From",related_name="origins")
    destination = models.ForeignKey(Location,on_delete=models.CASCADE,verbose_name="To",related_name="destinations")
    requested_at = models.TimeField(auto_created=True)


    def __str__(self):
        return f"Trip- {self.id}: {self.origin} to {self.destination}"
