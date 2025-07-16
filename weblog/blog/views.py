from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def index(request):
    context={}
    return render(request,"blog/index.html",context)

def post_list(request):
    posts = Post.publish.all()
    return render(request,"blog/post_list.html",{"posts":posts})

def post_detail(request,id):
    post = get_object_or_404(Post,id =id ,status =Post.Status.PUBLISHED)
    return render(request,'blog/post_detail.html',{"post":post})