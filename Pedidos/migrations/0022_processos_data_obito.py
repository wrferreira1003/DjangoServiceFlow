# Generated by Django 4.2.3 on 2023-10-15 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0021_processos_data_casamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='processos',
            name='data_obito',
            field=models.DateField(blank=True, null=True),
        ),
    ]
