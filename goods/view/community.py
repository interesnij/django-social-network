import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic import TemplateView
from django.views.generic import ListView
from goods.models import Good
from communities.models import Community
from common.check.community import check_can_get_lists
from rest_framework.exceptions import PermissionDenied
from stst.models import GoodNumbers
from common.template.good import get_template_community_good, get_permission_community_good

class CommunityGoods(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_template_community_good(self.community, "c_good/", "goods.html", request.user)
        return super(CommunityGoods,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityGoods,self).get_context_data(**kwargs)
        context["community"] = self.community
        return context

    def get_queryset(self):
        if self.request.user.is_staff_of_community_with_name(self.community.name):
            goods_list = self.community.get_admin_goods().order_by('-created')
        else:
            goods_list = self.community.get_goods().order_by('-created')
        return goods_list


class CommunityGood(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(uuid=self.kwargs["uuid"])
        self.good = Good.objects.get(pk=self.kwargs["pk"])
        self.goods = self.user.get_goods()

        self.template_name = get_template_community_good(self.community, "c_good/", "good.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(CommunityGood,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityGood,self).get_context_data(**kwargs)
        context["object"] = self.good
        context["user"] = self.user
        context["next"] = self.goods.filter(pk__gt=self.good.pk).order_by('pk').first()
        context["prev"] = self.goods.filter(pk__lt=self.good.pk).order_by('-pk').first()
        return context


class GoodCommunityCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.good = Good.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if not self.good.comments_enabled:
            raise PermissionDenied('Комментарии к товару отключены')
        self.template_name = get_permission_user_post(self.user, "c_good_comment/", "comments.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(GoodCommunityCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodCommunityCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.good
        context['community'] = self.community
        return context

    def get_queryset(self):
        check_can_get_lists(self.request.user, self.community)
        comments = self.good.get_comments()
        return comments
