from django.db import models
from Afiliados.models import AfiliadosModel
from django.contrib.auth.hashers import check_password
import uuid

def truncated_uuid():
    return str(uuid.uuid4())[:32] 

ESTADO_CIVIL_CHOICES = [
    ('Solteiro', 'Solteiro'),
    ('Casado', 'Casado'),
    ('Divorciado', 'Divorciado'),
    ('Viuvo', 'Viúvo'),
  ]
class Cliente(models.Model):
    afiliado = models.ForeignKey(AfiliadosModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='clientes_como_afiliado') 
    funcionario = models.ForeignKey(AfiliadosModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='clientes_como_funcionario') 
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14) # Para simplificar, estamos tratando
    email = models.EmailField()
    telefone = models.CharField(max_length=15, null=True, blank=True)
    RegistroGeral = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=10, blank=True, null=True)
    naturalidade = models.CharField(max_length=100, blank=True, null=True)
    cnh = models.CharField(max_length=20, blank=True, null=True)
    acesso = models.CharField(max_length=15, default='Sem acesso')
    
    def __str__(self):
        return str(self.id)

    @classmethod
    def get_field_names(cls):
        return [f.name for f in cls._meta.get_fields()]    


class ClienteEndereco(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cep = models.CharField(max_length=8, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
    logradouro = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    complemento = models.CharField(max_length=300, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @classmethod
    def get_field_names(cls):
        return [f.name for f in cls._meta.get_fields()]    