from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteModelAdmin(admin.ModelAdmin):
    list_display= [ 'id',
                    'afiliado', 
                    'nome', 
                    'cpf', 
                    'email', 
                    'password',
                    'telefone',
                    'telefone2', 
                    'cep',
                    'estado',
                    'logradouro',
                    'bairro',
                    'cidade',
                    'complemento',
                    'numero',
                    'is_validated',
                    'validation_token'
                ]
