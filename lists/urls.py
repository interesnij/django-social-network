from lists.views import ListsView
from django.conf.urls import url

urlpatterns = [
    url(r'^lists/$', ListsView.as_view(), name='lists')
]
