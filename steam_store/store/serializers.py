from rest_framework.serializers import ModelSerializer
from .models import SteamPayReplenishment, SteamPayReplenishmentCode


class SteamPayReplenishmentSerializer(ModelSerializer):
    class Meta:
        model = SteamPayReplenishment
        fields = '__all__'


class SteamPayReplenishmentCodeSerializer(ModelSerializer):
    class Meta:
        model = SteamPayReplenishmentCode
        fields = '__all__'
