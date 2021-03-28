
from django.views.generic.base import TemplateView
from users.models import User
from video.models import Video, VideoComment, VideoAlbum
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from users.models import User
from django.views.generic import ListView
from video.forms import AlbumForm, VideoForm, CommentForm
from rest_framework.exceptions import PermissionDenied
from common.template.video import get_permission_user_video
from django.http import Http404
from common.template.user import get_settings_template, render_for_platform


class UserVideoAlbumAdd(View):
    def get(self,request,*args,**kwargs):
        list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.users.add(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class UserVideoAlbumRemove(View):
    def get(self,request,*args,**kwargs):
        list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.users.remove(request.user)
            return HttpResponse()
        else:
            return HttpResponse()


class VideoCommentUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        video = Video.objects.get(uuid=request.POST.get('uuid'))

        if request.is_ajax() and form_post.is_valid() and video.comments_enabled:
            comment = form_post.save(commit=False)
            if request.user.pk != user.pk:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items'):
                from common.notify.notify import user_notify

                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, video=video, text=comment.text)
                user_notify(request.user, video.creator.pk, None, "vic"+str(new_comment.pk)+", vid"+str(video.pk), "u_video_comment_notify", "COM")
                return render_for_platform(request, 'video/u_video_comment/my_parent.html',{'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class VideoReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        parent = VideoComment.objects.get(pk=request.POST.get('video_comment'))

        if request.is_ajax() and form_post.is_valid() and parent.video_comment.comments_enabled:
            comment = form_post.save(commit=False)

            if request.user != user:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items'):
                from common.notify.notify import user_notify

                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, video=None, text=comment.text)
                user_notify(request.user, parent.post.creator.pk, None, "vir"+str(new_comment.pk)+",vic"+str(parent.pk)+",pos"+str(parent.post.pk), "u_post_comment_notify", "REP")
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'video/u_video_comment/my_reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class VideoCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.delete_comment(self)
            return HttpResponse()
        else:
            raise Http404

class VideoCommentUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.abort_delete_comment(self)
            return HttpResponse()
        else:
            raise Http404

class UserVideoDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.delete_video()
            return HttpResponse()
        else:
            raise Http404

class UserVideoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.abort_delete_video()
            return HttpResponse()
        else:
            raise Http404

class UserOpenCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.comments_enabled = True
            video.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserCloseCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.comments_enabled = False
            video.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserOffVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.votes_on = False
            video.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.votes_on = True
            video.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.is_public = False
            video.save(update_fields=['is_public'])
            return HttpResponse()
        else:
            raise Http404

class UserOffPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.is_public = True
            video.save(update_fields=['is_public'])
            return HttpResponse()
        else:
            raise Http404

class VideoWallCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == user.pk:
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class UserVideoListCreate(TemplateView):
    form_post = None
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("video/user_create/create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoListCreate,self).get_context_data(**kwargs)
        context["form_post"] = AlbumForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = AlbumForm(request.POST)
        self.user = User.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and self.form_post.is_valid() and request.user == self.user:
            new_album = self.form_post.save(commit=False)
            new_album.creator = request.user
            new_album.save()
            return render_for_platform(request, 'users/user_video_list/my_list.html',{'album': new_album, 'user': request.user})
        else:
            return HttpResponseBadRequest()


class UserVideoAttachCreate(TemplateView):
    form_post = None
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("video/user_create/create_video_attach.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoAttachCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoAttachCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = VideoForm(request.POST, request.FILES)
        self.user = User.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form_post.is_valid() and request.user == self.user:
            self.my_list = VideoAlbum.objects.get(creator_id=self.user.pk, community__isnull=True, type=VideoAlbum.MAIN)
            new_video = self.form_post.save(commit=False)
            new_video.creator = request.user
            new_video.save()
            my_list.video_album.add(new_video)
            return render_for_platform(request, 'video/video_new/video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()


class UserVideoCreate(TemplateView):
    form_post = None
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("video/user_create/create_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = VideoForm(request.POST, request.FILES)
        self.user = User.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and self.form_post.is_valid() and request.user == self.user:
            from common.notify.notify import user_notify

            new_video = self.form_post.save(commit=False)
            new_video.creator = request.user
            albums = request.POST.getlist("album")
            new_video.save()
            for _album_pk in albums:
                _album = VideoAlbum.objects.get(pk=_album_pk)
                _album.video_album.add(new_video)
            if new_video.is_public:
                user_notify(request.user, new_video.creator.pk, None, "vid"+str(new_video.pk), "u_video_create", "ITE")
            return render_for_platform(request, 'video/video_new/video.html',{'object': new_video})
        else:
            return HttpResponse()


class UserVideoAlbumPreview(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.album = VideoAlbum.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_settings_template("users/user_video/album_preview.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVideoAlbumPreview,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideoAlbumPreview,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context


class UserVideolistEdit(TemplateView):
    """
    изменение списка видео пользователя
    """
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("video/user_create/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideolistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideolistEdit,self).get_context_data(**kwargs)
        context["user"] = self.user
        context["album"] = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        self.form = AlbumForm(request.POST,instance=self.list)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and self.user == request.user:
            list = self.form.save(commit=False)
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserVideolistEdit,self).get(request,*args,**kwargs)

class UserVideolistDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and user == request.user and list.type == VideoAlbum.ALBUM:
            list.is_deleted = True
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class UserVideolistAbortDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and user == request.user:
            list.is_deleted = False
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404
