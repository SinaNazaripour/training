from django.urls import path
from . import  views
# from.views import PostListView
app_name ="blog"
urlpatterns=[
    path('',views.index,name="index"),
    path('posts/',views.post_list,name='post_list'),
    # path('posts/',PostListView.as_view(),name='post_list'),
    path('posts/<int:id>',views.post_detail,name='post_detail'),
    path('ticket/',views.ticket,name="ticket"),
    path('posts/<int:id>/comment/',views.comment,name="comment")

]