
from django.conf.urls import url
from base.retailer.balance.views import *

urlpatterns = [
    url(r'^retail/balance/$', balance , name='retailBalance'),
    url(r'^retail/balance/balanceArticle/', balanceArticle, name='retailBalanceArticle'),
]
