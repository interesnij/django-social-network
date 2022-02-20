from tr.celery import app

@app.task(bind=True, max_retries=5)
def abort_suspended(self, item):
    if item.is_suspended():
        return
    else:
        return item.unsuspend_item()
