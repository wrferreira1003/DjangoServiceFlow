# Generated by Django 4.2.3 on 2023-12-07 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0033_processos_telefoneenvolvido'),
    ]

    operations = [
        migrations.CreateModel(
            name='financiamentoVeiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_veiculo', models.CharField(blank=True, max_length=100, null=True)),
                ('marca', models.CharField(blank=True, max_length=100, null=True)),
                ('modelo', models.CharField(blank=True, max_length=100, null=True)),
                ('ano', models.CharField(blank=True, max_length=100, null=True)),
                ('placa', models.CharField(blank=True, max_length=100, null=True)),
                ('versao', models.CharField(blank=True, max_length=100, null=True)),
                ('estado_licenciamento', models.CharField(blank=True, max_length=100, null=True)),
                ('valor', models.CharField(blank=True, max_length=100, null=True)),
                ('entrada', models.CharField(blank=True, max_length=100, null=True)),
                ('prazo', models.CharField(blank=True, max_length=100, null=True)),
                ('banco', models.CharField(blank=True, max_length=100, null=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pedidos.processos')),
            ],
        ),
        migrations.CreateModel(
            name='ClientJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profissao', models.CharField(blank=True, max_length=100, null=True)),
                ('cargo', models.CharField(blank=True, max_length=100, null=True)),
                ('renda_mensal', models.CharField(blank=True, max_length=100, null=True)),
                ('data_admissao', models.DateField(blank=True, null=True)),
                ('telefone_trabalho', models.CharField(blank=True, max_length=15, null=True)),
                ('empresa', models.CharField(blank=True, max_length=100, null=True)),
                ('cep_trabalho', models.CharField(blank=True, max_length=9, null=True)),
                ('logradouro_trabalho', models.TextField(blank=True, null=True)),
                ('complemento_trabalho', models.TextField(blank=True, null=True)),
                ('numero_trabalho', models.CharField(blank=True, max_length=9, null=True)),
                ('bairro_trabalho', models.CharField(blank=True, max_length=100, null=True)),
                ('cidade_trabalho', models.CharField(blank=True, max_length=100, null=True)),
                ('estado_trabalho', models.CharField(blank=True, max_length=50, null=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Pedidos.processos')),
            ],
        ),
    ]
