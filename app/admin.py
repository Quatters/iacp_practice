from django.contrib import admin
from . import models


admin.site.register(models.NewsItem)
admin.site.register(models.Staff)
admin.site.register(models.Publication)
admin.site.register(models.Tag)
