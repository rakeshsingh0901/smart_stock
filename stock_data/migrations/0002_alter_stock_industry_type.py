# Generated by Django 4.0.6 on 2022-12-02 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='industry_type',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Industry Type'),
        ),
    ]