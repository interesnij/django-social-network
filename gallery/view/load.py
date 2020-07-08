from django.views.generic.base import TemplateView
from users.models import User
from posts.models import PostComment
from gallery.models import Album, Photo
from gallery.forms import PhotoDescriptionForm
from communities.models import Community
from common.get_template import get_detail_template_user, get_detail_template_community


class UserPhoto(TemplateView):
    """
    страница фото, не имеющего альбома для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.photos = self.photo.creator.get_photos()
        self.template_name = get_detail_template_user(self.photo.creator, "photo_user/", "photo.html", request)
        return super(UserPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserPhoto,self).get_context_data(**kwargs)
        context["object"]=self.photo
        context["next"]=self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"]=self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["avatar"]=self.photo.is_avatar(self.request.user)
        context["user_form"]=PhotoDescriptionForm(instance=self.photo)
        return context


class UserAlbumPhoto(TemplateView):
    """
    страница отдельного фото в альбоме для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.album=Album.objects.get(uuid=self.kwargs["album_uuid"])
        self.photos = self.photo.creator.get_photos_for_my_album(album_id=self.album.pk)
        self.template_name = get_detail_template_user(self.photo.creator, "photo_user/", "album_photo.html", request)
        return super(UserAlbumPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserAlbumPhoto,self).get_context_data(**kwargs)
        context["object"]=self.photo
        context["album"]=self.album
        context["next"]=self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"]=self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["avatar"]=self.photo.is_avatar(self.request.user)
        context["user_form"]=PhotoDescriptionForm(instance=self.photo)
        return context


class UserWallPhoto(TemplateView):
    """
    страница отдельного фото альбома пользователя "Фото со стены"
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(creator_id=self.user.pk, is_generic=True, community=None, title="Фото со стены")
        self.photos = self.user.get_photos_for_album(album_id=self.album.pk)
        self.template_name = get_detail_template_user(self.user, "photo_user/", "wall_photo.html", request)
        return super(UserWallPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserWallPhoto,self).get_context_data(**kwargs)
        context["object"]=self.photo
        context["user_form"]=PhotoDescriptionForm(instance=self.photo)
        context["avatar"]=self.photo.is_avatar(self.request.user)
        context["next"]=self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"]=self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["album"] = self.album
        return context


class UserDetailAvatar(TemplateView):
    """
    страница отдельного фото аватаров (альбом "Фото со страницы") пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.avatar_photos = self.photo.creator.get_avatar_photos()
        self.template_name = get_detail_template_user(self.photo.creator, "photo_user/", "avatar_photo.html", request)
        return super(UserDetailAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserDetailAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["next"] = self.avatar_photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.avatar_photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        context["album"] = Album.objects.get(creator=self.photo.creator, is_generic=True, title="Фото со страницы", community=None)
        return context

class CommunityDetailAvatar(TemplateView):
    """
    страница отдельного фото альбома "Фото со страницы" сообщества с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.form_image = PhotoDescriptionForm(request.POST,instance=self.photo)
        self.avatar_photos = self.photo.community.get_avatar_photos()
        self.template_name = get_detail_template_community(self.photo.community, "photo_community/", "avatar_photo.html", request)
        return super(CommunityDetailAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityDetailAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["next"] = self.avatar_photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.avatar_photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["user_form"]=PhotoDescriptionForm(instance=self.photo)
        context["album"] = Album.objects.get(is_generic=True, title="Фото со страницы", community=self.photo.community)
        return context


class CommunityPhoto(TemplateView):
    """
    страница фото, не имеющего альбома для сообщества с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.photos = self.photo.community.get_photos()
        self.template_name = get_detail_template_community(self.photo.community, "photo_community/", "photo.html", request)
        return super(CommunityPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityPhoto,self).get_context_data(**kwargs)
        context["object"]=self.photo
        context["next"]=self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"]=self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["avatar"]=self.photo.is_avatar(self.request.user)
        context["user_form"]=PhotoDescriptionForm(instance=self.photo)
        return context


class CommunityAlbumPhoto(TemplateView):
    """
    страница отдельного фото в альбоме для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.album=Album.objects.get(uuid=self.kwargs["album_uuid"])
        self.photos = self.photo.community.get_photos_for_album(album_id=self.album.pk)
        self.template_name = get_detail_template_community(self.photo.community, "photo_community/", "album_photo.html", request)
        return super(CommunityAlbumPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityAlbumPhoto,self).get_context_data(**kwargs)
        context["object"]=self.photo
        context["album"]=self.album
        context["next"]=self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"]=self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["avatar"]=self.photo.is_avatar(self.request.user)
        context["user_form"]=PhotoDescriptionForm(instance=self.photo)
        return context


class CommunityWallPhoto(TemplateView):
    """
    страница отдельного фото альбома пользователя "Фото со стены"
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.album = Album.objects.get(community=self.community, is_generic=True, title="Фото со стены")
        self.photos = self.user.get_photos_for_album(album_id=self.album.pk)
        self.template_name = get_detail_template_community(self.user, "photo_community/", "wall_photo.html", request)
        return super(CommunityWallPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityWallPhoto,self).get_context_data(**kwargs)
        context["object"]=self.photo
        context["user_form"]=PhotoDescriptionForm(instance=self.photo)
        context["avatar"]=self.photo.is_avatar(self.request.user)
        context["next"]=self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"]=self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["album"] = self.album
        return context
