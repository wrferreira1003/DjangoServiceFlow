from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('Cliente.urls', namespace='ApiCliente')),
    path('api/', include('Afiliados.urls', namespace='ApiAfiliados')),
    path('api/', include('Servicos.urls', namespace='ApiServicos')),
    path('api/', include('Pedidos.urls', namespace='ApiPedidos')),
    
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
