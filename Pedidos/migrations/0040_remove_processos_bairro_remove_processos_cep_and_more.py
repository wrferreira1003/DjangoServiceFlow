# Generated by Django 4.2.3 on 2023-12-09 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0039_processos_data_emissao_rg_processos_orgao_emissor_rg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processos',
            name='bairro',
        ),
        migrations.RemoveField(
            model_name='processos',
            name='cep',
        ),
        migrations.RemoveField(
            model_name='processos',
            name='cidade',
        ),
        migrations.RemoveField(
            model_name='processos',
            name='complemento',
        ),
        migrations.RemoveField(
            model_name='processos',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='processos',
            name='logradouro',
        ),
        migrations.RemoveField(
            model_name='processos',
            name='numero',
        ),
    ]
