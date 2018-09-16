import datetime

from django.contrib.auth import get_user_model

from rest_framework import  serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4)

    def validate_code(self, code):
        one_mintes_ago = datetime.now()

    class Meta:
        model = User
        fields = ('username', 'code')
