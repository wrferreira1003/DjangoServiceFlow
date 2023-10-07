from django.db import models

ESTADO_CIVIL_CHOICES = [
    ('Solteiro', 'Solteiro'),
    ('Casado', 'Casado'),
    ('Divorciado', 'Divorciado'),
    ('Viuvo', 'Viúvo'),
  ]

STATUS_CHOICES = [
    ('Pendente', 'Pendente'),
    ('Em analise', 'Em Analise'),
    ('Aprovado', 'Aprovado'),
    ('Recusado', 'Recusado'),
    ('Ajustar documentação', 'Ajustar documentação'),
  ]

class Processos(models.Model):
  from Afiliados.models import AfiliadosModel
  from Servicos.models import Servico

  idCliente = models.CharField(max_length=10, blank=True, null=True)
  nome = models.CharField(max_length=100, blank=True, null=True)
  email = models.EmailField(blank=True, null=True) #unique=True Valor unico no banco de dados
  telefone = models.CharField(max_length=15, blank=True, null=True) 
  RegistroGeral = models.CharField(max_length=20, blank=True, null=True)
  cpf = models.CharField(max_length=11, blank=True, null=True)
  estado_civil = models.CharField(max_length=15, 
                                  choices=ESTADO_CIVIL_CHOICES,
                                  blank=True,  null=True)
  #blank=True e null=True aceita ficar sem valor esse campo
  profissao = models.CharField(max_length=100, blank=True, null=True)
  data_nascimento = models.DateField(blank=True, null=True)
  estado = models.CharField(max_length=50, blank=True, null=True)
  endereco = models.TextField(blank=True, null=True)
  cidade = models.CharField(max_length=100, blank=True, null=True)
  bairro = models.CharField(max_length=100, blank=True, null=True)
  cep = models.CharField(max_length=9, blank=True, null=True)
  status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendente')
  data_pedido = models.DateTimeField(auto_now_add=True)
  afiliado = models.ForeignKey(AfiliadosModel, 
                            on_delete=models.SET_NULL, 
                            null=True, blank=True)

  servico = models.CharField(max_length=100, blank=True, null=True)
  subservico = models.CharField(max_length=100, blank=True, null=True)
  
  servicoCadastro = models.ForeignKey(Servico, on_delete=models.SET_NULL, null=True, blank=True)

  filiacao1 = models.CharField(max_length=100, blank=True, null=True)
  filiacao2 = models.CharField(max_length=100, blank=True, null=True)

  nomeEnvolvido = models.CharField(max_length=100, blank=True, null=True)
  sobrenomeEnvolvido = models.CharField(max_length=100, blank=True, null=True)
  RegistroGeralEnvolvido = models.CharField(max_length=20, blank=True, null=True)
  cpfEnvolvido = models.CharField(max_length=11, blank=True, null=True)

  nomeCartorio = models.CharField(max_length=100, blank=True, null=True)
  estadoCartorio = models.CharField(max_length=100, blank=True, null=True)
  cidadeCartorio = models.CharField(max_length=100, blank=True, null=True)

  livroCartorio = models.CharField(max_length=100, blank=True, null=True)
  folhaCartorio = models.CharField(max_length=100, blank=True, null=True)
  termo = models.CharField(max_length=100, blank=True, null=True)

  tipoDeEntrega = models.CharField(max_length=100, blank=True, null=True)
  FormaDePagamento = models.CharField(max_length=100, blank=True, null=True)
  
  nomeCartorioFirmaReconhecida = models.CharField(max_length=100, blank=True, null=True)
  estadoCartorioFirmaReconhecida = models.CharField(max_length=100, blank=True, null=True)
  livroCartorioFirmaReconhecida = models.CharField(max_length=100, blank=True, null=True)
  Observacoes = models.CharField(max_length=2000, blank=True, null=True)
  
  def __str__(self):
    return self.nome

class Documento(models.Model):
    cliente = models.ForeignKey(Processos, on_delete=models.CASCADE,blank=True, null=True)
    arquivo = models.FileField(upload_to='documentos/')
    descricao = models.CharField(max_length=255, blank=True, null=True)  # Uma descrição curta sobre o documento
    data_upload = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return f"Documento {self.id}: {self.descricao}"