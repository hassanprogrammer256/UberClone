from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser, DriverProfile, CustomerProfile, AdminProfile
from django.dispatch import Signal


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created,**kwargs):
    if created and instance.role:
        role = instance.role.lower()
        
        with transaction.atomic():
            if role == 'driver':
                DriverProfile.objects.create(
                    user=instance, 
                    date_of_birth='2000-01-01'
                )
            elif role == 'customer':
                CustomerProfile.objects.create(
                    user=instance
                   
                )
            elif role == 'admin':
                AdminProfile.objects.create(
                    user=instance
                )
