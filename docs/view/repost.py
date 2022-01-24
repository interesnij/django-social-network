from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post, PostsList
from docs.models import Doc, DocsList
from users.models import User
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists


class UUCMDocWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.doc, self.template_name = Doc.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("docs/repost/u_ucm_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.doc.list.is_user_can_copy_el(request.user.pk)
        if self.doc.creator != request.user:
            check_user_can_get_list(request.user, self.doc.creator)
        return super(UUCMDocWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UUCMDocWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["can_copy_item"] = PostForm(), self.doc, self.can_copy_item
        return c

class CUCMDocWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.doc, self.template_name = Doc.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("docs/repost/c_ucm_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.doc.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.doc.community)
        return super(CUCMDocWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CUCMDocWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["community"], c["can_copy_item"] = PostForm(), self.doc, self.doc.community, self.can_copy_item
        return c


class UUCMDocListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.list, self.template_name = DocsList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("docs/repost/u_ucm_list.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        if self.list.creator != request.user:
            check_user_can_get_list(request.user, self.user)
        return super(UUCMDocListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UUCMDocListWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["can_copy_item"] = PostForm(), self.list, self.can_copy_item
        return c

class CUCMDocListWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.list, self.template_name = DocsList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("docs/repost/c_ucm_list.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.list.community)
        return super(CUCMDocListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CUCMDocListWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["community"], c["can_copy_item"] = PostForm(), self.list, self.list.community, self.can_copy_item
        return c


class UUDocRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        doc, form_post, attach, lists, count, creator = Doc.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if doc.creator.pk != creator.pk:
            check_user_can_get_list(creator, doc.creator)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=doc.creator, community=None, attach="doc"+str(doc.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=request.user, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                user_notify(creator, None, parent.pk, "DOC", "create_u_doc_notify", "RE")
                user_wall(creator, None, parent.pk, "DOC", "create_u_doc_wall", "RE")

            doc.repost += count
            doc.save(update_fields=["repost"])
            creator.plus_posts(count)

            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUDocRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        doc, form_post, attach, lists, count, creator = Doc.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, doc.community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=doc.creator, community=doc.community, attach="doc"+str(doc.pk))

            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                community_notify(creator, parent.community, None, parent.pk, "DOC", "create_c_doc_notify", "RE")
                community_wall(creator, parent.community, None, parent.pk, "DOC", "create_c_doc_wall", "RE")

            doc.repost += count
            doc.save(update_fields=["repost"])

            creator.plus_posts(count)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCDocRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        doc, form_post, attach, lists, count, creator = Doc.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if doc.creator.pk != creator.pk:
            check_user_can_get_list(creator, doc.creator)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=doc.creator, community=None, attach="doc"+str(doc.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    user_notify(creator, community.pk, parent.pk, "DOC", "create_u_doc_notify", "CR")
                    user_wall(creator, community.pk, parent.pk, "DOC", "create_u_doc_wall", "CR")

            doc.repost += count
            doc.save(update_fields=["repost"])
        return HttpResponse()


class CCDocRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        doc, form_post, attach, lists, count, creator = Doc.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, doc.community)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=doc.creator, community=doc.community, attach="doc"+str(doc.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    community_notify(creator, parent.community, community.pk, parent.pk, "DOC", "create_c_doc_notify", "CR")
                    community_wall(creator, parent.community, community.pk, parent.pk, "DOC", "create_c_doc_wall", "CR")

            doc.repost += count
            doc.save(update_fields=["repost"])
        return HttpResponse()


class UMDocRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        doc = Doc.objects.get(pk=self.kwargs["pk"])
        if doc.creator.pk != request.user.pk:
            check_user_can_get_list(request.user, doc.creator)
        repost_message_send(doc, "doc"+str(doc.pk), None, request)

        return HttpResponse()


class CMDocRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        doc = Doc.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, doc.community)
        repost_message_send(doc, "doc"+str(doc.pk), doc.community, request)
        return HttpResponse()


class UUDocListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        list, form_post, attach, lists, count, creator = DocsList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if list.creator.pk != creator.pk:
            check_user_can_get_list(creator, list.creator)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, attach="ldo"+str(list.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=request.user, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                user_notify(creator, None, parent.pk, "DOL", "create_u_doc_notify", "RE")
                user_wall(creator, None, parent.pk, "DOL", "create_u_doc_wall", "RE")

            list.repost += count
            list.save(update_fields=["repost"])
            creator.plus_posts(count)

            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUDocListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        list, form_post, attach, lists, count, creator = DocsList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, list.community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=list.community, attach="ldo"+str(list.pk))

            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
                count += 1

                community_notify(creator, parent.community, None, parent.pk, "DOL", "create_c_doc_notify", "RE")
                community_wall(creator, parent.community, None, parent.pk, "DOL", "create_c_doc_wall", "RE")

            list.repost += count
            list.save(update_fields=["repost"])

            creator.plus_posts(count)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCDocListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import user_notify, user_wall

        list, form_post, attach, lists, count, creator = DocsList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        if list.creator.pk != creator.pk:
            check_user_can_get_list(creator, list.creator)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, attach="ldo"+str(list.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    user_notify(creator, community.pk, parent.pk, "DOL", "create_u_doc_notify", "CR")
                    user_wall(creator, community.pk, parent.pk, "DOL", "create_u_doc_wall", "CR")

            list.repost += count
            list.save(update_fields=["repost"])
        return HttpResponse()


class CCDocListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.notify.notify import community_notify, community_wall

        list, form_post, attach, lists, count, creator = DocsList.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items'), request.POST.getlist('lists'), 0, request.user
        check_can_get_lists(creator, list.community)

        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=list.community, attach="ldo"+str(list.pk))
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if post_list.is_user_can_create_el(creator.pk):
                    community = post_list.community
                    post.create_post(creator=creator, list=post_list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

                    community_notify(creator, parent.community, community.pk, parent.pk, "DOL", "create_c_doc_notify", "CR")
                    community_wall(creator, parent.community, community.pk, parent.pk, "DOL", "create_c_doc_wall", "CR")

            list.repost += count
            list.save(update_fields=["repost"])
        return HttpResponse()


class UMDocListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        list = DocsList.objects.get(pk=self.kwargs["pk"])
        if list.creator.pk != request.user.pk:
            check_user_can_get_list(request.user, list.creator)
        repost_message_send(list, "ldo"+str(list.pk), None, request)

        return HttpResponse()


class CMDocListRepost(View):
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        list = DocsList.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, list.community)
        repost_message_send(list, "ldo"+str(list.pk), list.community, request)
        return HttpResponse()
