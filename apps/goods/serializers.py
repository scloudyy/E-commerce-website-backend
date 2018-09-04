from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsImage, Banner
from goods.models import GoodsCategoryBrand, IndexAd


# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True, max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Goods` instance, given the validated data.
#         """
#         return Goods.objects.create(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = '__all__'
