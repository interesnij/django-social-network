from gallery.models import Photo, PhotoList
from django.views.generic.base import TemplateView
from django.views.generic import ListView


class PhotoDetail(TemplateView):
	template_name, community, user_form = None, None, None

	def get(self,request,*args,**kwargs):
		self.photo = Photo.objects.get(pk=self.kwargs["pk"])
		self.list = self.photo.list
		if self.photo.community:
			from common.templates import get_template_community_item, get_template_anon_community_item
			self.community = self.photo.community
			if request.user.is_administrator_of_community(self.community.pk):
				from gallery.forms import PhotoDescriptionForm
				self.photos = self.list.get_staff_items()
				self.user_form = PhotoDescriptionForm(instance=self.photo)
			else:
				self.photos = self.list.get_items()
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.photo, "gallery/c_photo/photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.photo, "gallery/c_photo/photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from common.templates import get_template_user_item, get_template_anon_user_item
			if request.user.pk == self.photo.creator.pk:
				from gallery.forms import PhotoDescriptionForm
				self.photos = self.list.get_staff_items()
				self.user_form = PhotoDescriptionForm(instance=self.photo)
			else:
				self.photos = self.list.get_items()
			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.photo, "gallery/u_photo/photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.photo, "gallery/u_photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PhotoDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(PhotoDetail,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["list"] = self.list
		context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
		context["avatar"] = self.photo.is_avatar(self.request.user)
		context["user_form"] = self.user_form
		context["community"] = self.community
		return context

class MessagePhotoDetail(TemplateView):
	template_name, community, user_form = None, None, None

	def get(self,request,*args,**kwargs):
		from chat.models import Message

		self.photo = Photo.objects.get(pk=self.kwargs["pk"])
		self.message = Message.objects.get(uuid=self.kwargs["uuid"])
		self.photos = self.message.get_attach_photos()
		if self.photo.community:
			from common.templates import get_template_community_item, get_template_anon_community_item
			self.community = self.photo.community
			if request.user.is_administrator_of_community(self.community.pk):
				from gallery.forms import PhotoDescriptionForm
				self.user_form = PhotoDescriptionForm(instance=self.photo)
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.photo, "chat/attach/photo/c/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.photo, "chat/attach/photo/c/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from common.templates import get_template_user_item, get_template_anon_user_item
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
		context["message"] = self.message
		context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
		context["avatar"] = self.photo.is_avatar(self.request.user)
		context["user_form"] = self.user_form
		context["community"] = self.community
		return context


class LoadPhotoList(ListView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.list = PhotoList.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			from common.templates import get_template_community_item, get_template_anon_community_item
			self.community = self.list.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.list, "gallery/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.list, "gallery/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from common.templates import get_template_user_item, get_template_anon_user_item

			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.list, "gallery/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.list, "gallery/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadPhotoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadPhotoList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.community
		return context

	def get_queryset(self):
		return self.list.get_items()
