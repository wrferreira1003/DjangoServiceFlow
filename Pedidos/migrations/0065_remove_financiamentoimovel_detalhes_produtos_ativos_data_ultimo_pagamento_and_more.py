# Generated by Django 4.2.3 on 2023-12-14 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0064_remove_financiamentoimovel_detalhes_produtos_ativos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='detalhes_produtos_ativos_data_ultimo_pagamento',
        ),
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='detalhes_produtos_ativos_qtde_prestacoes',
        ),
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='detalhes_produtos_ativos_tipo',
        ),
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='detalhes_produtos_ativos_tipo_instituicao_financeira',
        ),
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='detalhes_produtos_ativos_tipo_valor',
        ),
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_alimentacao',
        ),
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_aluguel',
        ),
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_combustivel_transporte',
        ),
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_condominio',
        ),
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_conta_de_luz_agua',
        ),
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_contas_telefone',
        ),
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_despesas_com_saude',
        ),
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_educacao',
        ),
        migrations.RemoveField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas_pensao_alimenticia',
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='detalhes_produtos_ativos',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='financiamentoimovel',
            name='valores_aproximados_despesas',
            field=models.JSONField(blank=True, null=True),
        ),
    ]