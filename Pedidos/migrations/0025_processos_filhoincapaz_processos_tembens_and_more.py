# Generated by Django 4.2.3 on 2023-10-16 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0024_processos_data_final_processos_data_inicial'),
    ]

    operations = [
        migrations.AddField(
            model_name='processos',
            name='filhoIncapaz',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='processos',
            name='temBens',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='processos',
            name='temFilhosMenores',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]