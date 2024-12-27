from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Content(models.Model):
    title = models.TextField(max_length=300)

    class Meta:
        abstract = True


class Anime(Content):
    title_rus = models.TextField(max_length=300, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    img = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    season = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.title


class Movie(Content):
    rating = models.TextField(null=True, blank=True)
    img = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    year = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Manga(Content):
    rating = models.FloatField(null=True, blank=True)
    img = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Book(Content):
    rating = models.TextField(null=True, blank=True)
    img = models.TextField(null=True, blank=True)
    author = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title


class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    rating = models.IntegerField(null=True, blank=True)
    note = models.TextField(max_length=300, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.user:
            self.user = kwargs.get('user')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.content_object.title}'

    class Meta:
        verbose_name = 'List'






