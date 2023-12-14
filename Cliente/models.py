from django.db import models
from Afiliados.models import AfiliadosModel
from django.contrib.auth.hashers import check_password


ESTADO_CIVIL_CHOICES = [
    ('Solteiro', 'Solteiro'),
    ('Casado', 'Casado'),
    ('Divorciado', 'Divorciado'),
    ('Viuvo', 'Viúvo'),
  ]
class Cliente(models.Model):
    afiliado =models.ForeignKey(AfiliadosModel, on_delete=models.SET_NULL, null=True, blank=True) #Caso o afiliado seja excluido o cliente que tem aquele afiliado fica null.
    nome = models.CharField(max_length=300)
    cpf = models.CharField(max_length=14, unique=True) # Para simplificar, estamos tratando
    email = models.EmailField(null=True, blank=True, unique=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    telefone2 = models.CharField(max_length=15, null=True, blank=True,)
    RegistroGeral = models.CharField(max_length=20, blank=True, null=True)
    Data_emissao_rg = models.DateField(blank=True, null=True)
    orgao_emissor_rg = models.CharField(max_length=20, blank=True, null=True)
    estado_civil = models.CharField(max_length=15, 
                                  choices=ESTADO_CIVIL_CHOICES,
                                  blank=True,  null=True)
    profissao = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=10, blank=True, null=True)
    naturalidade = models.CharField(max_length=100, blank=True, null=True)
    cnh = models.CharField(max_length=20, blank=True, null=True)
    

    # Endereço do cliente
    cep = models.CharField(max_length=8, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
    logradouro = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    complemento = models.CharField(max_length=300, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)

    nome_mae = models.CharField(max_length=100, null=True, blank=True)
    nome_pai = models.CharField(max_length=100, null=True, blank=True)

    is_validated = models.BooleanField(default=False)
    validation_token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
 
    def __str__(self):
        return str(self.id)

    @classmethod
    def get_field_names(cls):
        return [f.name for f in cls._meta.get_fields() if f.name != "afiliado"]    

