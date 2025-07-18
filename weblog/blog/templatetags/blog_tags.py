from django import template
from django.db.models import Avg,Count,Max,Min,Sum
from django.utils.safestring import mark_safe
from django.utils.timezone import activate
from markdown import markdown

from ..models import *

register=template.Library()
@register.inclusion_tag("partials/latest_posts.html",name="latest_p")
def latest_posts(count=3):
    l_posts=Post.publish.order_by("-published")[:count]
    context={
        "l_posts":l_posts
    }
    return context

@register.simple_tag(name="count_of_comments")
def comments_counter():
    return Comment.objects.filter(activation=True).count()

@register.simple_tag(name="count_of_posts")
def total_posts():
    return Post.publish.count()

@register.simple_tag(name="sum_of_reading")
def total_time():
    return Post.publish.aggregate(Sum("reading_time"))['reading_time__sum']

@register.simple_tag(name="most_pop_posts")
def pop_posts(count=3):
    return Post.publish.annotate(comment_count=Count("comments")).order_by("-comment_count")[:count]

@register.filter(name="markdown")
def to_markdown(text):
    return mark_safe(markdown(text))