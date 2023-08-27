from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import AfiliadosModel

class AfiliadosRegistrationTestCase(APITestCase):

    def test_registration(self):
        # Defina a URL para registro
        url = reverse('Afiliados:register')  # Assumindo que 'register' é o nome da URL em urls.py

        # Dados que você deseja enviar na solicitação POST
        data = {
            "nome": "Wellington Ferreira",
            "senha": "123456",
            "razao_social": "Afiliado-001",
            "cnpj": "12345678901234",
            "email": "wrf.wellington@gmail.com",
            "telefone": "123456",
            "endereco": "Endereço do Afiliado",
            "bairro": "Bairro do Afiliado",
            "cidade": "Cidade do Afiliado",
            "estado": "Estado do Afiliado",
            "cep": "12345678"
        }

        # Faça a solicitação POST
        response = self.client.post(url, data, format='json')
        print(response.data)
        # Verifique se a resposta tem status 200 OK
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # (Opcional) Verifique se o afiliado foi realmente criado no banco de dados
        self.assertEqual(AfiliadosModel.objects.count(), 1)


