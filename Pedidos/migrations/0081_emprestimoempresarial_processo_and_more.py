# Generated by Django 4.2.3 on 2024-01-03 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0080_remove_emprestimosemgeral_cpf_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprestimoempresarial',
            name='processo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pedidos.processos'),
        ),
        migrations.AddField(
            model_name='garantiaimoveis',
            name='processo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pedidos.processos'),
        ),
        migrations.AddField(
            model_name='garantiaveiculo',
            name='processo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pedidos.processos'),
        ),
    ]