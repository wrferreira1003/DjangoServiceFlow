# Generated by Django 4.2.3 on 2023-10-01 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Servicos', '0007_delete_subservico'),
        ('Pedidos', '0016_alter_processos_idcliente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processos',
            name='servicoCadastro',
        ),
        migrations.AlterField(
            model_name='processos',
            name='servico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Servicos.servico'),
        ),
    ]
