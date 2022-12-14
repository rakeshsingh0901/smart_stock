# Generated by Django 4.0.6 on 2022-12-10 13:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stock_data', '0005_rename_traded_quantity_weeklydelivery_volume'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='day20_avg',
            field=models.FloatField(blank=True, null=True, verbose_name='SMAvg of 20 day '),
        ),
        migrations.AddField(
            model_name='weeklydelivery',
            name='cr_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weeklydelivery',
            name='week20_avg',
            field=models.FloatField(blank=True, null=True, verbose_name='SMAvg of 20 week'),
        ),
    ]
