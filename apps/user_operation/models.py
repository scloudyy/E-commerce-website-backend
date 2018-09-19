from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from apps.goods.models import Goods

User = get_user_model()


class UserFav(models.Model):
    """
    user favorite
    """
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.ProtectedError)
    goods = models.ForeignKey(Goods, verbose_name="goods name", help_text="goods name", on_delete=models.ProtectedError)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="added time")

    class Meta:
        verbose_name = 'user favorite'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return self.user


class UserLeavingMessage(models.Model):
    """
    user leaving message
    """
    MESSAGE_CHOICES = (
        (1, "message"),
        (2, "complain"),
        (3, "query"),
        (4, "after sale"),
        (5, "buy")
    )
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.ProtectedError)
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name="message type",
                                       help_text="message type: 1(message), 2(compalin), 3(query), 4(after sale), 5(buy)")
    subject = models.CharField(max_length=100, default="", verbose_name="subject")
    message = models.TextField(default="", verbose_name="content", help_text="content")
    file = models.FileField(upload_to="message/images/", verbose_name="upload file", help_text="upload file")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="added time")

    class Meta:
        verbose_name = "user leaving message"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserAddress(models.Model):
    """
    user address
    """
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.ProtectedError)
    province = models.CharField(max_length=100, default="", verbose_name="state")
    city = models.CharField(max_length=100, default="", verbose_name="city")
    district = models.CharField(max_length=100, default="", verbose_name="region")
    address = models.CharField(max_length=100, default="", verbose_name="address")
    signer_name = models.CharField(max_length=100, default="", verbose_name="signer name")
    signer_mobile = models.CharField(max_length=11, default="", verbose_name="signer mobile")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="added time")

    class Meta:
        verbose_name = "user address"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address
