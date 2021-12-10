from django.contrib import admin
from notify.models import *


admin.site.register(Notify)
admin.site.register(Wall)

admin.site.register(UserProfileNotify)
admin.site.register(CommunityProfileNotify)
