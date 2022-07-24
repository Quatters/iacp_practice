from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy, pgettext_lazy


class Tag(models.Model):
    name = models.CharField(max_length=64, db_index=True, verbose_name=pgettext_lazy('lifeless', 'name'))

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_name')
        ]
        verbose_name = gettext_lazy('tag')
        verbose_name_plural = gettext_lazy('tags')

    def __str__(self):
        return self.name


class NewsItem(models.Model):
    name = models.CharField(max_length=256, db_index=True, verbose_name=pgettext_lazy('lifeless', 'name'))
    contents = RichTextField(db_index=True, verbose_name=gettext_lazy('contents'))
    thumbnail = models.ImageField(
        blank=True,
        default=None,
        upload_to='thumbnails/',
        verbose_name=gettext_lazy('thumbnail')
    )
    created_at = models.DateField(auto_now_add=True, verbose_name=gettext_lazy('created at'))
    is_public = models.BooleanField(
        default=False,
        help_text=pgettext_lazy(
            'one news',
            'If set, news will be visible on the main site. Otherwise it will be visible only on the admin page.'
        ),
        verbose_name=gettext_lazy('is public')
    )
    tags = models.ManyToManyField(Tag, blank=True, default=None, verbose_name=gettext_lazy('tags'))
    is_archived = models.BooleanField(default=False, verbose_name=pgettext_lazy('one news', 'is archived'))

    class Meta:
        ordering = ['-id', 'name']
        verbose_name = pgettext_lazy('one', 'news')
        verbose_name_plural = gettext_lazy('news')

    def __str__(self):
        return self.name


class Staff(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name=gettext_lazy('user'))
    patr = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        default=None,
        verbose_name=gettext_lazy('patronymic')
    )
    info = models.TextField(blank=True, null=True, default=None, verbose_name=gettext_lazy('info'))
    photo = models.ImageField(
        blank=True,
        null=True,
        default=None,
        upload_to='publisher_photos/',
        verbose_name=gettext_lazy('photo')
    )

    class Meta:
        verbose_name = pgettext_lazy('one', 'staff')
        verbose_name_plural = gettext_lazy('staff')

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
    MAGAZINE_ARTICLE = 'MAGAZINE_ARTICLE'
    CHAPTER = 'CHAPTER'
    REPORT = 'REPORT'
    BOOK = 'BOOK'
    PATENT = 'PATENT'
    THESIS = 'THESIS'

    TYPES = (
        (MAGAZINE_ARTICLE, gettext_lazy('Magazine article')),
        (CHAPTER, gettext_lazy('Article collection/chapter')),
        (REPORT, gettext_lazy('Report')),
        (BOOK, gettext_lazy('Book/monograph')),
        (PATENT, gettext_lazy('Patent')),
        (THESIS, gettext_lazy('Thesis'))
    )

    name = models.TextField(db_index=True, verbose_name=pgettext_lazy('lifeless', 'name'))
    staff_authors = models.ManyToManyField(Staff, db_index=True, verbose_name=gettext_lazy('authors (staff)'))
    other_authors = models.TextField(
        verbose_name=gettext_lazy('other authors'),
        db_index=True,
        null=True,
        blank=True,
        default=None,
        help_text=gettext_lazy('One author per line')
    )
    year = models.IntegerField(db_index=True, verbose_name=gettext_lazy('year'))
    type = models.CharField(
        db_index=True,
        verbose_name=gettext_lazy('publication type'),
        choices=TYPES,
        max_length=32
    )
    annotation = RichTextField(verbose_name=gettext_lazy('annotation'))
    pages = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        default=None,
        help_text=gettext_lazy('Format: x-y (from x to y)'),
        verbose_name=gettext_lazy('pages'),
    )
    volume = models.CharField(max_length=32, verbose_name=gettext_lazy('volume'), null=True, blank=True, default=None)
    link = models.CharField(
        max_length=512,
        help_text=gettext_lazy('Link to publication in doi.org'),
        verbose_name=gettext_lazy('link'),
        null=True,
        blank=True,
        default=None
    )

    @property
    def other_authors_list(self):
        if self.other_authors is None:
            return []
        other_authors = self.other_authors.strip().split('\n')
        return list(filter(lambda x: x != '' and x != '\r', other_authors))

    class Meta:
        ordering = ['-id', 'name']
        verbose_name = gettext_lazy('publication')
        verbose_name_plural = gettext_lazy('publications')

    def __str__(self):
        return self.name
