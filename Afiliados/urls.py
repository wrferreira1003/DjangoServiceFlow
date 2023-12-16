from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from .views import AfiliadosViewSet, RegistrarAfiliadoView, LoginView,AfiliadosPublicosView,TodosAfiliadosViewSet,FuncionariosPorAfiliadoView,ClientePorAfiliadoView

app_name = 'Afiliados'

router = DefaultRouter(trailing_slash=False) #False para nao precisar colocar / no final
router.register(r'afiliado', AfiliadosViewSet)
router.register(r'todos_afiliados', TodosAfiliadosViewSet, basename='todos_afiliados')

urlpatterns = router.urls


urlpatterns = [
    path('register/', RegistrarAfiliadoView.as_view(), name='register'),
    path('registerclient/<int:afiliado_id>/', ClientePorAfiliadoView.as_view(), name='register-cliente'),
    path('login/', LoginView.as_view(), name='login'),
    path('afiliados/<int:afiliado_id>/funcionarios/', FuncionariosPorAfiliadoView.as_view(), name='funcionarios-por-afiliado'),
    re_path('afiliados-publicos/(?P<estado>[A-Z]{2})?/$', AfiliadosPublicosView.as_view(), name='afiliados-publicos'),
    # ... outras URLs manuais se você tiver ...
] + router.urls