from django.contrib import admin
from .models import Driver, Customer
# Register your models here.
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'phone_number')
    list_filter = ('role',)
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'phone_number')
    list_filter = ('role',)
    search_fields = ('username', 'email', 'first_name', 'last_name')