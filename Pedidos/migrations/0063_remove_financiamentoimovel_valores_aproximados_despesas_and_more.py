# Generated by Django 4.2.3 on 2023-12-14 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0062_remove_financiamentoimovel_detalhes_instituicao_financeira'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas',
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='detalhes_produtos_ativos_data_ultimo_pagamento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='detalhes_produtos_ativos_qtde_prestacoes',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='detalhes_produtos_ativos_tipo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='detalhes_produtos_ativos_tipo_instituicao_financeira',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='detalhes_produtos_ativos_tipo_valor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_alimentacao',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_aluguel',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_combustivel_transporte',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_condominio',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_conta_de_luz_agua',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_contas_telefone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_despesas_com_saude',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_educacao',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_pensao_alimenticia',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
