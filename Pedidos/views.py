from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NovoClienteSerializer,DocumentoSerializer

@api_view(['POST'])
def criar_cliente_com_relacionados(request):
    data = request.data.copy()  # Mudança aqui
    files = request.FILES
    
    documentos_data = []

    # Captura todos os documentos enviados
    for key, arquivo in files.items():
        if key.startswith('documentos'):
            index = key.split('[')[1].split(']')[0]  # pegar o índice dos documentos
            descricao = data.get(f'documentos[{index}].descricao')
            documentos_data.append({
                'descricao': descricao,
                'arquivo': arquivo
            })
    
    # Remover campos de documentos do data original para evitar problemas com o serializador
    for key in list(data.keys()):
        if key.startswith('documentos'):
            del data[key]

    # Incluindo os documentos processados na data
    data['documentos'] = documentos_data
    

    # Vamos testar a validação dos documentos aqui
    doc_serializer = DocumentoSerializer(data=documentos_data, many=True)
    if doc_serializer.is_valid():
        print("Documentos validados corretamente!")
    else:
        print("Erro na validação dos documentos:", doc_serializer.errors)

    print(data) 
    cliente_serializer = NovoClienteSerializer(data=data)
    
    if cliente_serializer.is_valid():
        cliente_serializer.validated_data['documentos'] = documentos_data
        cliente_serializer.save()
        return Response(cliente_serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(f"Erro no serializer: {cliente_serializer.errors}")
        return Response(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

