import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo
from django.views.generic import ListView
from gallery.forms import AlbumForm, PhotoDescriptionForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.shortcuts import render
from common.template.photo import get_template_user_photo, get_permission_user_photo
from django.http import Http404


class UserGalleryView(TemplateView):
    """
    галерея для пользователя, своя галерея, галерея для анонима, плюс другие варианты
    """
    template_name = None
    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.pk == request.user.pk:
            self.albums_list = self.user.get_my_albums().order_by('-created')
        else:
            self.albums_list = self.user.get_albums().order_by('-created')

        self.template_name = get_template_user_photo(self.user, "gallery_user/", "gallery.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserGalleryView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserGalleryView,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['albums_list'] = self.albums_list
        return context

class UserAlbumView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])

        self.template_name = get_template_user_photo(self.user, "album_user/", "album.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserAlbumView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserAlbumView,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['album'] = self.album
        return context


class UserAddAvatar(View):
    """
    загрузка аватара пользователя
    """
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and user == request.user:
            photo_input = request.FILES.get('file')
            try:
                _album = Album.objects.get(creator=user, type=Album.AVATAR, community=None)
            except:
                _album = Album.objects.create(creator=user, type=Album.AVATAR, title="Фото со страницы", description="Фото с моей страницы")
            photo = Photo.objects.create(file=photo_input, creator=user)
            photo.album.add(_album)

            request.user.create_s_avatar(photo_input)
            request.user.create_b_avatar(photo_input)
            return render(request, 'u_photo/my_photo.html',{'object': photo, 'user': request.user})
        else:
            return HttpResponseBadRequest()

class PhotoUserCreate(View):
    """
    асинхронная мульти загрузка фотографий пользователя в основной альбом
    """
    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        photos = []
        if request.is_ajax() and self.user == request.user:
            try:
                _album = Album.objects.get(creator_id=self.user.id, community=None, type=Album.MAIN)
            except:
                _album = Album.objects.create(creator_id=self.user.id, community=None, type=Album.MAIN, title="Основной альбом")
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, creator=self.user)
                _album.photo_album.add(photo)
                photos += [photo,]

            return render(request, 'gallery_user/my_list.html',{'object_list': photos, 'user': request.user})
        else:
            raise Http404

class PhotoAlbumUserCreate(View):
    """
    асинхронная мульти загрузка фотографий пользователя в альбом
    """
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        _album = Album.objects.get(uuid=self.kwargs["uuid"])
        photos = []
        uploaded_file = request.FILES['file']
        if request.is_ajax() and user == request.user:
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, creator=user)
                _album.photo_album.add(photo)
                photos += [photo,]
            return render(request, 'album_user/my_list.html',{'object_list': photos, 'album': _album, 'user': request.user})
        else:
            raise Http404

class PhotoAttachUserCreate(View):
    """
    мульти сохранение изображений с моментальным выводом в превью
    """
    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        photos = []
        if request.is_ajax() and self.user == request.user:
            try:
                _album = Album.objects.get(creator=request.user, community=None, type=Album.WALL)
            except:
                _album = Album.objects.create(creator=request.user, community=None, type=Album.WALL, description="Фото со стены")
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, creator=self.user)
                _album.photo_album.add(photo)
                photos += [photo,]
            return render(request, 'gallery_user/my_list.html',{'object_list': photos, 'user': request.user})
        else:
            raise Http404

class AlbumUserCreate(TemplateView):
    """
    создание альбома пользователя
    """
    template_name = "album_user/add_album.html"
    form=None

    def get(self,request,*args,**kwargs):
        self.form = AlbumForm()
        self.user = User.objects.get(pk=self.kwargs["pk"])
        return super(AlbumUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AlbumUserCreate,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["user"] = self.user
        return context

    def post(self,request,*args,**kwargs):
        self.form = AlbumForm(request.POST)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and self.user == request.user:
            album = self.form.save(commit=False)
            if not album.description:
                album.description = "Без описания"
            new_album = Album.objects.create(title=album.title, description=album.description, type=Album.ALBUM, is_public=album.is_public, order=album.order,creator=self.user)
            return render(request, 'album_user/my_album.html',{'album': new_album, 'user': self.user})
        else:
            return HttpResponseBadRequest()
        return super(AlbumUserCreate,self).get(request,*args,**kwargs)


class UserPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.user, "gallery_user/", "list.html", request.user)
        else:
            raise Http404
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
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
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.user, "album_user/", "list.html", request.user)
        else:
            raise Http404
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserAlbumPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserAlbumPhotosList,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['album'] = self.album
        return context

    def get_queryset(self):
        photo_list = self.album.get_photos().order_by('-created')
        return photo_list


class UserPhoto(TemplateView):
    """
    страница фото, не имеющего альбома для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(creator=self.user, type=Album.MAIN)
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.user, "u_photo/photo/", "photo.html", request.user)
        else:
            raise Http404

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["album"] = self.album
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context


class UserAlbumPhoto(TemplateView):
    """
    страница отдельного фото в альбоме для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(creator=self.user, type=Album.ALBUM)
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.user, "u_photo/album_photo/", "photo.html", request.user)
        else:
            raise Http404

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserAlbumPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserAlbumPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["album"] = self.album
        context["user"] = self.user
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context


class UserWallPhoto(TemplateView):
    """
    страница отдельного фото альбома пользователя "Фото со стены"
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(creator=self.user, type=Album.WALL)
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.user, "u_photo/wall_photo/", "photo.html", request.user)
        else:
            raise Http404
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserWallPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserWallPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["album"] = self.album
        return context


class UserDetailAvatar(TemplateView):
    """
    страница отдельного фото аватаров (альбом "Фото со страницы") пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(creator=self.user, type=Album.AVATAR, community=None)
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.user, "u_photo/avatar/", "photo.html", request.user)
        else:
            raise Http404
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserDetailAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserDetailAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        context["album"] = self.album
        return context
