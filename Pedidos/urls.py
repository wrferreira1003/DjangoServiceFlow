from rest_framework.routers import DefaultRouter
from .views import EmprestimoEmGeralViewSet, ConsultaSimplesServicosView, ClienteSemCadastroView, ClienteFinanciamentoImoveis, ClienteFinanciamentoVeiculo, ClienteDetailViewAlteracaoStatusAdmAfiliado,criar_cliente_com_relacionados,NovoClienteDetailView,TodosClientesView,ClienteDetailView,TodosClientesViewSemFiltro,ClienteDetailViewAlteracao,AtualizaClienteView,PedidosPorAfiliadoListView, PedidosPorClienteListView, delete_documento_api,PedidosPorFuncionarioListView
from django.urls import path

app_name = 'pedidos'

router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns = [
    path('criar_cliente/', criar_cliente_com_relacionados, name='criar_cliente_com_relacionados'),
    path('financiamento/', ClienteFinanciamentoVeiculo, name='processo_financiamento'),
    path('imoveis/', ClienteFinanciamentoImoveis, name='processo_financiamento_imoveis'),
    path('client_sem_cadastro/', ClienteSemCadastroView, name='client_sem_cadastro'),
    path('emprestimo_geral/', EmprestimoEmGeralViewSet.as_view(), name='emprestimo_geral'),
    
    path('consulta_geral/', ConsultaSimplesServicosView.as_view(), name='servico_geral'),
    path('requests/<str:id>/', NovoClienteDetailView.as_view(), name='cliente-detail'),
    path('listrequest/', TodosClientesView.as_view(), name='todos-clientes'),
    path('listrequests/', TodosClientesViewSemFiltro.as_view(), name='todos-clientes-sem-filtro'),
    path('deleterequest/<int:id>/', ClienteDetailView.as_view(), name='cliente-detail'),
    path('statusrequest/<int:id>/', ClienteDetailViewAlteracao.as_view(), name='cliente-Status_detail'),
    path('statusadmafiliado/<int:id>/', ClienteDetailViewAlteracaoStatusAdmAfiliado.as_view(), name='cliente-Status_afiliadoAdm'),
    path('atualizarequest/<int:id>/', AtualizaClienteView, name='cliente-Atualiza'),
    
    path('pedidos_por_funcionario/<int:funcionario_id>/', PedidosPorFuncionarioListView.as_view(), name='pedidos-por-funcionario'),
    path('pedidos_por_afiliado/<int:afiliado_id>/', PedidosPorAfiliadoListView.as_view(), name='pedidos_por_afiliado'),
    path('pedidos_por_cliente/<int:cliente_id>/', PedidosPorClienteListView.as_view(), name='pedidos_por_cliente'),
    
    path('documento/delete/<int:documento_id>/', delete_documento_api, name='delete_documento_api'),
]
