from generic.mixins import EmojiListMixin
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from main.models import Item
from communities.models import Community, CommunityMembership
from django.views.generic.detail import DetailView
from follows.models import CommunityFollow
from common.checkers import check_can_get_posts_for_community_with_name


class CommunityItemView(EmojiListMixin, TemplateView):
    model=Item
    template_name="detail/item.html"

    def get(self,request,*args,**kwargs):
        self.community=Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,self.community.name)
        self.community = self.community.get_posts()
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.next = self.items.filter(pk__gt=self.item.pk).order_by('pk').first()
        self.prev = self.items.filter(pk__lt=self.item.pk).order_by('-pk').first()
        self.item.views += 1
        self.item.save()
        return super(CommunityItemView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityItemView,self).get_context_data(**kwargs)
        context["object"]=self.item
        context["community"]=self.community
        context["next"]=self.next
        context["prev"]=self.prev
        return context


class CommunityListView(ListView):
    template_name="detail/list.html"
    model=Item
    paginate_by=15

    def get(self,request,*args,**kwargs):
        try:
            self.fixed = Item.objects.get(community=self.community, is_fixed=True)
        except:
            self.fixed = None
        self.community=Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_posts_for_community_with_name(request.user,self.community.name)
        self.communities = self.community.get_posts().order_by('-created')
        return super(CommunityListView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(CommunityListView, self).get_context_data(**kwargs)
        context['object'] = self.fixed
        context['communities'] = self.communities
        context["community"]=self.community
        return context


class CommunityDetailView(DetailView):
    template_name = "community_detail.html"
    model = Community
    administrator = False
    staff = False
    creator = False
    member = False

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.membersheeps=CommunityMembership.objects.filter(community__id=self.community.pk)[0:5]
        if request.user.is_authenticated and request.user.is_administrator_of_community_with_name(self.community.name):
            self.administrator=True
        if request.user.is_authenticated and request.user.is_creator_of_community_with_name(self.community.name):
            self.creator=True
        if request.user.is_authenticated and request.user.is_staff_of_community_with_name(self.community.name):
            self.staff=True
        if request.user.is_authenticated and request.user.is_member_of_community_with_name(self.community.name):
            self.member=True
        try:
            self.follow = CommunityFollow.objects.get(community=self.community,user=self.request.user)
        except:
            self.follow = None
        return super(CommunityDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityDetailView,self).get_context_data(**kwargs)
        context["membersheeps"]=self.membersheeps
        context["follow"]=self.follow
        context["administrator"]=self.administrator
        context["creator"]=self.creator
        context["staff"]=self.staff
        context["member"]=self.member
        return context


class CommunityDetailReload(DetailView):
    template_name="detail_reload.html"
    model=Community
    administrator = False
    staff = False
    creator = False
    member = False

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.membersheeps=CommunityMembership.objects.filter(community__id=self.community.pk)[0:5]
        if request.user.is_authenticated and request.user.is_administrator_of_community_with_name(self.community.name):
            self.administrator=True
        if request.user.is_authenticated and request.user.is_creator_of_community_with_name(self.community.name):
            self.creator=True
        if request.user.is_authenticated and request.user.is_staff_of_community_with_name(self.community.name):
            self.staff=True
        if request.user.is_authenticated and request.user.is_member_of_community_with_name(self.community.name):
            self.member=True
        try:
            self.follow = CommunityFollow.objects.get(community=self.community,user=self.request.user)
        except:
            self.follow = None
        return super(CommunityDetailReload,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityDetailReload,self).get_context_data(**kwargs)
        context["membersheeps"]=self.membersheeps
        context["follow"]=self.follow
        context["administrator"]=self.administrator
        context["creator"]=self.creator
        context["staff"]=self.staff
        context["member"]=self.member
        return context
