from .serializers import AfiliadosModelSerializer
from rest_framework import viewsets, permissions
from .models import AfiliadosModel

class AfiliadosViewSet(viewsets.ModelViewSet):
    queryset = AfiliadosModel.objects.all()
    serializer_class = AfiliadosModelSerializer
    permission_classes = [permissions.IsAuthenticated]
