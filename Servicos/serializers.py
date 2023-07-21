from rest_framework import serializers
from .models import Servico, Subservico, ModelPedido

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = '__all__'

class SubservicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subservico
        fields = '__all__'

class ModelPedidoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ModelPedido
        fields = '__all__'