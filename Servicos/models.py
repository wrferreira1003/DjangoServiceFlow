from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from Cliente.models import Cliente
from validations.validators import valida_file_extension

import os

class Servico(models.Model):
  nome_servico = models.CharField(max_length=200)
  def __str__(self):
    return self.nome_servico
  
class Subservico(models.Model):
  nome_subservico = models.CharField(max_length=200)
  servico = models.ForeignKey(Servico, 
                              related_name='subservicos', 
                              on_delete=models.CASCADE)
  
  def __str__(self):
    return self.nome_subservico
  

# Cadastro Servicos Referente a Cartorio Tabelionato

STATUS_CHOICES = [
    ('pendente', 'Pendente'),
    ('em_analise', 'Em Analise'),
    ('aprovado', 'Aprovado'),
    ('recusado', 'Recusado'),
  ]

#Caso solicitar pedido Ata Notarial, passo os dados do cliente, que precisa de um afiliado e os demais dados desse servico.
class ModelPedido(models.Model):
  sub_servico = models.ForeignKey(Subservico, on_delete=models.CASCADE)
  cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
  status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pendente')
  mensagem = models.CharField(max_length=500)
  documento= models.FileField(upload_to='documentos/', validators=[valida_file_extension])

  nome_envolvido = models.CharField(max_length=200, blank=True, null=True)
  cpf_envolvido = models.CharField(max_length=14, blank=True, null=True)
  indetidade_envolvido = models.CharField(max_length=20, blank=True, null=True)
  documento_envolvido = models.FileField(upload_to='documentos_partes/', 
                                         validators=[valida_file_extension],
                                         blank=True, null=True)
  

  def __str__(self):
    return self.cliente

