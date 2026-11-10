from django.contrib import admin
from .models import Location,Vehicle,Trip

# Register your models here.
admin.site.register(Location)
admin.site.register(Vehicle)

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
 model = Trip
 list_display = ['customer',"driver",'origin','destination','requested_at']
 ordering =['-requested_at']

