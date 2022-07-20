from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


class Tag(models.Model):
    name = models.CharField(max_length=64, db_index=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_name')
        ]

    def __str__(self):
        return self.name


class NewsItem(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    contents = RichTextField(db_index=True)
    thumbnail = models.ImageField(blank=True, default=None, upload_to='thumbnails/')
    created_at = models.DateField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, default=None)

    class Meta:
        ordering = ['-id', 'name']

    def __str__(self):
        return self.name


class Publisher(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    patr = models.CharField(max_length=128, blank=True, null=True, default=None)
    info = models.TextField(blank=True, null=True, default=None)
    photo = models.ImageField(blank=True, null=True, default=None, upload_to='publisher_photos/')

    @property
    def full_name(self):
        if not self.user.first_name or not self.user.last_name:
            return ''
        name = f'{self.user.last_name} {self.user.first_name}'
        if self.patr:
            name += f' {self.patr}'
        return name

    @property
    def short_name(self):
        if not self.user.first_name or not self.user.last_name:
            return ''
        name = f'{self.user.last_name} {self.user.first_name[0].capitalize()}.'
        if self.patr:
            name += f' {self.patr[0].capitalize()}.'
        return name

    def __str__(self):
        return self.short_name


class Publication(models.Model):
    name = models.TextField(db_index=True)
    authors = models.ManyToManyField(Publisher, db_index=True)
    edition = models.TextField()
    publication_date = models.DateField()
    contents = RichTextField()
    volume = models.CharField(max_length=64, blank=True, null=True, default=None)
    no = models.PositiveIntegerField(blank=True, null=True, default=None, help_text='№ of publication')
    pages = models.CharField(max_length=32, blank=True, null=True, default=None, help_text='Format: x-y (from x to y)')
    doi_link = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        default=None,
        help_text='Link to publication in doi.org'
    )

    class Meta:
        ordering = ['-id', 'name']

    def __str__(self):
        return self.name
