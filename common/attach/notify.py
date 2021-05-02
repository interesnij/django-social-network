def get_notify(user, notify):
    type = notify.type
    if type[:1] == "PO":
        from common.items.post import get_post
        return get_post(user, notify)
    elif type[:1] == "PH":
        from common.items.photo import get_photo
        return get_photo(user, notify)
