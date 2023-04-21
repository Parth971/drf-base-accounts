from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from accounts.models import User
from accounts.serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
