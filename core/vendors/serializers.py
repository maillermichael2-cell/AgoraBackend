from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ['slug', 'user']
