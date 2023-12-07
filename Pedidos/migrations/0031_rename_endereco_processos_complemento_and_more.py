# Generated by Django 4.2.3 on 2023-12-06 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0030_processos_bairro_envolvido_processos_cep_envolvido_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='processos',
            old_name='endereco',
            new_name='complemento',
        ),
        migrations.RenameField(
            model_name='processos',
            old_name='endereco_envolvido',
            new_name='complemento_envolvido',
        ),
        migrations.AddField(
            model_name='processos',
            name='logradouro',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='processos',
            name='logradouro_envolvido',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='processos',
            name='numero',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
        migrations.AddField(
            model_name='processos',
            name='numero_envolvido',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
    ]
