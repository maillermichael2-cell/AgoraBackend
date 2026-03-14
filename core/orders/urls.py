from django.urls import path
from .views import (
    CartView, 
    AddToCartView, 
    RemoveFromCartView,
    CheckoutView, 
    CustomerOrderHistoryView, 
    VendorOrdersView,
    VendorUpdateStatusView
)

urlpatterns = [
    # --- CART ENDPOINTS ---
    # View my current cart
    path('cart/', CartView.as_view(), name='cart-view'),
    # Add a product to cart (requires product_id and quantity)
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    # Remove an item from cart
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='cart-remove'),

    # --- CHECKOUT & HISTORY ---
    # Convert Cart to Order (The multi-vendor splitting happens here)
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    # Customer viewing their own past orders
    path('history/', CustomerOrderHistoryView.as_view(), name='order-history'),

    # --- VENDOR ENDPOINTS ---
    # Vendor viewing only the items they need to ship
    path('vendor/orders/', VendorOrdersView.as_view(), name='vendor-orders'),
    # Vendor updating status (e.g., changing 'Pending' to 'Shipped')
    path('vendor/order-item/<int:pk>/update/', VendorUpdateStatusView.as_view(), name='vendor-status-update'),
]
