from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import PhotoList, Photo
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.template.photo import get_template_user_photo, get_permission_user_photo, get_permission_user_photo_detail
from django.http import Http404
from gallery.forms import PhotoDescriptionForm
from common.template.user import get_detect_platform_template


class UserLoadPhotoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_permission_user_photo(self.list, "gallery/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		if request.user.is_authenticated and request.user.pk == self.list.creator.pk:
			self.photo_list = self.list.get_staff_items()
		else:
			self.photo_list = self.list.get_items()
		return super(UserLoadPhotoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(UserLoadPhotoList,self).get_context_data(**kwargs)
		c['user'], c['list'] = self.list.creator, self.list
		return c

	def get_queryset(self):
		return self.photo_list


class UserPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(creator_id=self.user.pk, type=PhotoList.MAIN, community__isnull=True)
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.list, "users/user_gallery/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404

        if self.user == request.user:
            self.photo_list = self.list.get_staff_items()
        else:
            self.photo_list = self.list.get_items()
        return super(UserPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhotosList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        return self.photo_list

class UserPhotoAlbumList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.list, "users/user_photo_list/", "photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        if self.user == request.user:
            self.photo_list = self.list.get_staff_items()
        else:
            self.photo_list = self.list.get_items()
        return super(UserPhotoAlbumList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhotoAlbumList,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['list'] = self.list
        return context

    def get_queryset(self):
        return self.photo_list


class PhotoUserCommentList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.template.photo import get_permission_user_photo_2

		self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
		self.user = User.objects.get(pk=self.kwargs["pk"])
		if not request.is_ajax() or not self.photo.comments_enabled:
			raise Http404
		self.template_name = get_permission_user_photo_2(self.user, "gallery/u_photo_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PhotoUserCommentList,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(PhotoUserCommentList, self).get_context_data(**kwargs)
		context['parent'] = self.photo
		context['user'] = self.user
		return context

	def get_queryset(self):
		return self.photo.get_comments()


class UserPhoto(TemplateView):
    """
    страница фото, не имеющего альбома для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        self.photos = self.list.get_items()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.list, "gallery/u_photo/photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["list"] = self.list
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context


class UserPhotosListPhoto(TemplateView):
    """
    страница отдельного фото в альбоме для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.list = PhotosList.objects.get(uuid=self.kwargs["uuid"])
        self.photos = self.list.get_items()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.list, "gallery/u_photo/list_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserPhotosListPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhotosListPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["list"] = self.list
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
        self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        try:
            self.list = PhotosList.objects.get(creator=self.user, type=PhotosList.WALL, community__isnull=True)
        except:
            self.list = PhotosList.objects.create(creator=self.user, type=PhotosList.WALL, title="Фото со стены", description="Фото со стены")
        self.photos = self.list.get_items()
        if request.is_ajax():
            self.template_name = get_permission_user_photo_detail(self.list, self.photo, "gallery/u_photo/wall_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserWallPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserWallPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["list"] = self.list
        context["user"] = self.user
        return context


class UserDetailAvatar(TemplateView):
    """
    страница отдельного фото аватаров (альбом "Фото со страницы") пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(creator=self.user, community__isnull=True, type=PhotoList.AVATAR)
        self.photos = self.list.get_items()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.list, "gallery/u_photo/avatar/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserDetailAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserDetailAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user"] = self.user
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        context["list"] = self.list
        return context

class UserPostPhoto(TemplateView):
	"""
	страница отдельного фото записи пользователя с разрещениями и без
	"""
	template_name = None

	def get(self,request,*args,**kwargs):
		from posts.models import Post
		from common.template.photo import get_permission_user_photo_2

		self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
		self.post = Post.objects.get(uuid=self.kwargs["uuid"])
		self.photos = self.post.get_attach_photos()
		if request.is_ajax():
			self.template_name = get_permission_user_photo_2(self.photo.creator, "gallery/u_photo/post_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			raise Http404
		return super(UserPostPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPostPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["post"] = self.post
		context["user"] = self.request.user
		context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
		context["user_form"] = PhotoDescriptionForm(instance=self.photo)
		return context

class UserCommentPhoto(TemplateView):
	"""
	страница отдельного фото комментария к записи пользователя с разрещениями и без
	"""
	template_name = None

	def get(self,request,*args,**kwargs):
		from posts.models import PostComment
		from common.template.photo import get_permission_user_photo_2

		self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
		self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
		self.photos = self.comment.get_attach_items()
		if request.is_ajax():
			self.template_name = get_permission_user_photo_2(self.photo.creator, "gallery/u_photo/comment_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			raise Http404
		return super(UserCommentPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserCommentPhoto,self).get_context_data(**kwargs)
		context["object"] = self.photo
		context["user"] = self.request.user
		context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
		context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
		context["user_form"] = PhotoDescriptionForm(instance=self.photo)
		return context


class UserFirstAvatar(TemplateView):
	"""страница аватара пользователя с разрещениями и без"""
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = PhotoList.objects.get(creator=self.user, type=PhotoList.AVATAR, community__isnull=True)
		self.photos = self.list.get_items()
		self.photo = self.photos.first()
		if request.is_ajax():
			self.template_name = get_permission_user_photo(self.list, "gallery/u_photo/avatar/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			raise Http404
		return super(UserFirstAvatar,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserFirstAvatar,self).get_context_data(**kwargs)
		context["object"] = self.photo
		try:
			context["prev"] = self.photos.filter(pk__lt=self.photo.pk, status="PUB").order_by('-pk').first()
		except:
			pass
		context["user_form"] = PhotoDescriptionForm(instance=self.photo)
		context["list"] = self.list
		context["user"] = self.user
		return context


class GetUserPhoto(TemplateView):
    """
    страница отдельного фото. Для уведомлений и тому подобное
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            self.template_name = get_detect_platform_template("gallery/u_photo/photo/my_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(GetUserPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GetUserPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context


class UserChatPhoto(TemplateView):
    """
    страница отдельного фото чата пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        from chat.models import Chat

        self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        self.chat = Chat.objects.get(pk=self.kwargs["pk"])
        self.photos = self.chat.get_attach_items()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.photo.creator, "chat/attach/photo/", "u_detail.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserChatPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserChatPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["chat"] = self.chat
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context
