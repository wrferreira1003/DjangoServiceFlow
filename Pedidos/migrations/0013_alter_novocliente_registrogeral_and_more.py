# Generated by Django 4.2.3 on 2023-10-01 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0012_novocliente_tipodeentrega'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novocliente',
            name='RegistroGeral',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='novocliente',
            name='bairro',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='novocliente',
            name='cep',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='novocliente',
            name='cidade',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='novocliente',
            name='cpf',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='novocliente',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='novocliente',
            name='endereco',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='novocliente',
            name='estado',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='novocliente',
            name='nome',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='novocliente',
            name='sobrenome',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='novocliente',
            name='telefone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
