from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from posts.forms import PostForm
from posts.models import Post
from video.models import Video, VideoList
from users.models import User
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.processing.post import get_post_processing, repost_message_send
from common.templates import get_detect_platform_template


class UUCMVideoWindow(TemplateView):
    """
    форма репоста видеозаписи пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        self.template_name = get_detect_platform_template("video/repost/u_ucm_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UUCMVideoWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMVideoWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.video
        context["user"] = self.user
        return context

class CUCMVideoWindow(TemplateView):
    """
    форма репоста видеозаписи сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, self.community)
        self.template_name = get_detect_platform_template("video/repost/c_ucm_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CUCMVideoWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMVideoWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.video
        context["community"] = self.community
        return context


class UUCMVideoListWindow(TemplateView):
    """
    форма репоста видеоальбома пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        self.template_name = get_detect_platform_template("video/repost/u_ucm_video_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UUCMVideoListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMVideoListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.list
        context["user"] = self.user
        return context

class CUCMVideoListWindow(TemplateView):
    """
    форма репоста видеоальбома сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, self.community)
        self.template_name = get_detect_platform_template("video/repost/c_ucm_video_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CUCMVideoListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMVideoListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.list
        context["community"] = self.community
        return context


class UUVideoRepost(View):
    """
    создание репоста видеозаписи пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        attach = request.POST.getlist('attach_items')
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=video.creator, community=None, attach="vid"+str(video.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, is_public=request.POST.get("is_public"),community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUVideoRepost(View):
    """
    создание репоста видеозаписи сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        attach = request.POST.getlist('attach_items')
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=video.creator, community=community, attach="vid"+str(video.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, is_public=request.POST.get("is_public"),community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCVideoRepost(View):
    """
    создание репоста видеозаписи пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
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
            parent = Post.create_parent_post(creator=video.creator, community=community, attach="vid"+str(video.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, is_public=request.POST.get("is_public"),community=Community.objects.get(pk=community_id))
        return HttpResponse()


class CCVideoRepost(View):
    """
    создание репоста видеозаписи сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=video.creator, community=community, attach="vid"+str(video.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, is_public=request.POST.get("is_public"),community=Community.objects.get(pk=community_id))
        return HttpResponse()


class UMVideoRepost(View):
    """
    создание репоста видеозаписи пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(video, "vid"+str(video.pk), None, request, "Репост видеозаписи пользователя")
        return HttpResponse()


class CMVideoRepost(View):
    """
    создание репоста видеозаписи сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(video, "vid"+str(video.pk), community, request, "Репост видеозаписи сообщества")
        return HttpResponse()


class UUVideoListRepost(View):
    """
    создание репоста видеоальбома пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        attach = request.POST.getlist('attach_items')
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, attach="lvi"+str(list.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, is_public=request.POST.get("is_public"),community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUVideoListRepost(View):
    """
    создание репоста видеоальбома сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        attach = request.POST.getlist('attach_items')
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=community, attach="lvi"+str(list.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, is_public=request.POST.get("is_public"),community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCVideoListRepost(View):
    """
    создание репоста видеоальбома пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
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
            parent = Post.create_parent_post(creator=list.creator, community=community, attach="lvi"+str(list.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, is_public=request.POST.get("is_public"),community=Community.objects.get(pk=community_id))
        return HttpResponse()


class CCVideoListRepost(View):
    """
    создание репоста видеоальбома сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=community, attach="lvi"+str(list.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, is_public=request.POST.get("is_public"),community=Community.objects.get(pk=community_id))
        return HttpResponse()


class UMVideoListRepost(View):
    """
    создание репоста видеоальбома пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(list, "lvi"+str(list.pk), None, request, "Репост видеоальбома пользователя")
        return HttpResponse()


class CMVideoListRepost(View):
    """
    создание репоста видеоальбома сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(list, "lvi"+str(list.pk), community, request, "Репост видеоальбома сообщества")
        return HttpResponse()
