# Generated by Django 4.2.3 on 2023-09-29 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Servicos', '0004_servico_nome_categoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servico',
            name='nome_categoria',
        ),
    ]
