from rest_framework import serializers
from .models import AfiliadosModel

class AfiliadosModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Defina password como não obrigatório
    class Meta:
        model = AfiliadosModel
        fields = [
                'id', 
                'nome',
                'password',
                'email', 
                'razao_social',
                'cnpj',
                'telefone',
                'endereco',
                'bairro',
                'cidade',
                'estado',
                'cep',
                'foto',
                'user_type',
                'last_login',
                'afiliado_relacionado',
                'cpf',
                'telefone2',
                'RegistroGeral',
                'Data_emissao_rg',
                'orgao_emissor_rg',
                'estado_civil',
                'profissao',
                'data_nascimento',
                'genero',
                'naturalidade',
                'cnh',
                'nome_mae',
                'nome_pai',
                'logradouro',
                'complemento',
                'numero',
                'password',
                'is_validated',
                'validation_token',
                ]  # Lista todos os campos, exceto a senha
    #Metodo de criação do afiliado/cliente
    def create(self, validated_data):
        # Se a password não for fornecida, definir password padrão
        if 'password' not in validated_data or validated_data['password'] in [None, '']:
            if validated_data.get('user_type') == 'AFILIADO':
                validated_data['password'] = validated_data.get('cnpj', 'rcfacil2024')
            elif validated_data.get('user_type') == 'FUNC':
                validated_data['password'] = validated_data.get('cpf', 'rcfacil2024')
            
        password = validated_data.pop('password')
        afiliado = AfiliadosModel(**validated_data)
        afiliado.set_password(password)  # Use o método set_password para armazenar a senha de forma segura
        afiliado.save()
        return afiliado

    #Metodo de atualização do afiliado/cliente
    def update(self, instance, validated_data):
        # Verifique se a senha está sendo atualizada
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        # Atualize os outros campos normalmente
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class AfiliadosPublicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = AfiliadosModel
        fields = [
            'id',
            'nome',
            'razao_social',
            'bairro',
            'cidade',
            'estado',
            'cep',
            'telefone',
            'endereco',
            'cnpj',

        ]

class FuncionarioSerializerFuncionarios(serializers.ModelSerializer):
    class Meta:
        model = AfiliadosModel
        fields = ['id', 
                  'nome', 
                  'email', 
                  'telefone', 
                  'endereco', 
                  'bairro', 
                  'cidade', 
                  'estado', 
                  'cep', 
                  'cpf', 
                  'foto',
                  'last_login',
                  ]

