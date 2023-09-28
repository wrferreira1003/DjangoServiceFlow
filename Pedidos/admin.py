from django.contrib import admin
from .models import NovoCliente, Documento

@admin.register(NovoCliente)
class NovoClienteModelAdmin(admin.ModelAdmin):
    list_display= [ 'id',
                    'idCliente',
                    'status',
                    'nome', 
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
                   'data_pedido',
                   'afiliado',
                   'servico',
                   'subservico',
                   'nomeEnvolvido',
                   'sobrenomeEnvolvido',
                   'RegistroGeralEnvolvido',
                   'cpfEnvolvido',
                   'nomeCartorio',
                   'estadoCartorio',
                   'livroCartorio',
                   'folhaCartorio',
                    'nomeCartorioFirmaReconhecida',
                    'estadoCartorioFirmaReconhecida',
                    'livroCartorioFirmaReconhecida'
                   ]
    

class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['id','cliente', 'descricao', 'data_upload', 'arquivo']
    search_fields = ['cliente__idCliente', 'descricao']  # Permite a pesquisa por nome do cliente e descrição do documento
    list_filter = ['data_upload']  # Permite filtrar documentos por data de upload

admin.site.register(Documento, DocumentoAdmin)