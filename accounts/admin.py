from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile
from django.utils.html import format_html
from django.contrib.sessions.models import Session
# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'username')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        try:
            return format_html('<img src="{}" style="border-radius: 50%;" width="30px">'.format(object.profile_picture.url))
        except:
            None
    thumbnail.short_description = 'Profile Picture'

    list_display = ('thumbnail','user', 'state', 'city','country')
    list_display_links = ('thumbnail', 'user')

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ('session_key', '_session_data', 'expire_date')

admin.site.register(Session, SessionAdmin)