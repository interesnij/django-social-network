from django.views.generic.base import TemplateView
from communities.models import Community
from gallery.models import PhotoList, Photo
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from rest_framework.exceptions import PermissionDenied
from common.template.photo import get_template_community_photo, get_permission_community_photo
from common.check.community import check_can_get_lists
from django.http import Http404
from gallery.forms import PhotoDescriptionForm


class CommunityPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(community_id=self.community.pk, type=PhotoList.MAIN)
        if request.is_ajax():
            self.template_name = get_permission_community_photo(self.list, "communities/photos/main_list/", "photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        if request.user.is_authenticated and request.user.is_staff_of_community(self.community.pk):
            self.photo_list = self.list.get_staff_items()
        else:
            self.photo_list = self.list.get_items()
        return super(CommunityPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityPhotosList,self).get_context_data(**kwargs)
        context['community'] = self.community
        return context

    def get_queryset(self):
        photo_list = self.photo_list
        return photo_list

class CommunityAlbumPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            self.template_name = get_permission_community_photo(self.list, "communities/photos/list/", "photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        if request.user.is_authenticated and request.user.is_staff_of_community(self.community.pk):
            self.photo_list = self.list.get_staff_items()
        else:
            self.photo_list = self.list.get_items()
        return super(CommunityAlbumPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityAlbumPhotosList,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['list'] = self.list
        return context

    def get_queryset(self):
        photo_list = self.photo_list
        return photo_list

class PhotoCommunityCommentList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_comments

		self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
		self.community = self.photo.community
		if not request.is_ajax() or not self.photo.comments_enabled:
			raise Http404
		self.template_name = get_template_user_comments(self.photo, "gallery/c_photo_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PhotoCommunityCommentList,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(PhotoCommunityCommentList, self).get_context_data(**kwargs)
		context['parent'] = self.photo
		context['community'] = self.community
		return context

	def get_queryset(self):
		check_can_get_lists(self.request.user, self.community)
		comments = self.photo.get_comments()
		return comments


class CommunityFirstAvatar(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_community_item, get_template_anon_community_item

		self.community = Community.objects.get(pk=self.kwargs["pk"])
		try:
			self.list = PhotoList.objects.get(community=self.community, type=PhotoList.AVATAR)
		except:
			self.list = PhotoList.objects.create(creator=self.community.creator, community=self.community, type=PhotoList.AVATAR, title="Фото со страницы", description="Фото со страницы")
		self.photo = self.list.get_first_photo()
		self.form_image = PhotoDescriptionForm(request.POST,instance=self.photo)
		self.photos = self.list.get_items()
		if request.user.is_authenticated:
			self.template_name = get_template_community_item(self.photo, "gallery/c_photo/photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_community_item(self.photo, "gallery/c_photo/photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityFirstAvatar,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityFirstAvatar,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["community"] = self.community
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
		context["list"] = self.list
		return context


class CommunityAlbumPhotoList(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_community_item, get_template_anon_community_item

		self.photo = Photo.objects.get(pk=self.kwargs["pk"])
		self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated:
			self.template_name = get_template_community_item(self.photo, "gallery/c_photo/list_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_community_item(self.photo, "gallery/c_photo/list_photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		if request.user.is_authenticated and request.user.is_administrator_of_community(self.list.community.pk):
			self.photos = self.list.get_staff_items()
		else:
			self.photos = self.list.get_items()
		return super(CommunityAlbumPhotoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityAlbumPhotoList,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["community"] = self.list.community
		context["list"] = self.list
		context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
		context["avatar"] = self.photo.is_avatar(self.request.user)
		context["user_form"] = PhotoDescriptionForm(instance=self.photo)
		return context

class CommunityPostPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from posts.models import Post
		from common.templates import get_template_community_item, get_template_anon_community_item

		self.photo = Photo.objects.get(pk=self.kwargs["pk"])
		self.post = Post.objects.get(uuid=self.kwargs["uuid"])
		self.photos = self.post.get_attach_photos()
		if request.user.is_authenticated:
			self.template_name = get_template_community_item(self.photo, "gallery/c_photo/post_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_community_item(self.photo, "gallery/c_photo/post_photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityPostPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPostPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["community"] = self.post.community
		context["post"] = self.post
		context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
		context["user_form"] = PhotoDescriptionForm(instance=self.photo)
		return context


class GetCommunityPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from common.templates import get_detect_platform_template

		self.photo = Photo.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax():
			self.template_name = get_detect_platform_template("gallery/c_photo/preview/admin_photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			raise Http404
		return super(GetCommunityPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(GetCommunityPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["user_form"] = PhotoDescriptionForm(instance=self.photo)
		return context

class CommunityChatPhoto(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from common.templates import get_template_community_item, get_template_anon_community_item

		self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		self.photos = self.chat.get_attach_items()
		if request.user.is_authenticated:
			self.template_name = get_template_community_item(self.photo, "chat/attach/photo/", "c_detail.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_community_item(self.photo, "chat/attach/photo/anon_c_detail.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityChatPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityChatPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["chat"] = self.chat
		context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
		context["user_form"] = PhotoDescriptionForm(instance=self.photo)
		return context
