from django.contrib import admin
from .models import AfiliadosModel

@admin.register(AfiliadosModel)
class AfiliadosModelAdmin(admin.ModelAdmin):
    list_display= ['nome', 'sobrenome', 'email', 'telefone', 'Cnpj', 'endereco' ,'cartorio']

