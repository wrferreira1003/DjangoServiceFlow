# Generated by Django 4.2.3 on 2023-12-28 23:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0079_emprestimosemgeral_garantiaveiculo_garantiaimoveis_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emprestimosemgeral',
            name='cpf',
        ),
        migrations.RemoveField(
            model_name='emprestimosemgeral',
            name='data_nascimento',
        ),
        migrations.RemoveField(
            model_name='emprestimosemgeral',
            name='email',
        ),
        migrations.RemoveField(
            model_name='emprestimosemgeral',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='emprestimosemgeral',
            name='telefone',
        ),
    ]
