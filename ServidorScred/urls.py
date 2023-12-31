from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home 

urlpatterns = [
    path('', home, name='home'),
    path('api/', include('Cliente.urls', namespace='ApiCliente')),
    path('api/', include('Afiliados.urls', namespace='ApiAfiliados')),
    path('api/', include('Servicos.urls', namespace='ApiServicos')),
    path('api/', include('Pedidos.urls', namespace='ApiPedidos')),
    path('api/', include('financeiro.urls', namespace='Apifinanceiro')),
    

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)