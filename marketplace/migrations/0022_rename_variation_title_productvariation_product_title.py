# Generated by Django 4.0.10 on 2023-05-23 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0021_productvariation_slug_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productvariation',
            old_name='variation_title',
            new_name='product_title',
        ),
    ]
