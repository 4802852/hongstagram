from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "writer",
    )
    fields = [
        "id",
        "writer",
        "text",
    ]
    search_fields = ("id", "writer")
