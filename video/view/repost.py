from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post, PostsList
from video.models import Video, VideoList
from users.models import User
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists


class UUCMVideoWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.video, self.template_name = Video.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("video/repost/u_ucm_video.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.video.list.is_user_can_copy_el(request.user.pk)
        if self.video.creator != request.user:
            check_user_can_get_list(request.user, self.video.creator)
        return super(UUCMVideoWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UUCMVideoWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["can_copy_item"] = PostForm(), self.video, self.can_copy_item
        return c

class CUCMVideoWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.video, self.template_name = Video.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("video/repost/c_ucm_video.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.video.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.video.community)
        return super(CUCMVideoWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CUCMVideoWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["community"], c["can_copy_item"] = PostForm(), self.video, self.video.community, self.can_copy_item
        return c


class UUCMVideoListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.list, self.template_name = VideoList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("video/repost/u_ucm_list.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        if self.list.creator != request.user:
            check_user_can_get_list(request.user, self.user)
        return super(UUCMVideoListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UUCMVideoListWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["can_copy_item"] = PostForm(), self.list, self.can_copy_item
        return c

class CUCMVideoListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.list, self.template_name = VideoList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("video/repost/c_ucm_list.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.list.community)
        return super(CUCMVideoListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CUCMVideoListWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["community"], c["can_copy_item"] = PostForm(), self.list, self.list.community, self.can_copy_item
        return c


class UUVideoRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        video, form_post, attach, lists, count, creator = Video.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if video.creator.pk != creator.pk:
            check_user_can_get_list(creator, video.creator)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=video.creator, community=None, attach="vid"+str(video.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=request.user, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                user_notify(creator, None, parent.pk, "VID", "create_u_video_notify", "RE")
                user_wall(creator, None, parent.pk, "VID", "create_u_video_wall", "RE")

            video.repost += count
            video.save(update_fields=["repost"])
            creator.plus_posts(count)

            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUVideoRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        video, form_post, attach, lists, count, creator = Video.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, video.community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=video.creator, community=video.community, attach="vid"+str(video.pk))

            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                community_notify(creator, parent.community, None, parent.pk, "VID", "create_c_video_notify", "RE")
                community_wall(creator, parent.community, None, parent.pk, "VID", "create_c_video_wall", "RE")

            video.repost += count
            video.save(update_fields=["repost"])

            creator.plus_posts(count)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCVideoRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        video, form_post, attach, lists, count, creator = Video.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if video.creator.pk != creator.pk:
            check_user_can_get_list(creator, video.creator)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=video.creator, community=None, attach="vid"+str(video.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    user_notify(creator, community.pk, parent.pk, "VID", "create_u_video_notify", "CR")
                    user_wall(creator, community.pk, parent.pk, "VID", "create_u_video_wall", "CR")

            video.repost += count
            video.save(update_fields=["repost"])
        return HttpResponse()


class CCVideoRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        video, form_post, attach, lists, count, creator = Video.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, video.community)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=video.creator, community=video.community, attach="vid"+str(video.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    community_notify(creator, parent.community, community.pk, parent.pk, "VID", "create_c_video_notify", "CR")
                    community_wall(creator, parent.community, community.pk, parent.pk, "VID", "create_c_video_wall", "CR")

            video.repost += count
            video.save(update_fields=["repost"])
        return HttpResponse()


class UMVideoRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        video = Video.objects.get(pk=self.kwargs["pk"])
        if video.creator.pk != request.user.pk:
            check_user_can_get_list(request.user, video.creator)
        repost_message_send(video, "vid"+str(video.pk), None, request)

        return HttpResponse()


class CMVideoRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        video = Video.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, video.community)
        repost_message_send(video, "vid"+str(video.pk), video.community, request)
        return HttpResponse()


class UUVideoListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        list, form_post, attach, lists, count, creator = VideoList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if list.creator.pk != creator.pk:
            check_user_can_get_list(creator, list.creator)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, attach="lvi"+str(list.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=request.user, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                user_notify(creator, None, parent.pk, "VIL", "create_u_video_notify", "RE")
                user_wall(creator, None, parent.pk, "VIL", "create_u_video_wall", "RE")

            list.repost += count
            list.save(update_fields=["repost"])
            creator.plus_posts(count)

            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUVideoListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        list, form_post, attach, lists, count, creator = VideoList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, list.community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=list.community, attach="lvi"+str(list.pk))

            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                community_notify(creator, parent.community, None, parent.pk, "VIL", "create_c_video_notify", "RE")
                community_wall(creator, parent.community, None, parent.pk, "VIL", "create_c_video_wall", "RE")

            list.repost += count
            list.save(update_fields=["repost"])

            creator.plus_posts(count)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCVideoListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        list, form_post, attach, lists, count, creator = VideoList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if list.creator.pk != creator.pk:
            check_user_can_get_list(creator, list.creator)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, attach="lvi"+str(list.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    user_notify(creator, community.pk, parent.pk, "VIL", "create_u_video_notify", "CR")
                    user_wall(creator, community.pk, parent.pk, "VIL", "create_u_video_wall", "CR")

            list.repost += count
            list.save(update_fields=["repost"])
        return HttpResponse()


class CCVideoListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        list, form_post, attach, lists, count, creator = VideoList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, list.community)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=list.community, attach="lvi"+str(list.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    community_notify(creator, parent.community, community.pk, parent.pk, "VIL", "create_c_video_notify", "CR")
                    community_wall(creator, parent.community, community.pk, parent.pk, "VIL", "create_c_video_wall", "CR")

            list.repost += count
            list.save(update_fields=["repost"])
        return HttpResponse()


class UMVideoListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        list = VideoList.objects.get(pk=self.kwargs["pk"])
        if list.creator.pk != request.user.pk:
            check_user_can_get_list(request.user, list.creator)
        repost_message_send(list, "lvi"+str(list.pk), None, request)

        return HttpResponse()


class CMVideoListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        list = VideoList.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, list.community)
        repost_message_send(list, "lvi"+str(list.pk), list.community, request)
        return HttpResponse()
