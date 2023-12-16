from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

ESTADO_CIVIL_CHOICES = [
        ('Solteiro', 'Solteiro'),
        ('Casado', 'Casado'),
        ('Divorciado', 'Divorciado'),
        ('Viuvo', 'Viúvo'),
    ]

class AfiliadoManager(BaseUserManager):
    def create_user(self, email, nome, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, nome, password, **extra_fields)
    
class AfiliadosModel(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=100)
    razao_social = models.CharField(max_length=100, null=True, blank=True)
    cnpj = models.CharField(max_length=14, unique=True, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15 ,null=True, blank=True,)
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
    nome_mae = models.CharField(max_length=100, null=True, blank=True)
    nome_pai = models.CharField(max_length=100, null=True, blank=True)
    
   
    
    endereco = models.CharField(max_length=200, null=True, blank=True)
    bairro = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=9, verbose_name="CEP", null=True, blank=True)
    logradouro = models.CharField(max_length=100, null=True, blank=True)
    complemento = models.CharField(max_length=300, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    
    
    foto = models.ImageField(upload_to='afiliados_fotos/', blank=True, null=True)
    
    USER_TYPE_CHOICES = (
        ('AFILIADO', 'Afiliado'),
        ('ADMIN', 'Administrador'),
        ('FUNC', 'Funcionario'),
        ('CLIENTE', 'Cliente'),
    )
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES)

    #Esse campo so é relevante quando o usuario for um funcionario ou cliente
    afiliado_relacionado = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='funcionarios',
        help_text='Afiliado ao está associado',
        limit_choices_to={'user_type': 'AFILIADO'},  # Limita as escolhas a usuários do tipo AFILIADO
    )


    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    is_validated = models.BooleanField(default=False)
    validation_token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    objects = AfiliadoManager()

    def save(self, *args, **kwargs):
         # Verificações para CPF e CNPJ
        if self.user_type == 'FUNC':
            if not self.cpf:
                raise ValueError("Um funcionário deve ter um CPF.")
            self.cnpj = None  # Garantir que CNPJ não seja definido para funcionários
        elif self.user_type == 'AFILIADO':
            if not self.cnpj:
                raise ValueError("Um afiliado deve ter um CNPJ.")
            self.cpf = None  # Garantir que CPF não seja definido para afiliados

            
        # Verifica se o objeto é um funcionário e se está associado a um afiliado
        if self.user_type == 'FUNC' and self.afiliado_relacionado:
            # Conta quantos funcionários o afiliado relacionado já tem
            funcionarios_count = AfiliadosModel.objects.filter(
                afiliado_relacionado=self.afiliado_relacionado, 
                user_type='FUNC'
            ).count()
            # Se o afiliado já tem 1 ou mais funcionários, impede a criação de mais um
            if funcionarios_count >= 1:
                raise ValueError("Quantidade permitida de funcionários ja atingido.")

        # Certifique-se de que um afiliado não possa ser associado a outro afiliado
        if self.user_type == 'AFILIADO' and self.afiliado_relacionado is not None:
            raise ValueError("Um afiliado não pode ser afiliado de outro afiliado.")
        
        # Se o usuário é um funcionário ou cliente, certifique-se de que ele esteja sendo associado a um afiliado
        if self.user_type in ['FUNC', 'CLIENTE'] and self.afiliado_relacionado is None:
            raise ValueError("Um funcionário ou cliente deve estar associado a um afiliado.")

        super(AfiliadosModel, self).save(*args, **kwargs)

    def get_short_name(self):
        return self.nome
    
    def __str__(self):
        return str(self.id)

#acessar todos os clientes de um afiliado usando afiliado.clientes.all().
class Cliente(models.Model):
    afiliado = models.ForeignKey(
        'Afiliados.AfiliadosModel', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='clientes',  # Altere o related_name para 'clientes'
    )