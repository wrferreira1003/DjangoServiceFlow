from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from Cliente.models import Cliente
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

#Funcao para validacao de documentos
def valida_file_extension(value):
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.jpeg']
  if not ext.lower() in valid_extensions:
    raise ValidationError(u'Tipo de arquivo não suportado!')

#Caso solicitar pedido Ata Notarial, passo os dados do cliente, que precisa de um afiliado e os demais dados desse servico.
class ModelPedido(models.Model):
  sub_servico = models.ForeignKey(Subservico, on_delete=models.CASCADE)
  cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
  status = models.CharField(max_length=50, choices=STATUS_CHOICES)
  mensagem = models.CharField(max_length=500)
  documento= models.FileField(upload_to='documentos/', validators=[valida_file_extension])

