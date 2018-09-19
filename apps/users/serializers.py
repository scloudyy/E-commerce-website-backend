from datetime import datetime, timezone
from datetime import timedelta
import re

from django.contrib.auth import get_user_model
from rest_framework import  serializers
from rest_framework.validators import UniqueValidator

from Ecommerce.settings import REGEX_MOBILE
from apps.users.models import VerifyCode

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
    code = serializers.CharField(required=True, max_length=4, min_length=4, write_only=True, label='sms verify code',
                                 help_text='input verify code',
                                 error_messages={'required': 'please input verify code',
                                                 'blank': 'please input verify code',
                                                 'max_length': 'illegal verify code format',
                                                 'min_length': 'illegal verify code format'})
    # Set write_only to True to ensure that this field may be used when updating or creating an instance,
    # but is not included when serializing the representation.
    username = serializers.CharField(required=True, allow_blank=False, help_text='username',
                                     validators=[UniqueValidator(User.objects.all(), message='username already exist')])

    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    # password should also be write_only since we should not return back password which is insecure

    def validate_code(self, data):
        records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if records:
            last_record = records[0]

            five_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=5)
            # Django's auto added time is timezone aware, so compared time should also be time zone aware
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError('verify code expired')
            if data != last_record.code:
                raise serializers.ValidationError('verify code error')
        else:
            raise serializers.ValidationError('verify code error')

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        # since we have set code to write_only, it will not serializer to output
        # and we can delete it safely
        return attrs

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    class Meta:
        model = User
        fields = ['username', 'mobile', 'code', 'password']


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4)

    def validate_code(self, code):
        one_mintes_ago = datetime.now()

    class Meta:
        model = User
        fields = ('username', 'code')
