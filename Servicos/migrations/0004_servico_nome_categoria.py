# Generated by Django 4.2.3 on 2023-09-29 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Servicos', '0003_servico_categoria_servico_preco'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='nome_categoria',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]