from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, UpdateAPIView, get_object_or_404,
    RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.constants import RESTORE_PASSWORD_LINK_SENT
from accounts.mixins import ValidateRestorePassword
from accounts.models import User, ActivateUserToken
from accounts.serializers import (
    LoginSerializer, RegisterSerializer, ChangePasswordSerializer,
    RestorePasswordSerializer, ForgotPasswordSerializer, ResendVerifyEmailSerializer,
    ProfilePicSerializer, ProfileSerializer
)
from accounts.utils import send_forgot_password_email, send_email_verification_email


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class RetrieveUpdateProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class RetrieveUpdateDestroyProfilePicView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfilePicSerializer

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance: User):
        instance.profile_pic.delete()

    def perform_update(self, serializer: serializer_class):
        # This will delete old image file
        serializer.instance.profile_pic.delete()
        super().perform_update(serializer)


class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, token):
        """
        Get request to check token and activate user.
        :param request:
        :param token:
        :return: status code 200 for success and 404 for invalid token.
        """
        activate_user_token: ActivateUserToken = get_object_or_404(ActivateUserToken, token=token)
        activate_user_token.user.activate()
        activate_user_token.delete_token()
        return Response(status=status.HTTP_200_OK)


class ResendVerifyEmailView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Post request to send email regarding email verification.
        :param request: contains data attribute with entered user's email.
        :return: status code 200 for success and 400 for invalid email or already activated email with error message.
        """
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
        """
        Post request to send email regarding restore password.
        :param request: contains data attribute with entered user's email.
        :return: status code 200 for success and 400 for invalid email or not activated email with error message.
        """
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_forgot_password_email(user=User.get_user(query={'email': serializer.data['email']}))
        return Response(data={'message': RESTORE_PASSWORD_LINK_SENT}, status=status.HTTP_200_OK)


class RestorePasswordView(ValidateRestorePassword, UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RestorePasswordSerializer


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
