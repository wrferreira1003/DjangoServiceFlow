# Generated by Django 4.2.3 on 2023-10-01 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0013_alter_novocliente_registrogeral_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novocliente',
            name='sobrenome',
        ),
    ]
