# Generated by Django 5.0.4 on 2024-05-06 09:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
