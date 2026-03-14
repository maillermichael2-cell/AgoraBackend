from django.urls import path
from .views import VendorProfileView, VendorCreateView, VendorListView

urlpatterns = [
    path('all/', VendorListView.as_view(), name='vendor-list'),
    path('register/', VendorCreateView.as_view(), name='vendor-register'),
    path('profile/', VendorProfileView.as_view(), name='vendor-profile'),
]
