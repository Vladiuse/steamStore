from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from .models import SteamPayReplenishment, SteamPayReplenishmentCode, SteamAccount
from .serializers import SteamPayReplenishmentSerializer, SteamPayReplenishmentCodeSerializer, SteamAccountSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view()
def store_root(request, format=None):
    return Response({
        'items': reverse(viewname='item-list', request=request, format=format),
        'steam_codes': reverse(viewname='steam-code-list', request=request, format=format),
        'steam_accounts': reverse(viewname='steam-account-list', request=request, format=format),
    })

class SteamPayReplenishmentView(ModelViewSet):
    serializer_class = SteamPayReplenishmentSerializer
    queryset = SteamPayReplenishment.available.all()


class SteamPayReplenishmentCodeView(ModelViewSet):
    serializer_class = SteamPayReplenishmentCodeSerializer
    queryset = SteamPayReplenishmentCode.objects.all()


class SteamAccountListView(ListAPIView):
    queryset = SteamAccount.objects.all()
    serializer_class = SteamAccountSerializer

