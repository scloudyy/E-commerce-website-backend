from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField


class GoodsCategory(models.Model):
    """
    goods category
    """
    CATEGORY_TYPE = (
        (1, "first level category"),
        (2, "second level category"),
        (3, "third level category"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="category name", help_text="category name")
    code = models.CharField(default="", max_length=30, verbose_name="category code", help_text="category code")
    desc = models.TextField(default="", verbose_name="category description", help_text="category description")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="category level", help_text="category level")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="parent category", help_text="parent categoty",
                                        related_name="sub_cat")
    is_tab = models.BooleanField(default=False, verbose_name="whether on the tab", help_text="whether on the tab")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="added time")

    class Meta:
        verbose_name = "goods category"
        verbose_name_plural = "goods categories"

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌名
    """
    category = models.ForeignKey(GoodsCategory, related_name='brands', null=True, blank=True, verbose_name="category name")
    name = models.CharField(default="", max_length=30, verbose_name="brand name", help_text="brand name")
    desc = models.TextField(default="", max_length=200, verbose_name="brand description", help_text="brand description")
    image = models.ImageField(max_length=200, upload_to="brands/images/")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="added time")

    class Meta:
        verbose_name = "brand"
        verbose_name_plural = "brands"
        db_table = "goods_goodsbrand"

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    goods
    """
    category = models.ForeignKey(GoodsCategory, verbose_name="category name")
    goods_sn = models.CharField(max_length=50, default="", verbose_name="good sn")
    name = models.CharField(max_length=100, verbose_name="good name")
    click_num = models.IntegerField(default=0, verbose_name="click name")
    sold_num = models.IntegerField(default=0, verbose_name="sold number")
    fav_num = models.IntegerField(default=0, verbose_name="favorite number")
    goods_num = models.IntegerField(default=0, verbose_name="goods number")
    market_price = models.FloatField(default=0, verbose_name="market price")
    shop_price = models.FloatField(default=0, verbose_name="shop price")
    goods_brief = models.TextField(max_length=500, verbose_name="goods brief description")
    goods_desc = UEditorField(verbose_name="content", imagePath="goods/images/", width=1000, height=300,
                              filePath="goods/files/", default='')
    ship_free = models.BooleanField(default=True, verbose_name="whether ship is free")
    goods_front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="goods images")
    is_new = models.BooleanField(default=False, verbose_name="whether is new goods")
    is_hot = models.BooleanField(default=False, verbose_name="whether is hot goods")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="added time")

    class Meta:
        verbose_name = 'good'
        verbose_name_plural = 'goods'

    def __str__(self):
        return self.name
