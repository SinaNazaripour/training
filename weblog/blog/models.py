import os.path
from pathlib import Path

from django.template.defaultfilters import slugify
from jdatetime import datetime as jdate
from django.db.models import ImageField
from django.urls import reverse
from django.utils import timezone
from django_jalali.db import models as jmodels
from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField


# Create your models here.
class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    reading_time = models.PositiveIntegerField(default=3)
    slug = models.SlugField(max_length=30)

    class Status(models.TextChoices):
        DRAFT = "DR", "Draft"
        PUBLISHED = "PB", "Published"
        REJECTED = "RJ", "Rejected"

    status = models.CharField(choices=Status.choices, default=Status.DRAFT)
    # managers
    objects = jmodels.jManager()
    publish = PublishManager()
    # dates
    published = jmodels.jDateTimeField(default=timezone.now())
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published"]
        indexes = [models.Index(fields=['-published'])]
        # فارسی سازی
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage, img.image_file.path
            storage.delete(path)
        super().delete(*args,**kwargs)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=120, null=True, blank=True, verbose_name='موضوع')
    description = models.TextField(max_length=120, null=True, blank=True, verbose_name='توضیحات')
    created = jmodels.jDateTimeField(auto_now_add=True)
    folder_name = str(jdate.now())[:10]
    image_file = ResizedImageField(upload_to=folder_name, quality=75, size=[500, 500], crop=['middle', 'center'])

    def save(self, *args, **kwargs):
        if self.image_file and not self.title:
            self.title = os.path.splitext(os.path.basename(self.image_file.name))[0]
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=['-created'])]
        # فارسی سازی
        verbose_name = "تصویر"
        verbose_name_plural = "تصویر ها"

    def __str__(self):
        return self.title


class Ticket(models.Model):
    author_name = models.CharField(max_length=30)
    author_email = models.EmailField()
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=30)
    date = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        indexes = [models.Index(fields=['-date'])]
        # فارسی سازی
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=30)
    body = models.CharField(max_length=300)
    activation = models.BooleanField(default=False)
    # date
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created"])]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f" written by {self.name} : {self.body}"
