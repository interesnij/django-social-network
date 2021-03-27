from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.template.photo import get_template_user_photo, get_permission_user_photo, get_permission_user_photo_detail
from django.http import Http404
from gallery.forms import PhotoDescriptionForm
from common.template.user import get_detect_platform_template


class UserLoadAlbum(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.album = Album.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_permission_user_photo(self.album, "gallery/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		if request.user.is_authenticated and request.user.pk == self.album.creator.pk:
			self.photo_list = self.album.get_staff_photos()
		else:
			self.photo_list = self.album.get_photos()
		return super(UserLoadAlbum,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(UserLoadAlbum,self).get_context_data(**kwargs)
		c['user'], c['album'] = self.album.creator, self.album
		return c

	def get_queryset(self):
		list = self.photo_list
		return list


class UserPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(creator_id=self.user.pk, type=Album.MAIN, community__isnull=True)
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.album, "users/user_gallery/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404

        if self.user == request.user:
            self.photo_list = self.album.get_staff_photos()
        else:
            self.photo_list = self.album.get_photos()
        return super(UserPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhotosList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        photo_list = self.photo_list
        return photo_list

class UserAlbumPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.album, "users/user_album/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        if self.user == request.user:
            self.photo_list = self.album.get_staff_photos()
        else:
            self.photo_list = self.album.get_photos()
        return super(UserAlbumPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserAlbumPhotosList,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['album'] = self.album
        return context

    def get_queryset(self):
        photo_list = self.photo_list
        return photo_list


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
		comments = self.photo.get_comments()
		return comments


class UserPhoto(TemplateView):
    """
    страница фото, не имеющего альбома для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.album, "gallery/u_photo/photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["album"] = self.album
        context["next"] = self.photos.filter(pk__gt=self.photo.pk, is_deleted=False).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context


class UserAlbumPhoto(TemplateView):
    """
    страница отдельного фото в альбоме для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.album, "gallery/u_photo/album_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserAlbumPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserAlbumPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["album"] = self.album
        context["next"] = self.photos.filter(pk__gt=self.photo.pk, is_deleted=False).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
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
            self.album = Album.objects.get(creator=self.user, type=Album.WALL, community__isnull=True)
        except:
            self.album = Album.objects.create(creator=self.user, type=Album.WALL, title="Фото со стены", description="Фото со стены")
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo_detail(self.album, self.photo, "gallery/u_photo/wall_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserWallPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserWallPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["next"] = self.photos.filter(pk__gt=self.photo.pk, is_deleted=False).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
        context["album"] = self.album
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
        try:
            self.album = Album.objects.get(creator=self.user, community__isnull=True, type=Album.AVATAR)
        except:
            self.album = Album.objects.create(creator=self.user, type=Album.AVATAR, title="Фото со страницы", description="Фото со страницы")
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.album, "gallery/u_photo/avatar/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserDetailAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserDetailAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user"] = self.user
        context["next"] = self.photos.filter(pk__gt=self.photo.pk, is_deleted=False).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        context["album"] = self.album
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
        context["next"] = self.photos.filter(pk__gt=self.photo.pk, is_deleted=False).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
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
        self.photos = self.comment.get_attach_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo_2(self.photo.creator, "gallery/u_photo/comment_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserCommentPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserCommentPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user"] = self.request.user
        context["next"] = self.photos.filter(pk__gt=self.photo.pk, is_deleted=False).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context


class UserFirstAvatar(TemplateView):
	"""страница аватара пользователя с разрещениями и без"""
	template_name = None

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		try:
			self.album = Album.objects.get(creator=self.user, type=Album.AVATAR, community__isnull=True)
		except:
			self.album = Album.objects.create(creator=self.user, type=Album.AVATAR, title="Фото со страницы", description="Фото со страницы")
		self.photo, self.photos = self.album.get_first_photo(), self.album.get_photos()
		if request.is_ajax():
			self.template_name = get_permission_user_photo(self.album, "gallery/u_photo/avatar/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			raise Http404
		return super(UserFirstAvatar,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserFirstAvatar,self).get_context_data(**kwargs)
		context["object"] = self.photo
		try:
			context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
		except:
			pass
		context["user_form"] = PhotoDescriptionForm(instance=self.photo)
		context["album"] = self.album
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
        self.photos = self.chat.get_attach_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.photo.creator, "chat/attach/photo/", "u_detail.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserChatPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserChatPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["chat"] = self.chat
        context["next"] = self.photos.filter(pk__gt=self.photo.pk, is_deleted=False).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk, is_deleted=False).order_by('-pk').first()
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context
