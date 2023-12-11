from django.contrib import admin
from .models import Certidoes, Cartorio, ClienteTerceiro, Processos, Documento, ClientJob, FinanciamentoVeiculo, ClientEmpresarial

@admin.register(Processos)
class NovoClienteModelAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    
@admin.register(ClientJob)
class NovoClienteJob(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    
@admin.register(FinanciamentoVeiculo)
class NovoClienteModelFinance(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

@admin.register(ClientEmpresarial)
class NovoClienteModelEmpresa(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    
@admin.register(Cartorio)
class NovoClienteModelCartorio(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    
@admin.register(ClienteTerceiro)
class NovoClienteModelClienteTerceiro(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

@admin.register(Certidoes)
class NovoClienteModelCertidoes(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['id','cliente', 'descricao', 'data_upload', 'arquivo']
    search_fields = ['cliente__idCliente', 'descricao']  # Permite a pesquisa por nome do cliente e descrição do documento
    list_filter = ['data_upload']  # Permite filtrar documentos por data de upload

admin.site.register(Documento, DocumentoAdmin)