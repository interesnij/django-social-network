
def get_notify(user, notify):
    attach = notify.attach
    if attach[:3] == "pos":
        from common.items.post import get_post
        return get_post(user, notify)
    elif attach[:3] == "pho":
        from common.items.photo import get_photo
        return get_photo(user, notify)
