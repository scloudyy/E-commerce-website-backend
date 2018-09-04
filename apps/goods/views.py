from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Goods
from .serializers import GoodsSerializer


class GoodsListView(APIView):
    """
    list all goods
    """
    def get(self, request, format=None):
        goods = Goods.objects.all()[:4]
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
