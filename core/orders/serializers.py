from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from catalog.serializers import ProductSerializer

# --- CART SERIALIZERS ---

class CartItemSerializer(serializers.ModelSerializer):
    """ Shows individual items in the cart with full product info """
    product_details = ProductSerializer(source='product', read_only=True)
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_details', 'quantity', 'subtotal']

class CartSerializer(serializers.ModelSerializer):
    """ Shows the customer's active cart and total cost """
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']


# --- ORDER SERIALIZERS ---

class OrderItemSerializer(serializers.ModelSerializer):
    """ 
    The Vendor's view of an order. 
    Shows product name and handles status updates.
    """
    product_name = serializers.ReadOnlyField(source='product.name')
    # Helps the customer see which shop sold them the item
    vendor_shop_name = serializers.ReadOnlyField(source='vendor.username') 

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product_name', 'vendor_shop_name', 
            'quantity', 'price_at_purchase', 'status', 'updated_at'
        ]
        read_only_fields = ['price_at_purchase']

class OrderSerializer(serializers.ModelSerializer):
    """ The Customer's view of their full purchase history """
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'total_amount', 'full_name', 'address', 
            'phone', 'is_paid', 'created_at', 'order_items'
        ]


# --- CHECKOUT SERIALIZER ---

class CheckoutSerializer(serializers.Serializer):
    """ 
    A Virtual Serializer used only to capture shipping data 
    and trigger the 'Cart to Order' conversion.
    """
    full_name = serializers.CharField(max_length=255)
    address = serializers.CharField()
    phone = serializers.CharField(max_length=20)

    def validate(self, attrs):
        user = self.context['request'].user
        if not hasattr(user, 'cart') or not user.cart.items.exists():
            raise serializers.ValidationError("Your cart is empty.")
        return attrs
