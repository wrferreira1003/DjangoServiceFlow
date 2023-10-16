from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NovoPedidoSerializer,DocumentoSerializer,ClienteSerializerConsulta,NovoClienteSerializerConsulta, ClienteSerializerAlteracao,AtualizaClienteSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Processos, Documento
from Cliente.models import Cliente
from Cliente.serializers import ClienteSerializer, ClienteExistenteSerializer
from Servicos.models import Servico
from financeiro.models import Transacao
from Afiliados.models import AfiliadosModel

#Funcao que cria ou atualiza um novo cliente na hora que uma nova solicitacao e feita.
def criar_ou_atualizar_cliente(data):
    #Verificar se o cliente existe
    cliente_existente = None
    if 'cpf' in data:
        cliente_existente = Cliente.objects.filter(cpf=data['cpf']).first()

    #Caso o cliente existe vamos atualizar os dados dele
    if cliente_existente:
        cliente_serializer = ClienteExistenteSerializer(instance=cliente_existente, data=data, partial=True)
    else:
        cliente_serializer = ClienteSerializer(data=data)
    
    if cliente_serializer.is_valid(raise_exception=True):
        cliente_serializer.save()
        return cliente_serializer.data, cliente_existente is None

    return None, False

def criar_transacao(cliente_data,processo_obj, servico_id):
    try:
        cliente_instance = Cliente.objects.get(id=cliente_data.get('id'))
        
        #afiliado_instance = AfiliadosModel.objects.get(id=cliente_data.get('afiliado'))
        afiliado_id = cliente_data.get('afiliado')
        if afiliado_id:
            afiliado_instance = AfiliadosModel.objects.get(id=afiliado_id)
        else:
            afiliado_instance = None
        
        pedido_instance = Processos.objects.get(id=processo_obj.id)
        servico_instance = Servico.objects.get(pk=servico_id)

        servico_obj = Servico.objects.get(pk=servico_id)
        preco = servico_obj.preco

        transacao_data = {
            "cliente": cliente_instance,
            "afiliado": afiliado_instance,  # Assumindo que o cliente tem um campo afiliado
            "servico": servico_instance,
            "pedido": pedido_instance,  # Assumindo que a relação OneToOne entre Processos e Transacao é essa
            "preco": preco,  # Supondo que o modelo Servico tenha um campo chamado "valor"
            "FormaDePagamento": processo_obj.FormaDePagamento,  # você pode definir isso conforme necessário
            "status": "PENDENTE"
        }
        return Transacao.objects.create(**transacao_data)
    except Servico.DoesNotExist:
        print("erro")
        return None  # O serviço com o ID fornecido não existe.

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
    

    # Chamada para a função que cria ou atualiza o cliente
    cliente_data, is_new = criar_ou_atualizar_cliente(data)
    if not cliente_data:
        print("Erro ao criar ou atualizar cliente",status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Erro ao criar ou atualizar cliente."}, status=status.HTTP_400_BAD_REQUEST)
    # Vamos testar a validação dos documentos aqui
    doc_serializer = DocumentoSerializer(data=documentos_data, many=True)
    if doc_serializer.is_valid():
        print("Documentos validados corretamente!")
    else:
        print("Erro na validação dos documentos:", doc_serializer.errors)

   
    processo_serializer = NovoPedidoSerializer(data=data)


    if processo_serializer.is_valid():
        processo_serializer.validated_data['documentos'] = documentos_data

        # Aqui você atualiza o validated_data com o ID do cliente antes de salvar o processo.
        processo_serializer.validated_data['idCliente'] = cliente_data['id']  # ou cliente_data.id se for um objeto

        processo_obj = processo_serializer.save()

        # Agora, vamos criar a transação associada a esse cliente
        servico_id = data.get('servico')  # você mencionou que passa o id do serviço
        
        transacao_obj = criar_transacao(cliente_data,processo_obj, servico_id,)

        if not transacao_obj:
            # Handle error. O serviço com o ID fornecido não existe.
            return Response({"error": "Serviço não encontrado."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(processo_serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(f"Erro no serializer: {processo_serializer.errors}")
        return Response(processo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Consultar os pedidos pelo id do cliente
class NovoClienteDetailView(APIView):

    def get(self, request, id, format=None):
        clientes = Processos.objects.filter(idCliente=id)
        if clientes.exists():
            serializer = NovoClienteSerializerConsulta(clientes, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

#Consultar todos os pedidos, pelo painel do administrado.        
class TodosClientesViewSemFiltro(ListCreateAPIView):
    queryset = Processos.objects.all()
    serializer_class = ClienteSerializerConsulta

class TodosClientesView(ListCreateAPIView):
    queryset = Processos.objects.all()
    serializer_class = NovoClienteSerializerConsulta

#Excluir processos do banco de dados
class ClienteDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Processos.objects.all()
    serializer_class = NovoClienteSerializerConsulta
    lookup_field = 'id'

#Alteracao de informacoes no banco de dados
class ClienteDetailViewAlteracao(UpdateAPIView):
    queryset = Processos.objects.all()
    serializer_class = ClienteSerializerAlteracao
    lookup_field = 'id'

@api_view(['PATCH'])
def AtualizaClienteView(request, id):  # Adicionando cliente_id para identificar o registro
    try:
        cliente = Processos.objects.get(pk=id)  # Obtenha o cliente pelo ID
    except Processos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    files = request.FILES

    documentos_data = []

    # Captura todos os documentos enviados
    for key, arquivo in files.items():
        if key.startswith('documentos'):
            index = key.split('[')[1].split(']')[0]
            descricao = data.get(f'documentos[{index}].descricao')
            documentos_data.append({
                'descricao': descricao,
                'arquivo': arquivo
            })

    # Remover campos de documentos do data original para evitar problemas com o serializador
    for key in list(data.keys()):
        if key.startswith('documentos'):
            del data[key]

    data['documentos'] = documentos_data

    cliente_serializer = AtualizaClienteSerializer(cliente, data=data, partial=True)  # Usando um serializer para atualização

    if cliente_serializer.is_valid():
        
        cliente_serializer.validated_data['documentos'] = documentos_data
   
        cliente_serializer.save()
        return Response(cliente_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(cliente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PedidosPorAfiliadoListView(generics.ListAPIView):
    serializer_class = ClienteSerializerConsulta

    def get_queryset(self):
        """
        Este método irá retornar uma lista de pedidos para o afiliado especificado.
        O afiliado é determinado pelo `id` passado na URL.
        """
        afiliado_id = self.kwargs['afiliado_id']
        return Processos.objects.filter(afiliado__id=afiliado_id)
    
class PedidosPorClienteListView(generics.ListAPIView):
    serializer_class = ClienteSerializerConsulta

    def get_queryset(self):
        """
        Este método irá retornar uma lista de pedidos para o afiliado especificado.
        O afiliado é determinado pelo `id` passado na URL.
        """
        cliente_id = self.kwargs['idCliente']
        return Processos.objects.filter(idCliente=cliente_id)
    
@api_view(['DELETE'])
def delete_documento_api(request, documento_id):
    try:
        documento = Documento.objects.get(id=documento_id)
    except Documento.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        documento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)