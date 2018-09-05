from django_filters import rest_framework as filters
from .models import Goods


class GoodsFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'name']
