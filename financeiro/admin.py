from django.contrib import admin
from .models import Transacao, TransacaoAfiliadoAdministrador

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

@admin.register(TransacaoAfiliadoAdministrador)
class TransacaoAfiliadoADMModelAdmin(admin.ModelAdmin):
    list_display= [ 'id',
                    'afiliado',
                    'servico',
                    'pedido',
                    'preco',
                    'statusPagamento',
                    'FormaDePagamento',
                    'data_criacao',
                    'data_atualizacao',
                    'ObservacoesAdm',
                   ]
