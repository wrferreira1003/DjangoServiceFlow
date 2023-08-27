from rest_framework import serializers
from .models import AfiliadosModel
from django.contrib.auth.hashers import make_password

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
                ]  # Lista todos os campos, exceto a senha

    def create(self, validated_data):
        # Se a password não for fornecida, definir password padrão
        if 'password' not in validated_data:
            validated_data['password'] = 'Hcred@2023'
        
        password = validated_data.pop('password')
        afiliado = AfiliadosModel(**validated_data)
        afiliado.set_password(password)  # Use o método set_password para armazenar a senha de forma segura
        afiliado.save()
        return afiliado

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