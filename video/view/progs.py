from django.views.generic.base import TemplateView
from users.models import User
from video.models import VideoAlbum, Video
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from video.forms import AlbumForm, VideoForm
from django.shortcuts import render_to_response


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
            return render_to_response('user_video_list/my_list.html',{'album': new_album, 'user': request.user, 'request': request})
        else:
            return HttpResponseBadRequest()


class UserVideoCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(UserVideoCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = VideoForm(request.POST, request.FILES)
        user = User.objects.get(pk=self.kwargs["pk"])

        if form_post.is_valid() and request.user == user:
            try:
                my_list = VideoAlbum.objects.get(creator_id=request.user.pk, community=None, is_generic=True)
            except:
                my_list = VideoAlbum.objects.create(creator_id=request.user.pk, community=None, is_generic=True, name="Все видео")
            new_video = form_post.save(commit=False)
            new_video.creator = request.user
            new_video.save()
            my_list.add(new_video)
            return render_to_response('video_new/video.html',{'object': new_video, 'request': request})
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
        user = User.objects.get(uuid=self.kwargs["uuid"])

        if form_post.is_valid() and request.user == user:
            new_video = form_post.save(commit=False)
            new_video.creator = request.user
            new_video.save()
            return render_to_response('video_new/video.html',{'object': new_video, 'request': request})
        else:
            return HttpResponseBadRequest()
