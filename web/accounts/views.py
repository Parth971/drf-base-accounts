from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User

from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import LoginSerializer, RegisterSerializer, ForgotPasswordSerializer, ChangePasswordSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # send_forgot_password_email()
        return Response(data={'message': 'Restore password link has been sent to email.'}, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    lookup_url_kwarg = 'user_id'
