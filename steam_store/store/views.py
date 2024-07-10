from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import SteamPayReplenishment, SteamPayReplenishmentCode
from .serializers import SteamPayReplenishmentSerializer, SteamPayReplenishmentCodeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view()
def store_root(request, format=None):
    return Response({
        'items': reverse(viewname='item-list', request=request, format=format),
        'steam_codes': reverse(viewname='steam-code-list', request=request, format=format),
    })
class SteamPayReplenishmentView(ModelViewSet):
    serializer_class = SteamPayReplenishmentSerializer
    queryset = SteamPayReplenishment.objects.all()


class SteamPayReplenishmentCodeView(ModelViewSet):
    serializer_class = SteamPayReplenishmentCodeSerializer
    queryset = SteamPayReplenishmentCode.objects.all()




