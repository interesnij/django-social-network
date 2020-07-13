import re
from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo
from gallery.forms import PhotoDescriptionForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.checkers import check_can_get_posts_for_community_with_name
from gallery.models import Photo, PhotoComment
from django.shortcuts import render
from django.views.generic import ListView
from gallery.forms import CommentForm
from communities.models import Community
from rest_framework.exceptions import PermissionDenied


class PhotoCommunityCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])

        if not self.photo.comments_enabled:
            raise PermissionDenied('Комментарии для фотографии отключены')
        elif request.user.is_authenticated:
            if request.user.is_staff_of_community_with_name(self.community.name):
                self.template_name = "c_photo_comment/admin_comments.html"
            elif request.user.is_photo_manager():
                self.template_name = "c_photo_comment/staff_comments.html"
            elif check_can_get_posts_for_community_with_name(request.user, self.community.name):
                self.template_name = "c_photo_comment/comments.html"
            else:
                self.template_name = "c_photo_comment/comments.html"
        elif request.user.is_anonymous:
            if self.is_public():
                self.template_name = "c_photo_comment/anon_comments.html"

        MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name += "mob_"
        return super(PhotoCommunityCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PhotoCommunityCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.photo
        context['community'] = self.community
        return context

    def get_queryset(self):
        check_can_get_posts_for_community_with_name(self.request.user, self.community.name)
        comments = self.photo.get_comments()
        return comments


class PhotoCommentCommunityCreate(View):

    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        photo_comment = Photo.objects.get(uuid=request.POST.get('uuid'))

        if form_post.is_valid() and photo_comment.comments_enabled:
            comment=form_post.save(commit=False)

            check_can_get_posts_for_community_with_name(request.user, community.name)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.photo_comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=None, photo_comment=photo_comment, text=comment.text)
                get_comment_attach(request, new_comment)
                if request.user.pk != photo_comment.creator.pk:
                    new_comment.notification_community_comment(request.user, community)
                return render(request, 'c_photo_comment/admin_parent.html',{'comment': new_comment, 'community': community})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PhotoReplyCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        parent = PhotoComment.objects.get(pk=request.POST.get('photo_comment'))

        if form_post.is_valid() and parent.photo_comment.comments_enabled:
            comment = form_post.save(commit=False)

            check_can_get_posts_for_community_with_name(request.user, community.name)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.photo_comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, photo_comment=None, text=comment.text)
                get_comment_attach(request, new_comment)
                if request.user.pk != parent.commenter.pk:
                    new_comment.notification_community_reply_comment(request.user, community)
            else:
                return HttpResponseBadRequest()
            return render(request, 'c_photo_comment/admin_reply.html',{'reply': new_comment, 'comment': parent, 'community': community})
        else:
            return HttpResponseBadRequest()

class PhotoCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent_comment.post.community
        if request.user.is_staff_of_community_with_name(community.name):
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class PhotoCommentCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent_comment.post.community
        if request.user.is_staff_of_community_with_name(community.name):
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")


class CommunityPhotoDescription(View):
    form_image = None

    def post(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        form_image = PhotoDescriptionForm(request.POST, instance=photo)
        if form_image.is_valid() and request.user.is_administrator_of_community_with_name(photo.community.name):
            form_image.save()
            return HttpResponse(form_image.cleaned_data["description"])
        return super(CommunityPhotoDescription,self).post(request,*args,**kwargs)


class CommunityPhotoDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.is_deleted = True
            photo.save(update_fields=['is_deleted'])
        return HttpResponse("!")

class CommunityPhotoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.is_deleted = False
            photo.save(update_fields=['is_deleted'])
        return HttpResponse("!")


class CommunityOpenCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.comments_enabled = True
            photo.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class CommunityCloseCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.comments_enabled = False
            photo.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class CommunityOffVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.votes_on = False
            photo.save(update_fields=['votes_on'])
        return HttpResponse("!")

class CommunityOnVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.votes_on = True
            photo.save(update_fields=['votes_on'])
        return HttpResponse("!")

class CommunityOnPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.is_public = False
            photo.save(update_fields=['is_public'])
        return HttpResponse("!")

class PhotoWallCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user or request.user.is_staff_of_community_with_name(community.name):
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class PhotoWallCommentCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user or request.user.is_staff_of_community_with_name(community.name):
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class CommunityOffPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user or request.user.is_administrator_of_community_with_name(photo.community.name):
            photo.is_public = True
            photo.save(update_fields=['is_public'])
        return HttpResponse("!")


class CommunityAddAvatarPhoto(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        try:
            album = Album.objects.get(community=community, title="Фото со страницы",  is_generic=True,)
        except:
            album = Album.objects.create(creator=request.user, community=community, title="Фото со страницы",  is_generic=True,)
        if photo.creator == request.user or request.user.is_administrator_of_community_with_name(community.name):
            photo.save(update_fields=['album'])
        return HttpResponse("!")

class CommunityRemoveAvatarPhoto(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if photo.creator == request.user or request.user.is_administrator_of_community_with_name(community.name):
            photo.album = None
            try:
                album = Album.objects.get(community=community, title="Сохраненные фото",  is_generic=True,)
            except:
                return HttpResponse("!")
            photo.album = album
            photo.save()
        return HttpResponse("!")
