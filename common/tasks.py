from tr.celery import app

@app.task(bind=True, max_retries=5)
def abort_suspended(self, type):
    if type[0] == "l":
        from common.utils import get_item_of_type
        item = get_list_of_type(type)
    elif "use" in type:
        from users.models import User
        item = User.objects.get(pk=type[3:])
    elif "com" in type:
        from communities.models import Community
        item = Community.objects.get(pk=type[3:])

    if item.is_suspended():
        return
    else:
        return item.unsuspend_item()
