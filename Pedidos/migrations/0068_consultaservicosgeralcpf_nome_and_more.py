# Generated by Django 4.2.3 on 2023-12-26 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0067_consultaservicosgeralveiculo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultaservicosgeralcpf',
            name='nome',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='consultaservicosgeralveiculo',
            name='nome',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
