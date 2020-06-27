from django.contrib import admin
from managers.models import *


admin.site.register(UserStaff)
admin.site.register(CommunityStaff)
admin.site.register(PostUserStaff)
admin.site.register(GoodUserStaff)
admin.site.register(PhotoUserStaff)
admin.site.register(VideoUserStaff)
admin.site.register(AudioUserStaff)

admin.site.register(CanWorkStaffUser)
admin.site.register(CanWorkStaffCommunity)
admin.site.register(CanWorkStaffPostUser)
admin.site.register(CanWorkStaffGoodUser)
admin.site.register(CanWorkStaffPhotoUser)
admin.site.register(CanWorkStaffVideoUser)
admin.site.register(CanWorkStaffAudioUser)
