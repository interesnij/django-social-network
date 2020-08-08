import re
MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from users.models import User
from posts.models import PostComment
from gallery.models import Album, Photo
from gallery.forms import PhotoDescriptionForm
from communities.models import Community
from common.template.photo import *
from django.http import Http404
