from rest_framework import viewsets
from .models import Transacao
from .serializers import TransacaoSerializer, ClienteSerializerAlteracao
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

class ModelFinanceiroViewSet(viewsets.ModelViewSet):
  queryset = Transacao.objects.all()
  serializer_class = TransacaoSerializer

#Alteracao de informacoes no banco de dados
class ClienteDetailViewAlteracaoPagamento(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Transacao.objects.all()
    serializer_class = ClienteSerializerAlteracao
    lookup_field = 'pedido__id'