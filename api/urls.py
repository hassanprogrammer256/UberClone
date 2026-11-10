from django.urls import path,include
from .views import LocationView
from rest_framework.routers import DefaultRouter


router  = DefaultRouter()
router.register(r'locations',LocationView,basename='location')

urlpatterns = [
    path('',include(router.urls))
]
