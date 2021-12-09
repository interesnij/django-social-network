from django.contrib import admin
from notify.models import *


admin.site.register(Notify)
admin.site.register(Wall)

admin.site.register(UserNewsPk)
admin.site.register(CommunityNewsPk)

admin.site.register(UserFeaturedPk)
admin.site.register(CommunityFeaturedPk)

admin.site.register(UserProfileNotify)
admin.site.register(CommunityProfileNotify)
