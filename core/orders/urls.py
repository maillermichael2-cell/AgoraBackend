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
    # --- CUSTOMER CART ---
    # GET: View my current items and total price
    path('cart/', CartView.as_view(), name='cart-view'),
    
    # POST: Add product_id and quantity to my cart
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    
    # DELETE: Remove a specific row from my cart using the CartItem ID
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='cart-remove'),

    # --- CHECKOUT & PERSONAL HISTORY ---
    # POST: Submit shipping details to convert Cart -> Order + split by Vendor
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    
    # GET: List of all full orders I have placed
    path('history/', CustomerOrderHistoryView.as_view(), name='order-history'),

    # --- VENDOR DASHBOARD ---
    # GET: List of specific product items sold by the logged-in vendor
    path('vendor/orders/', VendorOrdersView.as_view(), name='vendor-orders'),
    
    # PATCH/PUT: Update status (e.g., 'SHIPPED') for a specific item I sold
    path('vendor/order-item/<int:pk>/update/', VendorUpdateStatusView.as_view(), name='vendor-status-update'),
]
