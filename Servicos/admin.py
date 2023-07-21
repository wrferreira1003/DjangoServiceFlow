from django.contrib import admin
from .models import Servico, Subservico, ModelPedido

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display= ['nome_servico']

@admin.register(Subservico)
class SubServicoAdmin(admin.ModelAdmin):
    list_display= ['nome_subservico', 'servico']

@admin.register(ModelPedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['sub_servico', 'cliente', 'status', 'mensagem']