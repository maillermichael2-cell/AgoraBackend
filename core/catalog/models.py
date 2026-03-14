from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid
from vendors.models import Vendor

# Create your models here.

def category_image_path(instance, filename):
    return f'categories/{instance.slug}/{filename}'

def product_image_path(instance, filename):
    vendor_slug = instance.vendor.slug if instance.vendor else 'no-vendor'
    return f'products/{vendor_slug}/{filename}'

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True) # this is for clean URLS like eg /category/electronics/
    image = models.ImageField(upload_to=category_image_path, null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories" 
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
           
    def __str__(self):
        return self.name



class Product(models.Model) :
    # this vendor helps that every product must be owned by a vendor , then it can delete all products if vendor delets their account
    # the related_name allows us to get all products of a vendor usin uer.products.all()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    # this links the category model to the products
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=300,unique=True, blank=True, null=True)
    description = models.TextField(default='')

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_Price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to=product_image_path, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta :
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
        ]


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = f'{base_slug}-{str(uuid.uuid4())[:8]}'
        super().save(*args, **kwargs)


    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        vendor_name = self.vendor.store_name if self.vendor else "No Vendor"
        return f"{self.name} by {vendor_name}"
