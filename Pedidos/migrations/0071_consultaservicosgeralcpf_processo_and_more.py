# Generated by Django 4.2.3 on 2023-12-26 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0070_rename_servicocadastro_consultaservicosgeralcpf_servico'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultaservicosgeralcpf',
            name='processo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pedidos.processos'),
        ),
        migrations.AddField(
            model_name='consultaservicosgeralveiculo',
            name='processo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pedidos.processos'),
        ),
    ]
