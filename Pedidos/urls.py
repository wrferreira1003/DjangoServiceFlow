from rest_framework.routers import DefaultRouter
from .views import NovoPedidoViewSet,criar_cliente_com_relacionados
from django.urls import path

app_name = 'pedidos'

router = DefaultRouter(trailing_slash=False)
router.register(r'pedidos',NovoPedidoViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('criar_cliente/', criar_cliente_com_relacionados, name='criar_cliente_com_relacionados'),
    # ... outras rotas ...
]

