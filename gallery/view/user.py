from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo
from gallery.helpers import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import ListView
from gallery.forms import AlbumForm, AvatarUserForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied


class AvatarReload(TemplateView):
    template_name="photo_user/avatar_reload.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        return super(AvatarReload,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(AvatarReload,self).get_context_data(**kwargs)
        return context


class UserGalleryView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])

		if self.user == request.user:
			self.template_name="photo_user/gallery/my_gallery.html"
		elif request.user != self.user and request.user.is_authenticated:
			if request.user.is_blocked_with_user_with_id(user_id=self.user.id):
				self.template_name = "photo_user/gallery/block_gallery.html"
			elif self.user.is_closed_profile():
				if not request.user.is_connected_with_user_with_id(user_id=self.user.id):
					self.template_name = "photo_user/gallery/close_gallery.html"
				else:
					self.template_name = "photo_user/gallery/gallery.html"
			else:
				self.template_name = "photo_user/gallery/gallery.html"
		elif request.user.is_anonymous and self.user.is_closed_profile():
			self.template_name = "photo_user/gallery/close_gallery.html"
		elif request.user.is_anonymous and not self.user.is_closed_profile():
			self.template_name = "photo_user/gallery/anon_gallery.html"
		return super(UserGalleryView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserGalleryView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

class UserAlbumView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        if self.user == request.user:
            self.template_name="photo_user/album/my_album.html"
        elif request.user != self.user and request.user.is_authenticated:
            if request.user.is_blocked_with_user_with_id(user_id=self.user.id):
                self.template_name = "photo_user/album/block_album.html"
            elif self.user.is_closed_profile():
                if not request.user.is_connected_with_user_with_id(user_id=self.user.id):
                    self.template_name = "photo_user/album/close_album.html"
                else:
                    self.template_name = "photo_user/album/album.html"
            else:
                self.template_name = "photo_user/album/album.html"
        elif request.user.is_anonymous and self.user.is_closed_profile():
            self.template_name = "photo_user/album/close_album.html"
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.template_name = "photo_user/album/anon_album.html"
        return super(UserAlbumView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserAlbumView,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['album'] = self.album
        return context


class UserAlbomReload(TemplateView):
	template_name="photo_user/album_reload.html"

	def get(self,request,*args,**kwargs):
		self.album=Album.objects.get(uuid=self.kwargs["uuid"])
		self.photos = Photo.objects.filter(album=self.album)
		return super(UserAlbomReload,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserAlbomReload,self).get_context_data(**kwargs)
		context['album'] = self.album
		context['photos'] = self.photos
		return context


class AlbomGygView(TemplateView):
	template_name="photo_user/gygyg.html"

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		self.album = Album.objects.filter(creator=self.user)
		self.new_url = self.album.last().uuid
		return super(AlbomGygView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(AlbomGygView,self).get_context_data(**kwargs)
		context["new_url"]=self.new_url
		context["album"]=self.album
		return context


class UserAddAvatar(TemplateView):
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

class PhotoUserCreate(View,AjaxResponseMixin,JSONResponseMixin):

	def post(self, request, *args, **kwargs):
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		try:
			self.album = Album.objects.get(pk=self.kwargs["pk"])
		except:
			self.album = None

		uploaded_file = request.FILES['file']
		Photo.objects.create(album=self.album, file=uploaded_file, creator=self.user)

		response_dict = {'message': 'File uploaded successfully!',}
		return self.render_json_response(response_dict, status=200)

class AlbumUserCreate(TemplateView):
	template_name="photo_user/add_album.html"
	form=None

	def get(self,request,*args,**kwargs):
		self.form=AlbumForm()
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		return super(AlbumUserCreate,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(AlbumUserCreate,self).get_context_data(**kwargs)
		context["form"]=self.form
		context["user"]=self.user
		return context

	def post(self,request,*args,**kwargs):
		self.form = AlbumForm(request.POST)
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if self.form.is_valid() and request.is_ajax():
			new_album = self.form.save(commit=False)
			new_album.creator=self.user
			new_album = self.form.save()
		else:
			return HttpResponseBadRequest()
		return super(AlbumUserCreate,self).get(request,*args,**kwargs)


class UserAlbomList(View):
    def get(self,request,**kwargs):
        context = {}
        album=Album.objects.get(uuid=self.kwargs["uuid"])
        user=User.objects.get(pk=self.kwargs["pk"])
        if user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
            photos = user.get_photos_for_album(album_id=album.pk)
        elif request.user.is_anonymous and user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.',)
        elif request.user.is_anonymous and not user.is_closed_profile():
            photos = user.get_photos_for_album(album_id=album.pk)
        elif user == request.user:
            photos = user.get_photos_for_album(album_id=album.pk)

        current_page = Paginator(photos, 12)
        page = request.GET.get('page')
        context['user'] = user
        context['album'] = album
        try:
            context['photos'] = current_page.page(page)
        except PageNotAnInteger:
            context['photos'] = current_page.page(1)
        except EmptyPage:
            context['photos'] = current_page.page(current_page.num_pages)
        return render_to_response('photo_user/album/album_list.html', context)

class UserAlbumsList(View):
	def get(self,request,**kwargs):
		context = {}
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if self.user != request.user and request.user.is_authenticated:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
			if self.user.is_closed_profile():
				check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
			albums_list = self.user.get_albums().order_by('-created')
			current_page = Paginator(albums_list, 12)
		elif request.user.is_anonymous and self.user.is_closed_profile():
			raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
		elif request.user.is_anonymous and not self.user.is_closed_profile():
			albums_list = self.user.get_albums().order_by('-created')
			current_page = Paginator(albums_list, 12)
		elif self.user == request.user:
			albums_list = self.user.get_albums().order_by('-created')
			current_page = Paginator(albums_list, 12)

		page = request.GET.get('page')
		context['user'] = self.user
		try:
			context['albums_list'] = current_page.page(page)
		except PageNotAnInteger:
			context['albums_list'] = current_page.page(1)
		except EmptyPage:
			context['albums_list'] = current_page.page(current_page.num_pages)
		return render_to_response('photo_user/albums.html', context)

class UserPhotosList(View):
	def get(self,request,**kwargs):
		context = {}
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		if self.user != request.user and request.user.is_authenticated:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
			if self.user.is_closed_profile():
				check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
			photo_list = self.user.get_photos().order_by('-created')
			current_page = Paginator(photo_list, 12)
		elif request.user.is_anonymous and self.user.is_closed_profile():
			raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.',)
		elif request.user.is_anonymous and not self.user.is_closed_profile():
			photo_list = self.user.get_photos().order_by('-created')
			current_page = Paginator(photo_list, 12)
		elif self.user == request.user:
			photo_list = self.user.get_photos().order_by('-created')
			current_page = Paginator(photo_list, 12)

		page = request.GET.get('page')
		context['user'] = self.user
		try:
			context['photo_list'] = current_page.page(page)
		except PageNotAnInteger:
			context['photo_list'] = current_page.page(1)
		except EmptyPage:
			context['photo_list'] = current_page.page(current_page.num_pages)
		return render_to_response('photo_user/photos.html', context)
