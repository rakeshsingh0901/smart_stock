# Generated by Django 4.0.6 on 2022-12-04 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_data', '0003_delivery_delivery_high_weeklydelivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeklydelivery',
            name='delivery_high',
            field=models.FloatField(blank=True, null=True, verbose_name='Delivery is High Of AVG'),
        ),
    ]
