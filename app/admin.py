from django.contrib import admin
from django.utils.translation import gettext_lazy
from . import models


admin.site.register(models.NewsItem)
admin.site.register(models.Staff)
admin.site.register(models.Publication)
admin.site.register(models.Tag)

admin.site.site_header = gettext_lazy('Laboratory №52 Admin Page')
admin.site.site_title = gettext_lazy('Laboratory №52 Admin Page')
admin.site.index_title = gettext_lazy('Laboratory №52 Admin Page')
