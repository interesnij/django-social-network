import json
from users.models import User
from goods.models import Good, GoodComment
from communities.models import Community
from django.http import HttpResponse
from django.views import View
from common.model.votes import GoodVotes, GoodCommentVotes
from common.check.user import check_user_can_get_list
from rest_framework.exceptions import PermissionDenied
from common.check.community import check_can_get_lists
from django.http import Http404
from common.notify.notify import *


class GoodUserLikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), good.likes_count(), good.dislikes_count()
        if not good.votes_on or not request.is_ajax():
            raise Http404

        if user != request.user:
            check_user_can_get_list(request.user, user)
        return good.send_like(request.user, None)


class GoodUserDislikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        user, likes, dislikes = User.objects.get(pk=self.kwargs["pk"]), good.likes_count(), good.dislikes_count()
        if not good.votes_on or not request.is_ajax():
            raise Http404
        if user != request.user:
            check_user_can_get_list(request.user, user)
        return good.send_dislike(request.user, None)


class GoodCommunityLikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), good.likes_count(), good.dislikes_count()
        if not good.votes_on or not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user,community)
        return good.send_like(request.user, community)


class GoodCommunityDislikeCreate(View):
    def get(self, request, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        community, likes, dislikes = Community.objects.get(pk=self.kwargs["pk"]), good.likes_count(), good.dislikes_count()
        if not good.votes_on or not request.is_ajax():
            raise Http404
        check_can_get_lists(request.user, community)
        return good.send_dislike(request.user, community)
