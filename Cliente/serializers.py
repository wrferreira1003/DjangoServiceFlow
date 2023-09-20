from rest_framework import serializers
from .models import Cliente
from validations.validators import validate_nome, validate_email,validate_telefone, validate_cpf
from django.contrib.auth.hashers import make_password
import uuid
from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import urlencode

link = 'http://127.0.0.1:8000/api/'
src = 'http://127.0.0.1:8000/static/img/logo.png'

#Funcao que gera um token unico para o cliente
def generate_validation_token():
    return uuid.uuid4().hex

#Funcao de email para o cliente
def send_validation_email(email, token):
    params = urlencode({'token': token})
    validation_url = f"{link}validate?{params}" #Ajustar em producao
    html_content = """
    <div style="text-align: center;">
        <img src="{src}" alt="Logo" style="max-width: 100px; margin-bottom: 20px;"><br>
        <h1>Valide seu e-mail para confirmar sua identidade.</h1>
        <p>Clique no botão abaixo para confirmar o seu endereço de e-mail.</p>
        <a href="{validation_url}" 
            style="background-color: #4CAF50; 
            border: none; color: white; 
            padding: 15px 32px; text-align: center; 
            text-decoration: none; display: 
            inline-block; font-size: 16px; margin: 
            4px 2px; cursor: pointer; border-radius: 12px;"
            >VALIDAR EMAIL
        </a>

            <p
            style=margin-top: 30px;
            >Essa mensagem foi enviada para 
            <a href="mailto:{email}">wrf.wellington@gmail.com</a>.
            </p>
    </div>
    """.format(validation_url=validation_url, email=email, link=link, src=src)

    send_mail(
        'Cadastro RCFácil - Validação de conta',
        f'{validation_url}',
        settings.DEFAULT_FROM_EMAIL,  
        [email],
        html_message=html_content,  # Definir mensagem HTML com o conteúdo formatado
    )

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [ 'id',
                    'afiliado', 
                    'nome', 
                    'cpf', 
                    'email', 
                    'password',
                    'telefone',
                    'telefone2', 
                    'cep',
                    'estado',
                    'logradouro',
                    'bairro',
                    'cidade',
                    'complemento',
                    'numero',
                ]
        
    #Aplicando as validacoes nos campos por seguranca
    nome = serializers.CharField(validators=[validate_nome])
    email = serializers.CharField(validators=[validate_email])
    telefone = serializers.CharField(validators=[validate_telefone])
    cpf = serializers.CharField(validators=[validate_cpf])

    #Removendo o campo password dos dados retornados
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password', None)  # Remover o campo 'password' dos dados serializados
        return data
    
    #Validação customizada no serializer para verificar se o e-mail já existe no banco de dados. 
    def validate_email(self, value):
        if Cliente.objects.filter(email=value).exists():
            raise serializers.ValidationError('E-mail já está em uso')
        return value
    
    def validate_cpf(self, value):
        if Cliente.objects.filter(cpf=value).exists():
            raise serializers.ValidationError('CPF já está em uso')
        return value

    def create(self, validated_data):
        validation_token = generate_validation_token()
        validated_data['validation_token'] = validation_token
        validated_data['password'] = make_password(validated_data.get('password'))
    
        instance = super().create(validated_data)
    
        send_validation_email(instance.email, validation_token)
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [ 'id',
                    'afiliado', 
                    'nome', 
                    'cpf', 
                    'email', 
                    'telefone',
                    'telefone2', 
                    'cep',
                    'estado',
                    'logradouro',
                    'bairro',
                    'cidade',
                    'complemento',
                    'numero',
                ]

class AtualizaClienteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cliente
        fields = [
            'afiliado', 'nome', 'cpf', 'email', 'password', 'telefone', 
            'telefone2', 'cep', 'estado', 'logradouro', 'bairro', 
            'cidade', 'complemento', 'numero'
        ]
        extra_kwargs = {
            'nome': {'required': False},
            'password': {'required': False},
            'telefone': {'required': False},
            'cep': {'required': False},
            'estado': {'required': False},
            'logradouro': {'required': False},
            'bairro': {'required': False},
            'cidade': {'required': False},
            'complemento': {'required': False},
            'numero': {'required': False},
            'cpf': {'required': False, 'validators': []},
            'email': {'required': False, 'validators': []},
        }
    
    def update(self, instance, validated_data):
        # Se 'password' está nos dados validados, hash ele antes de salvar
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        
        # Agora, atualize a instância com os dados validados
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance
    

    def validate(self, attrs):
        if self.instance:
            if 'cpf' in attrs:
                if attrs['cpf'] is not None and Cliente.objects.exclude(pk=self.instance.pk).filter(cpf=attrs['cpf']).exists():
                    del attrs['cpf']
            else:
                attrs['cpf'] = self.instance.cpf

            if 'email' in attrs:
                if attrs['email'] is not None and Cliente.objects.exclude(pk=self.instance.pk).filter(email=attrs['email']).exists():
                    del attrs['email']
            else:
                attrs['email'] = self.instance.email
        else:
            if attrs.get('cpf') is not None and Cliente.objects.filter(cpf=attrs.get('cpf')).exists():
                raise serializers.ValidationError({"cpf": "Este CPF já está cadastrado."})

            if attrs.get('email') is not None and Cliente.objects.filter(email=attrs.get('email')).exists():
                raise serializers.ValidationError({"email": "Este e-mail já está cadastrado."})

        return attrs
