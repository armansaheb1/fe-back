# Generated by Django 4.1.3 on 2022-12-27 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='limit',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='limit_amount',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='sl',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='sl_amount',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='tp',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='tp_amount',
            field=models.FloatField(null=True),
        ),
    ]
