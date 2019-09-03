from django.urls import url, include
from users.views import AllUsers

categories_patterns = [
    url(r'^all-users/$', AllUsers.as_view(), name='all_users')
]
