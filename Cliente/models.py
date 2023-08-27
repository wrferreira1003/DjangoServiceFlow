from django.db import models
from Afiliados.models import AfiliadosModel

class Cliente(models.Model):
    afiliado =models.ForeignKey(AfiliadosModel, on_delete=models.SET_NULL, null=True) #Caso o afiliado seja excluido o cliente que tem aquele afiliado fica null.
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=14, unique=True) # Para simplificar, estamos tratando
    endereco = models.CharField(max_length=200)

    def __str__(self):
        return self.nome
