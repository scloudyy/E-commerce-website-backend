from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods

User = get_user_model()


class ShoppingCart(models.Model):
    """
    Shopping Cart
    """
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.ProtectedError)
    goods = models.ForeignKey(Goods, verbose_name="good", on_delete=models.ProtectedError)
    nums = models.IntegerField(default=0, verbose_name="good number")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="added time")

    class Meta:
        verbose_name = 'shopping cart'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return "%s(%d)".format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    """
    Order
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "success"),
        ("TRADE_CLOSED", "trade close"),
        ("WAIT_BUYER_PAY", "wait buyer pay"),
        ("TRADE_FINISHED", "trade finished"),
        ("PAYING", "paying"),
    )

    user = models.ForeignKey(User, verbose_name="user", on_delete=models.ProtectedError)
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="order sn")
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="trade sn")
    pay_status = models.CharField(choices=ORDER_STATUS, default="paying", max_length=30, verbose_name="pay status")
    post_script = models.CharField(max_length=200, verbose_name="order post script")
    order_mount = models.FloatField(default=0.0, verbose_name="order mount")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="pay time")

    # user info
    address = models.CharField(max_length=100, default="", verbose_name="address")
    signer_name = models.CharField(max_length=20, default="", verbose_name="signer name")
    singer_mobile = models.CharField(max_length=11, verbose_name="signer mobile")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="added time")

    class Meta:
        verbose_name = "order"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    """
    Order Goods
    """
    order = models.ForeignKey(OrderInfo, verbose_name="order info", related_name="goods",
                              on_delete=models.ProtectedError)
    goods = models.ForeignKey(Goods, verbose_name="goods name", on_delete=models.ProtectedError)
    goods_num = models.IntegerField(default=0, verbose_name="goods number")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="added time")

    class Meta:
        verbose_name = "order goods"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
