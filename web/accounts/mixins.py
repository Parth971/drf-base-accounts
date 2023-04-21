from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import ValidationError

from accounts.models import User


class ValidateRestorePassword:
    token_generator = PasswordResetTokenGenerator()

    def __init__(self):
        self.user = None

    def is_token_valid(self, token):
        return self.token_generator.check_token(self.user, token)

    def is_uid_valid(self, uid):
        self.user = User.get_user(query={'id': uid})
        return self.user

    def validate(self, uid, token):
        if not self.is_uid_valid(uid):
            raise ValidationError({'error': 'UID invalid'})

        if not self.is_token_valid(token):
            raise ValidationError({'error': 'Token invalid'})

        return self.user
