from django.db import models

class Transacao(models.Model):
    from Cliente.models import Cliente
    from Afiliados.models import AfiliadosModel
    from Servicos.models import Servico
    from Pedidos.models import Processos

    cliente = models.ForeignKey('Cliente.Cliente', on_delete=models.CASCADE, related_name="transacoes")
    afiliado = models.ForeignKey('Afiliados.AfiliadosModel', on_delete=models.SET_NULL, null=True, blank=True, related_name="transacoes") 
    servico = models.ForeignKey('Servicos.Servico', on_delete=models.SET_NULL, null=True)
    pedido = models.OneToOneField('Pedidos.Processos', on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    FormaDePagamento = models.CharField(max_length=100, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    Observacoes = models.CharField(max_length=2000, blank=True, null=True)
    comprovante = models.FileField(upload_to='comprovantesPagamento/', blank=True, null=True)
    linkpagamento = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(
    choices=[('PENDENTE', 'Pendente de Pagamento'), 
             ('PAGO', 'Pago'),
             ('AGUARDANDO', 'Aguardando Confirmação'), 
            ],
    max_length=20,
    default='PENDENTE'
    )
    @property
    def processo_id(self):
        return self.pedido.id

    def __str__(self):
        return f"Transação {self.id} - Cliente: {self.cliente.nome} - Afiliado: {self.afiliado.nome if self.afiliado else 'N/A'} - Preço: {self.preco} - Status: {self.status}"
