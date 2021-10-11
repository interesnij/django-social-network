from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import PhotoList, Photo
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from gallery.forms import PhotoDescriptionForm
from common.templates import get_detect_platform_template


class UserPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_item, get_template_anon_user_item

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(creator_id=self.user.pk, type=PhotoList.MAIN, community__isnull=True)
        if request.is_ajax():
            if request.user.is_authenticated:
                self.template_name = get_template_user_item(self.photo, "users/photos/main_list/", "photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
            else:
                self.template_name = get_template_anon_user_item(self.photo, "users/photos/main_list/anon_photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404

        if self.user == request.user:
            self.photo_list = self.list.get_staff_items()
        else:
            self.photo_list = self.list.get_items()
        return super(UserPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhotosList,self).get_context_data(**kwargs)
        context['user'], context['list'] = self.user, self.list
        return context

    def get_queryset(self):
        return self.photo_list

class UserPhotosAlbumList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            if request.user.is_authenticated:
                self.template_name = get_template_user_item(self.photo, "users/photos/list/", "photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
            else:
                self.template_name = get_template_anon_user_item(self.photo, "users/photos/list/anon_photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        if self.user == request.user:
            self.photo_list = self.list.get_staff_items()
        else:
            self.photo_list = self.list.get_items()
        return super(UserPhotosAlbumList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhotosAlbumList,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['list'] = self.list
        return context

    def get_queryset(self):
        return self.photo_list


class PhotoUserCommentList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_comments

		self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
		self.user = self.photo.creator
		if not request.is_ajax() or not self.photo.comments_enabled:
			raise Http404
		self.template_name = get_template_user_comments(self.photo, "gallery/u_photo_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PhotoUserCommentList,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(PhotoUserCommentList, self).get_context_data(**kwargs)
		context['parent'] = self.photo
		context['user'] = self.user
		return context

	def get_queryset(self):
		return self.photo.get_comments()


class UserPostPhoto(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from posts.models import Post
        from common.templates import get_template_user_item, get_template_anon_user_item

        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        self.photos = self.post.get_attach_photos()
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.photo, "gallery/u_photo/post_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.photo, "gallery/u_photo/post_photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPostPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPostPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["post"] = self.post
        context["user"] = self.request.user
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context

class UserCommentPhoto(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from posts.models import PostComment
        from common.templates import get_template_user_item, get_template_anon_user_item

        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.photo, "gallery/u_photo/comment_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.photo, "gallery/u_photo/comment_photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserCommentPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserCommentPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user"] = self.request.user
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context


class UserFirstAvatar(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_item, get_template_anon_user_item

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(creator=self.user, type=PhotoList.AVATAR, community__isnull=True)
        self.photos = self.list.get_items()
        self.photo = self.list.get_first_photo()
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.photo, "gallery/u_photo/photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.photo, "gallery/u_photo/photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserFirstAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserFirstAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        try:
            context["prev"] = self.photos.filter(pk__lt=self.photo.pk, type="PUB").order_by('-pk').first()
        except:
            pass
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        context["list"] = self.list
        context["user"] = self.user
        return context


class GetUserPhoto(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            self.template_name = get_detect_platform_template("gallery/u_photo/preview/my_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(GetUserPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GetUserPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context


class UserChatPhoto(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from chat.models import Chat
        from common.templates import get_template_user_item, get_template_anon_user_item

        self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"]
        self.chat = Chat.objects.get(pk=self.kwargs["pk"])
        self.photos = self.chat.get_attach_photos()
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.photo, "chat/attach/photo/", "u_detail.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.photo, "chat/attach/photo/anon_u_detail.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserChatPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserChatPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["chat"] = self.chat
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context
