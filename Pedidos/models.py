from django.db import models

ESTADO_CIVIL_CHOICES = [
    ('Solteiro', 'Solteiro'),
    ('Casado', 'Casado'),
    ('Divorciado', 'Divorciado'),
    ('Viuvo', 'Viúvo'),
  ]

STATUS_CHOICES = [
    ('pendente', 'Pendente'),
    ('em_analise', 'Em Analise'),
    ('aprovado', 'Aprovado'),
    ('recusado', 'Recusado'),
  ]

class NovoCliente(models.Model):
  from Afiliados.models import AfiliadosModel
  from Servicos.models import Servico

  idCliente = models.CharField(max_length=10)
  nome = models.CharField(max_length=100)
  sobrenome = models.CharField(max_length=100)
  email = models.EmailField() #unique=True Valor unico no banco de dados
  telefone = models.CharField(max_length=15)
  RegistroGeral = models.CharField(max_length=20)
  cpf = models.CharField(max_length=11)
  estado_civil = models.CharField(max_length=15, 
                                  choices=ESTADO_CIVIL_CHOICES,
                                  blank=True,  null=True)
  #blank=True e null=True aceita ficar sem valor esse campo
  profissao = models.CharField(max_length=100, blank=True, null=True)
  data_nascimento = models.DateField(blank=True, null=True)
  estado = models.CharField(max_length=50)
  endereco = models.TextField()
  cidade = models.CharField(max_length=100)
  bairro = models.CharField(max_length=100)
  cep = models.CharField(max_length=9)
  status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pendente')
  data_pedido = models.DateTimeField(auto_now_add=True)
  afiliado = models.ForeignKey(AfiliadosModel, 
                            on_delete=models.SET_NULL, 
                            null=True, blank=True)

  servico = models.CharField(max_length=100, blank=True, null=True)
  subservico = models.CharField(max_length=100, blank=True, null=True)
  

  nomeEnvolvido = models.CharField(max_length=100, blank=True, null=True)
  sobrenomeEnvolvido = models.CharField(max_length=100, blank=True, null=True)
  RegistroGeralEnvolvido = models.CharField(max_length=20, blank=True, null=True)
  cpfEnvolvido = models.CharField(max_length=11, blank=True, null=True)

  nomeCartorio = models.CharField(max_length=100, blank=True, null=True)
  estadoCartorio = models.CharField(max_length=100, blank=True, null=True)
  livroCartorio = models.CharField(max_length=100, blank=True, null=True)
  folhaCartorio = models.CharField(max_length=100, blank=True, null=True)

  nomeCartorioFirmaReconhecida = models.CharField(max_length=100, blank=True, null=True)
  estadoCartorioFirmaReconhecida = models.CharField(max_length=100, blank=True, null=True)
  livroCartorioFirmaReconhecida = models.CharField(max_length=100, blank=True, null=True)

  def __str__(self):
    return self.nome

class Documento(models.Model):
    cliente = models.ForeignKey(NovoCliente, on_delete=models.CASCADE,blank=True, null=True)
    arquivo = models.FileField(upload_to='documentos/')
    descricao = models.CharField(max_length=255, blank=True, null=True)  # Uma descrição curta sobre o documento
    data_upload = models.DateTimeField(auto_now_add=True,blank=True, null=True)