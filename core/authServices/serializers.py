from rest_framework import serializers
from django.db import transaction
from .models import Account, VendorProfile, CustomerProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# vendor registration serializer
class VendorRegistrationSerializer(serializers.ModelSerializer) :
    # this are the fields we are collecting from the frontend 
    country = serializers.CharField(write_only=True)
    business_name = serializers.CharField(write_only=True)
    is_registered = serializers.BooleanField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    business_address = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('username', 'email', 'password', 'country', 'business_name',
                  'is_registered', 'phone_number', 'business_address'
        )
        extra_kwargs = {'password': {"write_only": True}}

    """
        this transaction ensures if the profile creation fails (db error,networkerr)
        the user account isint created either. it prevent 'ghost users'
    """
    @transaction.atomic
    def create(self, validated_data):
        #pop profile data out
        profile_data = {
            'country': validated_data.pop('country'),
            'business_name': validated_data.pop('business_name'),
            'is_registered': validated_data.pop('is_registered'),
            'phone_number': validated_data.pop('phone_number'),
            'business_address': validated_data.pop('business_address'),
        }
        #create user with vendor role
        user = Account.objects.create_user(**validated_data, role=Account.Role.Vendor)
        #create profile
        VendorProfile.objects.create(user=user, **profile_data)
        return user
    

# customer registration seralizer
class CustomerRegistrationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    location = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('username', 'email', 'password', 'full_name', 'phone_number','location')
        extra_kwargs = {'password': {'write_only': True}}

    """
        this transaction ensures if the profile creation fails (db error,networkerr)
        the user account isint created either. it prevent 'ghost users'
    """
    @transaction.atomic
    def create(self, validated_data):
        profile_data = {
            'full_name': validated_data.pop('full_name'),
            'phone_number': validated_data.pop('phone_number'),
            'location': validated_data.pop('location',)
        }
        user = Account.objects.create_user(**validated_data, role=Account.Role.Customer)
        CustomerProfile.objects.create(user=user, **profile_data)
        return user

# login serializer
class MyTokenObtainPairSerializers(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        #add custom fields to the response (profile info to response)
        data['role'] = self.user.role
        data['username'] = self.user.username

        if self.user.role == 'VENDOR':
            data['profile_id'] = self.user.vendor_profile.id
        else:
            data['profile_id'] = self.user.customer_profile.id

        return data