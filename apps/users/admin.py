from django.contrib import admin
from users.models import UserProfile, VerifyCode

admin.site.register(UserProfile)
admin.site.register(VerifyCode)
