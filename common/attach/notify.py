def get_notify(user, notify):
    type = notify.type
    if type == "POS":
        from common.items.post import get_post
        return get_post(user, notify)
    elif type == "PHO":
        from common.items.photo import get_photo
        return get_photo(user, notify)
