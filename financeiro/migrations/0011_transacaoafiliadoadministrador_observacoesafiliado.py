# Generated by Django 4.2.3 on 2023-12-01 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0010_transacaoafiliadoadministrador'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacaoafiliadoadministrador',
            name='ObservacoesAfiliado',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
