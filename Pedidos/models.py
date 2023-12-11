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

  #Dados do cliente
  idCliente = models.CharField(max_length=10, blank=True, null=True)
  fisico_juridico = models.CharField(max_length=50, blank=True, null=True)
  status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendente')
  status_adm_afiliado = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendente')
  data_pedido = models.DateTimeField(auto_now_add=True)
  afiliado = models.ForeignKey(
    AfiliadosModel, 
    on_delete=models.SET_NULL, 
    null=True, 
    blank=True,
    related_name="processos_afiliado",
    limit_choices_to={'user_type': 'AFILIADO'},
  )
  funcionario = models.ForeignKey(
        AfiliadosModel, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='processos_funcionario',
        limit_choices_to={'user_type': 'FUNC'},
    )
  servico = models.CharField(max_length=100, blank=True, null=True)
  subservico = models.CharField(max_length=100, blank=True, null=True)
  servicoCadastro = models.ForeignKey(Servico, on_delete=models.SET_NULL, null=True, blank=True)
  tipoDeEntrega = models.CharField(max_length=100, blank=True, null=True)
  FormaDePagamento = models.CharField(max_length=100, blank=True, null=True)
  Observacoes = models.CharField(max_length=2000, blank=True, null=True)
  
  def __str__(self):
    return str(self.id)

class Certidoes(models.Model):
  processo = models.ForeignKey(Processos, on_delete=models.CASCADE,blank=True, null=True)
  servico = models.CharField(max_length=100, blank=True, null=True)
  filiacao1 = models.CharField(max_length=100, blank=True, null=True)
  filiacao2 = models.CharField(max_length=100, blank=True, null=True)
  conjugue1 = models.CharField(max_length=100, blank=True, null=True)
  conjugue2 = models.CharField(max_length=100, blank=True, null=True) 
  data_casamento = models.DateField(blank=True, null=True)
  data_inicial = models.DateField(blank=True, null=True)
  data_final = models.DateField(blank=True, null=True)
  #Dados do falecido
  data_obito = models.DateField(blank=True, null=True)
  nome_falecido = models.CharField(max_length=100, blank=True, null=True)
  
  temFilhosMenores = models.CharField(max_length=5, blank=True, null=True)
  temBens = models.CharField(max_length=5, blank=True, null=True)
  filhoIncapaz = models.CharField(max_length=5, blank=True, null=True)

  @classmethod
  def get_field_names(cls):
    return [f.name for f in cls._meta.get_fields() if f.name != "processo"]
  
  
class Documento(models.Model):
    cliente = models.ForeignKey(Processos, on_delete=models.CASCADE,blank=True, null=True)
    arquivo = models.FileField(upload_to='documentos/')
    descricao = models.CharField(max_length=255, blank=True, null=True)  # Uma descrição curta sobre o documento
    data_upload = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return f"Documento {self.id}: {self.descricao}"
    
class Cartorio(models.Model):
    processo = models.ForeignKey(Processos, on_delete=models.CASCADE,blank=True, null=True)
    nomeCartorio = models.CharField(max_length=100, blank=True, null=True)
    estadoCartorio = models.CharField(max_length=100, blank=True, null=True)
    cidadeCartorio = models.CharField(max_length=100, blank=True, null=True)
    livroCartorio = models.CharField(max_length=100, blank=True, null=True)
    folhaCartorio = models.CharField(max_length=100, blank=True, null=True)
    termo = models.CharField(max_length=100, blank=True, null=True)
    nomeCartorioFirmaReconhecida = models.CharField(max_length=100, blank=True, null=True)
    estadoCartorioFirmaReconhecida = models.CharField(max_length=100, blank=True, null=True)
    livroCartorioFirmaReconhecida = models.CharField(max_length=100, blank=True, null=True) 

    @classmethod
    def get_field_names(cls):
        return [f.name for f in cls._meta.get_fields() if f.name != "processo"]

class ClienteTerceiro(models.Model):
    processo = models.ForeignKey(Processos, on_delete=models.CASCADE,blank=True, null=True)
    nomeEnvolvido = models.CharField(max_length=100, blank=True, null=True) #envolvido
    sobrenomeEnvolvido = models.CharField(max_length=100, blank=True, null=True) #envolvido
    RegistroGeralEnvolvido = models.CharField(max_length=20, blank=True, null=True) #envolvido
    cpfEnvolvido = models.CharField(max_length=11, blank=True, null=True) #envolvido
    emailEnvolvido = models.EmailField(blank=True, null=True) #envolvido
    telefoneEnvolvido = models.CharField(max_length=15, blank=True, null=True) #envolvido
    
    estado_envolvido = models.CharField(max_length=50, blank=True, null=True)
    logradouro_envolvido = models.TextField(blank=True, null=True)
    complemento_envolvido = models.TextField(blank=True, null=True)
    cidade_envolvido = models.CharField(max_length=100, blank=True, null=True)
    bairro_envolvido = models.CharField(max_length=100, blank=True, null=True)
    cep_envolvido = models.CharField(max_length=9, blank=True, null=True)
    numero_envolvido = models.CharField(max_length=9, blank=True, null=True)

    @classmethod
    def get_field_names(cls):
        return [f.name for f in cls._meta.get_fields() if f.name != "processo"]

class ClientJob(models.Model): 
    processo = models.OneToOneField(Processos, on_delete=models.CASCADE,blank=True, null=True)
    profissao = models.CharField(max_length=100, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    renda_mensal = models.CharField(max_length=100, blank=True, null=True)
    data_admissao = models.DateField(blank=True, null=True)
    telefone_trabalho = models.CharField(max_length=15, blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    cep_trabalho = models.CharField(max_length=9, blank=True, null=True)
    logradouro_trabalho = models.TextField(blank=True, null=True)
    complemento_trabalho = models.TextField(blank=True, null=True)
    numero_trabalho = models.CharField(max_length=9, blank=True, null=True)
    bairro_trabalho = models.CharField(max_length=100, blank=True, null=True)
    cidade_trabalho = models.CharField(max_length=100, blank=True, null=True)
    estado_trabalho = models.CharField(max_length=50, blank=True, null=True)

    nome_referencia = models.CharField(max_length=100, blank=True, null=True)
    telefone_referencia = models.CharField(max_length=100, blank=True, null=True)
    #Criar novos campos precisa atualizar a views criar_cliente_com_relacionados
    
    @classmethod
    def get_field_names(cls):
        return [f.name for f in cls._meta.get_fields() if f.name != "processo"]

class FinanciamentoVeiculo(models.Model): 
    processo = models.OneToOneField(Processos, on_delete=models.CASCADE,blank=True, null=True)
    tipo_veiculo = models.CharField(max_length=100, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    ano_modelo = models.CharField(max_length=100, blank=True, null=True)
    placa = models.CharField(max_length=100, blank=True, null=True)
    versao = models.CharField(max_length=100, blank=True, null=True)
    estado_licenciamento = models.CharField(max_length=100, blank=True, null=True)
    valor = models.CharField(max_length=100, blank=True, null=True)
    entrada = models.CharField(max_length=100, blank=True, null=True)
    prazo = models.CharField(max_length=100, blank=True, null=True)    
    banco = models.CharField(max_length=100, blank=True, null=True)

    possui_carroceria = models.CharField(max_length=100, blank=True, null=True)
    ano_fabricacao = models.CharField(max_length=100, blank=True, null=True)
    combustivel = models.CharField(max_length=100, blank=True, null=True)
    cambio = models.CharField(max_length=100, blank=True, null=True)

    
    #Criar novos campos precisa atualizar a views criar_cliente_com_relacionados
    
    @classmethod
    def get_field_names(cls):
        return [f.name for f in cls._meta.get_fields() if f.name != "processo"]

class ClientEmpresarial(models.Model): 
    processo = models.OneToOneField(Processos, on_delete=models.CASCADE,blank=True, null=True)
    nome_fantasia = models.CharField(max_length=100, blank=True, null=True)
    razao_social = models.CharField(max_length=100, blank=True, null=True)
    cnpj = models.CharField(max_length=100, blank=True, null=True)
    data_abertura = models.DateField(blank=True, null=True)
    faturamento_mensal = models.CharField(max_length=100, blank=True, null=True)
    contador_nome = models.CharField(max_length=100, blank=True, null=True)
    telefone_contador = models.TextField(max_length=15, blank=True, null=True)
    
    @classmethod
    def get_field_names(cls):
        return [f.name for f in cls._meta.get_fields() if f.name != "processo"]
