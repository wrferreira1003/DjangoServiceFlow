# Generated by Django 4.2.3 on 2023-09-24 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0003_novocliente_observacoes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novocliente',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('em_analise', 'Em Analise'), ('aprovado', 'Aprovado'), ('recusado', 'Recusado'), ('Ajustar_Documentaçao', 'Ajustar Documentação')], default='pendente', max_length=50),
        ),
    ]