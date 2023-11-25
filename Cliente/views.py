from .serializers import ClienteSerializer, UserSerializer,AtualizaClienteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cliente
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

class TodosClientesViewSet(viewsets.ModelViewSet):  # ReadOnly porque só queremos listar, sem criar, atualizar ou deletar
   
    queryset = Cliente.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']

    def retrieve(self, request, pk=None):
        try:
            cliente = Cliente.objects.get(pk=pk)
            serializer = UserSerializer(cliente)
            return Response(serializer.data)
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente não encontrado'}, status=404)

#Verificar se o CPF ja existe
@api_view(['GET'])
def verifica_cpf(request, cpf):
    if Cliente.objects.filter(cpf=cpf).exists():
        return Response({"message": "CPF já existe"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "CPF não encontrado"}, status=status.HTTP_200_OK)

#Verificar se o Email ja existe
@api_view(['GET'])
def verifica_email(request, email):
    if Cliente.objects.filter(email=email).exists():
        return Response({"message": "Email já existe"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Email não encontrado"}, status=status.HTTP_200_OK)

#Registrar um novo cliente
class RegistrarClientesViewSet(APIView):
    def post(self, request):
        serializer = ClienteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class AtualizaClienteViewSet(APIView):
    def put(self, request, pk=None):
        try:
            cliente = Cliente.objects.get(pk=pk)
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AtualizaClienteSerializer(cliente, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#verifica o token e, se válido, ativa a conta do usuário.
@api_view(['GET'])
def validate_account(request):
    token = request.GET.get('token')
    try:
        user = Cliente.objects.get(validation_token=token)
        
        if user.is_validated:
            # O e-mail já foi validado, renderizando página com uma mensagem informativa
            return render(request, 'cliente/sucesso.html', {'message': 'Seu e-mail já foi validado anteriormente.'})
        
        user.is_validated = True
        user.save()
        # E-mail validado com sucesso, renderizando página com mensagem de sucesso
        return render(request, 'cliente/sucesso.html', {
                                'message': 'Seu e-mail foi validado com sucesso! ',
                                'link_url': 'https://www.rcfacildocumentoseservicos.com.br/'
})
    except ObjectDoesNotExist:
        # Token não encontrado, renderizando página com mensagem de erro
        return render(request, 'cliente/erro.html', {'message': 'Ocorreu um erro ao validar seu e-mail. O token pode ser inválido ou ter expirado.'})

class LoginUserView(APIView):
   
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("senha")
     
        try:
            cliente = Cliente.objects.get(email=email)
        except Cliente.DoesNotExist:
            return Response({"error": "Email inválido."}, status=status.HTTP_401_UNAUTHORIZED)
        

        if not cliente.check_password(password):
            return Response({"error": "Senha inválida."}, status=status.HTTP_401_UNAUTHORIZED)
   
 
        # Se chegou aqui, as credenciais são válidas; gere o token
        refresh = RefreshToken.for_user(cliente)
        access_token = str(refresh.access_token)

        # Serializar os dados do afiliado
        cliente_data = UserSerializer(cliente).data

        return Response({"token": access_token, "user": cliente_data}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def ListagemClienteCpf(request, cpf):
    try:
        cliente = Cliente.objects.get(cpf=cpf)
        serializer = UserSerializer(cliente)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Cliente.DoesNotExist:
        return Response({"message": "CPF não encontrado"}, status=status.HTTP_400_BAD_REQUEST)