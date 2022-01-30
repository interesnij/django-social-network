from django.views.generic.base import TemplateView
from users.models import User
from video.models import Video, VideoComment, VideoList
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from django.views.generic import ListView
from video.forms import VideoForm, CommentForm
from rest_framework.exceptions import PermissionDenied
from common.templates import get_settings_template, render_for_platform


class UserVideoDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.delete_item(None)
            return HttpResponse()
        else:
            raise Http404

class UserVideoRecover(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.restore_item(None)
            return HttpResponse()
        else:
            raise Http404

class UserOpenCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.comments_enabled = True
            video.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserCloseCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.comments_enabled = False
            video.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserOffVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.votes_on = False
            video.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.votes_on = True
            video.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.make_private()
            return HttpResponse()
        else:
            raise Http404

class UserOffPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and video.creator == request.user:
            video.make_publish()
            return HttpResponse()
        else:
            raise Http404

class UserVideoCreate(TemplateView):
    template_name, form_post  = None, None
    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("video/user_create/create_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from video.models import VideoList
        from video.forms import VideoForm

        context = super(UserVideoCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        context['video_lists'] = VideoList.get_user_staff_lists(self.request.user.pk)
        return context

    def post(self,request,*args,**kwargs):
        from video.forms import VideoForm

        self.form_post = VideoForm(request.POST, request.FILES)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form_post.is_valid():
            video = self.form_post.save(commit=False)
            new_video = video.create_video(creator=request.user,image=video.image, title=video.title,file=video.file,uri=video.uri,description=video.description,list=video.list,comments_enabled=video.comments_enabled,votes_on=video.votes_on,community=None)
            return render_for_platform(request, 'video/video_new/video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()

class UserVideoEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("video/user_create/edit.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoEdit,self).get_context_data(**kwargs)
        context["form"] = VideoForm()
        context["sub_categories"] = VideoSubCategory.objects.only("id")
        context["categories"] = VideoCategory.objects.only("id")
        context["video"] = Video.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.video = Video.objects.get(pk=self.kwargs["pk"])
        self.form = VideoForm(request.POST,request.FILES, instance=self.video)

        if request.is_ajax() and self.form.is_valid() and request.user == self.user:
            video = self.form.save(commit=False)
            new_video = video.edit_video(
                                        title=new_video.title,
                                        file=new_video.file,
                                        uri=new_video.uri,
                                        description=new_video.description,
                                        list=new_video.list,
                                        comments_enabled=new_video.comments_enabled,
                                        votes_on=new_video.votes_on)
            return render_for_platform(request, 'video/video_new/video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()
