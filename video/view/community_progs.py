import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from communities.models import Community
from video.models import VideoAlbum, Video, VideoComment
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from video.forms import AlbumForm, VideoForm
from django.shortcuts import render
from common.checkers import check_can_get_posts_for_community_with_name



class VideoCommunityCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])

        if not self.video.comments_enabled:
            raise PermissionDenied('Комментарии для фотографии отключены')
        elif request.user.is_authenticated:
            if request.user.is_staff_of_community_with_name(self.community.name):
                self.template_name = "c_video_comment/admin_comments.html"
            elif request.user.is_video_manager():
                self.template_name = "c_video_comment/staff_comments.html"
            elif check_can_get_posts_for_community_with_name(request.user, self.community.name):
                self.template_name = "c_video_comment/comments.html"
            else:
                self.template_name = "c_video_comment/comments.html"
        elif request.user.is_anonymous:
            if self.is_public():
                self.template_name = "c_video_comment/anon_comments.html"

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

        if form_post.is_valid() and video_comment.comments_enabled:
            comment = form_post.save(commit=False)

            check_can_get_posts_for_community_with_name(request.user, community.name)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.photo_comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=None, video_comment=video_comment, text=comment.text)
                get_comment_attach(request, new_comment)
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

        if form_post.is_valid() and parent.video_comment.comments_enabled:
            comment = form_post.save(commit=False)

            check_can_get_posts_for_community_with_name(request.user, community.name)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.photo_comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, video_comment=None, text=comment.text)
                get_comment_attach(request, new_comment)
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
                my_list = VideoAlbum.objects.get(creator_id=self.user.pk, community=community, is_generic=True, title="Все видео")
            except:
                my_list = VideoAlbum.objects.create(creator_id=self.user.pk, community=community, is_generic=True, title="Все видео")
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
                album = VideoAlbum.objects.get(creator_id=self.user.pk, community=community, is_generic=True, title="Все видео")
            except:
                album = VideoAlbum.objects.create(creator_id=self.user.pk, community=community, is_generic=True, title="Все видео")
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
