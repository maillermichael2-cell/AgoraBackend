from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import VendorRegistrationSerializer, CustomerRegistrationSerializer, MyTokenObtainPairSerializers
from rest_framework_simplejwt.views import TokenObtainPairView

# vendor registration view logic
class VendorRegistrationView(generics.CreateAPIView):
    serializer_class = VendorRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # getting the serialized data
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": "success",
            "message": "Vendor account created, please log in to continue"
        },status=status.HTTP_201_CREATED)


class CustomerRegistrationView(generics.CreateAPIView):
    serializer_class = CustomerRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # getting the serialized data
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": "success",
            "message": "Cuatomer account created, please log in to continue"
        },status=status.HTTP_201_CREATED)

#login view 
class LoginView(TokenObtainPairView) :
    serializer_class = MyTokenObtainPairSerializers
    permission_classes = [AllowAny]