
def get_notify(user, verb, attach):
    if attach[:3] == "pos":
        from common.items.post import get_post
        if verb == "ITE":
            return get_post(user, attach[3:])
        else:
            return '<p><a href="' + user.get_link() + '" class="ajax">' + user.get_full_name() + '</a>' + verb + 'запись</p>'
