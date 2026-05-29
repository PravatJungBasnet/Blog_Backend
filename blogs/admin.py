# Register your models here.
from django.contrib import admin
from .models import Blog, Like


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "status"]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["blog", "user", "is_liked"]
