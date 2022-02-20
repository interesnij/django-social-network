from __future__ import absolute_import

import os
import sys
from celery import Celery

from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings

# Установите модуль настроек Django по умолчанию для программы "celery".
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tr.settings')

project_name = 'tr'
app = Celery(project_name, broker='redis://localhost')

# Использование строки здесь означает, что рабочему не нужно сериализовать
# объект конфигурации для дочерних процессов.
# - namespace='СЕЛЬДЕРЕЙ' означает все ключи конфигурации, связанные с сельдереем
# должен иметь префикс `CELERY_`.

app.config_from_object('django.conf:settings')

# Загружайте модули задач из всех зарегистрированных приложений Django.
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)
