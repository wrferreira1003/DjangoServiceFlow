# Generated by Django 4.2.3 on 2023-12-15 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Afiliados', '0013_afiliadosmodel_is_validated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afiliadosmodel',
            name='afiliado_relacionado',
            field=models.ForeignKey(blank=True, help_text='Afiliado ao está associado', limit_choices_to={'user_type': 'AFILIADO'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='funcionarios', to=settings.AUTH_USER_MODEL),
        ),
    ]