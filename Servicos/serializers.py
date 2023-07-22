from rest_framework import serializers
from .models import Servico, Subservico, ModelPedido
from Cliente.serializers import ClienteSerializer
from Afiliados.serializers import AfiliadosModelSerializer
from Afiliados.models import AfiliadosModel
from django.core.exceptions import ValidationError
import os

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['nome_servico']

class SubservicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subservico
        fields = ['nome_subservico', 'servico']


class ModelPedidoSerializers(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    sub_servico = serializers.PrimaryKeyRelatedField(queryset=Subservico.objects.all())
   
    class Meta:
        model = ModelPedido
        fields = ['cliente', 'status', 'mensagem', 'documento', 'nome_envolvido',
                  'cpf_envolvido', 'indetidade_envolvido', 'documento_envolvido',
                  'sub_servico']

    def create(self, validated_data):
        cliente_data = validated_data.pop('cliente')
        cliente = ClienteSerializer.create(ClienteSerializer(), validated_data=cliente_data)
        pedido, created = ModelPedido.objects.update_or_create(cliente=cliente, 
                                                               **validated_data)
        return pedido