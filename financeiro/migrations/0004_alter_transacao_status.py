# Generated by Django 4.2.3 on 2023-11-01 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0003_rename_arquivo_transacao_comprovante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='status',
            field=models.CharField(choices=[('PENDENTE', 'Pendente de Pagamento'), ('PAGO', 'Pago'), ('AGUARDANDO', 'Aguardando Pagamento')], default='PENDENTE', max_length=20),
        ),
    ]