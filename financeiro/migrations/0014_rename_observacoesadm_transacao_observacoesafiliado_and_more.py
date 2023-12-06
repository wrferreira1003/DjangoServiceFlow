# Generated by Django 4.2.3 on 2023-12-05 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0013_rename_observacoes_transacao_observacoesadm_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transacao',
            old_name='ObservacoesAdm',
            new_name='ObservacoesAfiliado',
        ),
        migrations.RemoveField(
            model_name='transacao',
            name='ObservacoesFranqueado',
        ),
        migrations.AddField(
            model_name='transacaoafiliadoadministrador',
            name='ObservacoesAdm',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
