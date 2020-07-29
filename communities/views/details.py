import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from posts.models import Post
from communities.models import Community, CommunityMembership
from follows.models import CommunityFollow
from common.check.community import check_can_get_lists
from django.views.generic import ListView
from rest_framework.exceptions import PermissionDenied
from common.template.post import get_template_community_post


class PostCommunity(TemplateView):
    model = Post
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.items = self.community.get_posts()
        self.next = self.items.filter(pk__gt=self.item.pk).order_by('pk').first()
        self.prev = self.items.filter(pk__lt=self.item.pk).order_by('-pk').first()

        self.template_name = get_template_community_post(self.user, "c_lenta/", "item.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(PostCommunity,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommunity,self).get_context_data(**kwargs)
        context["object"] = self.item
        context["community"] = self.community
        context["next"] = self.next
        context["prev"] = self.prev
        return context


class CommunityDetail(TemplateView):
    template_name = None
    common_friends = None

    def get(self,request,*args,**kwargs):
        from stst.models import CommunityNumbers

        self.community = Community.objects.get(pk=self.kwargs["pk"])

        if self.community.is_suspended():
            self.template_name = "c_detail/community_suspended.html"
        elif self.community.is_blocked():
            self.template_name = "c_detail/community_blocked.html"
        elif request.user.is_authenticated:
            if request.user.is_member_of_community_with_name(self.community.name):
                if request.user.is_administrator_of_community_with_name(self.community.name):
                    self.template_name = "c_detail/admin_community.html"
                elif request.user.is_moderator_of_community_with_name(self.community.name):
                    self.template_name = "c_detail/moderator_community.html"
                elif request.user.is_editor_of_community_with_name(self.community.name):
                    self.template_name = "c_detail/editor_community.html"
                elif request.user.is_advertiser_of_community_with_name(self.community.name):
                    self.template_name = "c_detail/advertiser_community.html"
                elif request.user.is_community_manager():
                    self.template_name = "c_detail/staff_member_community.html"
                else:
                    self.template_name = "c_detail/member_community.html"
            elif request.user.is_follow_from_community_with_name(self.community.pk):
                self.template_name = "c_detail/follow_community.html"
            elif request.user.is_community_manager():
                self.template_name = "c_detail/staff_community.html"
            elif request.user.is_banned_from_community_with_name(self.community.name):
                self.template_name = "c_detail/block_community.html"
            elif self.community.is_public():
                if request.user.is_child() and not self.community.is_child_safety():
                    self.template_name = "c_detail/no_child_safety.html"
                else:
                    self.template_name = "c_detail/public_community.html"
            elif self.community.is_closed():
                self.template_name = "c_detail/close_community.html"
            elif self.community.is_private():
                self.template_name = "c_detail/private_community.html"
            if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
                CommunityNumbers.objects.create(user=request.user.pk, community=self.community.pk, platform=1)
            else:
                CommunityNumbers.objects.create(user=request.user.pk, community=self.community.pk, platform=0)
            self.common_friends = request.user.get_common_friends_of_community(self.community.pk)[0:6]
        elif request.user.is_anonymous:
            if self.community.is_public():
                if not self.community.is_child_safety():
                    self.template_name = "c_detail/anon_no_child_safety.html"
                else:
                    self.template_name = "c_detail/anon_public_community.html"
            elif self.community.is_closed():
                self.template_name = "c_detail/anon_close_community.html"
            elif self.community.is_private():
                self.template_name = "c_detail/anon_private_community.html"

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(CommunityDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityDetail,self).get_context_data(**kwargs)
        context["membersheeps"] = self.community.get_community_with_name_members(self.community.name)[0:6]
        context["community"] = self.community
        context["common_friends"] = self.common_friends
        context["community_goods"] = self.community.get_goods()[:3]
        return context
