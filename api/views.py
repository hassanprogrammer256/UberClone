from rest_framework.response import Response
from rest_framework import status
from .models import Location
from .serializers import Locationserializer
from rest_framework.viewsets import ModelViewSet


class LocationView(ModelViewSet):
    serializer_class = Locationserializer
    queryset = Location.objects.all()

    
    