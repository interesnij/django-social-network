from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo
from gallery.helpers import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import ListView
from gallery.forms import AlbumForm, AvatarUserForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.shortcuts import render_to_response


class UserGalleryView(TemplateView):
    """
    галерея для пользователя, своя галерея, галерея для анонима, плюс другие варианты
    """
    template_name = None
    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.albums_list = self.user.get_albums().order_by('-created')
        self.template_name = self.user.get_template_user(folder="gallery_user/", template="gallery.html", request=request)
        return super(UserGalleryView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserGalleryView,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['albums_list'] = self.albums_list
        return context

class UserAlbumView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.user.get_template_user(folder="album_user/", template="album.html", request=request)
        return super(UserAlbumView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserAlbumView,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['album'] = self.album
        return context


class UserAddAvatar(TemplateView):
    """
    изменение аватара пользователя
    """
    template_name = "photo_user/user_add_avatar.html"

    def get(self,request,*args,**kwargs):
        self.form=AvatarUserForm()
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album=Album.objects.get(creator=request.user, title="Фото со страницы", is_generic=True, community=None)
        return super(UserAddAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserAddAvatar,self).get_context_data(**kwargs)
        context["form_avatar"]=self.form
        context["user"]=self.user
        context["album"]=self.album
        return context

    def post(self,request,*args,**kwargs):
        self.album=Album.objects.get(creator=request.user, title="Фото со страницы", is_generic=True, community=None)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.form=AvatarUserForm(request.POST,request.FILES)
        if self.form.is_valid() and self.user == request.user:
            avatar=self.form.save(commit=False)
            new_avatar=avatar.create_avatar(creator=request.user, community=None, file=avatar.file, is_public=True, album_2=self.album )
            if request.is_ajax():
                return HttpResponse ('!')
        else:
            return HttpResponse ('!!!')
        return super(UserAddAvatar,self).get(request,*args,**kwargs)


class PhotoUserCreate(View):
    """
    асинхронная мульти загрузка фотографий пользователя прямо в галерею
    """
    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        photos = []
        if self.user == request.user:
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, creator=self.user)
                photos += [photo,]
            return render_to_response('gallery_user/my_list.html',{'object_list': photos, 'user': request.user, 'request': request})


class PhotoCommentUserCreate(View):
    """
    мульти сохранение изображений для комментов с моментальным выводом в превью
    """
    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        photos = []
        if self.user == request.user:
            try:
                album = Album.objects.get(creator=request.user, is_generic=True, title="Фото со стены")
            except:
                album = Album.objects.create(creator=request.user, is_generic=True, title="Фото со стены")
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, album=album, creator=self.user)
                photos += [photo,]
            return render_to_response('gallery_user/my_list.html',{'object_list': photos, 'user': request.user, 'request': request})


class PhotoAlbumUserCreate(View):
    """
    асинхронная мульти загрузка фотографий пользователя в альбом
    """
    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        self.album = Album.objects.get(pk=self.kwargs["pk"])
        uploaded_file = request.FILES['file']
        if self.user == request.user:
            Photo.objects.create(album=self.album, file=uploaded_file, creator=self.user)
            return HttpResponse ('!')


class AlbumUserCreate(TemplateView):
    """
    создание альбома пользователя
    """
    template_name="album_user/add_album.html"
    form=None

    def get(self,request,*args,**kwargs):
        self.form=AlbumForm()
        self.user = User.objects.get(pk=self.kwargs["pk"])
        return super(AlbumUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(AlbumUserCreate,self).get_context_data(**kwargs)
        context["form"]=self.form
        context["user"]=self.user
        return context

    def post(self,request,*args,**kwargs):
        self.form = AlbumForm(request.POST)
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.form.is_valid() and self.user == request.user and request.is_ajax():
            album = self.form.save(commit=False)
            if not.album.description:
                album.description = "Без описания"
            new_album = Album.objects.create(title=album.title, description=album.description, is_generic=False, is_public=album.is_public, order=album.order,creator=self.user)
        else:
            return HttpResponseBadRequest()
        return super(AlbumUserCreate,self).get(request,*args,**kwargs)


class UserPhotosList(ListView):
    template_name = None
    model = Photo
    paginate_by = 30

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.user.get_permission_list_user(folder="gallery_user/", template="list.html", request=request)
        return super(UserPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhotosList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        photo_list = self.user.get_photos().order_by('-created')
        return photo_list

class UserAlbumPhotosList(ListView):
    template_name = None
    paginate_by = 30

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.user.get_permission_list_user(folder="album_user/", template="list.html", request=request)
        return super(UserAlbumPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserAlbumPhotosList,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['album'] = self.album
        return context

    def get_queryset(self):
        photo_list = self.user.get_photos_for_album(album_id=self.album.pk).order_by('-created')
        return photo_list
