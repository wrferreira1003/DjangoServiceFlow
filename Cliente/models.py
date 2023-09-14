from django.db import models
from Afiliados.models import AfiliadosModel
from django.contrib.auth.hashers import check_password

class Cliente(models.Model):
    afiliado =models.ForeignKey(AfiliadosModel, on_delete=models.SET_NULL, null=True) #Caso o afiliado seja excluido o cliente que tem aquele afiliado fica null.
    nome = models.CharField(max_length=300)
    cpf = models.CharField(max_length=14, unique=True) # Para simplificar, estamos tratando
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    telefone2 = models.CharField(max_length=15, null=True, blank=True,)
    
    cep = models.CharField(max_length=8)
    estado = models.CharField(max_length=100)
    logradouro = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    complemento = models.CharField(max_length=300)
    numero = models.IntegerField()

    is_validated = models.BooleanField(default=False)
    validation_token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
 
    def __str__(self):
        return self.nome
