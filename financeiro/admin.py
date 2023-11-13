from django.contrib import admin
from .models import Transacao

def processo_id(obj):
    return obj.pedido.id
processo_id.short_description = 'ID do Processo'

@admin.register(Transacao)
class TransacaoNovoClienteModelAdmin(admin.ModelAdmin):
    list_display= [ processo_id,
                    'id',
                    'cliente',
                    'afiliado',
                    'servico',
                    'pedido',
                    'preco',
                    'statusPagamento',
                    'FormaDePagamento',
                    'data_criacao',
                    'data_atualizacao'
                   ]
