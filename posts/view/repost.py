from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from common.templates import (
								get_template_community_item,
								get_template_anon_community_item,
								get_template_user_item,
								get_template_anon_user_item,
								#get_template_community_list,
								#get_template_anon_community_list,
								#get_template_user_list,
								#get_template_anon_user_list,
							)


class UUPostCopy(View):
    def post(self, request, *args, **kwargs):
        parent, lists, count = Post.objects.get(pk=self.kwargs["pk"]), request.POST.getlist('lists'), 0

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            if parent.creator.pk != request.user.pk:
                check_user_can_get_list(request.user, parent.creator)
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if parent.list.pk != post_list.pk and post_list.is_user_can_create_el(request.user.pk):
                    Post.create_post(creator=parent.creator, list=post_list, attach=parent.attach, text=parent.text, category=parent.category, comments_enabled=parent.comments_enabled, is_signature=False, votes_on=parent.votes_on, community=None)
                    count += 1
            if count > 0:
                parent.copy += count
                parent.save(update_fields=["copy"])

                creator.plus_posts(count)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUPostCopy(View):
    def post(self, request, *args, **kwargs):
        parent, lists, count = Post.objects.get(pk=self.kwargs["pk"]), request.POST.getlist('lists'), 0
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            check_can_get_lists(request.user, list.community)
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if parent.list.pk != post_list.pk and post_list.is_user_can_create_el(request.user.pk):
                    Post.create_post(creator=parent.creator, list=post_list, attach=parent.attach, text=parent.text, category=parent.category, comments_enabled=parent.comments_enabled, is_signature=False, votes_on=parent.votes_on, community=None)
                    count += 1

            if count > 0:
                parent.copy += count
                parent.save(update_fields=["copy"])

                creator.plus_posts(count)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCPostCopy(View):
    def post(self, request, *args, **kwargs):
        parent, lists, count = Post.objects.get(pk=self.kwargs["pk"]), request.POST.getlist('lists'), 0
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            if parent.creator.pk != request.user.pk:
                check_user_can_get_list(request.user, parent.creator)
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if parent.list.pk != post_list.pk and post_list.is_user_can_create_el(request.user.pk):
                    community = post_list.community
                    Post.create_post(creator=parent.creator, list=post_list, attach=parent.attach, text=parent.text, category=parent.category, comments_enabled=parent.comments_enabled, is_signature=False, votes_on=parent.votes_on, community=community)
                    count += 1
                    community.plus_posts(1)

            if count > 0:
                parent.copy += count
                parent.save(update_fields=["copy"])

            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CCPostCopy(View):
    def post(self, request, *args, **kwargs):
        parent, lists, count = Post.objects.get(pk=self.kwargs["pk"]), request.POST.getlist('lists'), 0
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            check_can_get_lists(request.user, list.community)
            for list_pk in lists:
                post_list = PostsList.objects.get(pk=list_pk)
                if parent.list.pk != post_list.pk and post_list.is_user_can_create_el(request.user.pk):
                    community = post_list.community
                    Post.create_post(creator=parent.creator, list=post_list, attach=parent.attach, text=parent.text, category=parent.category, comments_enabled=parent.comments_enabled, is_signature=False, votes_on=parent.votes_on, community=community)
                    count += 1

            if count > 0:
                parent.copy += count
                parent.save(update_fields=["copy"])

            return HttpResponse()
        else:
            return HttpResponseBadRequest()
