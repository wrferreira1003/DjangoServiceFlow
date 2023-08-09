from rest_framework import viewsets
from .serializers import ServicoSerializer
from .models import Servico

class ModelPedidoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
