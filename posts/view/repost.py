from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from users.models import User
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.attach.post_attacher import get_post_attach
from common.processing.post import get_post_processing
from common.template.user import get_detect_platform_template
from notify.model.post import *


class UUCMPostWindow(TemplateView):
    """
    форма репоста записи пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user, self.template_name = User.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("posts/post_repost_window/u_ucm_post.html", request.user, request.META['HTTP_USER_AGENT'])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        return super(UUCMPostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMPostWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = Post.objects.get(uuid=self.kwargs["uuid"])
        context["user"] = self.user
        return context

class CUCMPostWindow(TemplateView):
    """
    форма репоста записи сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("posts/post_repost_window/c_ucm_post.html", request.user, request.META['HTTP_USER_AGENT'])
        check_can_get_lists(request.user, self.community)
        return super(CUCMPostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMPostWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = Post.objects.get(uuid=self.kwargs["uuid"])
        context["community"] = self.community
        return context

class UUPostRepost(View):
    """
    создание репоста записи пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        parent, user, form_post, lists = Post.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist("lists")
        if user != request.user:
            check_user_can_get_list(request.user, user)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            if parent.parent:
                parent = parent.parent
            else:
                parent = parent
            new_post = post.create_post(creator=request.user, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            if parent.creator.pk != request.user.pk:
                post_repost_notification_handler(request.user, parent.creator, None, parent, PostNotify.REPOST)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUPostRepost(View):
    """
    создание репоста записи сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        parent, community, form_post, lists = Post.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist("lists")
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            if parent.parent:
                parent = parent.parent
            else:
                parent = parent
            new_post = post.create_post(creator=request.user, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            post_repost_community_notification_handler(request.user, community, None, parent, PostCommunityNotify.REPOST)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCPostRepost(View):
    """
    создание репоста записи пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        parent, user, form_post, lists, communities = Post.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist("lists"), request.POST.getlist("communities")
        if user != request.user:
            check_user_can_get_list(request.user, user)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            if parent.parent:
                parent = parent.parent
            else:
                parent = parent
            if not communities:
                return HttpResponseBadRequest()
            for community_id in communities:
                community = Community.objects.get(pk=community_id)
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
                    get_post_attach(request, new_post)
                    get_post_processing(new_post)
                    if parent.creator.pk != request.user.pk:
                        post_repost_notification_handler(request.user, parent.creator, community, parent, PostNotify.COMMUNITY_REPOST)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CCPostRepost(View):
    """
    создание репоста записи сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        parent, community, form_post, lists, communities = Post.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist("lists"), request.POST.getlist("communities")
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            if parent.parent:
                parent = parent.parent
            else:
                parent = parent
            if not communities:
                return HttpResponseBadRequest()
            for community_id in communities:
                _community = Community.objects.get(pk=community_id)
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
                    get_post_attach(request, new_post)
                    get_post_processing(new_post)
                    post_repost_community_notification_handler(request.user, community, _community, parent, PostCommunityNotify.COMMUNITY_REPOST)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UMPostRepost(View):
    """
    создание репоста записи пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        parent, user, connections, form_post = Post.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"]), request.POST.getlist("chat_items"), PostForm(request.POST)
        if user != request.user:
            check_user_can_get_list(request.user, user)
        if not connections:
            return HttpResponseBadRequest()

        if request.is_ajax() and form_post.is_valid():
            from common.attach.message_attacher import get_message_attach
            from chat.models import Message, Chat

            post = form_post.save(commit=False)
            if parent.parent:
                parent = parent.parent
            else:
                parent = parent
            for object_id in connections:
                new_post = post.create_post(creator=request.user, category=None, lists=[], is_signature=False, text=post.text, community=None, comments_enabled=False, votes_on=False, parent=parent, status="PG")
                get_post_attach(request, new_post)
                if object_id[0] == "c":
                    chat = Chat.objects.get(pk=object_id[1:])
                    message = Message.send_message(chat=chat, creator=request.user, post=new_post, parent=None, text="Репост записи пользователя")
                    get_message_attach(request, message)
                elif object_id[0] == "u":
                    user = User.objects.get(pk=object_id[1:])
                    message = Message.get_or_create_chat_and_send_message(creator=request.user, user=user, post=new_post, text="Репост записи пользователя")
                    get_message_attach(request, message)
                else:
                    return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
        return HttpResponse()

class CMPostRepost(View):
    """
    создание репоста записи сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        parent, community, connections, form_post = Post.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"]), request.POST.getlist("chat_items"), PostForm(request.POST)
        check_can_get_lists(request.user, community)

        if not connections:
            return HttpResponseBadRequest()
        if request.is_ajax() and form_post.is_valid():
            from common.attach.message_attacher import get_message_attach
            from chat.models import Message, Chat

            post = form_post.save(commit=False)
            if parent.parent:
                parent = parent.parent
            else:
                parent = parent
            for object_id in connections:
                new_post = post.create_post(creator=request.user, category=None, lists=[], is_signature=False, text=post.text, community=community, comments_enabled=False, votes_on=False, parent=parent, status="PG")
                get_post_attach(request, new_post)
                if object_id[0] == "c":
                    chat = Chat.objects.get(pk=object_id[1:])
                    message = Message.send_message(chat=chat, creator=request.user, post=new_post, parent=None, text="Репост записи сообщества")
                    get_message_attach(request, message)
                elif object_id[0] == "u":
                    user = User.objects.get(pk=object_id[1:])
                    message = Message.get_or_create_chat_and_send_message(creator=request.user, user=user, post=new_post, text="Репост записи сообщества")
                    get_message_attach(request, message)
                else:
                    return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
        return HttpResponse()
