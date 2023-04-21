from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from accounts.views import RegisterView, LoginView, ForgotPasswordView, ChangePasswordView, RestorePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout_user'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('restore-password/<int:uid>/<str:token>/', RestorePasswordView.as_view(), name='restore_password'),
    path('change_password/<int:user_id>/', ChangePasswordView.as_view(), name='change_password'),
]

