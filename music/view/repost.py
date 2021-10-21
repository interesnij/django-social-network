from django.views.generic.base import TemplateView
from communities.models import Community
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from music.models import SoundList, Music
from users.models import User
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.processing.post import repost_message_send
from common.templates import get_detect_platform_template
from django.views import View


class UUCMMusicWindow(TemplateView):
    """
    форма репоста аудиозаписи пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.track, self.user = Music.objects.get(pk=self.kwargs["track_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        self.template_name = get_detect_platform_template("music/repost/u_ucm_music.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
        return super(UUCMMusicWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMMusicWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.track
        context["user"] = self.user
        return context

class CUCMMusicWindow(TemplateView):
    """
    форма репоста аудиозаписи сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.track, self.community = Music.objects.get(pk=self.kwargs["track_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, self.community)
        self.template_name = get_detect_platform_template("music/repost/c_ucm_music.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
        return super(CUCMMusicWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMMusicWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.track
        context["community"] = self.community
        return context

class UUCMMusicListWindow(TemplateView):
    """
    форма репоста плейлиста пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.playlist, self.user = SoundList.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        self.template_name = get_detect_platform_template("music/repost/u_ucm_list_music.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
        return super(UUCMMusicListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMMusicListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.playlist
        context["user"] = self.user
        return context

class CUCMMusicListWindow(TemplateView):
    """
    форма репоста плейлиста сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.playlist, self.community = SoundList.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, self.community)
        self.template_name = get_detect_platform_template("music/repost/c_ucm_list_music.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
        return super(CUCMMusicListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMMusicListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.playlist
        context["community"] = self.community
        return context


class UUMusicRepost(View):
    """
    создание репоста записи пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        track, user, attach = Music.objects.get(pk=self.kwargs["track_pk"]), User.objects.get(pk=self.kwargs["pk"]), request.POST.getlist('attach_items')
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=user, community=None, attach="mus"+str(track.pk))
            track.item.add(parent)
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, is_signature=False, text=post.text, comments_enabled=post.comments_enabled, parent=parent, is_public=request.POST.get("is_public"),community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUMusicRepost(View):
    """
    создание репоста записи сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        track, community, form_post, attach = Music.objects.get(pk=self.kwargs["track_pk"]), Community.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items')
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=request.user, community=community, attach="mus"+str(track.pk))
            track.item.add(parent)
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, is_signature=False, text=post.text, comments_enabled=post.comments_enabled, parent=parent, is_public=request.POST.get("is_public"),community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCMusicRepost(View):
    """
    создание репоста записи пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        track, user = Music.objects.get(pk=self.kwargs["track_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        communities = request.POST.getlist("communities")
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, attach="mus"+str(track.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on,is_public=request.POST.get("is_public"),community=Community.objects.get(pk=community_id))
        return HttpResponse()

class CCMusicRepost(View):
    """
    создание репоста записи сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        track, community = Music.objects.get(pk=self.kwargs["track_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        communities = request.POST.getlist("communities")
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, community=community, attach="mus"+str(track.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, is_public=request.POST.get("is_public"),community=Community.objects.get(pk=community_id))
        return HttpResponse()


class UMMusicRepost(View):
    """
    создание репоста записи пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        track, user = Music.objects.get(pk=self.kwargs["track_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(track, "mus"+str(track.pk), None, request, "Репост плейлиста пользователя")
        return HttpResponse()

class CMMusicRepost(View):
    """
    создание репоста записи сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        track, community = Music.objects.get(pk=self.kwargs["track_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(track, "mus"+str(track.pk), community, request, "Репост плейлиста сообщества")
        return HttpResponse()


class UUMusicListRepost(View):
    """
    создание репоста плейлиста пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        playlist, user, attach = SoundList.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"]), request.POST.getlist('attach_items')
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=playlist.creator, community=None, attach="lmu"+str(playlist.pk))
            playlist.post.add(parent)
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, is_signature=False, text=post.text, comments_enabled=post.comments_enabled, parent=parent, is_public=request.POST.get("is_public"),community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUMusicListRepost(View):
    """
    создание репоста плейлиста сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        playlist, community, form_post, attach = SoundList.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items')
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=playlist.creator, community=community, attach="lmu"+str(playlist.pk))
            playlist.post.add(parent)
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, is_signature=False, text=post.text, comments_enabled=post.comments_enabled, parent=parent, is_public=request.POST.get("is_public"),community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCMusicListRepost(View):
    """
    создание репоста плейлиста пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        playlist, user = SoundList.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=playlist.creator, attach="lmu"+str(playlist.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, is_public=request.POST.get("is_public"),community=Community.objects.get(pk=community_id))
        return HttpResponse()


class CCMusicListRepost(View):
    """
    создание репоста плейлиста сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        playlist, community = SoundList.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=playlist.creator, attach="lmu"+str(playlist.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, is_public=request.POST.get("is_public"),community=Community.objects.get(pk=community_id))
        return HttpResponse()


class UMMusicListRepost(View):
    """
    создание репоста плейлиста пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        playlist, user = SoundList.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(playlist, "lmu"+str(playlist.pk), None, request, "Репост плейлиста пользователя")
        return HttpResponse()


class CMMusicListRepost(View):
    """
    создание репоста плейлиста сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        playlist, community = SoundList.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(playlist, "lmu"+str(playlist.pk), community, request, "Репост плейлиста сообщества")
        return HttpResponse()
