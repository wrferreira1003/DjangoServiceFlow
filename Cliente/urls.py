from rest_framework.routers import DefaultRouter
from .views import RegistrarClientesViewSet, TodosClientesViewSet,validate_account,verifica_cpf,verifica_email, LoginUserView
from django.urls import path

app_name = 'cliente'

router = DefaultRouter(trailing_slash=False) #False para nao precisar colocar / no final
router.register(r'user', TodosClientesViewSet)

urlpatterns = [
  path('register/', RegistrarClientesViewSet.as_view(), name='register'),
  path('validate/', validate_account, name='validate'),
  path('cpf/<str:cpf>/', verifica_cpf),
  path('email/<str:email>/', verifica_email),
  path('loginuser/', LoginUserView.as_view(), name='loginuser'),
] +router.urls