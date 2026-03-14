from django.urls import path
from .views import ProductListCreateView, ProductDetailView, CategoryListView

urlpatterns = [
    # Get all products or POST a new one: /api/products/
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    
    # Get, Update, or Delete a specific product: /api/products/1/
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    
    # Get all categories: /api/categories/
    path('categories/', CategoryListView.as_view(), name='category-list'),
]
