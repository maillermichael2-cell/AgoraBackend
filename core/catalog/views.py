from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# 1. Optimized List & Create View
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Optimized Query: 
        - Only active products
        - Filter by category slug if provided in URL: ?category=shoes
        - Prefetch category/vendor to reduce DB hits (N+1 problem)
        """
        queryset = Product.objects.filter(is_active=True).select_related('category', 'vendor')
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def perform_create(self, serializer):
        """
        Logic: Only users with a vendor_main profile can create products.
        The product is automatically linked to their store.
        """
        if not hasattr(self.request.user, 'vendor_main'):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You must have a Vendor profile to post products.")
        
        serializer.save(vendor=self.request.user.vendor_main)


# 2. Optimized Detail, Update & Delete View
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # Security: Only the owner (vendor) can update
        obj = self.get_object()
        if not hasattr(self.request.user, 'vendor_main') or obj.vendor != self.request.user.vendor_main:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Not authorized to edit this product.")
        serializer.save()

    def perform_destroy(self, instance):
        # Security: Only the owner (vendor) can delete
        if not hasattr(self.request.user, 'vendor_main') or instance.vendor != self.request.user.vendor_main:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Not authorized to delete this product.")
        instance.delete()


# 3. Optimized Category View (Read Only)
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
