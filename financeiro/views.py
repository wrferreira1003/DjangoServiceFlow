from rest_framework import viewsets
from .models import Transacao, TransacaoAfiliadoAdministrador
from .serializers import TransacaoSerializer, ClienteSerializerAlteracao, TransacaoAfiliadoAdministradorSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import ListAPIView

class ModelFinanceiroViewSet(viewsets.ModelViewSet):
  queryset = Transacao.objects.all()
  serializer_class = TransacaoSerializer

#Alteracao de informacoes no banco de dados
class ClienteDetailViewAlteracaoPagamento(UpdateAPIView):
    queryset = Transacao.objects.all()
    serializer_class = ClienteSerializerAlteracao
    lookup_field = 'pedido__id'

class TransacaoAfiliadoAdministradorViewSet(viewsets.ModelViewSet):
  queryset = TransacaoAfiliadoAdministrador.objects.all()
  serializer_class = TransacaoAfiliadoAdministradorSerializer

#Alteracao de informacoes no banco de dados
class AfiliadoDetailViewAlteracaoPagamento(UpdateAPIView):
    queryset = TransacaoAfiliadoAdministrador.objects.all()
    serializer_class = TransacaoAfiliadoAdministradorSerializer
    lookup_field = 'pedido__id'

class TransacaoPorPedidoListView(ListAPIView):
    serializer_class = TransacaoAfiliadoAdministradorSerializer

    def get_queryset(self):
        """
        Este view retorna uma lista de todas as transações para o pedido dado pelo 'id_pedido' na URL.
        """
        id_pedido = self.kwargs['id_pedido']
        return TransacaoAfiliadoAdministrador.objects.filter(servico_id=id_pedido)

