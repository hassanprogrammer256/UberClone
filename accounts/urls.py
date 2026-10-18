from django.urls import path
from .views import *



urlpatterns = [
    path('auth/', auth_view, name='auth'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView, name='register'),
    path('customer/', CustomerIndexView, name='customer_index'),
    path('driver/', DriverIndexView, name='driver_index'),
    path('admin/', AdminIndexView, name='admin_index'),
]