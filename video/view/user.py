from django.views.generic.base import TemplateView
from users.models import User
from video.models import VideoAlbum, Video
from django.views.generic import ListView
from video.forms import VideoForm


class UserVideoList(ListView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        self.album = VideoAlbum.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_template_user(folder="user_album_list/", template="list.html", request=request)
        if self.user == request.user:
            self.video_list = self.album.get_my_queryset()
        else:
            self.video_list = self.album.get_queryset()
        return super(UserVideoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoList,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['album'] = self.album
        return context

    def get_queryset(self):
        video_list = self.video_list
        return video_list


class UserVideoDetail(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        import re
        from stst.models import VideoNumbers

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.user.get_template_user(folder="u_video_detail/", template="video.html", request=request)
        if request.user.is_authenticated:
            try:
                VideoNumbers.objects.get(user=request.user.pk, video=self.video.pk)
            except:
                MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
                if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
                    VideoNumbers.objects.create(user=request.user.pk, video=self.video.pk, platform=1)
                else:
                    VideoNumbers.objects.create(user=request.user.pk, video=self.video.pk, platform=0)
        return super(UserVideoDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoDetail,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['object'] = self.video
        return context


class UserCreateVideoWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="user_create/", template="create_video.html", request=request)

        return super(UserCreateVideoWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserCreateVideoWindow,self).get_context_data(**kwargs)
        context['form_post'] = VideoForm()
        return context


class UserCreateVideoAttachWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="user_create/", template="create_video_attach.html", request=request)

        return super(UserCreateVideoAttachWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserCreateVideoAttachWindow,self).get_context_data(**kwargs)
        context['form_post'] = VideoForm()
        return context

class UserCreateListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="user_create/", template="create_list.html", request=request)
        return super(UserCreateListWindow,self).get(request,*args,**kwargs)


class UserCreateVideoListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        self.album = VideoAlbum.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="user_create/", template="create_list_video.html", request=request)
        return super(UserCreateVideoListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserCreateVideoListWindow,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['album'] = self.album
        context['form_post'] = VideoForm({'album': self.album})
        return context
