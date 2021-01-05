import re
import datetime
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from users.models import User
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)


class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user'), 'error'
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            User.objects.filter(id=request.user.id).update(last_activity=datetime.datetime.now(), device=User.PHONE)
        else:
            User.objects.filter(id=request.user.id).update(last_activity=datetime.datetime.now(), device=User.DESCTOP)
