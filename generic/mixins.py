from django.views.generic.base import ContextMixin
from django.conf import settings
from common.models import EmojiGroup, Emoji



class EmojiListMixin(ContextMixin):
	emojies_1 = Emoji.objects.filter(group=1)
	emojies_2 = Emoji.objects.filter(group=2)
	def get_context_data(self,**kwargs):
		context=super(EmojiListMixin,self).get_context_data(**kwargs)
		context["current_url"]=self.request.path
		context["emojies_1"]=self.emojies_1
		context["emojies_2"]=self.emojies_2
		return context


class CommunityMemdersMixin(ContextMixin):
	community = None
	administrator = False
	staff = False
	creator = False
	member = False
	follow = None

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated and request.user.is_administrator_of_community_with_name(self.community.name):
			self.administrator=True
		if request.user.is_authenticated and request.user.is_creator_of_community_with_name(self.community.name):
			self.creator=True
		if request.user.is_authenticated and request.user.is_staff_of_community_with_name(self.community.name):
			self.staff=True
		if request.user.is_authenticated and request.user.is_member_of_community_with_name(self.community.name):
			self.member=True
		self.follow = CommunityFollow.objects.get(community=self.community,user=self.request.user)
		return super(CommunityMemdersMixin,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityMemdersMixin,self).get_context_data(**kwargs)
		context["administrator"]=self.administrator
		context["creator"]=self.creator
		context["staff"]=self.staff
		context["member"]=self.member
		context["follow"]=self.follow
		return context
