# Generated by Django 4.2.3 on 2023-12-09 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0038_rename_ano_financiamentoveiculo_ano_fabricacao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='processos',
            name='Data_emissao_rg',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='processos',
            name='orgao_emissor_rg',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
