import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Post

@receiver(post_delete,sender=Post)
def delete_image_file(sender,instance,**kwargs):
    for fiels in
