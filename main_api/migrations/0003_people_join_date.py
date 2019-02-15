# Generated by Django 2.1.7 on 2019-02-15 16:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_api', '0002_people'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='join_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Join Date'),
            preserve_default=False,
        ),
    ]
