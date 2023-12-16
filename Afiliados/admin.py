from django.contrib import admin
from .models import AfiliadosModel

@admin.register(AfiliadosModel)
class AfiliadosModelAdmin(admin.ModelAdmin):
    list_display= ['get_cpf_cnpj','id','nome','user_type', 'afiliado_relacionado','email', 
                   'telefone', 'endereco' ,'bairro', 'cidade',
                   'estado', 'cep', 'afiliado_relacionado']
    
    def get_cpf_cnpj(self, obj):
        return obj.cnpj if obj.user_type == 'AFILIADO' else obj.cpf
    get_cpf_cnpj.short_description = 'CPF/CNPJ'  # Define o título da coluna

