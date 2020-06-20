from django.views.generic.base import TemplateView
from django.views.generic import ListView
from users.models import User
from posts.models import Post, PostComment
from communities.models import Community
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.model.votes import PostVotes, PostCommentVotes
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from common.checkers import check_can_get_posts_for_community_with_name
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render_to_response


class PostUserLikeWindow(TemplateView):
    """
    Перезагрузка окна с последними лайками для записи пользователя
    """
    template_name="post_votes/u_like.html"

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.likes = self.item.window_likes()
        elif self.user == request.user:
            self.likes = self.item.window_likes()
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.likes = self.item.window_likes()
        return super(PostUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context

class PostUserCommentLikeWindow(TemplateView):
    """
    Перезагрузка окна с последними дизлайками для записи пользователя
    """
    template_name="post_votes/u_comment_like.html"

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.likes = self.comment.window_likes()
        elif self.user == request.user:
            self.likes = self.comment.window_likes()
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.likes = self.comment.window_likes()
        return super(PostUserCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context

class PostUserDislikeWindow(TemplateView):
    """
    Перезагрузка окна с последними лайками для комментария записи пользователя
    """
    template_name="post_votes/u_dislike.html"

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.dislikes = self.item.window_dislikes()
        elif self.user == request.user:
            self.dislikes = self.item.window_dislikes()
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.dislikes = self.item.window_dislikes()
        return super(PostUserDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context

class PostUserCommentDislikeWindow(TemplateView):
    """
    Перезагрузка окна с последними дизлайками для комментария записи пользователя
    """
    template_name="post_votes/u_comment_dislike.html"

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.dislikes = self.comment.window_dislikes()
        elif self.user == request.user:
            self.dislikes = self.comment.window_dislikes()
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.dislikes = self.comment.window_dislikes()
        return super(PostUserCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context


class PostCommunityLikeWindow(TemplateView):
    """
    Перезагрузка окна с последними лайками для записи сообщества
    """
    template_name="post_votes/c_like.html"

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.likes = self.item.window_likes()
        return super(PostCommunityLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostCommunityLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context

class PostCommunityDislikeWindow(TemplateView):
    """
    Перезагрузка окна с последними дизлайками для записи сообщества
    """
    template_name="post_votes/c_dislike.html"

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        self.dislikes = self.item.window_dislikes()
        return super(PostCommunityDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostCommunityDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context

class PostCommunityCommentLikeWindow(TemplateView):
    """
    Перезагрузка окна с последними лайками для комментария записи сообщества
    """
    template_name="post_votes/c_comment_like.html"

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_posts_for_community_with_name(request.user,self.community.name)
        self.likes = self.comment.window_likes()
        return super(PostCommunityCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostCommunityCommentLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context

class PostCommunityCommentDislikeWindow(TemplateView):
    """
    Перезагрузка окна с последними дизлайками для комментария записи сообщества
    """
    template_name="post_votes/c_comment_dislike.html"

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_posts_for_community_with_name(request.user,self.community.name)
        self.dislikes = self.comment.window_dislikes()
        return super(PostCommunityCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostCommunityCommentDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context


class AllPostUserLikeWindow(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.item.creator.get_permission_list_user(folder="all_post_votes/", template="u_like.html", request=request)
        return super(AllPostUserLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllPostUserLikeWindow,self).get_context_data(**kwargs)
        context['item'] = self.item
        return context

    def get_queryset(self): 
        likes = self.item.get_liker(self.item.creator)
        return likes


class AllPostUserDislikeWindow(View):
    """
    Окно со всеми дизлайками для записи пользователя
    """
    def get(self,request,*args,**kwargs):
        context = {}
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
            dislikes = item.dislikes()
        elif user == request.user:
            dislikes = item.dislikes()
        elif request.user.is_anonymous and user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not user.is_closed_profile():
            dislikes = item.dislikes()
        current_page = Paginator(dislikes, 15)
        page = request.GET.get('page')
        context['user'] = user
        try:
            context['dislikes'] = current_page.page(page)
        except PageNotAnInteger:
            context['dislikes'] = current_page.page(1)
        except EmptyPage:
            context['dislikes'] = current_page.page(current_page.num_pages)
        return render_to_response("post_votes/u_all_dislike.html", context)

class AllPostUserCommentDislikeWindow(View):
    """
    Окно со всеми дизлайками для комментария записи пользователя
    """
    def get(self,request,*args,**kwargs):
        context = {}
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
            dislikes = comment.dislikes()
        elif user == request.user:
            dislikes = comment.dislikes()
        elif request.user.is_anonymous and user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not user.is_closed_profile():
            dislikes = self.comment.dislikes()
        current_page = Paginator(dislikes, 15)
        page = request.GET.get('page')
        context['user'] = user
        try:
            context['dislikes'] = current_page.page(page)
        except PageNotAnInteger:
            context['dislikes'] = current_page.page(1)
        except EmptyPage:
            context['dislikes'] = current_page.page(current_page.num_pages)
        return render_to_response("post_votes/u_all_comment_dislike.html", context)

class AllPostUserCommentLikeWindow(View):
    """
    Окно со всеми лайками для комментария записи пользователя
    """
    def get(self,request,*args,**kwargs):
        context = {}
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
            likes = comment.dislikes()
        elif user == request.user:
            likes = comment.dislikes()
        elif request.user.is_anonymous and user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not user.is_closed_profile():
            likes = comment.dislikes()
        current_page = Paginator(likes, 15)
        page = request.GET.get('page')
        context['request_user'] = request.user
        try:
            context['likes'] = current_page.page(page)
        except PageNotAnInteger:
            context['likes'] = current_page.page(1)
        except EmptyPage:
            context['likes'] = current_page.page(current_page.num_pages)
        return render_to_response("post_votes/u_all_comment_like.html", context)


class AllPostCommunityLikeWindow(View):
    """
    Окно со всеми лайками для записи сообщества
    """
    def get(self,request,*args,**kwargs):
        context = {}
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        likes = item.likes()
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
        return render_to_response("post_votes/c_all_like.html", context)

class AllPostCommunityDislikeWindow(View):
    """
    Окно со всеми лайками для диззаписи сообщества
    """
    def get(self,request,*args,**kwargs):
        context = {}
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        dislikes = item.dislikes()
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
        return render_to_response("post_votes/c_all_dislike.html", context)

class AllPostCommunityCommentLikeWindow(View):
    """
    Окно со всеми лайками для комментария к записи сообщества
    """
    def get(self,request,*args,**kwargs):
        context = {}
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        likes = comment.likes()
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
        return render_to_response("post_votes/c_all_comment_like.html", context)

class AllPostCommunityCommentDislikeWindow(View):
    """
    Окно со всеми дизлайками для комментария к записи сообщества
    """
    def get(self,request,*args,**kwargs):
        context = {}
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        dislikes = self.comment.dislikes()
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
        return render_to_response("post_votes/c_all_comment_dislike.html", context)

class AllPostUserRepostWindow(View):
    """
    Окно со всеми поделившимися записью пользователя
    """
    def get(self,request,*args,**kwargs):
        context = {}
        item = Post.objects.get(pk=self.kwargs["pk"])
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
        return render_to_response("post_votes/u_all_repost.html", context)


class AllPostCommunityRepostWindow(View):
    """
    Окно со всеми поделившимися записью сообщества
    """
    def get(self,request,*args,**kwargs):
        context = {}
        item = Post.objects.get(pk=self.kwargs["pk"])
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
        return render_to_response("post_votes/c_all_repost.html", context)
