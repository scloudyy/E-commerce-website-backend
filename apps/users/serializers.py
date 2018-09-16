from datetime import datetime
from datetime import timedelta
import re

from django.contrib.auth import get_user_model
from rest_framework import  serializers
from rest_framework.validators import UniqueValidator

from Ecommerce.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """
    Serializer for sms code
    """
    # at begining sms code will not be sent by front end, sms code is created by back end
    # and we can only obtain mobile
    # so we cannot use ModelSerializer in this case
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


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4,
                                 error_messages={'required': 'please input verify code',
                                                 'blank': 'please input verify code',
                                                 'max_length': 'illegal verify code format',
                                                 'min_length': 'illegal verify code format'})
    username = serializers.CharField(required=True, allow_blank=False, help_text='username',
                                     validators=[UniqueValidator(User.objects.all(), message='username already exist')])

    def validate_code(self, data):
        records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if records:
            last_record = records[0]

            five_minutes_ago = datetime.now() - timedelta(minutes=5)
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError('verify code expired')
            if data != last_record.code:
                raise serializers.ValidationError('verify code error')
        else:
            raise serializers.ValidationError('verify code error')

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs


    class Meta:
        model = User
        fields = ['username', 'mobile', 'code']


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4)

    def validate_code(self, code):
        one_mintes_ago = datetime.now()

    class Meta:
        model = User
        fields = ('username', 'code')
