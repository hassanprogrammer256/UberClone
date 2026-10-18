from django.urls import path
from .views import manager_dashboard


urlpatterns = [
path('', manager_dashboard, name='admin_index')
]