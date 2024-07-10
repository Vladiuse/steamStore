# Generated by Django 5.0.6 on 2024-07-10 14:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_rename_order_id_orderpayment_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpayment',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_payment', to='orders.order'),
        ),
    ]