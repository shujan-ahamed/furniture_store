# Generated by Django 4.0.10 on 2023-05-11 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0011_alter_productvariation_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariation',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.products'),
        ),
    ]
