# Generated by Django 4.0.10 on 2023-05-23 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0019_deal_discount_offer_products_on_sale_products_deal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariation',
            name='discount_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]