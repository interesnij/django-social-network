from django.views.generic.base import TemplateView
from communities.models import Community
from video.models import VideoList, Video, VideoComment
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from video.forms import VideoForm
from common.check.community import check_can_get_lists
from django.views.generic import ListView
from common.templates import render_for_platform


class CommunityVideoDelete(View):
    def get(self,request,*args,**kwargs):
        video, c = Video.objects.get(pk=self.kwargs["video_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_administrator_of_community(c.pk):
            video.delete_video(c)
            return HttpResponse()
        else:
            raise Http404

class CommunityVideoRecover(View):
    def get(self,request,*args,**kwargs):
        video, c = Video.objects.get(pk=self.kwargs["video_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_administrator_of_community(c.pk):
            video.restore_video(c)
            return HttpResponse()
        else:
            raise Http404

class CommunityOpenCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["video_pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_administrator_of_community(photo.community.pk):
            video.comments_enabled = True
            video.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class CommunityCloseCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["video_pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_administrator_of_community(photo.community.pk):
            video.comments_enabled = False
            video.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOffVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["video_pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_administrator_of_community(photo.community.pk):
            video.votes_on = False
            video.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOnVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["video_pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_administrator_of_community(photo.community.pk):
            video.votes_on = True
            video.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOnPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["video_pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_administrator_of_community(photo.community.pk):
            video.make_private()
            return HttpResponse()
        else:
            raise Http404

class CommunityOffPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(pk=self.kwargs["video_pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_administrator_of_community(photo.community.pk):
            video.make_publish()
            return HttpResponse()
        else:
            raise Http404

class CommunityVideoEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("video/community_create/edit.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityVideoEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityVideoEdit,self).get_context_data(**kwargs)
        context["form"] = VideoForm()
        context["sub_categories"] = VideoSubCategory.objects.only("id")
        context["categories"] = VideoCategory.objects.only("id")
        context["video"] = Video.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.video = Video.objects.get(pk=self.kwargs["pk"])
        self.form = VideoForm(request.POST,request.FILES, instance=self.video)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and self.form.is_valid() and request.user.pk.is_administrator_of_community(self.kwargs["pk"]):
            new_video = self.form.save(commit=False)
            new_video = self.video.edit_video(
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
