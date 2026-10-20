from rest_framework.serializers import ModelSerializer
from .models import Location



class Locationserializer(ModelSerializer):
    class Meta:
        model = Location
        fields ='__all__'