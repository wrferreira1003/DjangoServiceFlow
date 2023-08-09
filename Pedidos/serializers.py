# serializers.py dentro do seu app
from rest_framework import serializers
from .models import NovoCliente, NovoClienteEnvolvido, Documento

class NovoClienteEnvolvidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NovoClienteEnvolvido
        fields = '__all__'

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'

class NovoClienteSerializer(serializers.ModelSerializer):
    envolvido = NovoClienteEnvolvidoSerializer(required=False)
    documentos = DocumentoSerializer(many=True, required=False)

    class Meta:
        model = NovoCliente
        fields = '__all__'
        
    def create(self, validated_data):
        envolvido_data = validated_data.pop('envolvido', None)
        documentos_data = validated_data.pop('documentos', [])

        cliente = NovoCliente.objects.create(**validated_data)

        if envolvido_data:
            NovoClienteEnvolvido.objects.create(cliente=cliente, **envolvido_data)

        for doc_data in documentos_data:
            Documento.objects.create(cliente=cliente, **doc_data)

        return cliente



#class ModelPedidoSerializers(serializers.ModelSerializer):
#    cliente = ClienteSerializer()
#    sub_servico = serializers.PrimaryKeyRelatedField(queryset=Subservico.objects.all())
#   
#    class Meta:
#        model = ModelPedido
#        fields = ['cliente', 'status', 'mensagem', 'documento', 'nome_envolvido',
#                  'cpf_envolvido', 'indetidade_envolvido', 'documento_envolvido',
#                  'sub_servico']
#
#    def create(self, validated_data):
#        cliente_data = validated_data.pop('cliente')
#        cliente = ClienteSerializer.create(ClienteSerializer(), validated_data=cliente_data)
#        pedido, created = ModelPedido.objects.update_or_create(cliente=cliente, 
#                                                               **validated_data)
 #       return pedido