from django.contrib.auth.models import AbstractUser, Group as DjangoGroup
from django.db import models
from django.utils.translation import gettext_lazy


class User(AbstractUser):
    patr = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        default=None,
        verbose_name=gettext_lazy('patronymic')
    )

    def get_full_name(self):
        if not self.first_name or not self.last_name:
            return self.username
        if not self.patr:
            return f'{self.first_name} {self.last_name}'
        return f'{self.last_name} {self.first_name} {self.patr}'

    def get_short_name(self):
        if not self.first_name or not self.last_name:
            return self.username
        if not self.patr:
            return f'{self.first_name} {self.last_name[0]}.'
        return f'{self.last_name} {self.first_name[0]}. {self.patr[0]}.'

    def __str__(self):
        return self.get_short_name()


class Group(DjangoGroup):
    class Meta:
        verbose_name = gettext_lazy("group")
        verbose_name_plural = gettext_lazy("groups")

