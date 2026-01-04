from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from menu.models import MenuItem, Label
from menu.serializers import MenuItemSerializer, LabelSerializer
from .permissions import IsOwnerOrAdmin


class AdminMenuItemViewSet(ModelViewSet):
    """
    Admin panel for full menu management
    """
    queryset = MenuItem.objects.all().prefetch_related("labels").order_by("-id")
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


class AdminLabelViewSet(ModelViewSet):
    """
    Admin panel for label management
    """
    queryset = Label.objects.all().order_by("name")
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
