from django.contrib import admin
from main.models import Item, Comment


admin.site.register(Item, Comment)
