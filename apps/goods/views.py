from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Goods
from .serializers import GoodsSerializer
from .filters import GoodsFilter

# class GoodsListView(APIView):
#     """
#     list all goods
#     """
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:4]
#         serializer = GoodsSerializer(goods, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = GoodsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

# update to use mixin

# The create/retrieve/update/delete operations that we've been using so far are going to be pretty similar for any
# model-backed API views we create. Those bits of common behaviour are implemented in REST framework's mixin classes.

# class GoodsListView(mixins.ListModelMixin,
#                     generics.GenericAPIView):
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

# update to use special generics, which combines GenericAPIView and mixin


class GoodsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'  # front end set param: http://127.0.0.1:8000/goods/?page_size=3
    page_query_param = 'p'
    max_page_size = 20


# class GoodsListView(generics.ListAPIView): # ListAPIView(mixins.ListModelMixin,GenericAPIView)
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsSetPagination

# Then update to ViewSet which rewirte as_view(), and we can coop with Router

# class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
#     # since GenericViewSet not define get() post(), we need to use ListModelMixin also
#
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsSetPagination
#
#     # define filter by overwrite get_queryset
#     def get_queryset(self):
#         queryset = Goods.objects.all()
#         price_min = self.request.query_params.get('price_min', 0)
#         if price_min:
#             queryset = queryset.filter(shop_price__gt=int(price_min))
#         return queryset

# update filter to django_filters and rest_framework.filters

class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # since GenericViewSet not define get() post(), we need to use ListModelMixin also
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('click_num', 'sold_num')
