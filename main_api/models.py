import os

from django.db import models
from django.dispatch import receiver


# Create your models here.

class News(models.Model):
    text = models.CharField(max_length=1000)
    pub_date = models.DateField('Publish Date')

    def __str__(self):
        return self.text[:100]


class People(models.Model):
    TITLE_CHOICES = (
        ('researcher', 'Researcher'),
        ('phd', 'PhD Student'),
        ('community', 'Star Community'),
        ('collab', 'Collaborator'),
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    description = models.CharField(max_length=200)
    web_page = models.CharField(max_length=500)
    join_date = models.DateField('Join Date')
    image = models.ImageField(upload_to='people_image', blank=True, default='people_image/default-pic.jpg')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


@receiver(models.signals.post_delete, sender=People)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image and instance.image.name != 'people_image/default-pic.jpg':
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=People)
def auto_delete_file_on_change(sender, instance, **kwargs):
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


class Software(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    introduction = models.TextField(blank=True)
    detail = models.FileField(upload_to='software_detail', blank=True)
    authors = models.ManyToManyField(People, through='SoftwareAuthors')
    pub_date = models.DateField('Publish Date')

    def __str__(self):
        return self.title


@receiver(models.signals.post_delete, sender=Software)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.detail:
        if os.path.isfile(instance.detail.path):
            os.remove(instance.detail.path)


@receiver(models.signals.pre_save, sender=Software)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Software.objects.get(pk=instance.pk).detail
    except Software.DoesNotExist:
        return False

    new_file = instance.detail
    if old_file.name != "":
        if not old_file == new_file:
            if os.path.exists(old_file.path):
                os.remove(old_file.path)


class SoftwareAuthors(models.Model):
    author = models.ForeignKey(People, on_delete=models.CASCADE)
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    order = models.IntegerField(blank=False,
                                help_text='Order of the author in software authors. Pictures will be shown in this '
                                          'order')

    class Meta:
        ordering = ['order', ]

    def __unicode__(self):
        return self.author.first_name + " " + self.author.last_name + " is a author of " + self.software.title + (
                " in position %d" % self.order)

    def __str__(self):
        return self.author.first_name + " " + self.author.last_name + " is a author of " + self.software.title + (
                " in position %d" % self.order)


class Highlight(models.Model):
    date = models.DateField()
    subject = models.CharField(max_length=1000)
    text = models.CharField(max_length=1000)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.subject


class Research(models.Model):
    title = models.CharField(max_length=1000)
    date_added = models.DateField('Date Added')

    def __str__(self):
        return self.title


class Project(models.Model):
    name = models.CharField(max_length=1000)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)


class Collaboration(models.Model):
    university = models.CharField(max_length=200)
    link = models.CharField(max_length=1000)
    researcher = models.ManyToManyField(People, through='CollaborationResearcher')
    start_date = models.DateField('Start Date')

    def __str__(self):
        return self.university


class CollaborationResearcher(models.Model):
    researcher = models.ForeignKey(People, on_delete=models.CASCADE)
    collaboration = models.ForeignKey(Collaboration, on_delete=models.CASCADE)
    field = models.CharField(max_length=200)
    start_date = models.DateField('Start Date')

    class Meta:
        ordering = ['-start_date', ]

    def __str__(self):
        return self.researcher.first_name + ' ' + self.researcher.last_name + ' started collaboration in \"' + \
               self.field + '\" since ' + str(self.start_date)
