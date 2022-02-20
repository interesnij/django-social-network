from datetime import datetime, timedelta
from celery import shared_task, current_task, task
from celery import Celery
from posts.models import PostsList

app = Celery('tasks', broker='redis://localhost')

@app.task
def test():
    print ("it's work!")
    list = PostsList.objects.get(pk=1)
    list.name = "бубубу"
    list.save(update_fields=["name"])


test.apply_async(eta=timezone.now() + timezone.timedelta(seconds=20))
