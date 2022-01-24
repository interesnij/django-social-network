from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post, PostsList
from music.models import Music, MusicList
from users.models import User
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists


class UUCMMusicWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.music, self.template_name = Music.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("music/repost/u_ucm_music.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.music.list.is_user_can_copy_el(request.user.pk)
        if self.music.creator != request.user:
            check_user_can_get_list(request.user, self.music.creator)
        return super(UUCMMusicWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UUCMMusicWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["can_copy_item"] = PostForm(), self.music, self.can_copy_item
        return c

class CUCMMusicWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.music, self.template_name = Music.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("music/repost/c_ucm_music.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.music.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.music.community)
        return super(CUCMMusicWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CUCMMusicWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["community"], c["can_copy_item"] = PostForm(), self.music, self.music.community, self.can_copy_item
        return c


class UUCMMusicListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.list, self.template_name = MusicList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("music/repost/u_ucm_list.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        if self.list.creator != request.user:
            check_user_can_get_list(request.user, self.user)
        return super(UUCMMusicListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UUCMMusicListWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["can_copy_item"] = PostForm(), self.list, self.can_copy_item
        return c

class CUCMMusicListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.list, self.template_name = MusicList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("music/repost/c_ucm_list.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.list.community)
        return super(CUCMMusicListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CUCMMusicListWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["community"], c["can_copy_item"] = PostForm(), self.list, self.list.community, self.can_copy_item
        return c


class UUMusicRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        music, form_post, attach, lists, count, creator = Music.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if music.creator.pk != creator.pk:
            check_user_can_get_list(creator, music.creator)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=music.creator, community=None, attach="mus"+str(music.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=request.user, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                user_notify(creator, None, parent.pk, "MUS", "create_u_music_notify", "RE")
                user_wall(creator, None, parent.pk, "MUS", "create_u_music_wall", "RE")

            music.repost += count
            music.save(update_fields=["repost"])
            creator.plus_posts(count)

            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUMusicRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        music, form_post, attach, lists, count, creator = Music.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, music.community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=music.creator, community=music.community, attach="mus"+str(music.pk))

            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                community_notify(creator, parent.community, None, parent.pk, "MUS", "create_c_music_notify", "RE")
                community_wall(creator, parent.community, None, parent.pk, "MUS", "create_c_music_wall", "RE")

            music.repost += count
            music.save(update_fields=["repost"])

            creator.plus_posts(count)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCMusicRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        music, form_post, attach, lists, count, creator = Music.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if music.creator.pk != creator.pk:
            check_user_can_get_list(creator, music.creator)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=music.creator, community=None, attach="mus"+str(music.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    user_notify(creator, community.pk, parent.pk, "MUS", "create_u_music_notify", "CR")
                    user_wall(creator, community.pk, parent.pk, "MUS", "create_u_music_wall", "CR")

            music.repost += count
            music.save(update_fields=["repost"])
        return HttpResponse()


class CCMusicRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        music, form_post, attach, lists, count, creator = Music.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, music.community)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=music.creator, community=music.community, attach="mus"+str(music.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    community_notify(creator, parent.community, community.pk, parent.pk, "MUS", "create_c_music_notify", "CR")
                    community_wall(creator, parent.community, community.pk, parent.pk, "MUS", "create_c_music_wall", "CR")

            music.repost += count
            music.save(update_fields=["repost"])
        return HttpResponse()


class UMMusicRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        music = Music.objects.get(pk=self.kwargs["pk"])
        if music.creator.pk != request.user.pk:
            check_user_can_get_list(request.user, user)
        repost_message_send(music, "mus"+music.pk), None, request)

        return HttpResponse()


class CMMusicRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        music = Music.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, music.community)
        repost_message_send(music, "mus"+str(music.pk), music.community, request)
        return HttpResponse()


class UUMusicListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        list, form_post, attach, lists, count, creator = MusicList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if list.creator.pk != creator.pk:
            check_user_can_get_list(creator, list.creator)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, attach="lmu"+str(list.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=request.user, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                user_notify(creator, None, parent.pk, "MUL", "create_u_music_notify", "RE")
                user_wall(creator, None, parent.pk, "MUL", "create_u_music_wall", "RE")

            list.repost += count
            list.save(update_fields=["repost"])
            creator.plus_posts(count)

            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUMusicListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        list, form_post, attach, lists, count, creator = MusicList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, list.community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=list.community, attach="lmu"+str(list.pk))

            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                community_notify(creator, parent.community, None, parent.pk, "MUL", "create_c_music_notify", "RE")
                community_wall(creator, parent.community, None, parent.pk, "MUL", "create_c_music_wall", "RE")

            list.repost += count
            list.save(update_fields=["repost"])

            creator.plus_posts(count)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCMusicListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        list, form_post, attach, lists, count, creator = MusicList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if list.creator.pk != creator.pk:
            check_user_can_get_list(creator, list.creator)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, attach="lmu"+str(list.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    user_notify(creator, community.pk, parent.pk, "MUL", "create_u_music_notify", "CR")
                    user_wall(creator, community.pk, parent.pk, "MUL", "create_u_music_wall", "CR")

            list.repost += count
            list.save(update_fields=["repost"])
        return HttpResponse()


class CCMusicListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        list, form_post, attach, lists, count, creator = MusicList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, list.community)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=list.community, attach="lmu"+str(list.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    community_notify(creator, parent.community, community.pk, parent.pk, "MUL", "create_c_music_notify", "CR")
                    community_wall(creator, parent.community, community.pk, parent.pk, "MUL", "create_c_music_wall", "CR")

            list.repost += count
            list.save(update_fields=["repost"])
        return HttpResponse()


class UMMusicListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        list = MusicList.objects.get(pk=self.kwargs["pk"])
        if list.creator.pk != request.user.pk:
            check_user_can_get_list(request.user, user)
        repost_message_send(list, "lmu"+str(list.pk), None, request)

        return HttpResponse()


class CMMusicListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        list = MusicList.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, list.community)
        repost_message_send(list, "lmu"+str(list.pk), list.community, request)
        return HttpResponse()
