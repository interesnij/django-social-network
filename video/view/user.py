from django.views.generic.base import TemplateView
from users.models import User
from video.models import VideoAlbum
from django.views.generic import ListView


class UserBasicVideoList(ListView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_template_user(folder="user_basic_list/", template="list.html", request=request)
        if self.user == request.user:
            self.video_list = self.user.get_my_video()
        else:
            self.video_list = self.user.get_video()
        return super(UserBasicVideoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserBasicVideoList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        video_list = self.video_list
        return video_list


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


class UserCreateListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="user_create/", template="create_list.html", request=request)

        return super(UserCreateListWindow,self).get(request,*args,**kwargs)


class UserCreateListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="user_create/", template="create_video.html", request=request)

        return super(UserCreateListWindow,self).get(request,*args,**kwargs)
