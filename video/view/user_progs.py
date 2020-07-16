import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from users.models import User
from video.models import Video, VideoComment
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.shortcuts import render
from users.models import User
from django.views.generic import ListView
from video.forms import AlbumForm, VideoForm, CommentForm
from rest_framework.exceptions import PermissionDenied
from django.views.generic import ListView


class VideoUserCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if not self.video.comments_enabled:
            raise PermissionDenied('Комментарии для ролика отключены')
        elif request.user.is_authenticated:
            if self.user.pk == request.user.pk:
                self.template_name = "u_video_comment/my_comments.html"
            elif request.user.is_video_manager():
                self.template_name = "u_video_comment/staff_comments.html"
            elif self.user != request.user:
                check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
                if self.user.is_closed_profile():
                    check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
                self.template_name = "u_video_comment/comments.html"
        elif request.user.is_anonymous:
            if self.user.is_closed_profile():
                raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
            else:
                self.template_name = "u_video_comment/anon_comments.html"
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + template_name
        return super(VideoUserCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(VideoUserCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.video
        context['user'] = self.user
        return context

    def get_queryset(self):
        comments = self.video.get_comments()
        return comments


class VideoCommentUserCreate(View):

    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        video_comment = Video.objects.get(uuid=request.POST.get('uuid'))

        if form_post.is_valid() and video_comment.comments_enabled:
            comment = form_post.save(commit=False)
            if request.user.pk != user.pk:
                check_is_not_blocked_with_user_with_id(user=request.user, user_id = user.pk)
                if user.is_closed_profile():
                    check_is_connected_with_user_with_id(user=request.user, user_id = user.pk)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.photo_comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=None, video_comment=video_comment, text=comment.text)
                get_comment_attach(request, new_comment)
                if request.user.pk != photo_comment.creator.pk:
                    new_comment.notification_user_comment(request.user)
                return render(request, 'u_video_comment/my_parent.html',{'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class VideoReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        parent = VideoComment.objects.get(pk=request.POST.get('video_comment'))

        if form_post.is_valid() and parent.video_comment.comments_enabled:
            comment = form_post.save(commit=False)

            if request.user != user:
                check_is_not_blocked_with_user_with_id(user=request.user, user_id = user.id)
                if user.is_closed_profile():
                    check_is_connected_with_user_with_id(user=request.user, user_id = user.id)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.photo_comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, video_comment=None, text=comment.text)
                get_comment_attach(request, new_comment)
                if request.user.pk != parent.commenter.pk:
                    new_comment.notification_user_reply_comment(request.user)
            else:
                return HttpResponseBadRequest()
            return render(request, 'u_video_comment/my_reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class VideoCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == comment.commenter.pk:
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class VideoCommentUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == comment.commenter.pk:
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class UserVideoDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user:
            video.is_deleted = True
            video.save(update_fields=['is_deleted'])
        return HttpResponse("!")

class UserVideoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user:
            video.is_deleted = False
            video.save(update_fields=['is_deleted'])
        return HttpResponse("!")


class UserOpenCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user:
            video.comments_enabled = True
            video.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class UserCloseCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user:
            video.comments_enabled = False
            video.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class UserOffVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user:
            video.votes_on = False
            video.save(update_fields=['votes_on'])
        return HttpResponse("!")

class UserOnVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user:
            video.votes_on = True
            video.save(update_fields=['votes_on'])
        return HttpResponse("!")

class UserOnPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user:
            video.is_public = False
            video.save(update_fields=['is_public'])
        return HttpResponse("!")

class UserOffPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user:
            video.is_public = True
            video.save(update_fields=['is_public'])
        return HttpResponse("!")


class VideoWallCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")


class UserVideoListCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(UserVideoListCreate,self).get_context_data(**kwargs)
        context["form_post"] = AlbumForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = AlbumForm(request.POST)
        user = User.objects.get(pk=self.kwargs["pk"])

        if form_post.is_valid() and request.user == user:
            new_album = form_post.save(commit=False)
            new_album.creator = request.user
            new_album.save()
            return render(request, 'u_video_list/my_list.html',{'album': new_album, 'user': request.user})
        else:
            return HttpResponseBadRequest()


class UserVideoAttachCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(UserVideoAttachCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = VideoForm(request.POST, request.FILES)
        user = User.objects.get(pk=self.kwargs["pk"])

        if form_post.is_valid() and request.user == user:
            try:
                my_list = VideoAlbum.objects.get(creator_id=self.user.pk, community=None, is_generic=True, title="Все видео")
            except:
                my_list = VideoAlbum.objects.create(creator_id=self.user.pk, community=None, is_generic=True, title="Все видео")
            new_video = form_post.save(commit=False)
            new_video.creator = request.user
            new_video.save()
            my_list.video_album.add(new_video)
            return render(request, 'video_new/video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()


class UserVideoInListCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(UserVideoInListCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        context["album"] = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        form_post = VideoForm(request.POST, request.FILES)
        user = User.objects.get(pk=self.kwargs["pk"])

        if form_post.is_valid() and request.user == user:
            try:
                album = VideoAlbum.objects.get(creator_id=self.user.pk, community=None, is_generic=True, title="Все видео")
            except:
                album = VideoAlbum.objects.create(creator_id=self.user.pk, community=None, is_generic=True, title="Все видео")
            new_video = form_post.save(commit=False)
            new_video.creator = request.user
            albums = form_post.cleaned_data.get("album")
            new_video.save()
            if not new_video.album:
                new_video.album = album
            else:
                for album in albums:
                    album.video_album.add(new_video)

            return render(request, 'video_new/video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()
