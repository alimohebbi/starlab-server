# Generated by Django 2.1.7 on 2019-03-04 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_api', '0005_auto_20190303_0623'),
    ]

    operations = [
        migrations.AddField(
            model_name='software',
            name='authors',
            field=models.ManyToManyField(through='main_api.SoftwareAuthors', to='main_api.People'),
        ),
        migrations.AlterField(
            model_name='people',
            name='title',
            field=models.CharField(choices=[('invest', 'Investigator'), ('post', 'Post-doc'), ('phd', 'PhD'), ('former', 'Former'), ('collab', 'Collaborator')], max_length=6),
        ),
        migrations.AlterField(
            model_name='software',
            name='detail',
            field=models.FileField(blank=True, upload_to='software_detail'),
        ),
    ]
