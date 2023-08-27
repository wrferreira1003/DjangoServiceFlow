# serializers.py dentro do seu app
from rest_framework import serializers
from .models import NovoCliente, Documento
from django.db import transaction
from validacoes import validate_file_type, validate_file_size
import os

class DocumentoSerializer(serializers.ModelSerializer):
    arquivo = serializers.FileField(validators=[validate_file_type, validate_file_size])
    class Meta:
        model = Documento
        fields = '__all__'

class NovoClienteSerializer(serializers.ModelSerializer):
    documentos = DocumentoSerializer(many=True, required=False)

    class Meta:
        model = NovoCliente
        fields = '__all__'
        
    def create(self, validated_data):
        with transaction.atomic():
            documentos_data = validated_data.pop('documentos', [])

            cliente = NovoCliente.objects.create(**validated_data)

            for doc in documentos_data:
                Documento.objects.create(cliente=cliente, **doc)

            return cliente

