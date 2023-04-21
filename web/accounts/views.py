from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.constants import RESTORE_PASSWORD_LINK_SENT
from accounts.mixins import ValidateRestorePassword
from accounts.models import User, ActivateUserToken
from accounts.serializers import (
    LoginSerializer, RegisterSerializer, ChangePasswordSerializer,
    RestorePasswordSerializer, ForgotPasswordSerializer, ResendVerifyEmailSerializer
)
from accounts.utils import send_forgot_password_email, send_email_verification_email


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, token):
        activate_user_token: ActivateUserToken = get_object_or_404(ActivateUserToken, token=token)
        activate_user_token.user.activate()
        activate_user_token.delete_token()
        return Response(status=status.HTTP_200_OK)


class ResendVerifyEmailView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ResendVerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_email_verification_email(user=User.get_user(query={'email': serializer.data['email']}))
        return Response(status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_forgot_password_email(user=User.get_user(query={'email': serializer.data['email']}))
        return Response(data={'message': RESTORE_PASSWORD_LINK_SENT}, status=status.HTTP_200_OK)


class RestorePasswordView(GenericAPIView, ValidateRestorePassword):
    permission_classes = (AllowAny,)
    serializer_class = RestorePasswordSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.user
        return context

    def post(self, request, uid, token, **kwargs):
        self.user = self.validate(uid, token)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(validated_data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
