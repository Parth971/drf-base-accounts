from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from accounts.models import User

from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import LoginSerializer, RegisterSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
