from .serializers import ClienteSerializer
from rest_framework import viewsets, permissions
from .models import Cliente

class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
