from django.views.generic.base import TemplateView
from main.models import Item
from communities.models import Community, CommunityMembership
from follows.models import CommunityFollow
from common.checkers import check_can_get_posts_for_community_with_name
from django.views.generic import ListView
from rest_framework.exceptions import PermissionDenied
from common.utils import is_mobile


class ItemsCommunity(ListView):
	template_name = None
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		self.community=Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.community.get_template_list(folder="c_lenta/", template="list.html", request=request)
		try:
			fixed = Item.objects.get(community=community, is_fixed=True)
		except:
			fixed = None
		return super(ItemsCommunity,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ItemsCommunity,self).get_context_data(**kwargs)
		context['object'] = fixed
        context["community"]=community
		return context

	def get_queryset(self):
		item_list=self.community.get_posts().order_by('-created')
		return item_list


class ItemCommunity(TemplateView):
    model=Item
    template_name="detail_sections/item.html"

    def get(self,request,*args,**kwargs):
        self.community=Community.objects.get(pk=self.kwargs["pk"])
        self.item = Item.objects.get(uuid=self.kwargs["uuid"])
        self.item.views += 1
        self.item.save()
        self.items = self.community.get_posts()
        self.next = self.items.filter(pk__gt=self.item.pk).order_by('pk').first()
        self.prev = self.items.filter(pk__lt=self.item.pk).order_by('-pk').first()

        if request.user.is_authenticated and request.user.is_member_of_community_with_name(self.community.name):
            if request.user.is_moderator_of_community_with_name(self.community.name):
                self.template_name = "detail_sections/moderator_item.html"
            elif request.user.is_administrator_of_community_with_name(self.community.name):
                self.template_name = "detail_sections/admin_item.html"
            else:
                self.template_name = "detail_sections/item.html"
        elif request.user.is_authenticated and self.community.is_public():
            self.template_name = "detail_sections/item.html"
        elif request.user.is_anonymous and self.community.is_public():
            self.template_name = "detail_sections/item.html"
        return super(ItemCommunity,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommunity,self).get_context_data(**kwargs)
        context["object"]=self.item
        context["community"]=self.community
        context["next"]=self.next
        context["prev"]=self.prev
        context["request_user"]=self.request.user
        return context


class CommunityDetail(TemplateView):
    template_name = None
    membersheeps = None
    common_friends = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.membersheeps=self.community.get_community_with_name_members(self.community.name)[0:6]
        try:
            self.common_friends = request.user.get_common_friends_of_community(self.community.pk)[0:6]
        except:
            self.common_friends = None
        self.template_name = self.community.get_template(folder="c_detail/", template="community.html", request=request)
        return super(CommunityDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityDetail,self).get_context_data(**kwargs)
        context["membersheeps"]=self.membersheeps
        context["community"]=self.community
        context["common_friends"]=self.common_friends
        return context


class CommunityDetailReload(TemplateView):
    template_name = None
    membersheeps = None
    common_friends = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.membersheeps=CommunityMembership.objects.filter(community__id=self.community.pk)[0:5]

        if request.user.is_authenticated and request.user.is_member_of_community_with_name(self.community.name):
            self.common_friends = request.user.get_common_friends_of_community(self.community.pk)[0:5]
            if request.user.is_moderator_of_community_with_name(self.community.name):
                self.template_name = "c_detail/moderator_community.html"
            elif request.user.is_administrator_of_community_with_name(self.community.name):
                self.template_name = "c_detail/admin_community.html"
            elif request.user.is_star_from_community_with_name(self.community.name):
                self.template_name = "c_detail/star_community.html"
            else:
                self.template_name = "c_detail/member_community.html"
        elif request.user.is_authenticated and request.user.is_follow_from_community_with_name(self.community.pk):
            self.common_friends = request.user.get_common_friends_of_community(self.community.pk)[0:5]
            self.template_name = "c_detail/follow_community.html"
        elif request.user.is_authenticated and request.user.is_banned_from_community_with_name(self.community):
            self.template_name = "c_detail/block_community.html"

        elif request.user.is_authenticated and self.community.is_public():
            self.common_friends = request.user.get_common_friends_of_community(self.community.pk)[0:5]
            self.template_name = "c_detail/public_community.html"
        elif request.user.is_authenticated and self.community.is_closed():
            self.common_friends = request.user.get_common_friends_of_community(self.community.pk)[0:5]
            self.template_name = "c_detail/close_community.html"
        elif request.user.is_authenticated and self.community.is_private():
            self.template_name = "c_detail/private_community.html"
        return super(CommunityDetailReload,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityDetailReload,self).get_context_data(**kwargs)
        context["membersheeps"]=self.membersheeps
        context["community"]=self.community
        context["common_friends"]=self.common_friends
        return context
