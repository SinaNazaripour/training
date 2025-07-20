
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .models import Post, Ticket
from .forms import *


# Create your views here.
def index(request):
    context = {"phrase":"**reza**"}
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

@login_required
def add_post(request):
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            post_obj=form.save(commit=False)
            post_obj.author=request.user
            post_obj.save()
            return redirect('blog:post_list')
    else:
        form=PostForm()
    return render(request,"forms/add_post.html",{"form":form})

def search(request):
    query,results=None,[]
    if 'query' in request.GET:
        form=Search(data=request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            results=Post.publish.filter(description__contains=query)
    context={
        "results":results,
         "query":query
        }
    return render(request, "blog/search.html", context)