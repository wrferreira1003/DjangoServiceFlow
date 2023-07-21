from django.db import models
import uuid

class AfiliadosModel(models.Model):    
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    Cnpj = models.CharField(max_length=14, unique=True) # Para simplificar, estamos tratando
    endereco = models.CharField(max_length=200)
    cartorio = models.CharField(max_length=200)

    def __str__(self):
      return self.nome
