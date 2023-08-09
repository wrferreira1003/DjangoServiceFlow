# views.py dentro do seu app
from rest_framework import viewsets
from .models import NovoCliente, NovoClienteEnvolvido, Documento
from .serializers import NovoClienteSerializer

class NovoPedidoViewSet(viewsets.ModelViewSet):
    queryset = NovoCliente.objects.all()
    serializer_class = NovoClienteSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NovoCliente, NovoClienteEnvolvido, Documento
from .serializers import NovoClienteSerializer, NovoClienteEnvolvidoSerializer, DocumentoSerializer

@api_view(['POST'])
def criar_cliente_com_relacionados(request):
    data = request.data
    
    # Primeiro, criamos o NovoCliente
    cliente_serializer = NovoClienteSerializer(data=data)
    if cliente_serializer.is_valid():
        cliente_serializer.save()
        cliente_id = cliente_serializer.instance.id
        print(cliente_id)
        
        # Agora, use o ID do cliente para criar o NovoClienteEnvolvido
        envolvido_data = data.get('envolvido')
        if envolvido_data:
            envolvido_data['cliente'] = cliente_id
            envolvido_serializer = NovoClienteEnvolvidoSerializer(data=envolvido_data)
        if envolvido_serializer.is_valid():
            envolvido_serializer.save()
        else:
            return Response(envolvido_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Faça o mesmo para Documento ou qualquer outra entidade relacionada
        documentos_data = data.get('documentos')
        for doc_data in documentos_data:
            doc_data['cliente'] = cliente_id
            doc_serializer = DocumentoSerializer(data=doc_data)
            if doc_serializer.is_valid():
                doc_serializer.save()
            else:
                return Response(doc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(cliente_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
