from rest_framework.routers import DefaultRouter
from .views import ClientesViewSet

app_name = 'cliente'

router = DefaultRouter(trailing_slash=False) #False para nao precisar colocar / no final
router.register(r'list', ClientesViewSet)

urlpatterns = router.urls