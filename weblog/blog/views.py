
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib import messages
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank,TrigramSimilarity
from django.views.generic import ListView

from .models import Post, Ticket,Image
from .forms import *


# Create your views here.
def index(request):
    context = {"phrase":"**reza**"}
    return render(request, "blog/index.html", context)


def post_list(request):
    posts = Post.publish.all()
    paginator = Paginator(posts, 3)
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
            messages.success(request, "پست با موفقیت ارسال شد!")
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
    messages.success(request,"کامنت در انتظار تایید")
    return redirect("blog:post_detail",post.id)

@login_required
def add_post(request):
    if request.method=="POST":
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post_obj=form.save(commit=False)
            post_obj.author=request.user
            post_obj.save()
            Image.objects.create(post=post_obj,image_file=form.cleaned_data['image'],description=post_obj.description[:10])

            messages.success(request, "پست با موفقیت ارسال شد!")
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
            # serach_query=SearchQuery(query)
            # vector=SearchVector('title',weight='A')+SearchVector('description',weight='B')+\
            #     SearchVector('slug',weight='C')
            # rank=SearchRank(vector,serach_query)
            # results=Post.publish.annotate(vector=vector,rank=rank).filter(rank__gt=.1).order_by('-rank')
            result1=Post.publish.annotate(similarity=TrigramSimilarity('title',query)).filter(similarity__gt=.1)
            result2=Post.publish.annotate(similarity=TrigramSimilarity('description',query)).filter(similarity__gt=.1)
            result3=Post.publish.annotate(similarity=TrigramSimilarity('images__title',query)).filter(similarity__gt=.1)
            results=(result1|result2|result3).order_by('-similarity')
    context={
        "results":results,
         "query":query
        }
    return render(request, "blog/search.html", context)

def profile(request):
    user=request.user
    posts=Post.publish.filter(author=user)
    context={
        'posts':posts,
        'user':user
    }
    return render(request,'blog/profile.html',context)

def delete_post(request,id):
    post=get_object_or_404(Post,id=id)
    if request.method=='POST':
        post.delete()
        messages.success(request,"پست با موفقیت حذف شد")
        return redirect('blog:profile')

    return render(request,'forms/delete_post.html',{'post':post})

def edit_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post=form.save()
            Image.objects.create(post=post,image_file=form.cleaned_data['image'],description=post.description[:10])
            return redirect('blog:profile')
    else:
        form=PostForm(instance=post)
    return render(request,'forms/add_post.html',{'form':form,'post':post})

def delete_image(request,image_id,post_id):
    image=get_object_or_404(Image,id=image_id)
    image.delete()
    return redirect('blog:edit_post',post_id)