# Generated by Django 2.2 on 2019-07-05 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricesite', '0006_preferencehouses_interest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferencehouses',
            name='furniture_state',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='preferencehouses',
            name='property_type',
            field=models.CharField(default='', max_length=20),
        ),
    ]