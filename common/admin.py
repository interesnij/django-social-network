from django.contrib import admin
from common.model.votes import *
from common.model.other import *


class PostVotesAdmin(admin.ModelAdmin):
    list_display = (
        'vote',
        'user',
        #'parent',
    )

admin.site.register(PostVotes, PostVotesAdmin)
admin.site.register(PhoneCodes)
admin.site.register(CustomLink)

admin.site.register(SmileCategory)
admin.site.register(Smiles)
admin.site.register(StickerCategory)
admin.site.register(Stickers)

admin.site.register(UserPopulateSmiles)
admin.site.register(UserPopulateStickers)
