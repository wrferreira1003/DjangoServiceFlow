# Generated by Django 4.2.3 on 2023-12-10 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0046_clienteterceiro_cartorio'),
    ]

    operations = [
        migrations.AddField(
            model_name='processos',
            name='fisico_juridico',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
