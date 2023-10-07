from rest_framework import serializers
from .models import Servico,Categoria

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields =  ['id', 'nome_servico', 'tipo', 'preco']

class CategoriaSerializer(serializers.ModelSerializer):
    servicos = ServicoSerializer(many=True)  # Aninhando a serializer de Categoria aqui

    class Meta:
        model = Categoria
        fields = ['id', 'nome_categoria', 'servicos']

