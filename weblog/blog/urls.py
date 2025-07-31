from django.urls import path
from . import  views
from django.contrib.auth import views as auth_views
# from.views import PostListView
app_name ="blog"
urlpatterns=[
    path('',views.index,name="index"),
    path('posts/',views.post_list,name='post_list'),
    # path('posts/',PostListView.as_view(),name='post_list'),
    path('posts/<int:id>',views.post_detail,name='post_detail'),
    path('profile/ticket/',views.ticket,name="ticket"),
    path('posts/<int:id>/comment/',views.comment,name="comment"),
    path('profile/add_post',views.add_post,name="add_post"),
    path('search/',views.search,name='search'),
    path('profile/',views.profile,name='profile'),
    path('profile/delete_post/<int:id>',views.delete_post,name='delete_post'),
    path('profile/edit_post/<int:post_id>',views.edit_post,name='edit_post'),
    path('profile/delete_image/<image_id>/<post_id>',views.delete_image,name='delete_image'),
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),

]
