from rest_framework.routers import DefaultRouter
from .views import AfiliadosViewSet

app_name = 'Afiliados'

router = DefaultRouter(trailing_slash=False) #False para nao precisar colocar / no final
router.register(r'afiliado', AfiliadosViewSet)

urlpatterns = router.urls