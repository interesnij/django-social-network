import os
from celery import Celery
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
#app.autodiscover_tasks(packages=['common'])

@app.task
def test():
    print ("it's work!")
    #list = PostsList.objects.get(pk=1)
    #list.name = "бубубу"
    #list.save(update_fields=["name"])


test.apply_async(eta=timezone.now() + timezone.timedelta(seconds=20))
