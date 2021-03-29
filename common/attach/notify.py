
def get_notify(user, notify):
    attach = notify.attach
    if attach[:3] == "pos":
        from common.items.post import get_post
        return get_post(user, notify)
