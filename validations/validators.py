from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from rest_framework import serializers
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
import re
import os

#Validacao Nome
def validate_nome(value):
    if len(value) < 3:
        raise ValidationError('O nome deve ter pelo menos 3 caracteres.')
    if not value.isalpha():
        raise ValidationError('O nome deve conter apenas letras.')
    
    return value.title()

#Validacao Email
def validate_email(value):
    validator = EmailValidator()
    try:
        validator(value)
    except ValidationError as e:
        raise ValidationError('O e-mail informado é inválido.')
    
    return value

#Validacao Telefone
def validate_telefone(value):
    try:
        phone_number = phonenumbers.parse(value, 'BR') # 'BR' é o código do país para o Brasil
        if not phonenumbers.is_valid_number(phone_number):
            raise serializers.ValidationError("Número de telefone inválido.")
        
        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)[3:] # Remover o código do país (+55) 
    except NumberParseException:
        raise serializers.ValidationError("Número de telefone inválido.")
    
from rest_framework import serializers

#Validacao CPF
def validate_cpf(value):
    cpf = ''.join(re.findall(r'\d', str(value)))

    if (not cpf) or (len(cpf) < 11):
        raise serializers.ValidationError("CPF inválido! Insira 11 dígitos.")

    inteiros = list(map(int, cpf))
    novo = inteiros[:9]

    while len(novo) < 11:
        r = sum([(len(novo)+1-i)*v for i,v in enumerate(novo)]) % 11

        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)

    if novo == inteiros:
        return cpf
    else:
        raise serializers.ValidationError("CPF inválido! Os dígitos verificadores estão incorretos.")

#Funcao para validacao de documentos
def valida_file_extension(value):
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.jpeg']
  if not ext.lower() in valid_extensions:
    raise ValidationError(u'Tipo de arquivo não suportado!')