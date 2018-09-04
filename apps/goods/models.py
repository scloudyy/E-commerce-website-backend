from datetime import datetime

from django.db import models


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
