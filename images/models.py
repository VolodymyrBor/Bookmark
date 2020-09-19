from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify


class Image(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)

    # foreign keys
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='image_created', on_delete=models.CASCADE)

    # many to many
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            self.slug = slugify(self.title)
            super().save(force_insert, force_update, using, update_fields)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
