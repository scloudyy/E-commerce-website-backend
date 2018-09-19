from random import choice

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import mixins, status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)  # get User instance

        re_dict = serializer.data

        payload = jwt_payload_handler(user)
        # it seems that we cannot access to serializer.data after perform .save()
        # so we use re_dict to replace serializer.data and return re_dict in Response
        # serializer.data['token'] = jwt_encode_handler(payload)
        # serializer.data['name'] = user.name if user.name else user.username

        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # when deserializing data, we can call .save() to return an object instance, based on the validated data.
        # in our case, in order to create jwt, we must obtain User instance
        # so we should return the instance returned by .save()
        return serializer.save()

