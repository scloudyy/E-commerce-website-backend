from datetime import datetime
from datetime import timedelta
import re

from django.contrib.auth import get_user_model
from rest_framework import  serializers

from Ecommerce.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, data):
        if User.objects.filter(mobile=data).count():
            raise serializers.ValidationError('user already exist')

        if not re.match(REGEX_MOBILE, data):
            raise serializers.ValidationError('mobile is illegal')

        one_minute_ago = datetime.now() - timedelta(minutes=1)
        if VerifyCode.objects.filter(mobile=data, add_time__gt=one_minute_ago).count():
            raise serializers.ValidationError('send verify code too frequent')

        return data


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4)

    def validate_code(self, code):
        one_mintes_ago = datetime.now()

    class Meta:
        model = User
        fields = ('username', 'code')
