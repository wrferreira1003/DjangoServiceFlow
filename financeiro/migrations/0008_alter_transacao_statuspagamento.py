# Generated by Django 4.2.3 on 2023-11-07 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0007_rename_status_transacao_statuspagamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='statusPagamento',
            field=models.CharField(choices=[('Pendente de Pagamento', 'Pendente de Pagamento'), ('Pago', 'Pago'), ('Aguardando Confirmação', 'Aguardando Confirmação')], default='Pendente de Pagamento', max_length=100),
        ),
    ]