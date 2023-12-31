# Generated by Django 4.2.3 on 2023-09-29 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Servicos', '0002_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='categoria',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='servicos', to='Servicos.categoria'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servico',
            name='preco',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
