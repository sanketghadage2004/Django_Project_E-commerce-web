# Generated by Django 4.0.1 on 2022-02-20 09:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_alter_order_date_alter_reviews_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 20, 14, 58, 19, 43573)),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 20, 14, 58, 19, 43573)),
        ),
    ]
