from rest_framework.routers import DefaultRouter
from .views import criar_cliente_com_relacionados,NovoClienteDetailView,TodosClientesView,ClienteDetailView
from django.urls import path

app_name = 'pedidos'

router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns = [
    path('criar_cliente/', criar_cliente_com_relacionados, name='criar_cliente_com_relacionados'),
    path('requests/<str:id>/', NovoClienteDetailView.as_view(), name='cliente-detail'),
    path('listrequest/', TodosClientesView.as_view(), name='todos-clientes'),
    path('deleterequest/<int:id>/', ClienteDetailView.as_view(), name='cliente-detail'),
]

