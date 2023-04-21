from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def send_forgot_password_email(user):
    token = PasswordResetTokenGenerator().make_token(user)
    link = F"https://{settings.FRONT_END_DOMAIN}/auth/restore-password/{user.id}/{token}"
    print(f"Restore password link: {link}")


def send_email_verification_email(user):
    token = user.generate_activation_token()
    link = F"https://{settings.FRONT_END_DOMAIN}/auth/verify-email/{token}"
    print(f"Email verification link: {link}")
