# Generated by Django 4.2.3 on 2024-01-06 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0089_delete_consultoriacontasbil_delete_contabilidade_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientempresarial',
            name='ramo_atividade',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
