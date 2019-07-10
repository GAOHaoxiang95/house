# Generated by Django 2.2 on 2019-07-09 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricesite', '0008_auto_20190706_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='baths',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='preference',
            name='latitude',
            field=models.DecimalField(decimal_places=8, default=51.49869386764022, max_digits=11),
        ),
        migrations.AlterField(
            model_name='preference',
            name='longitude',
            field=models.DecimalField(decimal_places=8, default=-0.17911445396727732, max_digits=11),
        ),
    ]