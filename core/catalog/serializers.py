from rest_framework import serializers
from .models import Product, Category
from vendors.models import Vendor


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer) :
    # 'category' return the ID by default.
    # use CategorySerializers to show nested details to customer
    category_details = CategorySerializer(source='category',read_only=True)
    # show the vendor`s bussiness name instead of just User ID
    vendor_name = serializers.ReadOnlyField(source='vendor.store_name')
    class Meta :
        model = Product
        fields = '__all__'
        # we allow the 'vendor read_only cus we will set it automatically in the view based on the logged in user
        read_only_fields = ['slug','vendor']
    
    # we validate the price (price should not be less than zero)
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than zero')
        return value