from rest_framework.routers import SimpleRouter
from django.urls import path, include
from . import views
router = SimpleRouter()
router.register('items', views.SteamPayReplenishmentView, basename='item')
router.register('steam-codes', views.SteamPayReplenishmentCodeView, basename='steam-code')

urlpatterns = [
    path('', include(router.urls),),
    path('', views.store_root, name='store_root'),
]
