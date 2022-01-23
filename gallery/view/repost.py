from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post, PostsList
from gallery.models import Photo
from users.models import User
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists


class UUCMPhotoWindow(TemplateView):
    """
    форма репоста фотографии пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.photo, self.template_name = Photo.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("gallery/repost/u_ucm_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.photo.list.is_user_can_copy_el(request.user.pk)
        if self.photo.creator != request.user:
            check_user_can_get_list(request.user, self.photo.creator)
        return super(UUCMPhotoWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UUCMPhotoWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["can_copy_item"] = PostForm(), self.photo, self.can_copy_item
        return c

class CUCMPhotoWindow(TemplateView):
    """
    форма репоста фотографии сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.photo, self.template_name = Photo.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("gallery/repost/c_ucm_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.photo.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.photo.community)
        return super(CUCMPhotoWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CUCMPhotoWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["community"], c["can_copy_item"] = PostForm(), self.photo, self.photo.community, self.can_copy_item
        return c


class UUCMPhotoListWindow(TemplateView):
    """
    форма репоста фотоальбома пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        from gallery.models import PhotoList
        from common.templates import get_detect_platform_template

        self.list, self.template_name = PhotoList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("gallery/repost/u_ucm_list.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        if self.list.creator != request.user:
            check_user_can_get_list(request.user, self.user)
        return super(UUCMPhotoListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UUCMPhotoListWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["can_copy_item"] = PostForm(), self.list, self.can_copy_item
        return c

class CUCMPhotoListWindow(TemplateView):
    """
    форма репоста фотоальбома сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        from gallery.models import PhotoList
        from common.templates import get_detect_platform_template

        self.list, self.template_name = PhotoList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("gallery/repost/c_ucm_list.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.list.community)
        return super(CUCMPhotoListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CUCMPhotoListWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["community"], c["can_copy_item"] = PostForm(), self.list, self.list.community, self.can_copy_item
        return c


class UUPhotoRepost(View):
    """
    создание репоста фотографии пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        photo, form_post, attach, lists, count, creator = Photo.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if photo.creator.pk != creator.pk:
            check_user_can_get_list(creator, photo.creator)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, community=None, attach="pho"+str(photo.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=request.user, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                user_notify(creator, None, parent.pk, "PHO", "create_u_photo_notify", "RE")
                user_wall(creator, None, parent.pk, "PHO", "create_u_photo_wall", "RE")

            photo.repost += count
            photo.save(update_fields=["repost"])
            creator.plus_posts(count)

            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUPhotoRepost(View):
    """
    создание репоста фотографии сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        photo, form_post, attach, lists, count, creator = Photo.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, photo.community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, community=photo.community, attach="pho"+str(photo.pk))

            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                community_notify(creator, parent.community, None, parent.pk, "PHO", "create_c_photo_notify", "RE")
                community_wall(creator, parent.community, None, parent.pk, "PHO", "create_c_photo_wall", "RE")

            parent.repost += count
            parent.save(update_fields=["repost"])

            creator.plus_posts(count)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCPhotoRepost(View):
    """
    создание репоста фотографии пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        photo, form_post, attach, lists, count, creator = Photo.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if photo.creator.pk != creator.pk:
            check_user_can_get_list(creator, photo.creator)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, attach="pho"+str(photo.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    user_notify(creator, community, parent.pk, "PHO", "create_u_photo_notify", "CR")
                    user_wall(creator, community, parent.pk, "PHO", "create_u_photo_wall", "CR")

            parent.repost += count
            parent.save(update_fields=["repost"])
        return HttpResponse()


class CCPhotoRepost(View):
    """
    создание репоста фотографии сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        photo, form_post, attach, lists, count, creator = Photo.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, photo.community)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, community=photo.community, attach="pho"+str(photo.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    community_notify(creator, parent.community, community.pk, parent.pk, "PHO", "create_c_photo_notify", "CR")
                    community_wall(creator, parent.community, community.pk, parent.pk, "PHO", "create_c_photo_wall", "CR")

            parent.repost += count
            parent.save(update_fields=["repost"])
        return HttpResponse()


class UMPhotoRepost(View):
    """
    создание репоста фотографии пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(photo, "pho"+str(photo.pk), None, request)
        return HttpResponse()


class CMPhotoRepost(View):
    """
    создание репоста фотографии сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(photo, "pho"+str(photo.pk), community, request)
        return HttpResponse()


class UUPhotoListRepost(View):
    """
    создание репоста фотоальбома пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        from gallery.models import PhotoList

        list = PhotoList.objects.get(pk=self.kwargs["list_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        attach = request.POST.getlist('attach_items')
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, attach="lph"+str(list.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUPhotoListRepost(View):
    """
    создание репоста фотоальбома сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        from gallery.models import PhotoList

        list = PhotoList.objects.get(pk=self.kwargs["list_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        attach = request.POST.getlist('attach_items')
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=community, attach="lph"+str(list.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCPhotoListRepost(View):
    """
    создание репоста фотоальбома пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        from gallery.models import PhotoList

        list = PhotoList.objects.get(pk=self.kwargs["list_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, attach="lph"+str(list.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=Community.objects.get(pk=community_id))
        return HttpResponse()


class CCPhotoListRepost(View):
    """
    создание репоста фотоальбома сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        from gallery.models import PhotoList

        list = PhotoList.objects.get(pk=self.kwargs["list_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, attach="lph"+str(list.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=Community.objects.get(pk=community_id))
        return HttpResponse()


class UMPhotoListRepost(View):
    """
    создание репоста фотоальбома пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        from gallery.models import PhotoList
        from common.processing.post import repost_message_send

        list = PhotoList.objects.get(pk=self.kwargs["list_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(list, "lph"+str(list.pk), None, request)
        return HttpResponse()


class CMPhotoListRepost(View):
    """
    создание репоста фотоальбома сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        from gallery.models import PhotoList
        from common.processing.post import repost_message_send

        list = PhotoList.objects.get(pk=self.kwargs["list_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(list, "lph"+str(list.pk), community, request)
        return HttpResponse()
