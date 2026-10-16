from django.db import models
from django.contrib.auth.models import AbstractUser

USER_ROLES = (
    ('driver', 'Driver'),
    ('customer', 'Customer'),
    ('admin', 'Admin')
)

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.username

    def save(self,*args,**kwargs):
        self.is_superuser = self.role == 'admin'
        self.is_staff = self.role == 'admin'
        super().save(*args, **kwargs)


class Driver(CustomUser):

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.role = 'driver'
        super().save(*args, **kwargs)


class Customer(CustomUser):

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.role = 'customer'
        super().save(*args, **kwargs)
