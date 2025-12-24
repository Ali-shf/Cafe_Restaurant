# menu/api.py
from rest_framework.viewsets import ModelViewSet
from .models import Dish
from .serializers import DishReadSerializer, DishWriteSerializer
from .permissions import IsStaffOrReadOnly

class DishViewSet(ModelViewSet):
    queryset = Dish.objects.all().order_by("id")
    permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return DishWriteSerializer
        return DishReadSerializer
