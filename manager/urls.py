from django.urls import path
from .views import dashboard, CustomersView, DriversView, EarningsView, TripsView


urlpatterns = [
path('', dashboard, name='admin_index'),
path('customers/', CustomersView.as_view(), name='admin_customers'),
path('drivers/', DriversView.as_view(), name='admin_drivers'),
path('trips/', TripsView.as_view(), name='admin_trips'),
path('earnings/', EarningsView.as_view(), name='admin_earnings'),
]

