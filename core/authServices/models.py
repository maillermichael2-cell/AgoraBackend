from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# custom user model
        # this Account  model handles who is loggin in .
class Account(AbstractUser):
    # main auth model this handles : username, password email, and the role.
    class Role(models.TextChoices) :
        Vendor = 'VENDOR', 'vendor'
        Customer = 'CUSTOMER', 'customer'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.Customer)
    email = models.EmailField(unique=True)

# this is the vendor profile model
class VendorProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='vendor_profile') 
    country = models.CharField(max_length=100)
    business_name = models.CharField(max_length=255)
    business_address = models.CharField(max_length=350)
    is_registered = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.business_name}'
    
class CustomerProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='customer_profile')
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.full_name}'
