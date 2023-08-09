from django.db import models

class AfiliadosModel(models.Model):    
    nome = models.CharField(max_length=100)
    razao_social = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14,
                                  unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    cep = models.CharField(max_length=9, verbose_name="CEP")
    
    def __str__(self):
      return self.nome
