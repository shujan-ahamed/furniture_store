# Generated by Django 4.0.9 on 2023-03-10 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_alter_colour_colour_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='image',
        ),
        migrations.AddField(
            model_name='productvariation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/'),
        ),
    ]
