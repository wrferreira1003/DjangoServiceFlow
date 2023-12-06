from rest_framework.routers import DefaultRouter
from .views import TransacaoPorPedidoListView, AfiliadoDetailViewAlteracaoPagamento, ModelFinanceiroViewSet, ClienteDetailViewAlteracaoPagamento, TransacaoAfiliadoAdministradorViewSet
from django.urls import path

app_name = 'financeiro'  

router = DefaultRouter(trailing_slash=False) #False para nao precisar colocar / no final
router.register(r'financeiro', ModelFinanceiroViewSet)
router.register(r'financeiro-afiliado', TransacaoAfiliadoAdministradorViewSet)

urlpatterns = [
    # ... adicione suas URLs personalizadas aqui
    path('alterar-status-pg/<int:pedido__id>/', ClienteDetailViewAlteracaoPagamento.as_view(), name='alterar-status'),
    path('alterar-status-afiliado/<int:pedido__id>/', AfiliadoDetailViewAlteracaoPagamento.as_view(), name='alterar-status-afiliado'),
    path('transacoes/pedido/<int:id_pedido>/', TransacaoPorPedidoListView.as_view(), name='transacao-por-pedido'),
]

urlpatterns += router.urls