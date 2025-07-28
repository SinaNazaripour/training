from django import template
from django.db.models import Avg,Count,Max,Min,Sum
from django.utils.safestring import mark_safe
from django.utils.timezone import activate
from markdown import markdown

from ..models import *

register=template.Library()
@register.inclusion_tag("partials/latest_posts.html",name="latest_posts")
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

@register.simple_tag(name="most_active_users")
def best_users(count=3):
    return User.objects.annotate(posts_count=Count("posts")).order_by("-posts")[:count]

@register.filter(name="markdown")
def to_markdown(text):
    return mark_safe(markdown(text))

@register.filter(name="bold")
def bold(text):
    return mark_safe(markdown(f"**{text}**"))

@register.simple_tag(name="comments_of_this_post")
def comment_counter(id):
    post=Post.objects.filter(id=id)[0]
    comments=post.comments.filter(activation=True)
    return comments.count()
# to have messages anywhere
@register.inclusion_tag("partials/message.html",name="show_messages")
def message(messages):
    return {
        "messages": messages
    }

