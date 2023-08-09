from django.db import models

CHOICES = [
    ('Nova Solicitacao', 'Nova Solicitacao'),
    ('Solicitacao de Consulta', 'Solicitacao de Consulta'),
  ]

class Servico(models.Model):
  nome_servico = models.CharField(max_length=200)
  tipo = models.CharField(max_length=100, 
                                  choices=CHOICES,
                                  blank=True,  null=True)
  def __str__(self):
    return self.nome_servico
  
