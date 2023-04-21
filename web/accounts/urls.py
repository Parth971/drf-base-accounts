from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from accounts.views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout_user'),
]
