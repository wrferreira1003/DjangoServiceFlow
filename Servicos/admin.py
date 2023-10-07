from django.contrib import admin
from .models import Servico, Categoria

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display= ['id', 'categoria', 'nome_servico','tipo','preco']

@admin.register(Categoria)
class Categoria(admin.ModelAdmin):
    list_display= ['id','nome_categoria']

