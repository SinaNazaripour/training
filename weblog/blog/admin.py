
from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter

from .models import Post
admin.sites.AdminSite.site_header =" هدر "
admin.sites.AdminSite.site_title ="پنل مدیریت تایتل سایت"
admin.sites.AdminSite.index_title ="پنل مدیریت تایتل ایندکس "

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
