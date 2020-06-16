from django.views.generic.base import TemplateView
from users.models import User
from communities.models import Community
from gallery.models import Album, Photo
from gallery.helpers import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import ListView
from gallery.forms import AlbumForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.checkers import check_can_get_posts_for_community_with_name
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied
from common.utils import is_mobile


class CommunityAddAvatar(View):
    """
    загрузка аватара сообщества
    """
    def post(self, request, *args, **kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        if user == request.user:
            photo_input = request.FILES.get('file')
            try:
                _album = Album.objects.get(creator=request.user, is_generic=True, community=community, title="Фото со страницы")
            except:
                _album = Album.objects.create(creator=request.user, is_generic=True, community=community, title="Фото со страницы", description="Фото со страницы сообщества")
            photo = Photo.objects.create(file=p, creator=request.user, community=community)
            _album.album.add(photo)
            return render_to_response('photo_community/admin_photo.html',{'object': photo, 'community': community, 'request': request})
        else:
            return HttpResponseBadRequest()


class CommunityGalleryView(TemplateView):
	template_name="photo_community/gallery.html"

	def get(self,request,*args,**kwargs):
		self.community=Community.objects.get(pk=self.kwargs["pk"])
		self.albums=Album.objects.filter(creator=self.user)
		return super(CommunityGalleryView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityGalleryView,self).get_context_data(**kwargs)
		context['community'] = self.community
		return context

class CommunityPhotosList(View):
	def get(self,request,**kwargs):
		context = {}
		self.community = Community.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated:
			check_can_get_posts_for_community_with_name(request.user,self.community.name)
			photo_list = self.community.get_photos().order_by('-created')
		if request.user.is_anonymous and self.community.is_public:
			photo_list = self.community.get_posts().order_by('-created')
		if request.user.is_anonymous and (self.community.is_closed or self.community.is_private):
			raise PermissionDenied('У Вас недостаточно прав для просмотра информации группы')
		current_page = Paginator(photo_list, 15)
		page = request.GET.get('page')
		context['community'] = self.community
		try:
			context['photo_list'] = current_page.page(page)
		except PageNotAnInteger:
			context['photo_list'] = current_page.page(1)
		except EmptyPage:
			context['photo_list'] = current_page.page(current_page.num_pages)
		return render_to_response('photo_community/photos.html', context)


class CommunityPhoto(TemplateView):
	template_name="photo_community/photo.html"

	def get(self,request,*args,**kwargs):
		self.community=Community.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated:
			check_can_get_posts_for_community_with_name(request.user,self.community.name)
			self.photos = self.community.get_photos()
			self.photo = Photo.objects.get(pk=self.kwargs["pk"])
			self.next = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
			self.prev = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
		if request.user.is_anonymous and (self.community.is_closed or self.community.is_private):
			raise PermissionDenied('У Вас недостаточно прав для просмотра информации группы')
		if request.user.is_anonymous and self.community.is_public:
			self.photos = self.user.get_photos()
			self.photo = Photo.objects.get(pk=self.kwargs["pk"])
			self.next = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
			self.prev = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
		return super(CommunityPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityPhoto,self).get_context_data(**kwargs)
		context["object"]=self.photo
		context["community"]=self.community
		context["next"]=self.next
		context["prev"]=self.prev
		return context


class CommunityAlbomView(View):
	def get(self,request,**kwargs):
		context = {}
		self.album=Album.objects.get(uuid=self.kwargs["uuid"])
		self.community=Community.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated:
			check_can_get_posts_for_community_with_name(request.user,self.community.name)
			photos = Photo.objects.filter(album=self.album).order_by('-created')
		if request.user.is_anonymous and self.community.is_public:
			photos = Photo.objects.filter(album=self.album).order_by('-created')
		if request.user.is_anonymous and (self.community.is_closed or self.community.is_private):
			raise PermissionDenied('У Вас недостаточно прав для просмотра информации группы')
		current_page = Paginator(photos, 15)
		page = request.GET.get('page')
		context['community'] = self.community
		try:
			context['photos'] = current_page.page(page)
		except PageNotAnInteger:
			context['photos'] = current_page.page(1)
		except EmptyPage:
			context['photos'] = current_page.page(current_page.num_pages)
		return render_to_response('photo_user/album.html', context)


class CommunityAlbomReload(TemplateView):
	template_name="photo_community/album_reload.html"

	def get(self,request,*args,**kwargs):
		self.album=Album.objects.get(uuid=self.kwargs["uuid"])
		self.photos = Photo.objects.filter(album=self.album)
		return super(CommunityAlbomReload,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityAlbomReload,self).get_context_data(**kwargs)
		context['album'] = self.album
		context['photos'] = self.photos
		return context


class PhotoCommunityCreate(View,AjaxResponseMixin,JSONResponseMixin):

	def post(self, request, *args, **kwargs):
		self.community = Community.objects.get(uuid=self.kwargs["uuid"])
		try:
			self.album = Album.objects.get(pk=self.kwargs["pk"])
		except:
			self.album = None

		uploaded_file = request.FILES['file']
		Photo.objects.create(album=self.album, file=uploaded_file, creator=request.user, community=self.community)

		response_dict = {'message': 'File uploaded successfully!',}
		return self.render_json_response(response_dict, status=200)


class AlbumCommunityCreate(TemplateView):
	template_name="photo_community/add_album.html"
	form=None

	def get(self,request,*args,**kwargs):
		self.form=AlbumForm()
		self.community = Community.objects.get(uuid=self.kwargs["uuid"])
		return super(AlbumCommunityCreate,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(AlbumCommunityCreate,self).get_context_data(**kwargs)
		context["form"]=self.form
		context["community"]=self.community
		return context

	def post(self,request,*args,**kwargs):
		self.form = AlbumForm(request.POST)
		self.community = Community.objects.get(uuid=self.kwargs["uuid"])
		if self.form.is_valid():
			new_album = self.form.save(commit=False)
			new_album.creator=request.user
			new_album = self.form.save()
			if request.is_ajax() :
				return HttpResponse("!")
		else:
			return HttpResponseBadRequest()
		return super(AlbumCommunityCreate,self).get(request,*args,**kwargs)


class CommunityAlbomGygView(TemplateView):
	template_name="photo_community/gygyg.html"

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(uuid=self.kwargs["uuid"])
		self.album = Album.objects.filter(creator=self.user)
		self.new_url = self.album.last().uuid
		return super(CommunityAlbomGygView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityAlbomGygView,self).get_context_data(**kwargs)
		context["new_url"]=self.new_url
		context["album"]=self.album
		return context
