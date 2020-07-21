from django.views.generic.base import TemplateView
from users.models import User
from django.shortcuts import render
from posts.models import Post
from django.http import HttpResponseBadRequest
from django.views import View
from communities.models import Community
from posts.forms import PostForm
from common.post_attacher import get_post_attach
from common.processing.post import get_post_processing, get_post_offer_processing


class PostCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = PostForm(request.POST)
        community = Community.objects.get(pk=self.kwargs["pk"])

        if (community.is_wall_close() or community.is_staff_post_member_can()) and not request.user.is_staff_of_community_with_name(community.name):
            raise PermissionDenied("Ошибка доступа.")
        elif (community.is_member_post_all_can() or community.is_member_post()) and not request.user.is_member_of_community_with_name(community.name):
            raise PermissionDenied("Ошибка доступа.")
        elif form_post.is_valid():
            post = form_post.save(commit=False)
            if request.POST.get('text') or request.POST.get('photo') or request.POST.get('video') or request.POST.get('music') or request.POST.get('good') or request.POST.get('article'):
                new_post = post.create_post(creator=request.user, text=post.text, community=community, comments_enabled=post.comments_enabled, is_signature=post.is_signature, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
                return render(request, 'post_community/admin_post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostOfferCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = PostForm(request.POST)
        community = Community.objects.get(pk=self.kwargs["pk"])

        if community.is_wall_close():
            raise PermissionDenied("Ошибка доступа.")
        elif community.is_staff_post_member_can() and not request.user.is_member_of_community_with_name(community.name):
            raise PermissionDenied("Ошибка доступа.")
        elif form_post.is_valid():
            post = form_post.save(commit=False)
            if request.POST.get('text') or request.POST.get('photo') or request.POST.get('video') or request.POST.get('music') or request.POST.get('good') or request.POST.get('article'):
                new_post = post.create_post(creator=request.user, text=post.text, community=community, comments_enabled=post.comments_enabled, is_signature=post.is_signature, status="PG")
                get_post_attach(request, new_post)
                get_post_offer_processing(new_post)
                return render(request, 'post_community/post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
