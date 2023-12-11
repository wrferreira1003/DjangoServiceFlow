# Generated by Django 4.2.3 on 2023-12-09 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0044_financiamentoveiculo_nome_referencia_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financiamentoveiculo',
            name='nome_referencia',
        ),
        migrations.RemoveField(
            model_name='financiamentoveiculo',
            name='telefone_referencia',
        ),
        migrations.AddField(
            model_name='clientjob',
            name='nome_referencia',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientjob',
            name='telefone_referencia',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]