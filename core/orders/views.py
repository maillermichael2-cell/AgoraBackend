from django.db import transaction
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, OrderSerializer, CheckoutSerializer, OrderItemSerializer

# --- CART VIEWS ---

class CartView(generics.RetrieveAPIView):
    """View current user's cart"""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartView(APIView):
    """Add or update item in cart"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        return Response({"message": "Added to cart"}, status=status.HTTP_201_CREATED)


class RemoveFromCartView(generics.DestroyAPIView):
    """
    Deletes a specific CartItem.
    URL: /api/orders/cart/remove/<int:item_id>/
    """
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'item_id'

    def get_queryset(self):
        # SECURITY: Only allow the user to delete items from THEIR cart
        return CartItem.objects.filter(cart__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
        return response

# --- CHECKOUT LOGIC (THE SPLITTING) ---

class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            cart = request.user.cart
            
            # 1. Create the Parent Order
            order = Order.objects.create(
                customer=request.user,
                total_amount=cart.total_price,
                full_name=serializer.validated_data['full_name'],
                address=serializer.validated_data['address'],
                phone=serializer.validated_data['phone']
            )

            # 2. Split CartItems into OrderItems for each Vendor
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    vendor=item.product.vendor, # Extract vendor from product
                    quantity=item.quantity,
                    price_at_purchase=item.product.price
                )
                
                # Optional: Reduce stock level
                item.product.stock -= item.quantity
                item.product.save()

            # 3. Clear the Cart
            cart.items.all().delete()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- VENDOR & CUSTOMER HISTORY ---

class CustomerOrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-created_at')

class VendorOrdersView(generics.ListAPIView):
    """Only shows items belonging to the logged-in vendor"""
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(vendor=self.request.user).order_by('-updated_at')

class VendorUpdateStatusView(generics.UpdateAPIView):
    """Vendor updates the shipping status of an item"""
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(vendor=self.request.user)
