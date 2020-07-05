from django.contrib import admin
from managers.models import *
from managers.model.user import *
from managers.model.community import *
from managers.model.post import *


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

admin.site.register(ModerationCategory)

admin.site.register(ModeratedUser)
admin.site.register(UserModerationReport)
admin.site.register(ModerationPenaltyUser)

admin.site.register(ModeratedCommunity)
admin.site.register(CommunityModerationReport)
admin.site.register(ModerationPenaltyCommunity)

admin.site.register(ModeratedPost)
admin.site.register(PostModerationReport)
admin.site.register(ModerationPenaltyPost)
