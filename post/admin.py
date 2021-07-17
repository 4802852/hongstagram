from django.contrib import admin

from .models import Post, Photo


class PhotoInline(admin.TabularInline):
    model = Photo


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("writer",)
    fields = [
        "writer",
        "text",
    ]
    search_fields = ("writer", "text")
    inlines = [
        PhotoInline,
    ]
