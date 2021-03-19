def linebreaks(value, autoescape=None):
    from django.utils.html import linebreaks
    from django.utils.safestring import mark_safe
    autoescape = autoescape and not isinstance(value, SafeData)
    return mark_safe(linebreaks(value, autoescape))


def get_notify(user, verb, attach):
    if attach[:3] == "pos":
        from common.items.post import get_u_post
        return get_u_post(user)
    if block:
        return block
    else:
        return "None"
