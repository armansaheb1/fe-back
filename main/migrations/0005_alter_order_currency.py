# Generated by Django 4.1.3 on 2022-12-11 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_order_leverage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='currency',
            field=models.CharField(max_length=100),
        ),
    ]
