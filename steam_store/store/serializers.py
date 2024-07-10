from rest_framework.serializers import ModelSerializer
from .models import SteamPayReplenishment



class SteamPayReplenishmentSerializer(ModelSerializer):

    class Meta:
        model = SteamPayReplenishment
        fields = '__all__'


