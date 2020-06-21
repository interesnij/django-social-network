from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo
from gallery.forms import PhotoDescriptionForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from gallery.models import Photo, PhotoComment
from django.shortcuts import render_to_response
from users.models import User
from django.views.generic import ListView
from gallery.forms import CommentForm


class PhotoUserCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_template_list_user(folder="u_photo_comment/", template="comments.html", request=request)
        return super(PhotoUserCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PhotoUserCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.photo
        context['user'] = self.user
        return context

    def get_queryset(self):
        comments = self.photo.get_comments()
        return comments


class PhotoCommentUserCreate(View):

    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('id'))
        photo_comment = Photo.objects.get(uuid=request.POST.get('photo_comment'))

        if form_post.is_valid():
            comment=form_post.save(commit=False)

            if request.user.pk != user.pk:
                check_is_not_blocked_with_user_with_id(user=request.user, user_id = user.pk)
                if user.is_closed_profile():
                    check_is_connected_with_user_with_id(user=request.user, user_id = user.pk)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.photo_comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=None, photo_comment=photo_comment, text=comment.text)
                get_comment_attach(request, new_comment)
                new_comment.notification_user_comment(request.user)
                return render_to_response('u_photo_comment/my_parent.html',{'comment': new_comment, 'request_user': request.user, 'request': request})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PhotoReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(uuid=request.POST.get('uuid'))
        parent = PhotoComment.objects.get(pk=request.POST.get('pk'))

        if form_post.is_valid():
            comment=form_post.save(commit=False)

            if request.user != user:
                check_is_not_blocked_with_user_with_id(user=request.user, user_id = user.id)
                if user.is_closed_profile():
                    check_is_connected_with_user_with_id(user=request.user, user_id = user.id)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.photo_comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, photo_comment=None, text=comment.text)
                get_comment_attach(request, new_comment)
                new_comment.notification_user_reply_comment(request.user)
            else:
                return HttpResponseBadRequest()
            return render_to_response('u_photo_comment/my_reply.html',{'reply': new_comment, 'comment': parent, 'user': user, 'request_user': request.user, 'request': request})
        else:
            return HttpResponseBadRequest()


class UserPhotoDescription(View):
    form_image = None

    def post(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.form_image = PhotoDescriptionForm(request.POST, instance=self.photo)
        if self.form_image.is_valid() and self.photo.creator.pk == requser.user.pk:
            self.form_image.save()
            return HttpResponse("jrrrr")
        return super(UserPhotoDescription,self).post(request,*args,**kwargs)


class UserPhotoDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.is_deleted = True
            photo.save(update_fields=['is_deleted'])
        return HttpResponse("!")

class UserPhotoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.is_deleted = False
            photo.save(update_fields=['is_deleted'])
        return HttpResponse("!")


class UserOpenCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.comments_enabled = True
            photo.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class UserCloseCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.comments_enabled = False
            photo.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class UserOffVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.votes_on = False
            photo.save(update_fields=['votes_on'])
        return HttpResponse("!")

class UserOnVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.votes_on = True
            photo.save(update_fields=['votes_on'])
        return HttpResponse("!")

class UserOnPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.is_public = False
            photo.save(update_fields=['is_public'])
        return HttpResponse("!")

class UserOffPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user:
            photo.is_public = True
            photo.save(update_fields=['is_public'])
        return HttpResponse("!")


class UserAddAvatarPhoto(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        try:
            album = Album.objects.get(creator=user, community=None, title="Фото со страницы",  is_generic=True,)
        except:
            album = Album.objects.create(creator=user, community=None, title="Фото со страницы",  is_generic=True,)
        if user == request.user:
            photo.save(update_fields=['album'])
        return HttpResponse("!")

class UserRemoveAvatarPhoto(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if user == request.user:
            photo.album = None
            try:
                album = Album.objects.get(creator=user, community=None, title="Сохраненные фото",  is_generic=True,)
            except:
                album = Album.objects.create(creator=user, community=None, title="Сохраненные фото",  is_generic=True,)
            photo.album = album
            photo.save()
        return HttpResponse("!")
