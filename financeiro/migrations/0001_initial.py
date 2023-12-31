# Generated by Django 4.2.3 on 2023-10-01 04:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Servicos', '0007_delete_subservico'),
        ('Pedidos', '0013_alter_novocliente_registrogeral_and_more'),
        ('Cliente', '0008_alter_cliente_telefone2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('FormaDePagamento', models.CharField(blank=True, max_length=100, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('PENDENTE', 'Pendente de Pagamento'), ('PAGO', 'Pago')], default='PENDENTE', max_length=20)),
                ('afiliado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transacoes', to=settings.AUTH_USER_MODEL)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transacoes', to='Cliente.cliente')),
                ('pedido', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Pedidos.novocliente')),
                ('servico', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Servicos.servico')),
            ],
        ),
    ]
