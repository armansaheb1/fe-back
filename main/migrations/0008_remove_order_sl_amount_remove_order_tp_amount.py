# Generated by Django 4.1.3 on 2022-12-28 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_order_limit_order_limit_amount_order_sl_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='sl_amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='tp_amount',
        ),
    ]