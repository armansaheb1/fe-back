# Generated by Django 4.1.3 on 2023-01-07 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_closedorder_startprice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='closedorder',
            options={'verbose_name': 'Close Order', 'verbose_name_plural': 'Close Orders'},
        ),
        migrations.AddField(
            model_name='order',
            name='canceled',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
