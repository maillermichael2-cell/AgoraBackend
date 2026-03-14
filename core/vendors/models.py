from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.
def vendor_upload_path(instance, filename):
    return f'vendors/{instance.slug}/{filename}'

class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_main')
    store_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    logo = models.ImageField(upload_to=vendor_upload_path, null=True, blank=True)
    banner = models.ImageField(upload_to=vendor_upload_path, null=True, blank=True)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta :
        ordering = ['created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.store_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.store_name
        
