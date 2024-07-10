from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import SteamPayReplenishment
from .serializers import SteamPayReplenishmentSerializer


class SteamPayReplenishmentView(ModelViewSet):
    serializer_class = SteamPayReplenishmentSerializer
    queryset = SteamPayReplenishment.objects.all()




