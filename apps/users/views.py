from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import mixins
from rest_framework import viewsets

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    user maybe use username or mobile to login, so we need to redefine user verification
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    user
    """


