from django.contrib import admin
from logs.model.audio import *
from logs.model.goods import *
from logs.model.photo import *
from logs.model.user_community import *
from logs.model.posts import *
from logs.model.video import *


admin.site.register(PostManageLog)
admin.site.register(PostWorkerManageLog)
admin.site.register(PostCreateWorkerManageLog)

admin.site.register(AudioManageLog)
admin.site.register(AudioWorkerManageLog)
admin.site.register(AudioCreateWorkerManageLog)

admin.site.register(GoodManageLog)
admin.site.register(GoodWorkerManageLog)
admin.site.register(GoodCreateWorkerManageLog)

admin.site.register(PhotoManageLog)
admin.site.register(PhotoWorkerManageLog)
admin.site.register(PhotoCreateWorkerManageLog)

admin.site.register(VideoManageLog)
admin.site.register(VideoWorkerManageLog)
admin.site.register(VideoCreateWorkerManageLog)

admin.site.register(UserManageLog)
admin.site.register(CommunityManageLog)
admin.site.register(UserWorkerManageLog)
admin.site.register(UserCreateWorkerManageLog)
admin.site.register(CommunityWorkerManageLog)
admin.site.register(CommunityCreateWorkerManageLog)
