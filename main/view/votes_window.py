from django.views.generic.base import TemplateView
from users.models import User
from main.models import Item, ItemComment
from communities.models import Community
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.model.votes import PostVotes, PostCommentVotes
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from common.checkers import check_can_get_posts_for_community_with_name
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render_to_response
from common.utils import is_mobile


class ItemUserLikeWindow(TemplateView):
    """
    Перезагрузка окна с последними лайками для записи пользователя
    """
    template_name="item_votes/u_like.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
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

class ItemUserCommentLikeWindow(TemplateView):
    """
    Перезагрузка окна с последними дизлайками для записи пользователя
    """
    template_name="item_votes/u_comment_like.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["comment_pk"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
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

class ItemUserDislikeWindow(TemplateView):
    """
    Перезагрузка окна с последними лайками для комментария записи пользователя
    """
    template_name="item_votes/u_dislike.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
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

class ItemUserCommentDislikeWindow(TemplateView):
    """
    Перезагрузка окна с последними дизлайками для комментария записи пользователя
    """
    template_name="item_votes/u_comment_dislike.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["comment_pk"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
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


class ItemCommunityLikeWindow(TemplateView):
    """
    Перезагрузка окна с последними лайками для записи сообщества
    """
    template_name="item_votes/c_like.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.likes = self.item.get_likes_for_item(request.user)[0:6]
        return super(ItemCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context

class ItemCommunityDislikeWindow(TemplateView):
    """
    Перезагрузка окна с последними дизлайками для записи сообщества
    """
    template_name="item_votes/c_dislike.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.dislikes = self.item.get_dislikes_for_item(request.user)[0:6]
        return super(ItemCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context

class ItemCommunityCommentLikeWindow(TemplateView):
    """
    Перезагрузка окна с последними лайками для комментария записи сообщества
    """
    template_name="item_votes/c_comment_like.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["comment_pk"])
        self.community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.likes = self.comment.get_likes_for_comment_item(request.user)[0:6]
        return super(ItemCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context

class ItemCommunityCommentDislikeWindow(TemplateView):
    """
    Перезагрузка окна с последними дизлайками для комментария записи сообщества
    """
    template_name="item_votes/c_comment_dislike.html"

    def get(self,request,*args,**kwargs):
        self.comment = ItemComment.objects.get(pk=self.kwargs["comment_pk"])
        self.community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.dislikes = self.comment.get_dislikes_for_comment_item(request.user)[0:6]
        return super(ItemCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context


class AllItemUserLikeWindow(View):
    """
    Окно со всеми лайками для записи пользователя
    """
    def get(self,request,*args,**kwargs):
        context = {}
        item = Item.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
            likes = item.get_likes_for_item(request.user)
        elif user == request.user:
            likes = item.get_likes_for_item(request.user)
        elif request.user.is_anonymous and user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not user.is_closed_profile():
            likes = item.get_likes_for_item(request.user)
        current_page = Paginator(likes, 15)
        page = request.GET.get('page')

        context['user'] = user
        try:
            context['likes'] = current_page.page(page)
        except PageNotAnInteger:
            context['likes'] = current_page.page(1)
        except EmptyPage:
            context['likes'] = current_page.page(current_page.num_pages)
        return render_to_response("item_votes/u_all_like.html", context)

class AllItemUserDislikeWindow(View):
    """
    Окно со всеми дизлайками для записи пользователя
    """
    def get(self,request,*args,**kwargs):
        context = {}
        item = Item.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
            dislikes = item.get_dislikes_for_item(request.user)
        elif user == request.user:
            dislikes = item.get_dislikes_for_item(request.user)
        elif request.user.is_anonymous and user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not user.is_closed_profile():
            dislikes = item.get_dislikes_for_item(request.user)
        current_page = Paginator(dislikes, 15)
        page = request.GET.get('page')
        context['user'] = user
        try:
            context['dislikes'] = current_page.page(page)
        except PageNotAnInteger:
            context['dislikes'] = current_page.page(1)
        except EmptyPage:
            context['dislikes'] = current_page.page(current_page.num_pages)
        return render_to_response("item_votes/u_all_dislike.html", context)

class AllItemUserCommentDislikeWindow(View):
    """
    Окно со всеми дизлайками для комментария записи пользователя
    """
    def get(self,request,*args,**kwargs):
        context = {}
        comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
            dislikes = comment.get_dislikes_for_comment_item(request.user)
        elif user == request.user:
            dislikes = comment.get_dislikes_for_comment_item(request.user)
        elif request.user.is_anonymous and user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not user.is_closed_profile():
            dislikes = self.comment.get_dislikes_for_comment_item(request.user)
        current_page = Paginator(dislikes, 15)
        page = request.GET.get('page')
        context['user'] = user
        try:
            context['dislikes'] = current_page.page(page)
        except PageNotAnInteger:
            context['dislikes'] = current_page.page(1)
        except EmptyPage:
            context['dislikes'] = current_page.page(current_page.num_pages)
        return render_to_response("item_votes/u_all_comment_dislike.html", context)

class AllItemUserCommentLikeWindow(View):
    """
    Окно со всеми лайками для комментария записи пользователя
    """
    def get(self,request,*args,**kwargs):
        context = {}
        comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
            likes = comment.get_likes_for_comment_item(request.user)
        elif user == request.user:
            likes = comment.get_likes_for_comment_item(request.user)
        elif request.user.is_anonymous and user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not user.is_closed_profile():
            likes = comment.get_likes_for_comment_item(request.user)
        current_page = Paginator(likes, 15)
        page = request.GET.get('page')
        context['request_user'] = request.user
        try:
            context['likes'] = current_page.page(page)
        except PageNotAnInteger:
            context['likes'] = current_page.page(1)
        except EmptyPage:
            context['likes'] = current_page.page(current_page.num_pages)
        return render_to_response("item_votes/u_all_comment_like.html", context)


class AllItemCommunityLikeWindow(View):
    """
    Окно со всеми лайками для записи сообщества
    """
    def get(self,request,*args,**kwargs):
        context = {}
        item = Item.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        likes = item.get_likes_for_item(request.user)
        current_page = Paginator(likes, 15)
        page = request.GET.get('page')
        context["community"]=community
        context['request_user'] = request.user
        try:
            context['likes'] = current_page.page(page)
        except PageNotAnInteger:
            context['likes'] = current_page.page(1)
        except EmptyPage:
            context['likes'] = current_page.page(current_page.num_pages)
        return render_to_response("item_votes/c_all_like.html", context)

class AllItemCommunityDislikeWindow(View):
    """
    Окно со всеми лайками для диззаписи сообщества
    """
    def get(self,request,*args,**kwargs):
        context = {}
        item = Item.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        dislikes = item.get_dislikes_for_item(request.user)
        current_page = Paginator(dislikes, 15)
        page = request.GET.get('page')
        context["community"]=community
        context['request_user'] = request.user
        try:
            context['dislikes'] = current_page.page(page)
        except PageNotAnInteger:
            context['dislikes'] = current_page.page(1)
        except EmptyPage:
            context['dislikes'] = current_page.page(current_page.num_pages)
        return render_to_response("item_votes/c_all_dislike.html", context)

class AllItemCommunityCommentLikeWindow(View):
    """
    Окно со всеми лайками для комментария к записи сообщества
    """
    def get(self,request,*args,**kwargs):
        context = {}
        comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        likes = comment.get_likes_for_comment_item(request.user)
        current_page = Paginator(likes, 15)
        page = request.GET.get('page')
        context["community"]=community
        context['request_user'] = request.user
        try:
            context['likes'] = current_page.page(page)
        except PageNotAnInteger:
            context['likes'] = current_page.page(1)
        except EmptyPage:
            context['likes'] = current_page.page(current_page.num_pages)
        return render_to_response("item_votes/c_all_comment_like.html", context)

class AllItemCommunityCommentDislikeWindow(View):
    """
    Окно со всеми дизлайками для комментария к записи сообщества
    """
    def get(self,request,*args,**kwargs):
        context = {}
        comment = ItemComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        dislikes = self.comment.get_dislikes_for_comment_item(request.user)
        current_page = Paginator(dislikes, 15)
        page = request.GET.get('page')
        context["community"]=community
        context['request_user'] = request.user
        try:
            context['dislikes'] = current_page.page(page)
        except PageNotAnInteger:
            context['dislikes'] = current_page.page(1)
        except EmptyPage:
            context['dislikes'] = current_page.page(current_page.num_pages)
        return render_to_response("item_votes/c_all_comment_dislike.html", context)

class AllItemUserRepostWindow(View):
    """
    Окно со всеми поделившимися записью пользователя
    """
    def get(self,request,*args,**kwargs):
        context = {}
        item = Item.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
            reposts = item.get_reposts()
        elif user == request.user:
            reposts = item.get_reposts()
        elif request.user.is_anonymous and user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not user.is_closed_profile():
            reposts = item.get_reposts()
        return render_to_response("item_votes/u_all_repost.html", context)


class AllItemCommunityRepostWindow(View):
    """
    Окно со всеми поделившимися записью сообщества
    """
    def get(self,request,*args,**kwargs):
        context = {}
        item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        reposts = item.get_reposts()
        current_page = Paginator(reposts, 15)
        page = request.GET.get('page')
        context["community"]=community
        context['request_user'] = request.user
        try:
            context['reposts'] = current_page.page(page)
        except PageNotAnInteger:
            context['reposts'] = current_page.page(1)
        except EmptyPage:
            context['reposts'] = current_page.page(current_page.num_pages)
        return render_to_response("item_votes/c_all_repost.html", context)
