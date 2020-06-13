from django.contrib import admin
from common.model.votes import *
from common.model.other import PhoneCodes


class PostVotesAdmin(admin.ModelAdmin):
    list_display = (
        'vote',
        'user',
        #'parent',
    )

admin.site.register(PostVotes, PostVotesAdmin)
admin.site.register(PhoneCodes)
