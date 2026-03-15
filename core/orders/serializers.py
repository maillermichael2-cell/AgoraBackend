from rest_framework import serializers
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from catalog.serializers import ProductSerializer

# --- CART SERIALIZERS ---

class CartItemSerializer(serializers.ModelSerializer):
    """Shows individual items in the cart with full product info"""
    product_details = ProductSerializer(source='product', read_only=True)
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_details', 'quantity', 'subtotal']

class CartSerializer(serializers.ModelSerializer):
    """Shows the customer's active cart and total cost"""
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']


# --- ORDER SERIALIZERS ---

class OrderItemSerializer(serializers.ModelSerializer):
    """The Vendor's and Customer's view of a specific product in an order"""
    product_name = serializers.ReadOnlyField(source='product.name')
    # FIXED: Points to vendor.store_name instead of user.username
    vendor_shop_name = serializers.ReadOnlyField(source='vendor.store_name') 

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product_name', 'vendor_shop_name', 
            'quantity', 'price_at_purchase', 'status', 'updated_at'
        ]
        read_only_fields = ['price_at_purchase', 'status']

class OrderSerializer(serializers.ModelSerializer):
    """The Customer's view of their full purchase history"""
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'total_amount', 'full_name', 'address', 
            'phone', 'is_paid', 'created_at', 'order_items'
        ]


# --- CHECKOUT SERIALIZER (The Engine) ---

class CheckoutSerializer(serializers.Serializer):
    """
    Captures shipping data and converts Cart -> Order + OrderItems.
    """
    full_name = serializers.CharField(max_length=255)
    address = serializers.CharField()
    phone = serializers.CharField(max_length=20)

    def validate(self, attrs):
        user = self.context['request'].user
        # Check if cart exists and has items
        if not hasattr(user, 'cart') or not user.cart.items.exists():
            raise serializers.ValidationError("Your cart is empty.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        cart = user.cart

        # We use a transaction to ensure if anything fails, no partial order is created
        with transaction.atomic():
            # 1. Create the Master Order
            order = Order.objects.create(
                customer=user,
                total_amount=cart.total_price,
                full_name=validated_data['full_name'],
                address=validated_data['address'],
                phone=validated_data['phone']
            )

            # 2. Convert each CartItem into an OrderItem
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    vendor=item.product.vendor, # Automatically routes to the right store
                    quantity=item.quantity,
                    price_at_purchase=item.product.price # Locks in the price
                )

                # Optional: Decrease product stock
                # item.product.stock -= item.quantity
                # item.product.save()

            # 3. Wipe the cart clean
            cart.items.all().delete()

        return order
