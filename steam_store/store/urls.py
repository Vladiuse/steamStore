from rest_framework.routers import SimpleRouter
from .views import SteamPayReplenishmentView

router = SimpleRouter()
router.register('items', SteamPayReplenishmentView)

urlpatterns = router.urls