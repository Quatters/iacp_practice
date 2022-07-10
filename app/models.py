from django.db import models
from ckeditor.fields import RichTextField


class Article(models.Model):
    name = models.CharField(max_length=256)
    contents = RichTextField()
    thumbnail = models.ImageField(blank=True, default='', upload_to='thumbnails/')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
