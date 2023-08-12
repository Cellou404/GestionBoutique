from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    list_display_links = ['username', 'email']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_per_page = 20
