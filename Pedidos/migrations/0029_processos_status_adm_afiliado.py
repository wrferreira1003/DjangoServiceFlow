# Generated by Django 4.2.3 on 2023-12-01 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0028_rename_cidade_cartorio_processos_formadepagamento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='processos',
            name='status_adm_afiliado',
            field=models.CharField(choices=[('Pendente', 'Pendente'), ('Em analise', 'Em Analise'), ('Aprovado', 'Aprovado'), ('Recusado', 'Recusado'), ('Ajustar documentação', 'Ajustar documentação')], default='Pendente', max_length=50),
        ),
    ]
