# Generated by Django 4.2.3 on 2023-12-09 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0043_processos_filiacao1_processos_filiacao2'),
    ]

    operations = [
        migrations.AddField(
            model_name='financiamentoveiculo',
            name='nome_referencia',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoveiculo',
            name='telefone_referencia',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
