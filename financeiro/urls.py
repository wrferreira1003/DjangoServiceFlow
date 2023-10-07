from rest_framework.routers import DefaultRouter
from .views import ModelFinanceiroViewSet, ClienteDetailViewAlteracaoPagamento
from django.urls import path

app_name = 'financeiro'  

router = DefaultRouter(trailing_slash=False) #False para nao precisar colocar / no final
router.register(r'financeiro', ModelFinanceiroViewSet)

urlpatterns = [
    # ... adicione suas URLs personalizadas aqui
    path('alterar-status-pg/<int:pedido__id>/', ClienteDetailViewAlteracaoPagamento.as_view(), name='alterar-status'),
]

urlpatterns += router.urls