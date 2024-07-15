from rest_framework.serializers import ModelSerializer
from .models import SteamPayReplenishment, SteamPayReplenishmentCode, SteamAccount


class SteamPayReplenishmentSerializer(ModelSerializer):
    class Meta:
        model = SteamPayReplenishment
        fields = '__all__'


class SteamPayReplenishmentCodeSerializer(ModelSerializer):
    class Meta:
        model = SteamPayReplenishmentCode
        fields = '__all__'


class SteamAccountSerializer(ModelSerializer):
    class Meta:
        model = SteamAccount
        fields = '__all__'
