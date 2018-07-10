
# 避免celery.py和celery的冲突问题
from __future__ import absolute_import

import os

from celery import Celery
from XSProject import settings

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE','XSProject.settings')

# 创建 celery 并指定 名称
app = Celery('XSProject')
app.config_from_object('django.conf:settings')

#自动发现当前项目下的所有app应用中的celery
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)


# python manage.py celery -A XSProject-1 worker -B
# python manage.py flower
#































