from gallery.models import PhotoList, Photo, PhotoComment
from gallery.forms import PhotoDescriptionForm, CommentForm, PhotoListForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.check.community import check_can_get_lists
from communities.models import Community
from common.template.user import render_for_platform
from common.template.community import get_community_manage_template
from django.http import Http404
from django.views.generic.base import TemplateView


class AddPhotoListInCommunityCollections(View):
    def post(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_community_can_add_list(community.pk):
            list.communities.add(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class RemovePhotoListFromCommunityCollections(View):
    def post(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_user_can_delete_list(community.pk):
            list.communities.remove(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class CommunityCreatePhotosInMainList(View):
    """
    асинхронная мульти загрузка фотографий пользователя в основной альбом
    """
    def post(self, request, *args, **kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            photos = []
            check_can_get_lists(request.user, community)
            list = PhotoList.objects.get(community=community, type=PhotoList.MAIN)
            for p in request.FILES.getlist('file'):
                photo = Photo.create_photo(creator=request.user, image=p, list=list, type="PHO", community=community)
                photos += [photo,]
            return render_for_platform(request, 'gallery/c_photo/new_photos.html',{'object_list': photos, 'community': community})
        else:
            raise Http404

class CommunityCreatePhotosInPhotoList(View):
    """
    асинхронная мульти загрузка фотографий пользователя в альбом
    """
    def post(self, request, *args, **kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            photos = []
            uploaded_file = request.FILES['file']
            check_can_get_lists(request.user, community)
            for p in request.FILES.getlist('file'):
                photo = Photo.create_photo(creator=request.user, image=p, list=list, type="PHLIS", community=community)
                photos += [photo,]
            return render_for_platform(request, 'gallery/c_photo/new_album_photos.html',{'object_list': photos, 'list': list, 'community': community})
        else:
            raise Http404

class CommunityAddAvatar(View):
    """
    загрузка аватара сообщества
    """
    def post(self, request, *args, **kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator_of_community(community.pk):
            photo_input = request.FILES.get('file')
            _list = PhotoList.objects.get(community=community, type=PhotoList.AVATAR)
            photo = Photo.create_photo(creator=request.user, image=photo_input, list=_list, type="PHAVA", community=community)
            community.create_s_avatar(photo_input)
            community.create_b_avatar(photo_input)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class PhotoCommentCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        photo = Photo.objects.get(uuid=request.POST.get('uuid'))

        if not community.is_comment_photo_send_all() and not request.user.is_member_of_community(community.pk):
            raise Http404
        elif community.is_comment_photo_send_admin() and not request.user.is_staff_of_community(community.pk):
            raise Http404
        elif request.is_ajax() and form_post.is_valid() and photo.comments_enabled:
            comment=form_post.save(commit=False)

            check_can_get_lists(request.user, community)
            if request.POST.get('text') or request.POST.get('attach_items'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, photo=photo, text=comment.text, community=community)
                return render_for_platform(request, 'gallery/c_photo_comment/admin_parent.html',{'comment': new_comment, 'community': community})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PhotoReplyCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        parent = PhotoComment.objects.get(pk=request.POST.get('photo_comment'))

        if not community.is_comment_photo_send_all() and not request.user.is_member_of_community(community.pk):
            raise Http404
        elif community.is_comment_photo_send_admin() and not request.user.is_staff_of_community(community.pk):
            raise Http404
        elif request.is_ajax() and form_post.is_valid() and parent.photo_comment.comments_enabled:
            comment = form_post.save(commit=False)

            check_can_get_lists(request.user, community)
            if request.POST.get('text') or request.POST.get('attach_items'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parentt=parent, photo=parent.photo, text=comment.text, community=community)
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'gallery/c_photo_comment/admin_reply.html',{'reply': new_comment, 'comment': parent, 'community': community})
        else:
            return HttpResponseBadRequest()

class PhotoCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent.post.community
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            comment.delete_comment()
            return HttpResponse()
        else:
            raise Http404

class PhotoCommentCommunityRecover(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent.post.community
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            comment.restore_comment()
            return HttpResponse()
        else:
            raise Http404


class CommunityPhotoDescription(View):
    form_image = None

    def post(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = photo.community
        form_image = PhotoDescriptionForm(request.POST, instance=photo)
        if request.is_ajax() and form_image.is_valid() and request.user.is_administrator_of_community(community.pk):
            form_image.save()
            return HttpResponse(form_image.cleaned_data["description"])
        else:
            raise Http404


class CommunityPhotoDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.delete_item(community)
            return HttpResponse()
        else:
            raise Http404

class CommunityPhotoRecover(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.restore_item(community)
            return HttpResponse()
        else:
            raise Http404


class CommunityOpenCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.comments_enabled = True
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class CommunityCloseCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.comments_enabled = False
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOffVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.votes_on = False
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOnVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.votes_on = True
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOnPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.make_private()
            return HttpResponse()
        else:
            raise Http404

class CommunityOffPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            comment.make_publish()
            return HttpResponse()
        else:
            raise Http404


class PhotoWallCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user or request.user.is_staff_of_community(community.pk):
            comment.delete_item()
            return HttpResponse()
        else:
            raise Http404

class PhotoWallCommentCommunityRecover(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["comment_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user or request.user.is_staff_of_community(community.pk):
            comment.restore_item()
            return HttpResponse()
        else:
            raise Http404


class PhotoListCommunityCreate(TemplateView):
    """
    создание альбома сообщества
    """
    template_name = None
    form = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("communities/photos/list/add_list.html", request.user, self.community, request.META['HTTP_USER_AGENT'])
        return super(PhotoListCommunityCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoListCommunityCreate,self).get_context_data(**kwargs)
        context["form"] = PhotoListForm()
        context["community"] = self.community
        return context

    def post(self,request,*args,**kwargs):
        self.form = PhotoListForm(request.POST)
        self.c = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator_of_community(self.c.pk):
            list = self.form.save(commit=False)
            if not list.description:
                list.description = "Без описания"
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, community=self.c,is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'communities/photos/list/new_list.html',{'list': new_list, 'community': self.c})
        else:
            return HttpResponseBadRequest()
        return super(PhotoListCommunityCreate,self).get(request,*args,**kwargs)

class PhotoListCommunityEdit(TemplateView):
    """
    изменение альбома сообщества
    """
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        self.community = self.list.community
        self.template_name = get_community_manage_template("communities/photos/list/edit_list.html", request.user, self.community, request.META['HTTP_USER_AGENT'])
        return super(PhotoListCommunityEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoListCommunityEdit,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["community"] = self.community
        context["list"] = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        self.form = PhotoListForm(request.POST,instance=self.list)
        self.community = self.list.community
        if request.is_ajax() and self.form.is_valid() and request.user.is_administrator_of_community(self.community.pk) and self.list.is_have_edit():
            list = self.form.save(commit=False)
            new_list = list.edit_list(name=list.name, description=list.description, is_public=request.POST.get("is_public"))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(PhotoListCommunityEdit,self).get(request,*args,**kwargs)

class PhotoListCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_administrator_of_community(list.community.pk) and list.is_have_edit():
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class PhotoListCommunityRecover(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_administrator_of_community(list.community.pk):
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404

class AddPhotoInCommunityList(View):
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=self.kwargs["pk"])
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_item_in_list(photo.pk) and request.user.is_administrator_of_community(list.community.pk):
            list.photo_list.add(photo)
            return HttpResponse()
        else:
            raise Http404

class RemovePhotoFromCommunityList(View):
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=self.kwargs["pk"])
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_item_in_list(photo.pk) and request.user.is_administrator_of_community(list.community.pk):
            list.photo_list.remove(photo)
            return HttpResponse()
        else:
            raise Http404
