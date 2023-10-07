from rest_framework import viewsets
from .serializers import CategoriaSerializer,ServicoSerializer
from .models import Categoria, Servico

class ModelPedidoViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ModelServicoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
