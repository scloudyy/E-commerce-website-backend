from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
import json
from goods.models import Goods


class GoodListView(View):
    def get(self, request):
        goods = Goods.objects.all()[:10]
        json_list = []
        # method1
        # for good in goods:
        #     json_dict = {'name': good.name, 'category': good.category.name}
        #     # json_dict['add_time'] = good.add_time  # Object of type 'datetime' is not JSON serializable
        #     json_list.append(json_dict)

        # method2
        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good) # ImageFiled and DateFiled cannot be dumped to json
        #     json_list.append(json_dict)

        # return HttpResponse(json.dumps(json_list), content_type='application/json')

        from django.core import serializers
        # serializers can serialize ImageFiled and DateFiled
        json_data = serializers.serialize('json', goods)

        return HttpResponse(json_data, safe=False)
        # 1. for the resources in /media, 'domain/media/' needed to be added to the their url
        #    this cannot be done by django serializers
