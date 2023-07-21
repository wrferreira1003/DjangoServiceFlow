from rest_framework.routers import DefaultRouter
from .views import ModelPedidoViewSet

app_name = 'servicos'  

router = DefaultRouter(trailing_slash=False) #False para nao precisar colocar / no final
router.register(r'pedido', ModelPedidoViewSet)

urlpatterns = router.urls