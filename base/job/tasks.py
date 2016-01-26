#-*- coding:utf-8 -*-
from __future__ import absolute_import

from scm import celery_app
import datetime

from base.models import BasUser

@celery_app.task(name="tasks.updateUser")
def updateUser():

    print(">>>>>>>>>>>>执行updateUserStatus().............")





