from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import AfiliadosViewSet, RegistrarAfiliadoView, LoginView,AfiliadosPublicosView,TodosAfiliadosViewSet

app_name = 'Afiliados'

router = DefaultRouter(trailing_slash=False) #False para nao precisar colocar / no final
router.register(r'afiliado', AfiliadosViewSet)
router.register(r'todos_afiliados', TodosAfiliadosViewSet, basename='todos_afiliados')

urlpatterns = router.urls


urlpatterns = [
    path('register/', RegistrarAfiliadoView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('afiliados-publicos/', AfiliadosPublicosView.as_view(), name='afiliados-publicos'),
    # ... outras URLs manuais se você tiver ...
] + router.urls