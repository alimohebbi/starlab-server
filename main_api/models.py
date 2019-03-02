from django.core.files import File
from django.db import models
import os
from django.dispatch import receiver


# Create your models here.

class News(models.Model):
    news_text = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.news_text[:100]


class People(models.Model):
    TITLE_CHOICES = (
        ('invest', 'Investigator'),
        ('post', 'Post-doc'),
        ('phd', 'PhD'),
        ('former', 'Former'),

    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    title = models.CharField(max_length=6, choices=TITLE_CHOICES)
    description = models.CharField(max_length=200)
    web_page = models.CharField(max_length=500)
    join_date = models.DateTimeField('Join Date')
    image = models.ImageField(upload_to='people_image', blank=True, default='people_image/default-pic.jpg')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


@receiver(models.signals.post_delete, sender=People)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image and instance.image.name != 'people_image/default-pic.jpg':
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=People)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = People.objects.get(pk=instance.pk).image
    except People.DoesNotExist:
        return False
    if instance.image.name == '':
        instance.image = 'people_image/default-pic.jpg'

    new_file = instance.image
    if old_file.name != "" and old_file.name != 'people_image/default-pic.jpg':
        if not old_file == new_file:
            if os.path.exists(old_file.path):
                os.remove(old_file.path)
