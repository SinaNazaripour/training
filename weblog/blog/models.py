from django.urls import reverse
from django.utils import timezone
from django_jalali.db import models as jmodels
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
   author=models.ForeignKey(User,related_name="posts",on_delete=models.CASCADE)
   title = models.CharField(max_length=12)
   description = models.TextField()
   reading_time=models.PositiveIntegerField(default=3)
   slug = models.SlugField(max_length=30)
   class Status(models.TextChoices):
       DRAFT="DR","Draft"
       PUBLISHED="PB","Published"
       REJECTED="RJ","Rejected"
   status =models.CharField(choices=Status.choices,default=Status.DRAFT)
   # managers
   objects = jmodels.jManager()
   publish=PublishManager()

   # dates
   published = jmodels.jDateTimeField(default=timezone.now())
   created = jmodels.jDateTimeField(auto_now_add=True)
   updated = jmodels.jDateTimeField(auto_now=True)


   class Meta:
       ordering=["-published"]
       indexes=[models.Index(fields=['-published'])]
       # فارسی سازی
       verbose_name = "پست"
       verbose_name_plural = "پست ها"

   def __str__(self):
       return self.title

   def get_absolute_url(self):
       return reverse('blog:post_detail',args=[self.id])

class Ticket(models.Model):
    author_name=models.CharField(max_length=30)
    author_email=models.EmailField()
    title=models.CharField(max_length=30)
    body=models.TextField(max_length=30)
    date = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        indexes = [models.Index(fields=['-date'])]
        # فارسی سازی
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"