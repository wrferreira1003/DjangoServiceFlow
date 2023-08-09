from django.contrib import admin
from .models import NovoCliente, NovoClienteEnvolvido, Documento

@admin.register(NovoCliente)
class NovoClienteModelAdmin(admin.ModelAdmin):
    list_display= ['nome', 
                   'sobrenome', 
                   'email', 
                   'telefone', 
                   'RegistroGeral', 
                   'cpf', 
                   'estado_civil',
                   'profissao',
                   'data_nascimento',
                   'estado',
                   'endereco',
                   'cidade',
                   'bairro',
                   'cep',
                   'status',
                   'data_pedido',
                   'afiliado',
                   'servico',
                   ]
    
@admin.register(NovoClienteEnvolvido)
class NovoClienteEnvolvidoModelAdmin(admin.ModelAdmin):
    list_display= ['nome','sobrenome','RegistroGeral','cpf' ,'cliente' ]

class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'descricao', 'data_upload', 'arquivo']
    search_fields = ['cliente__nome', 'descricao']  # Permite a pesquisa por nome do cliente e descrição do documento
    list_filter = ['data_upload']  # Permite filtrar documentos por data de upload

admin.site.register(Documento, DocumentoAdmin)