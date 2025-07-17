from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.transaction import commit
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation.trans_null import activate
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .models import Post, Ticket
from .forms import *


# Create your views here.
def index(request):
    context = {}
    return render(request, "blog/index.html", context)


def post_list(request):
    posts = Post.publish.all()
    paginator = Paginator(posts, 4)
    num_pages = request.GET.get('page')
    try:
        posts = paginator.get_page(num_pages)
    except EmptyPage:
        posts = paginator.get_page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.get_page(1)

    return render(request, "blog/post_list.html", {"posts": posts})


# class PostListView(ListView):
#     context_object_name = "posts"
#     template_name = 'blog/post_list.html'
#     model = Post
#     paginate_by = 2

def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    comments=post.comments.filter(activation=True)
    form=CommentForm()
    context={
        "post": post,
        "form":form,
        "comments":comments
    }
    return render(request, 'blog/post_detail.html', context)


def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj = Ticket.objects.create(author_name=cd["author_name"], title=cd["title"], body=cd["body"],
                                               author_email=cd["author_email"])
            return redirect("blog:index")
    else:
        form = TicketForm()
    return render(request, "forms/ticket.html", {"form": form})

@login_required
@require_POST
def comment(request,id):
    post=get_object_or_404(Post,id=id,status=Post.Status.PUBLISHED)
    comment_obj=None
    form=CommentForm(request.POST)
    if form.is_valid():
        comment_obj=form.save(commit=False)
        comment_obj.name=request.user
        comment_obj.post=post
        comment_obj.save()
    context={
        "post":post,
        "comment":comment_obj,
        "form":form
    }
    return render(request,"forms/comment.html",context)

