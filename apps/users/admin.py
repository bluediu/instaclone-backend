# Libs
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Apps
from apps.users.models.user import User

# Admin panel customization
admin.site.site_title = "Admin"
admin.site.site_header = "Instaclone Administration"
admin.site.index_title = "Instaclone"


@admin.register(User)
class ModelNameAdmin(BaseUserAdmin):
    """Register user admin."""
