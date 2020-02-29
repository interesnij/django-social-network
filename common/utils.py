

def safe_json(data):
    import json
    from django.utils.safestring import mark_safe

    return mark_safe(json.dumps(data))
    

def is_mobile(request):
    import re

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False
