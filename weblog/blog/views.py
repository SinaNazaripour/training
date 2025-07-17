from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
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
    return render(request, 'blog/post_detail.html', {"post": post})


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
