from django.contrib import admin
from .models import Cliente, ClienteEndereco

@admin.register(Cliente)
class ClienteModelAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    
@admin.register(ClienteEndereco)
class ClienteEndereco(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
