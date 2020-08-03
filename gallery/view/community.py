import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from users.models import User
from communities.models import Community
from gallery.models import Album, Photo
from django.views.generic import ListView
from gallery.forms import AlbumForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from common.template.photo import get_template_community_photo, get_permission_community_photo
from common.check.community import check_can_get_lists
from django.http import Http404


class CommunityAddAvatar(View):
    """
    загрузка аватара сообщества
    """
    def post(self, request, *args, **kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator_of_community_with_name(community.name):
            photo_input = request.FILES.get('file')
            try:
                _album = Album.objects.get(community=community, is_generic=True, title="Фото со страницы")
            except:
                _album = Album.objects.create(creator=request.user, community=community, is_generic=True, title="Фото со страницы", description="Фото со страницы сообщества")
            photo = Photo.objects.create(file=photo_input, creator=request.user, community=community)
            _album.album.add(photo)
            community.create_s_avatar(photo_input)
            community.create_b_avatar(photo_input)
            return render(request, 'c_photo/admin_photo.html',{'object': photo, 'community': community})
        else:
            return HttpResponseBadRequest()


class CommunityGalleryView(TemplateView):
    """
    галерея для пользователя, своя галерея, галерея для анонима, плюс другие варианты
    """
    template_name = None
    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.albums_list = self.community.get_albums().order_by('-created')

        self.template_name = get_template_community_photo(self.community, "gallery_community/", "gallery.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(CommunityGalleryView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityGalleryView,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['albums_list'] = self.albums_list
        return context

class CommunityAlbumView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = get_template_community_photo(self.community, "album_community/", "album.html", request.user)

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(CommunityAlbumView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityAlbumView,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['album'] = self.album
        return context

class PhotoCommunityCreate(View):
    """
    асинхронная мульти загрузка фотографий пользователя прямо в галерею
    """
    def post(self, request, *args, **kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            photos = []
            check_can_get_lists(request.user, community)
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, community=community, creator=request.user)
                photos += [photo,]
            return render(request, 'gallery_community/admin_list.html',{'object_list': photos, 'community': community})
        else:
            raise Http404

class PhotoAlbumCommunityCreate(View):
    """
    асинхронная мульти загрузка фотографий пользователя в альбом
    """
    def post(self, request, *args, **kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        _album = Album.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            photos = []
            uploaded_file = request.FILES['file']
            check_can_get_lists(request.user, community)
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, community=community, creator=request.user)
                _album.album.add(photo)
                photos += [photo,]
            return render(request, 'album_community/admin_list.html',{'object_list': photos, 'album': _album, 'community': community})
        else:
            raise Http404

class PhotoAttachCommunityCreate(View):
    """
    мульти сохранение изображений с моментальным выводом в превью
    """
    def post(self, request, *args, **kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            photos = []
            check_can_get_lists(request.user, community)
            try:
                _album = Album.objects.get(creator=request.user, is_generic=True, title="Фото со стены", community=community)
            except:
                _album = Album.objects.create(creator=request.user, is_generic=True, title="Фото со стены", community=community, description="Фото, прикрепленные к записям и комментариям")
            for p in request.FILES.getlist('file'):
                photo = Photo.objects.create(file=p, creator=request.user)
                _album.album.add(photo)
                photos += [photo,]
            return render(request, 'gallery_community/list.html',{'object_list': photos, 'community': community})
        else:
            raise Http404

class AlbumCommunityCreate(TemplateView):
    """
    создание альбома пользователя
    """
    template_name="album_community/add_album.html"
    form=None

    def get(self,request,*args,**kwargs):
        self.form = AlbumForm()
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        return super(AlbumCommunityCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(AlbumCommunityCreate,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["community"] = self.community
        return context

    def post(self,request,*args,**kwargs):
        self.form = AlbumForm(request.POST)
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and request.user.is_administrator_of_community_with_name(self.community.name):
            album = self.form.save(commit=False)
            if not album.description:
                album.description = "Без описания"
            new_album = Album.objects.create(title=album.title, description=album.description, is_generic=False, is_public=album.is_public, order=album.order,creator=request.user, community=self.community)
            return render(request, 'album_community/admin_album.html',{'album': new_album, 'community': self.community})
        else:
            return HttpResponseBadRequest()
        return super(AlbumCommunityCreate,self).get(request,*args,**kwargs)


class CommunityPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            self.template_name = get_permission_community_photo(self.community, "gallery_community/", "list.html", request.user)
        else:
			raise Http404
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name += "mob_"
        return super(CommunityPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityPhotosList,self).get_context_data(**kwargs)
        context['community'] = self.community
        return context

    def get_queryset(self):
        photo_list = self.community.get_photos().order_by('-created')
        return photo_list

class CommunityAlbumPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            self.template_name = get_permission_community_photo(self.community, "album_community/", "list.html", request.user)
        else:
            raise Http404
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(CommunityAlbumPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityAlbumPhotosList,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['album'] = self.album
        return context

    def get_queryset(self):
        photo_list = self.community.get_photos_for_album(album_id=self.album.pk).order_by('-created')
        return photo_list
