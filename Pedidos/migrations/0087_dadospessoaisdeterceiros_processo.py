# Generated by Django 4.2.3 on 2024-01-05 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0086_alter_dadospessoaisdeterceiros_data_emissao_rg_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dadospessoaisdeterceiros',
            name='processo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pedidos.processos'),
        ),
    ]
