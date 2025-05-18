from gallery.models import Photo, PhotoList
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.http import Http404
from django.views import View
from common.templates import (
								get_template_community_item,
								get_template_anon_community_item,
								get_template_user_item,
								get_template_anon_user_item,
								get_template_community_list,
								get_template_anon_community_list,
								get_template_user_list,
								get_template_anon_user_list,
							)


class PhotoDetail(TemplateView):
	template_name, community, user_form = None, None, None

	def get(self,request,*args,**kwargs):
		self.photo = Photo.objects.get(pk=self.kwargs["pk"])
		self.list = self.photo.list
		self.photos = self.list.get_items()
		if self.photo.community:
			self.community = self.photo.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.photo, "gallery/c_photo/photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.photo, "gallery/c_photo/photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.photo, "gallery/u_photo/photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.photo, "gallery/u_photo/photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PhotoDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(PhotoDetail,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["list"] = self.list
		if self.photos.filter(order=self.photo.order + 1).exists():
			context["next"] = self.photos.filter(order=self.photo.order + 1)[0]
		if self.photos.filter(order=self.photo.order - 1).exists():
			context["prev"] = self.photos.filter(order=self.photo.order - 1)[0]
		context["avatar"] = self.photo.is_avatar(self.request.user)
		context["user_form"] = self.user_form
		context["community"] = self.community
		return context

class MessagePhotoDetail(TemplateView):
	template_name, community, user_form = None, None, None

	def get(self,request,*args,**kwargs):
		from chat.models import Chat

		self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
		self.chat = Chat.objects.get(pk=self.kwargs["pk"])

		self.photos_ids = self.chat.get_attach_photos_ids()
		if self.photo.community:
			self.community = self.photo.community
			if request.user.is_administrator_of_community(self.community.pk):
				from gallery.forms import PhotoDescriptionForm
				self.user_form = PhotoDescriptionForm(instance=self.photo)
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.photo, "chat/attach/photo/c/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.photo, "chat/attach/photo/c/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.pk == self.photo.creator.pk:
				from gallery.forms import PhotoDescriptionForm
				self.user_form = PhotoDescriptionForm(instance=self.photo)
			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.photo, "chat/attach/photo/u/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.photo, "chat/attach/photo/u/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MessagePhotoDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(MessagePhotoDetail,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["chat"] = self.chat
		context["next"] = self.photos_ids[(self.photos_ids.index(self.photo.pk) + 1) % len(self.photos_ids)]
		context["prev"] = self.photos_ids[(self.photos_ids.index(self.photo.pk) - 1) % len(self.photos_ids)]
		context["user_form"] = self.user_form
		context["community"] = self.community
		return context


class LoadPhotoList(ListView):
	template_name, c, paginate_by, is_user_can_see_photo_section, is_user_can_see_photo_list, is_user_can_create_photos = None, None, 10, None, None, None

	def get(self,request,*args,**kwargs):
		self.list = PhotoList.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			self.c = self.list.community
			if request.user.is_authenticated:
				if request.user.is_staff_of_community(self.c.pk):
					self.get_lists = PhotoList.get_community_staff_lists(self.c.pk)
					self.is_user_can_see_photo_section = True
					self.is_user_can_create_photos = True
					self.is_user_can_see_photo_list = True
					self.template_name = get_template_community_list(self.list, "gallery/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
				else:
					self.get_lists = PhotoList.get_community_lists(self.c.pk)
					self.is_user_can_see_photo_section = self.c.is_user_can_see_photo(request.user.pk)
					self.is_user_can_see_photo_list = self.list.is_user_can_see_el(request.user.pk)
					self.is_user_can_create_photos = self.list.is_user_can_create_el(request.user.pk)
			elif request.user.is_anonymous:
				self.template_name = get_template_anon_community_list(self.list, "gallery/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_photo_section = self.c.is_anon_user_can_see_photo()
				self.is_user_can_see_photo_list = self.list.is_anon_user_can_see_el()
				self.get_lists = PhotoList.get_community_lists(self.c.pk)
		else:
			creator = self.list.creator
			if request.user.is_authenticated:
				creator = self.list.creator
				if request.user.pk == creator.pk:
					self.is_user_can_see_photo_section = True
					self.is_user_can_see_photo_list = True
					self.is_user_can_create_photos = True
				else:
					self.is_user_can_see_photo_section = creator.is_user_can_see_photo(request.user.pk)
					self.is_user_can_see_photo_list = self.list.is_user_can_see_el(request.user.pk)
					self.is_user_can_create_photos = self.list.is_user_can_create_el(request.user.pk)
				self.template_name = get_template_user_list(self.list, "gallery/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "gallery/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_photo_section = creator.is_anon_user_can_see_photo()
				self.is_user_can_see_photo_list = self.list.is_anon_user_can_see_el()
		return super(LoadPhotoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadPhotoList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.c
		context['is_user_can_see_photo_section'] = self.is_user_can_see_photo_section
		context['is_user_can_see_photo_list'] = self.is_user_can_see_photo_list
		context['is_user_can_create_photos'] = self.is_user_can_create_photos
		return context

	def get_queryset(self):
		return self.list.get_items()


class PostPhotoDetail(TemplateView):
	template_name, community, user_form = None, None, None

	def get(self,request,*args,**kwargs):
		from posts.models import Post

		self.photo = Photo.objects.get(pk=self.kwargs["pk"])
		self.post = Post.objects.get(pk=self.kwargs["post_pk"])
		self.photos = self.post.get_attach_photos()

		if self.photo.community:
			self.community = self.photo.community
			if request.user.is_administrator_of_community(self.community.pk):
				from gallery.forms import PhotoDescriptionForm
				self.user_form = PhotoDescriptionForm(instance=self.photo)
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.photo, "gallery/c_photo/post_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.photo, "gallery/c_photo/post_photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.pk == self.post.creator.pk:
				from gallery.forms import PhotoDescriptionForm
				self.user_form = PhotoDescriptionForm(instance=self.photo)
			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.photo, "gallery/u_photo/post_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.photo, "gallery/u_photo/post_photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PostPhotoDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(PostPhotoDetail,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["post"] = self.post
		if self.photos.filter(order=self.photo.order - 1).exists():
			context["next"] = self.photos.filter(order=self.photo.order - 1)[0]
		if self.photos.filter(order=self.photo.order + 1).exists():
			context["prev"] = self.photos.filter(order=self.photo.order + 1)[0]
		context["avatar"] = self.photo.is_avatar(self.request.user)
		context["user_form"] = self.user_form
		context["community"] = self.community
		return context

class AddPhotosInList(View):
	def post(self, request, *args, **kwargs):
		from common.templates import render_for_platform

		list = PhotoList.objects.get(pk=self.kwargs["pk"])
		if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and list.is_user_can_create_el(request.user.pk):
			photos = []
			uploaded_file = request.FILES['file']
			for p in request.FILES.getlist('file'):
				photo = Photo.create_photo(creator=request.user, image=p, list=list, type="PHLIS", community=list.community)
				photos += [photo,]
			return render_for_platform(request, 'gallery/new_photos.html',{'object_list': photos, 'list': list, 'community': list.community})
		else:
			raise Http404


class LoadPhotosList(ListView):
	template_name, community, paginate_by, is_user_can_see_photo_list, \
	is_user_can_see_photo_section, is_user_can_create_photos = None, None, 15, None, None, None

	def get(self,request,*args,**kwargs):
		self.list = PhotoList.objects.get(pk=self.kwargs["pk"])
		if request.user.is_anonymous:
			self.is_user_can_see_photo_list = self.list.is_anon_user_can_see_el()
			if self.list.community:
				self.community = self.list.community
				from common.templates import get_template_anon_community_list
				self.template_name = get_template_anon_community_list(self.list, "communities/photos/list/anon_photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_photo_section = self.community.is_anon_user_can_see_photo()
			else:
				from common.templates import get_template_anon_user_list
				self.template_name = get_template_anon_user_list(self.list, "users/photos/list/anon_photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_photo_section = self.list.creator.is_anon_user_can_see_photo()
		else:
			self.is_user_can_see_photo_list = self.list.is_user_can_see_el(request.user.pk)
			self.is_user_can_create_photos = self.list.is_user_can_create_el(request.user.pk)
			if self.list.community:
				self.community = self.list.community
				from common.templates import get_template_community_list
				self.template_name = get_template_community_list(self.list, "communities/photos/list/", "photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_photo_section = self.community.is_user_can_see_photo(request.user.pk)
			else:
				from common.templates import get_template_user_list
				self.template_name = get_template_user_list(self.list, "users/photos/list/", "photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_photo_section = self.list.creator.is_user_can_see_photo(request.user.pk)
		return super(LoadPhotosList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadPhotosList,self).get_context_data(**kwargs)
		context['list'] = self.list
		context['photo_list_pk'] = self.list.pk
		context['community'] = self.community
		context['is_user_can_see_photo_section'] = self.is_user_can_see_photo_section
		context['is_user_can_see_photo_list'] = self.is_user_can_see_photo_list
		context['is_user_can_create_photos'] = self.is_user_can_create_photos
		return context

	def get_queryset(self):
		return self.list.get_items()
