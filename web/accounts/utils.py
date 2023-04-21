from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def send_forgot_password_email(user):
    token = PasswordResetTokenGenerator().make_token(user)
    link = F"https://{settings.FRONT_END_DOMAIN}/restore-password/{user.id}/{token}"
    print(link, '???????????????????')
