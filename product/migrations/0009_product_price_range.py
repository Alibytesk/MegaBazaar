# Generated by Django 5.2 on 2025-04-14 13:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_pricerange'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_range',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pricerange', to='product.pricerange'),
        ),
    ]
