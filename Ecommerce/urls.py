"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from rest_framework_jwt.views import obtain_jwt_token

from Ecommerce.settings import MEDIA_ROOT
# from goods.views import GoodsListView
from goods.views import GoodsListViewSet, CategoryViewSet
from users.views import SmsCodeViewset

# goods_list = GoodsListViewSet.as_view({'get': 'list'})

router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name='goods')
router.register(r'categorys', CategoryViewSet, base_name='categorys')
router.register(r'smscode', SmsCodeViewset, base_name='smscode')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    # goods list
    # update to use GoodsListView
    # url(r'^goods/$', GoodsListView.as_view(), name='goods-list'),
    # update to use GoodsListViewSet
    # url(r'^goods/$', goods_list, name='goods-list'),
    # update to use router
    url(r'^', include(router.urls)),
    url(r'^login/', obtain_jwt_token),

    url(r'docs/', include_docs_urls(title='Ecommerce')),

]
