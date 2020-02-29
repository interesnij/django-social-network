from django.utils.safestring import mark_safe
import json


def safe_json(data):
    return mark_safe(json.dumps(data))

def is_mobile(request):
    import re

    self.MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if self.MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        self.mobile = True
    else:
        self.mobile = False
