#-*- coding:utf-8 -*-
from __future__ import absolute_import

from scm import celery_app

import datetime
from base.models import BasFee

@celery_app.task(name="tasks.updateUser")
def updateUser():
    print(">>>>>>>>>>>>run updateUser() start.............")
    today = datetime.date.today()
    BasFee.objects.filter(enddate__lt=today,status='Y').update(status="N")
    print(">>>>>>>>>>>>run updateUser() end.............")





