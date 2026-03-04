from django.contrib import admin
from .models import Account, VendorProfile, CustomerProfile

# Register your models here.

admin.site.register(Account)
admin.site.register(VendorProfile)
admin.site.register(CustomerProfile)
