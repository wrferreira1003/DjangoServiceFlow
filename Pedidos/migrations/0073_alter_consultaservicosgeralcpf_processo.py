# Generated by Django 4.2.3 on 2023-12-26 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0072_alter_consultaservicosgeralcpf_processo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultaservicosgeralcpf',
            name='processo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pedidos.processos'),
        ),
    ]