from django.views.generic import ListView
from users.models import User
from common.templates import (
								get_template_community_item,
								get_template_anon_community_item,
								get_template_user_item,
								get_template_anon_user_item,
								get_template_community_list,
								get_template_anon_community_list,
								get_template_user_list,
								get_template_anon_user_list,
							)


class ItemLikes(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.type = request.GET.get('type')
        self.item = request.user.get_item(self.type)
        if not self.item.votes_on:
            raise Http404
        if request.user.is_authenticated:
			if not self.item.list.is_user_can_see_el(request.user.pk):
				raise Http404
			if self.item.community:
				self.template_name = get_template_community_item(self.item, "generic/items/comment/", "likes.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_item(self.item, "generic/items/comment/", "likes.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if not self.item.list.is_anon_user_can_see_el(request.user.pk):
				raise Http404
			if self.item.community:
				self.template_name = get_template_anon_community_item(self.item, "generic/items/comment/anon_likes.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.item, "generic/items/comment/anon_likes.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ItemLikes,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ItemLikes,self).get_context_data(**kwargs)
        context['item'] = self.item
        context['text'] = "Элемент одобрили:"
        return context

    def get_queryset(self):
        return User.objects.filter(id__in=self.item.likes().values("user_id"))

class ItemDislikes(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.type = request.GET.get('type')
        self.item = request.user.get_item(self.type)
        if not self.item.votes_on:
            raise Http404
        if request.user.is_authenticated:
			if not self.item.list.is_user_can_see_el(request.user.pk):
				raise Http404
			if self.item.community:
				self.template_name = get_template_community_item(self.item, "generic/items/comment/", "dislikes.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_item(self.item, "generic/items/comment/", "dislikes.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if not self.item.list.is_anon_user_can_see_el(request.user.pk):
				raise Http404
			if self.item.community:
				self.template_name = get_template_anon_community_item(self.item, "generic/items/comment/anon_dislikes.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.item, "generic/items/comment/anon_dislikes.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ItemDislikes,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ItemDislikes,self).get_context_data(**kwargs)
        context['item'] = self.item
        context['text'] = "Элемент не одобрили:"
        return context

    def get_queryset(self):
        return User.objects.filter(id__in=self.item.dislikes().values("user_id"))
