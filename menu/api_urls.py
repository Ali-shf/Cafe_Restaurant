# menu/api_urls.py
from rest_framework.routers import DefaultRouter
from .api import DishViewSet

router = DefaultRouter()
router.register(r"dishes", DishViewSet, basename="dish")

urlpatterns = router.urls
