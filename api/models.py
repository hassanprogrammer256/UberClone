from django.db import models
import uuid

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



