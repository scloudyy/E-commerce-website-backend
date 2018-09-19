from random import choice

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import mixins, status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.users.serializers import SmsSerializer, UserRegSerializer
from apps.users.models import VerifyCode
from utils.yunpian import YunPian
from Ecommerce.settings import APIKEY

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


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    send verify code
    """
    serializer_class = SmsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']

        code = self.generate_code()

        yunpian = YunPian(APIKEY)

        sms_status = yunpian.send_sms(mobile=mobile, code=code)

        if sms_status['code'] != 0:
            return Response({'message': sms_status['msg']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_store = VerifyCode(mobile=mobile, code=code)
            code_store.save()
            return Response({'message': sms_status['msg']}, status=status.HTTP_201_CREATED)

    def generate_code(self):
        seeds = '0123456789'
        code = []

        for i in range(4):
            code.append(choice(seeds))

        return ''.join(code)


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    user viewset
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

