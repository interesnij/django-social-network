from django.views.generic.base import TemplateView
from users.models import User
from main.models import Item, ItemComment
from communities.models import Community
from django.http import JsonResponse, HttpResponse
from django.views import View
from common.models import ItemVotes, ItemCommentVotes
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from common.checkers import check_can_get_posts_for_community_with_name
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import PermissionDenied
from django.core import serializers


class ItemUserLikeWindow(TemplateView):
    template_name="item_votes/like_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.likes = self.item.get_likes_for_item(request.user)[0:6]
        elif self.user == request.user:
            self.likes = self.item.get_likes_for_item(request.user)[0:6]
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.likes = self.item.get_likes_for_item(request.user)[0:6]
        return super(ItemUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemUserLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context


class ItemCommunityLikeWindow(TemplateView):
    template_name="item_votes/like_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.likes = self.item.get_likes_for_item(request.user)[0:6]
        return super(ItemCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context


class ItemUserCommentLikeWindow(TemplateView):
    template_name="item_votes/comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.likes = self.comment.get_likes_for_comment_item(request.user)[0:6]
        elif self.user == request.user:
            self.likes = self.comment.get_likes_for_comment_item(request.user)[0:6]
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.likes = self.comment.get_likes_for_comment_item(request.user)[0:6]
        return super(ItemUserCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemUserCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context


class ItemCommunityCommentLikeWindow(TemplateView):
    template_name="item_votes/comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.likes = self.comment.get_likes_for_comment_item(request.user)[0:6]
        return super(ItemCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context


class ItemUserDislikeWindow(TemplateView):
    template_name="item_votes/dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.dislikes = self.item.get_dislikes_for_item(request.user)[0:6]
        elif self.user == request.user:
            self.dislikes = self.item.get_dislikes_for_item(request.user)[0:6]
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.dislikes = self.item.get_dislikes_for_item(request.user)[0:6]
        return super(ItemUserDislikeWindow,self).get(request,*args,**kwargs)


    def get_context_data(self,**kwargs):
        context=super(ItemUserDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context


class ItemCommunityDislikeWindow(TemplateView):
    template_name="item_votes/dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.dislikes = self.item.get_dislikes_for_item(request.user)[0:6]
        return super(ItemCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context


class ItemUserCommentDislikeWindow(TemplateView):
    template_name="item_votes/comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)[0:6]
        elif self.user == request.user:
            self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)[0:6]
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)[0:6]
        return super(ItemUserCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemUserCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context


class ItemCommunityCommentDislikeWindow(TemplateView):
    template_name="item_votes/comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.likes = self.comment.get_dislikes_for_comment_item(request.user)[0:6]
        return super(ItemCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context
