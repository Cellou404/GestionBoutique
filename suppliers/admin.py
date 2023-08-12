from django.contrib import admin
from .models import Suppliers

# Register your models here.
@admin.register(Suppliers)

class Admin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'address', 'town', 'date_created']
    list_display_links = ['name', 'email']
    list_filter = ['town', 'address']
    search_fields = ['name', 'email', 'address', 'town']
    
