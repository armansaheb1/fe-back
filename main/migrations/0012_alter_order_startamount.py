# Generated by Django 4.1.3 on 2023-01-07 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_rename_start_closedorder_startprice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='startamount',
            field=models.FloatField(null=True),
        ),
    ]
