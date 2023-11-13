from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

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
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    cep = models.CharField(max_length=9, verbose_name="CEP")
    foto = models.ImageField(upload_to='afiliados_fotos/', blank=True, null=True)
    
    USER_TYPE_CHOICES = (
        ('AFILIADO', 'Afiliado'),
        ('ADMIN', 'Administrador'),
        ('FUNC', 'Funcionario'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='AFILIADO')

    #Esse campo so é relevante quando o usuario for um funcionario
    afiliado_relacionado = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='funcionarios',
        help_text='Afiliado ao qual o funcionário está associado',
        limit_choices_to={'user_type': 'AFILIADO'},  # Limita as escolhas a usuários do tipo AFILIADO
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    
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
            # Se o afiliado já tem 5 ou mais funcionários, impede a criação de mais um
            if funcionarios_count >= 5:
                raise ValueError("Quantidade permitida de funcionários ja atingido.")

        # Certifique-se de que um afiliado não possa ser associado a outro afiliado
        if self.user_type == 'AFILIADO' and self.afiliado_relacionado is not None:
            raise ValueError("Um afiliado não pode ser afiliado de outro afiliado.")
        
        # Se o usuário é um funcionário, certifique-se de que ele esteja sendo associado a um afiliado
        if self.user_type == 'FUNC' and self.afiliado_relacionado is None:
            raise ValueError("Um funcionário deve estar associado a um afiliado.")

        super(AfiliadosModel, self).save(*args, **kwargs)

    def get_short_name(self):
        return self.nome
