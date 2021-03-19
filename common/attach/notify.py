
def get_notify(user, verb, attach):
    if attach[:3] == "pos":
        from common.items.post import get_u_post
        return get_post(user, attach[3:])
