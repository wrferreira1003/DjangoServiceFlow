# Generated by Django 4.2.3 on 2023-10-14 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0020_processos_conjugue1_processos_conjugue2'),
    ]

    operations = [
        migrations.AddField(
            model_name='processos',
            name='data_casamento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
