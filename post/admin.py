from django.contrib import admin

from .models import Post, Photo, Comment


class PhotoInline(admin.TabularInline):
    model = Photo


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "writer", "date")
    fields = [
        "writer",
        "text",
        "hashtags",
    ]
    search_fields = ("writer", "date")
    inlines = [
        PhotoInline,
    ]


admin.site.register(Comment)
