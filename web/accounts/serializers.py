from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.constants import (
    INVALID_EMAIL, INCORRECT_OLD_PASSWORD, PASSWORD_HELP_TEXT,
    PASSWORD_MISMATCH, EMAIL_NOT_ACTIVATED, EMAIL_ALREADY_ACTIVATED
)
from accounts.models import User
from accounts.utils import send_email_verification_email
from accounts.validators import validate_password, validate_first_name, validate_last_name, validate_mobile_number


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text=PASSWORD_HELP_TEXT,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'job_title', 'company_name', 'mobile_number')
        extra_kwargs = {
            'first_name': {'required': True, 'validators': [validate_first_name]},
            'last_name': {'required': True, 'validators': [validate_last_name]},
            'mobile_number': {'required': True, 'validators': [validate_mobile_number]}
        }

    def create(self, validated_data):
        """
        This function will create user instance and send email regarding email verification.
        :rtype: User object
        """
        user = User.objects.create_user(**validated_data, is_active=False)
        send_email_verification_email(user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'job_title', 'company_name', 'mobile_number')
        extra_kwargs = {
            'first_name': {'required': True, 'validators': [validate_first_name]},
            'last_name': {'required': True, 'validators': [validate_last_name]},
            'mobile_number': {'required': True, 'validators': [validate_mobile_number]},
            'email': {'read_only': True},
        }


class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_pic',)
        extra_kwargs = {
            'profile_pic': {'required': True, 'allow_null': False},
        }


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        """
        This function will check if user exists for given email field, if not raise Validation error.
        :rtype: dict
        """
        email = attrs.get('email')
        self.user = User.get_user(query={'email': email})
        if not self.user:
            raise serializers.ValidationError({'email': INVALID_EMAIL})

        return attrs


class ResendVerifyEmailSerializer(EmailSerializer):
    def validate(self, attrs):
        """
        This function will check if user should not be active, if user already active it will raise Validation error.
        :rtype: dict
        """
        attrs = super().validate(attrs)
        if self.user and self.user.is_active:
            raise serializers.ValidationError({'email': EMAIL_ALREADY_ACTIVATED})
        return attrs


class ForgotPasswordSerializer(EmailSerializer):
    def validate(self, attrs):
        """
        This function will check if user is active, if user not active it will raise Validation error.
        :rtype: dict
        """
        attrs = super().validate(attrs)
        if self.user and not self.user.is_active:
            raise serializers.ValidationError({'email': EMAIL_NOT_ACTIVATED})
        return attrs


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2')

    def validate(self, attrs):
        """
        This function will match both password, if not same then raise Validation error.
        :rtype: dict
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": PASSWORD_MISMATCH})

        return attrs

    def update(self, instance, validated_data):
        """
        This function will update new password of user.
        :rtype: User object
        """
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class ChangePasswordSerializer(PasswordSerializer):
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate_old_password(self, value):
        """
        This function will check user's password matches or not. If not, it will raise Serializer error.
        :rtype: dict
        """
        if not self.instance.check_password(value):
            raise serializers.ValidationError(INCORRECT_OLD_PASSWORD)
        return value


class RestorePasswordSerializer(PasswordSerializer):
    pass
