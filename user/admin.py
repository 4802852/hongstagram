from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'mobile_number',
        'full_name',
        'created_at',
        'introduction',
    )
    search_fields = ('email', 'mobile_number', 'username')

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
