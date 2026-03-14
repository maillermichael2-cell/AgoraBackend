from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import (VendorRegistrationView, CustomerRegistrationView, LoginView)

urlpatterns = [
    # Registration Endpoints
    path('register/vendor/', VendorRegistrationView.as_view(), name='vendor-register'),
    path('register/customer/',CustomerRegistrationView.as_view(), name='customer-register'),
    
    # Login & Token Management
    path('login/', LoginView.as_view(), name='login'),
    

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name= 'token_refresh'),
    
    # CRITICAL: This allows React to get a new access token using the refresh token
    path('login/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
]
