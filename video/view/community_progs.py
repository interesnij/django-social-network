import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from communities.models import Community
from video.models import VideoAlbum, Video, VideoComment
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from video.forms import AlbumForm, VideoForm, CommentForm
from django.shortcuts import render
from common.check.community import check_can_get_lists
from django.views.generic import ListView
from common.template.video import get_permission_community_video


class VideoCommunityCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])

        if not self.video.comments_enabled:
            raise PermissionDenied('Комментарии для видеозаписи отключены')
        self.template_name = get_permission_community_photo(self.video.community, "c_video_comment/", "comments.html", request.user)

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name += "mob_"
        return super(VideoCommunityCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(VideoCommunityCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.video
        context['community'] = self.community
        return context

    def get_queryset(self):
        comments = self.video.get_comments()
        return comments


class VideoCommentCommunityCreate(View):

    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        video_comment = Video.objects.get(uuid=request.POST.get('uuid'))

        if not community.is_comment_video_send_all() and not request.user.is_member_of_community_with_name(community.name):
            raise PermissionDenied("Ошибка доступа.")
        elif community.is_comment_video_send_admin() and not request.user.is_staff_of_community_with_name(community.name):
            raise PermissionDenied("Ошибка доступа.")
        elif form_post.is_valid() and video_comment.comments_enabled:
            comment = form_post.save(commit=False)

            check_can_get_lists(request.user, community)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=None, video_comment=video_comment, text=comment.text)
                get_comment_attach(request, new_comment, "video_comment")
                if request.user.pk != video_comment.creator.pk:
                    new_comment.notification_community_comment(request.user, community)
                return render(request, 'c_video_comment/admin_parent.html',{'comment': new_comment, 'community': community})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class VideoReplyCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        parent = VideoComment.objects.get(pk=request.POST.get('video_comment'))

        if not community.is_comment_video_send_all() and not request.user.is_member_of_community_with_name(community.name):
            raise PermissionDenied("Ошибка доступа.")
        elif community.is_comment_video_send_admin() and not request.user.is_staff_of_community_with_name(community.name):
            raise PermissionDenied("Ошибка доступа.")
        elif form_post.is_valid() and parent.video_comment.comments_enabled:
            comment = form_post.save(commit=False)

            check_can_get_lists(request.user, community)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, video_comment=None, text=comment.text)
                get_comment_attach(request, new_comment, "video_comment")
                if request.user.pk != parent.commenter.pk:
                    new_comment.notification_community_reply_comment(request.user, community)
            else:
                return HttpResponseBadRequest()
            return render(request, 'c_video_comment/admin_reply.html',{'reply': new_comment, 'comment': parent, 'community': community})
        else:
            return HttpResponseBadRequest()

class VideoCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent_comment.post.community
        if request.user.is_staff_of_community_with_name(community.name):
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class VideoCommentCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent_comment.post.community
        if request.user.is_staff_of_community_with_name(community.name):
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class CommunityVideoDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            video.is_deleted = True
            video.save(update_fields=['is_deleted'])
        return HttpResponse("!")

class CommunityVideoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            video.is_deleted = False
            video.save(update_fields=['is_deleted'])
        return HttpResponse("!")


class CommunityOpenCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            video.comments_enabled = True
            video.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class CommunityCloseCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            video.comments_enabled = False
            video.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class CommunityOffVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            video.votes_on = False
            video.save(update_fields=['votes_on'])
        return HttpResponse("!")

class CommunityOnVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            video.votes_on = True
            video.save(update_fields=['votes_on'])
        return HttpResponse("!")

class CommunityOnPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            video.is_public = False
            video.save(update_fields=['is_public'])
        return HttpResponse("!")

class CommunityOffPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if video.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            video.is_public = True
            video.save(update_fields=['is_public'])
        return HttpResponse("!")


class CommunityVideoListCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(CommunityVideoListCreate,self).get_context_data(**kwargs)
        context["form_post"] = AlbumForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = AlbumForm(request.POST)
        community = Community.objects.get(pk=self.kwargs["pk"])

        if form_post.is_valid() and request.user.is_staff_of_community_with_name(community.name):
            new_album = form_post.save(commit=False)
            new_album.creator = request.user
            new_album.save()
            return render(request, 'c_video_list/my_list.html',{'album': new_album, 'community': community})
        else:
            return HttpResponseBadRequest()


class CommunityVideoAttachCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(CommunityVideoAttachCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = VideoForm(request.POST, request.FILES)
        community = Community.objects.get(pk=self.kwargs["pk"])

        if form_post.is_valid() and request.user.is_staff_of_community_with_name(community.name):
            try:
                my_list = VideoAlbum.objects.get(creator_id=self.user.pk, community=community, is_generic=True, title="Основной список")
            except:
                my_list = VideoAlbum.objects.create(creator_id=self.user.pk, community=community, is_generic=True, title="Основной список")
            new_video = form_post.save(commit=False)
            new_video.creator = request.user
            new_video.save()
            my_list.video_album.add(new_video)
            return render(request, 'video_new/video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()


class CommunityVideoInListCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(CommunityVideoInListCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        context["album"] = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        form_post = VideoForm(request.POST, request.FILES)
        community = Community.objects.get(pk=self.kwargs["pk"])

        if form_post.is_valid() and request.user.is_staff_of_community_with_name(community.name):
            try:
                album = VideoAlbum.objects.get(creator_id=request.pk, community=community, is_generic=True, title="Основной список")
            except:
                album = VideoAlbum.objects.create(creator_id=request.pk, community=community, is_generic=True, title="Основной список")
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
