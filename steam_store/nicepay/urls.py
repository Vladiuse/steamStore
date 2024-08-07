from rest_framework.routers import SimpleRouter
from . import views
from django.urls import include, path


router = SimpleRouter()
router.register('payment', views.PaymentView, basename='payment')

urlpatterns = [
    path('', views.nicepay_root, name='nicepay_root'),
    path('nicepay_vars/', views.nicepay_vars, name='nicepay_vars'),
    path('', include(router.urls),),
]