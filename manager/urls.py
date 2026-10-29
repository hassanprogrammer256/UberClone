from django.urls import path
from .views import dashboard,CustomersView


urlpatterns = [
path('', dashboard, name='admin_index'),
path('customers/', CustomersView.as_view(), name='admin_customers')
]

