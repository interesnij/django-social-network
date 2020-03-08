from django.contrib import admin
from common.model.votes import *


class ItemVotesAdmin(admin.ModelAdmin):
    list_display = (
        'vote',
        'user',
        #'parent',
    )

admin.site.register(ItemVotes, ItemVotesAdmin)
