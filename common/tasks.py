from datetime import datetime, timedelta
from celery import Celery
from tr import celery_app
from posts.models import PostsList
from tr.celery import app
from django.utils import timezone

#class MyTask(celery_app.Task):
#    def run(self):
#        list = PostsList.objects.get(pk=1)
#        list.name = "бубубу"
#        list.save(update_fields=["name"])

#MyTask = app.register_task(MyTask())

@app.task(bind=True)
def custom(self):
    list = PostsList.objects.get(pk=1)
    list.name = "Записи))))"
    list.save(update_fields=["name"])
