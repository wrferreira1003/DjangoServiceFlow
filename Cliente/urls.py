from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import TodosClientesViewSet,validate_account,verifica_cpf,verifica_email, LoginUserView, AtualizaClienteViewSet, ListagemClienteCpf
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'cliente'

router = DefaultRouter(trailing_slash=False) #False para nao precisar colocar / no final
router.register(r'user', TodosClientesViewSet)

urlpatterns = [
  path('atualiza/<int:pk>/', AtualizaClienteViewSet.as_view(), name='atualizar_cliente'),
  path('validate/', validate_account, name='validate'),
  path('cpf/<str:cpf>/', verifica_cpf),
  path('email/<str:email>/', verifica_email),
  path('loginuser/', LoginUserView.as_view(), name='loginuser'),
  path('listcpf/<str:cpf>/', ListagemClienteCpf),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] +router.urls
