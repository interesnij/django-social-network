import os

from celery import Celery
from posts.models import PostsList
from datetime import datetime, timedelta

# Установите модуль настроек Django по умолчанию для программы "celery".
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tr.settings')

app = Celery('tr', backend='redis://localhost', broker='pyamqp://')

# Использование строки здесь означает, что рабочему не нужно сериализовать
# объект конфигурации для дочерних процессов.
# - namespace='СЕЛЬДЕРЕЙ' означает все ключи конфигурации, связанные с сельдереем
# должен иметь префикс `CELERY_`.

app.config_from_object('django.conf:settings')

# Загружайте модули задач из всех зарегистрированных приложений Django.
app.autodiscover_tasks("common")
