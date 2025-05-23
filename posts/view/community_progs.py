from django.views.generic.base import TemplateView
from users.models import User
from posts.models import *
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from communities.models import Community
from posts.forms import *
from common.check.community import check_can_get_lists
from django.views.generic.base import TemplateView


class PostCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = PostForm(request.POST)
        list = PostsList.objects.get(pk=self.kwargs["pk"])
        community = list.community
        creator = request.user
        if (community and request.user.is_administrator_of_community(community.pk)) \
            or (not community and creator.pk == list.creator.pk):
            can_create = True
        else:
            can_create = list.is_user_can_create_el(request.user.pk)

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and form_post.is_valid() and can_create:
            post = form_post.save(commit=False)

            if request.POST.get('text') or request.POST.get('attach_items'):
                from common.templates import render_for_platform

                attach = request.POST.getlist('attach_items')
                new_post = post.create_post(
                                            creator=creator,
                                            attach=attach,
                                            text=post.text,
                                            category=post.category,
                                            list=list,
                                            parent=None,
                                            comments_enabled=post.comments_enabled,
                                            is_signature=post.is_signature,
                                            votes_on=post.votes_on,
                                            community=community,
                                        )

                from common.notify.progs import community_send_notify, community_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="POS", object_id=new_post.pk, verb="ITE")
                community_send_wall(new_post.pk, creator.pk, community.pk, None, "create_c_post_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="POS", object_id=new_post.pk, verb="ITE")
                    community_send_notify(new_post.pk, creator.pk, user_id, community.pk, None, "create_c_post_notify")
                community.plus_posts(1)
                return render_for_platform(request, 'posts/post_community/admin_post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()

class CommunitySaveCreatorDraftPost(View):
    def post(self,request,*args,**kwargs):
        from common.check.community import check_private_post_exists

        form_post = PostForm(request.POST)
        list = PostsList.objects.get(pk=self.kwargs["pk"])
        community = list.community

        check_private_post_exists(community)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and form_post.is_valid():
            check_can_get_lists(request.user, community)
            post = form_post.save(commit=False)
            new_post = post.create_creator_draft_post(
                                        creator=request.user,
                                        attach=request.POST.getlist('attach_items'),
                                        text=post.text,
                                        category=post.category,
                                        list=list,
                                        comments_enabled=post.comments_enabled,
                                        is_signature=post.is_signature,
                                        votes_on=post.votes_on,
                                        community=community
                                        )
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommunitySaveOfferDraftPost(View):
    def post(self,request,*args,**kwargs):
        from common.check.community import check_private_post_exists

        form_post = PostForm(request.POST)
        list = PostsList.objects.get(pk=self.kwargs["pk"])
        community = list.community

        check_private_post_exists(community)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and form_post.is_valid():
            check_can_get_lists(request.user, community)
            post = form_post.save(commit=False)
            new_post = post.create_creator_offer_post(
                                        creator=request.user,
                                        attach=request.POST.getlist('attach_items'),
                                        text=post.text,
                                        category=post.category,
                                        list=list,
                                        comments_enabled=post.comments_enabled,
                                        is_signature=post.is_signature,
                                        votes_on=post.votes_on,
                                        community=community
                                        )
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class PostCommunityEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_admin_template
        self.post = Post.objects.get(pk=self.kwargs["pk"])
        self.community = self.post.community
        if request.user.is_administrator_of_community(self.community.pk):
            self.template_name = get_admin_template(self.community, "posts/post_community/edit_post.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PostCommunityEdit,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostCommunityEdit, self).get_context_data(**kwargs)
        context['post'] = self.post
        context['form'] = PostForm(instance=self.post)
        return context

    def post(self,request,*args,**kwargs):
        _post = Post.objects.get(pk=self.kwargs["pk"])
        community_pk = _post.community.pk
        form_post, attach = PostForm(request.POST, instance=_post), request.POST.getlist('attach_items')

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and form_post.is_valid() and request.user.is_administrator_of_community(community_pk):
            post = form_post.save(commit=False)
            if post.text or attach:
                from common.templates import render_for_platform
                new_post = post.edit_post(text=post.text,category=post.category,list=post.list,attach=attach,comments_enabled=post.comments_enabled,is_signature=post.is_signature,votes_on=post.votes_on)
                return render_for_platform(request, 'posts/post_community/admin_post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostOfferCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        from common.check.community import check_private_post_exists

        form_post = PostForm(request.POST)
        list = PostsList.objects.get(pk=self.kwargs["pk"])
        community = list.community
        check_private_post_exists(community)

        if community.is_wall_close():
            raise Http404
        elif community.is_staff_post_member_can() and not request.user.is_member_of_community(community.pk):
            raise Http404
        elif request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and form_post.is_valid():
            check_can_get_lists(request.user, community)
            post = form_post.save(commit=False)
            if request.POST.get('text') or request.POST.getlist('attach_items'):
                from common.notify.notify import community_notify
                from common.processing.post import get_post_offer_processing
                from common.templates import render_for_platform

                lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
                new_post = post.create_offer_post(
                                            creator=request.user,
                                            attach=attach,
                                            text=post.text,
                                            list=list,
                                            community=community)
                return render_for_platform(request, 'posts/post_community/post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()

class PostCommunityFixed(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_staff_of_community(post.community.pk):
            post.fixed_post(post.community)
            return HttpResponse()
        else:
            raise Http404

class PostCommunityUnFixed(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_staff_of_community(post.community.pk):
            post.unfixed_post()
            return HttpResponse()
        else:
            raise Http404

class PostCommunityOffComment(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_staff_of_community(item.community.pk):
            item.comments_enabled = False
            item.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class PostCommunityOnComment(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_staff_of_community(item.community.pk):
            item.comments_enabled = True
            item.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class PostCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        c = post.community
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_staff_of_community(c.pk):
            post.delete_item()
            return HttpResponse()
        else:
            raise Http404

class PostCommunityRecover(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        c = post.community
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_staff_of_community(c.pk):
            post.restore_item()
            return HttpResponse()
        else:
            raise Http404

class CommunityOnVotesPost(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_staff_of_community(post.community.pk):
            post.votes_on = True
            post.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOffVotesPost(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_staff_of_community(post.community.pk):
            post.votes_on = False
            post.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

def post_update_interactions(request):
    data_point = request.POST['id_value']
    item = Post.objects.get(pk=data_point)
    data = {'likes': item.count_likers(), 'dislikes': item.count_dislikers(), 'comments': item.count_thread()}
    return JsonResponse(data)
