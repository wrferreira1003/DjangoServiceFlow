# Generated by Django 4.2.3 on 2023-10-01 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0010_novocliente_termo'),
    ]

    operations = [
        migrations.AddField(
            model_name='novocliente',
            name='cidadeCartorio',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
