from django.contrib import admin
from common.model.votes import *
from common.model.other import PhoneCodes


class ItemVotesAdmin(admin.ModelAdmin):
    list_display = (
        'vote',
        'user',
        #'parent',
    )

admin.site.register(ItemVotes, ItemVotesAdmin)
admin.site.register(PhoneCodes)
