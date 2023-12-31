from django.contrib import admin
from .models import DadosPessoaisDeTerceiros, DadosBancariosclients, EmprestimoEmpresarial, GarantiaVeiculo, GarantiaImoveis, EmprestimosEmGeral, Certidoes, Cartorio, ClienteTerceiro, Processos, Documento, ClientJob, FinanciamentoVeiculo, ClientEmpresarial,FinanciamentoImovel, ConsultaServicosGeral

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

@admin.register(FinanciamentoImovel)
class NovoClienteModelFinanciamentoImovel(admin.ModelAdmin):
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

@admin.register(ConsultaServicosGeral)
class NovoClienteModelConsultaCPF(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

@admin.register(EmprestimosEmGeral)
class EmprestimosEmGeral(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    
@admin.register(GarantiaImoveis)
class GarantiaImoveisAdm(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

@admin.register(GarantiaVeiculo)
class GarantiaVeiculoAdm(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    
@admin.register(EmprestimoEmpresarial)
class EmprestimoEmpresarialAdm(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    
@admin.register(DadosBancariosclients)
class DadosBancariosclientsAdm(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    

@admin.register(DadosPessoaisDeTerceiros)
class DadosPessoaisDeTerceirosAdm(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]



admin.site.register(Documento, DocumentoAdmin)