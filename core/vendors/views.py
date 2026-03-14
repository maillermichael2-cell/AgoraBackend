from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Vendor
from .serializers import VendorSerializer
from django.shortcuts import get_object_or_404

# Create your views here.


class VendorProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or Update the logged-in user's vendor profile.
    URL: /api/vendor/profile/
    """
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Returns the vendor profile tied to the logged-in user
        return get_object_or_404(Vendor, user=self.request.user)

class VendorCreateView(generics.CreateAPIView):
    """
    Create a new Vendor profile for the logged-in user.
    """
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Check if they already have a vendor profile
        if Vendor.objects.filter(user=self.request.user).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError("You already have a vendor profile.")
        
        serializer.save(user=self.request.user)

class VendorListView(generics.ListAPIView):
    """
    Public list of all vendors (for customers to browse stores).
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.AllowAny]
