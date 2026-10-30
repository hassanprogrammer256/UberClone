from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser, DriverProfile, CustomerProfile, AdminProfile
from django.dispatch import Signal
