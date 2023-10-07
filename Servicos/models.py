from django.db import models

CHOICES = [
    ('Nova Solicitacao', 'Nova Solicitacao'),
    ('Solicitacao de Consulta', 'Solicitacao de Consulta'),
]

class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nome_categoria

class Servico(models.Model):
    nome_servico = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100, choices=CHOICES, blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="servicos")
    
    def __str__(self):
        return self.nome_servico



  
