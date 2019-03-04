# Generated by Django 2.1.7 on 2019-03-03 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_api', '0004_auto_20190303_0600'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoftwareAuthors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_api.People')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.RemoveField(
            model_name='software',
            name='authors',
        ),
        migrations.AddField(
            model_name='softwareauthors',
            name='software',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_api.Software'),
        ),
    ]
