# Generated by Django 4.2.3 on 2023-10-28 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0011_alter_cliente_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]