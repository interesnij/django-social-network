from django.contrib import admin
from logs.model.manage_audio import *
from logs.model.manage_goods import *
from logs.model.manage_photo import *
from logs.model.manage_user_community import *
from logs.model.manage_posts import *
from logs.model.manage_video import *


admin.site.register(PostManageLog)
admin.site.register(PostCommentManageLog)
admin.site.register(PostWorkerManageLog)
admin.site.register(PostCreateWorkerManageLog)

admin.site.register(AudioManageLog)
admin.site.register(AudioWorkerManageLog)
admin.site.register(AudioCreateWorkerManageLog)

admin.site.register(GoodManageLog)
admin.site.register(GoodCommentManageLog)
admin.site.register(GoodWorkerManageLog)
admin.site.register(GoodCreateWorkerManageLog)

admin.site.register(PhotoManageLog)
admin.site.register(PhotoCommentManageLog)
admin.site.register(PhotoWorkerManageLog)
admin.site.register(PhotoCreateWorkerManageLog)

admin.site.register(VideoManageLog)
admin.site.register(VideoCommentManageLog)
admin.site.register(VideoWorkerManageLog)
admin.site.register(VideoCreateWorkerManageLog)

admin.site.register(UserManageLog)
admin.site.register(CommunityManageLog)
admin.site.register(UserWorkerManageLog)
admin.site.register(UserCreateWorkerManageLog)
admin.site.register(CommunityWorkerManageLog)
admin.site.register(CommunityCreateWorkerManageLog)
