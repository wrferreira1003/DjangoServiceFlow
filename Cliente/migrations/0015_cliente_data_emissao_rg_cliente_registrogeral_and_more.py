# Generated by Django 4.2.3 on 2023-12-09 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0014_remove_cliente_groups_remove_cliente_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='Data_emissao_rg',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='RegistroGeral',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cnh',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='data_nascimento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='estado_civil',
            field=models.CharField(blank=True, choices=[('Solteiro', 'Solteiro'), ('Casado', 'Casado'), ('Divorciado', 'Divorciado'), ('Viuvo', 'Viúvo')], max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='filiacao1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='filiacao2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='genero',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='naturalidade',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='orgao_emissor_rg',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='profissao',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
