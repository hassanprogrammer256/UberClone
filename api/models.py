from django.db import models
import uuid
from accounts.models import DriverProfile,CustomerProfile
from django.db.models import Q



VEHICLE_STATUSES = [
    ('available','Available'),
    ('on_trip','On Trip'),
    ('mechanical_breakdown','Mechanical Breakdown')
]

TRIP_STATUSES = [
    ('completed','Completed'),
    ('in_progress','In Progress'),
    ('cancelled','Cancelled')
]

PAYMENT_METHODS = [
    ('cash','Cash'),
    ('mtn_momo','MTN MOMO'),
    ('airtel_money','Airtel Money'),
    ('credit_card','Credit Card'),
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
    name = models.CharField(max_length=50)
    driver = models.ForeignKey(DriverProfile,on_delete=models.CASCADE,null=True,blank=True)
    plate_number = models.CharField(max_length=15,unique=True)
    model = models.CharField(max_length=15)
    color = models.CharField(max_length=15)
    capacity= models.IntegerField(default=1)
    status  =  models.CharField(max_length=20,choices=VEHICLE_STATUSES,default='available')

    def __str__(self):
        return self.plate_number



class CustomerPayment(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.SET_NULL,null=True)
    trip = models.ForeignKey("Trip",on_delete=models.SET_NULL,null=True)
    amount =models.IntegerField(default=0)
    payment_method = models.CharField(max_length=15,choices=PAYMENT_METHODS,default="cash")
    payment_date = models.DateField(auto_created=True)
    payment_time = models.TimeField(auto_created=True)

# will be triggered in signals.py when a customer makes a payment for a trip
class Trip(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True)
    driver = models.ForeignKey(DriverProfile,on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle,on_delete=models.SET_NULL,null=True)
    trip_date = models.DateField(auto_created=True)
    origin = models.ForeignKey(Location,on_delete=models.CASCADE,verbose_name="From",related_name="origins")
    destination = models.ForeignKey(Location,on_delete=models.CASCADE,verbose_name="To",related_name="destinations")
    requested_at = models.TimeField(auto_created=True)
    status = models.CharField(max_length=12,choices=TRIP_STATUSES,default='in_progress') 


    def __str__(self):
        return f"Trip- {self.id}: {self.origin} to {self.destination}"

    @property
    def is_trip_paid(self):
        return CustomerPayment.objects.filter(
            Q(trip=self.id) & Q(customer=self.customer) & Q(payment_date = self.trip_date) 
            & Q(payment_time = self.requested_at)
        )


