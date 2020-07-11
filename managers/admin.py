from django.contrib import admin
from managers.models import *
from managers.model.user import *
from managers.model.community import *
from managers.model.post import *
from managers.model.good import *
from managers.model.photo import *
from managers.model.video import *
from managers.model.audio import *


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
admin.site.register(ModeratedPostComment)
admin.site.register(PostCommentModerationReport)
admin.site.register(ModerationPenaltyPostComment)

admin.site.register(ModeratedPhoto)
admin.site.register(PhotoModerationReport)
admin.site.register(ModerationPenaltyPhoto)
admin.site.register(ModeratedPhotoComment)
admin.site.register(PhotoCommentModerationReport)
admin.site.register(ModerationPenaltyPhotoComment)

admin.site.register(ModeratedGood)
admin.site.register(GoodModerationReport)
admin.site.register(ModerationPenaltyGood)
admin.site.register(ModeratedGoodComment)
admin.site.register(GoodCommentModerationReport)
admin.site.register(ModerationPenaltyGoodComment)

admin.site.register(ModeratedVideo)
admin.site.register(VideoModerationReport)
admin.site.register(ModerationPenaltyVideo)
admin.site.register(ModeratedVideoComment)
admin.site.register(VideoCommentModerationReport)
admin.site.register(ModerationPenaltyVideoComment)

admin.site.register(ModeratedAudio)
admin.site.register(AudioModerationReport)
admin.site.register(ModerationPenaltyAudio)
