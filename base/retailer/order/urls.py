from django.conf.urls import url
from base.retailer.order.views import *

urlpatterns = [
    url(r'^retail/order/$', retOrder, name='retailOrder'),
    url(r'^retail/order/orderArticle/', retOrderArticle, name='retOrderArticle'),
]
