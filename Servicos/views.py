from rest_framework import viewsets
from .models import ModelPedido
from .serializers import ModelPedidoSerializers


class ModelPedidoViewSet(viewsets.ModelViewSet):
    queryset = ModelPedido.objects.all()
    serializer_class = ModelPedidoSerializers
