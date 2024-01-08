from .serializers import UserSerializer,AtualizaClienteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from Afiliados.models import AfiliadosModel as Cliente
from rest_framework.decorators import permission_classes

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
def verifica_cpf(request, cpf, email):
    try:
        cliente_cpf = Cliente.objects.get(cpf=cpf)
        if cliente_cpf.email == email:
            return Response({"exists": False}, status=status.HTTP_200_OK)
        else:
            return Response({"exists": True}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"exists": False}, status=status.HTTP_200_OK)

#Verificar se o Email ja existe
@api_view(['GET'])
def verifica_email(request, email, cpf):
    try:
        cliente = Cliente.objects.get(email=email)
        if cliente.cpf == cpf:
            return Response({"exists": False}, status=status.HTTP_200_OK)
        else:
            return Response({"exists": True}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"exists": False}, status=status.HTTP_200_OK)

@api_view(['GET'])
def verifica_cpf_email(request, cpf, email):
    try:
        cliente_cpf = Cliente.objects.get(cpf=cpf, user_type='CLIENTE')
        cliente_email = Cliente.objects.get(email=email, user_type='CLIENTE')
    
        if cliente_cpf.id == cliente_email.id:
            return Response({"exists": True}, status=status.HTTP_200_OK)
        else:
            return Response({"exists": False}, status=status.HTTP_200_OK)
    except Cliente.DoesNotExist:
        return Response({"exists": False}, status=status.HTTP_200_OK)
    
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
        users = Cliente.objects.filter(validation_token=token)
        
        for user in users:
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
        pass# Token não encontrado, renderizando página com mensagem de erro
    return render(request, 'cliente/erro.html', {'message': 'Ocorreu um erro ao validar seu e-mail. O token pode ser inválido ou ter expirado.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListagemClienteCpf(request, cpf):
    try:
        cliente = Cliente.objects.get(cpf=cpf)
        serializer = UserSerializer(cliente)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente não encontrado'}, status=404)
    
@api_view(['GET'])
def valida_cpf(request, cpf):
    try:
        cliente = Cliente.objects.get(cpf=cpf)
        return Response({"exists": True}, status=status.HTTP_200_OK)
    except Cliente.DoesNotExist:
        return Response({"exists": False}, status=status.HTTP_200_OK)

@api_view(['GET'])
def valida_email(request, email):
    try:
        cliente = Cliente.objects.get(email=email)
        return Response({"exists": True}, status=status.HTTP_200_OK)
    except Cliente.DoesNotExist:
        return Response({"exists": False}, status=status.HTTP_200_OK)