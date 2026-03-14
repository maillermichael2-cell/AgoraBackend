from django.contrib import admin
from .models import Vendor

# Register your models here.

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'store_name', 'slug', 'created_at')
    search_fields = ('store_name',)
    prepopulated_fields = {'slug' : ('store_name',)}
