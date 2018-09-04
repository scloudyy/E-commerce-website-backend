from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics

from .models import Goods
from .serializers import GoodsSerializer


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

# update to use special generics

class GoodsListView(generics.ListAPIView):
    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer
