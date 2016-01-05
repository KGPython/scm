#-*- coding:utf-8 -*-
#!/bin/python
from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

#load pymysql
import pymysql
pymysql.install_as_MySQLdb()


