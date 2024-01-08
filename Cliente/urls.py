from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import valida_email, valida_cpf, verifica_cpf_email,TodosClientesViewSet,validate_account,verifica_cpf,verifica_email, AtualizaClienteViewSet, ListagemClienteCpf
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
  path('cpf/<str:cpf>/<str:email>/', verifica_cpf),
  path('email/<str:cpf>/<str:email>/', verifica_email),
  path('listcpf/<str:cpf>/', ListagemClienteCpf),
  path('cpf_email/<str:cpf>/<str:email>/', verifica_cpf_email),
  path('cpf/<str:cpf>/', valida_cpf),
  path('email/<str:email>/', valida_email),


] +router.urls
