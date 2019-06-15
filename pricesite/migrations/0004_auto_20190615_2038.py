# Generated by Django 2.2 on 2019-06-15 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pricesite', '0003_auto_20190608_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='Tourist', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='prefer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pricesite.Preference'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pricesite.Preference')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
