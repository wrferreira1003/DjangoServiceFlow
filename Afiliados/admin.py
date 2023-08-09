from django.contrib import admin
from .models import AfiliadosModel

@admin.register(AfiliadosModel)
class AfiliadosModelAdmin(admin.ModelAdmin):
    list_display= ['id','nome', 'razao_social', 'cnpj', 'email', 
                   'telefone', 'endereco' ,'bairro', 'cidade',
                   'estado', 'cep']

