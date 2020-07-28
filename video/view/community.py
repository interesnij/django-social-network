import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from communities.models import Community
from video.models import VideoAlbum, Video
from django.views.generic import ListView
from video.forms import VideoForm


class CommunityVideoList(ListView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.community.get_template(folder="c_album_list/", template="list.html", request_user=request.user)
        if request.user.is_staff_of_community_with_name(self.community.name):
            self.video_list = self.album.get_my_queryset()
        else:
            self.video_list = self.album.get_queryset()
        return super(CommunityVideoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityVideoList,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['album'] = self.album
        return context

    def get_queryset(self):
        video_list = self.video_list
        return video_list


class CommunityVideoDetail(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from stst.models import VideoNumbers

        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.community.get_template(folder="c_video_detail/", template="video.html", request_user=request.user)
        if request.user.is_authenticated:
            try:
                VideoNumbers.objects.get(user=request.user.pk, video=self.video.pk)
            except:
                if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
                    VideoNumbers.objects.create(user=request.user.pk, video=self.video.pk, platform=1)
                else:
                    VideoNumbers.objects.create(user=request.user.pk, video=self.video.pk, platform=0)
        return super(CommunityVideoDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityVideoDetail,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['object'] = self.video
        return context


class CommunityCreateVideoAttachWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.community.get_manage_template(folder="community_create/", template="create_video_attach.html", request=request)

        return super(CommunityCreateVideoAttachWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityCreateVideoAttachWindow,self).get_context_data(**kwargs)
        context['form_post'] = VideoForm()
        return context

class CommunityCreateListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.community.get_manage_template(folder="community_create/", template="create_list.html", request=request)
        return super(CommunityCreateListWindow,self).get(request,*args,**kwargs)


class CommunityCreateVideoListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.community.get_manage_template(folder="community_create/", template="create_list_video.html", request=request)
        return super(CommunityCreateVideoListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserCreateVideoListWindow,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['album'] = self.album
        context['form_post'] = VideoForm({'album': self.album})
        return context
