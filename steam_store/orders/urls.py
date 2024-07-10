from rest_framework import routers
from django.urls import path, include, re_path
from . import views
router = routers.SimpleRouter()
router.register('orders', views.OrderView)

urlpatterns = [
    path('', include(router.urls),),
    path('', views.orders_root, name='orders_root'),
]