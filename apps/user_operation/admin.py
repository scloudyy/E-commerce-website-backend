from django.contrib import admin
from apps.user_operation.models import UserFav, UserLeavingMessage, UserAddress

admin.site.register(UserFav)
admin.site.register(UserLeavingMessage)
admin.site.register(UserAddress)

