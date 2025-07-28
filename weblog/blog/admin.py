

from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter

from .models import Post, Ticket, Comment,Image

admin.sites.AdminSite.site_header =" هدر "
admin.sites.AdminSite.site_title ="پنل مدیریت تایتل سایت"
admin.sites.AdminSite.index_title ="پنل مدیریت تایتل ایندکس "
# inlines
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0



# Register your models here.
@admin.register(Post)
class PostAmin(admin.ModelAdmin):
    list_display = ["author","title","status","published"]
    ordering = ["published","title","author"]
    list_filter =["status",("published",JDateFieldListFilter),"author"]
    search_fields = ["title","description"]
    list_editable = ["status"]
    raw_id_fields = ["author"]
    prepopulated_fields = {'slug':['title']}
    list_display_links = ["title"]
    inlines = [
        CommentInline,
        ImageInline
    ]



@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["author_name", "title", "date"]
    list_display_links = ["title"]
    search_fields = ["title", "body"]
    ordering = ["-date"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "body", "created","post","activation"]
    list_display_links = ["name"]
    search_fields = ["name", "body"]
    ordering = ["-created"]
    list_filter = [("created",JDateFieldListFilter),'activation']
    list_editable = ["activation"]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "created", "post"]
    list_display_links = ["title"]
    ordering = ["-created"]
    list_filter = [("created", JDateFieldListFilter)]
