from rest_framework.routers import DefaultRouter
from .views_admin import AdminMenuItemViewSet, AdminLabelViewSet

router = DefaultRouter()
router.register(r"menu-items", AdminMenuItemViewSet, basename="admin-menu-item")
router.register(r"labels", AdminLabelViewSet, basename="admin-label")

urlpatterns = router.urls
