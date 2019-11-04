from django.views.generic.base import TemplateView
from users.models import User, UserProfile
from posts.models import Post
from main.models import Item
from frends.models import Connect
from follows.models import Follow
from goods.models import Good
from communities.models import Community
from main.forms import CommentForm
from users.forms import GeneralUserForm, AboutUserForm, AvatarUserForm
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.db.models import Q
from generic.mixins import CategoryListMixin



class UserItemView(CategoryListMixin, TemplateView):
    model=Item
    template_name="lenta/user_item.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.item.views += 1
        self.item.save()
        return super(UserItemView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserItemView,self).get_context_data(**kwargs)
        context["object"]=self.item
        return context


class AvatarReload(TemplateView):
    template_name="profile/avatar_reload.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        return super(AvatarReload,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(AvatarReload, self).get_context_data(**kwargs)
        
        return context


class ItemListView(ListView, CategoryListMixin):
    template_name="lenta/item_list.html"
    model=Item
    paginate_by=6

    def get(self,request,*args,**kwargs):
        try:
            self.fixed = Item.objects.get(creator=self.user, is_fixed=True)
        except:
            self.fixed = None
        return super(ItemListView,self).get(request,*args,**kwargs)

    def get_queryset(self):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        items = self.user.get_posts()
        return items

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['object'] = self.fixed
        return context


class AllUsers(ListView):
    template_name="all_users.html"
    model=User

    def get_queryset(self):
        users=User.objects.only('id')
        return users


class ProfileUserView(TemplateView):
    template_name = 'user.html'
    model=Item

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.communities=Community.objects.filter(memberships__user__id=self.user.pk)[0:5]

        return super(ProfileUserView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileUserView, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['form_avatar'] = AvatarUserForm()
        context['form_comment'] = CommentForm()
        context['communities'] = self.communities
        return context


class UserGeneralChange(TemplateView):
	template_name = "user_general_form.html"
	form=None
	profile=None

	def get(self,request,*args,**kwargs):
		self.user=request.user
		self.form=GeneralUserForm(instance=self.user)
		return super(UserGeneralChange,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserGeneralChange,self).get_context_data(**kwargs)
		context["profile"]=self.profile
		context["form"]=self.form
		return context

	def post(self,request,*args,**kwargs):
		self.user=request.user
		try:
			self.profile=UserProfile.objects.get(user=request.user)
		except:
			self.profile = None
		if not self.profile:
			self.user.profile = UserProfile.objects.create(user=request.user)
		self.form=GeneralUserForm(request.POST,instance=self.user.profile)
		if self.form.is_valid():
			user = self.request.user
			user.first_name = self.form.cleaned_data['first_name']
			user.last_name = self.form.cleaned_data['last_name']
			user.save()
			self.form.save()
			if request.is_ajax():
				return HttpResponse ('!')
		return super(UserGeneralChange,self).post(request,*args,**kwargs)


class UserAboutChange(TemplateView):
	template_name = "user_about_form.html"
	form=None
	profile=None

	def get(self,request,*args,**kwargs):
		self.user=request.user
		self.form=AboutUserForm(instance=self.user)
		return super(UserAboutChange,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserAboutChange,self).get_context_data(**kwargs)
		context["profile"]=self.profile
		context["form"]=self.form
		return context

	def post(self,request,*args,**kwargs):
		self.user=request.user
		try:
			self.profile=UserProfile.objects.get(user=request.user)
		except:
			self.profile = None
		if not self.profile:
			self.user.profile = UserProfile.objects.create(user=request.user)
		self.form=AboutUserForm(request.POST,instance=self.user.profile)
		if self.form.is_valid():
			self.form.save()
			if request.is_ajax():
				return HttpResponse ('!')
		return super(UserAboutChange,self).post(request,*args,**kwargs)


class UserAvatarChange(TemplateView):
	template_name = "user_avatar_form.html"
	form=None
	profile=None

	def get(self,request,*args,**kwargs):
		self.user=request.user
		self.form=AvatarUserForm(instance=self.user)
		return super(UserAvatarChange,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserAvatarChange,self).get_context_data(**kwargs)
		context["profile"]=self.profile
		context["form"]=self.form
		return context

	def post(self,request,*args,**kwargs):
		self.user=request.user
		try:
			self.profile=UserProfile.objects.get(user=request.user)
		except:
			self.profile = None
		if not self.profile:
			self.user.profile = UserProfile.objects.create(user=request.user)
		self.form=AvatarUserForm(request.POST,request.FILES, instance=self.user.profile)
		if self.form.is_valid():
			self.form.save()
			if request.is_ajax():
				return HttpResponse ('!')
		return super(UserAvatarChange,self).post(request,*args,**kwargs)


class UserDesign(TemplateView):
	template_name="user_design.html"


class ProfileButtonReload(TemplateView):
    template_name="profile_button.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        try:
            self.connect = Connect.objects.get(user=self.request.user,target_user=self.user)
        except:
            self.connect = None
        try:
            self.follow = Follow.objects.get(followed_user=self.user,user=self.request.user)
        except:
            self.follow = None
        try:
            self.follow2 = Follow.objects.get(followed_user=self.request.user,user=self.user)
        except:
            self.follow2 = None

        return super(ProfileButtonReload,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileButtonReload, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['connect'] = self.connect
        context['follow'] = self.follow
        context['follow2'] = self.follow2
        return context


class ProfileStatReload(TemplateView):
    template_name="profile_stat.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.follows_count=self.user.count_following()
        self.goods_count=self.user.count_goods()
        self.connect_count=self.user.count_connections()
        self.communities_count=self.user.count_community()
        return super(ProfileStatReload,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileStatReload, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['follows_count'] = self.follows_count
        context['frends_count'] = self.connect_count
        context['goods_count'] = self.goods_count
        context['communities_count'] = self.communities_count
        return context


def fixed(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.is_fixed=True
    item.save()
    return HttpResponse("!")


def unfixed(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.is_fixed=False
    item.save()
    return HttpResponse("!")

def item_delete(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.is_deleted=True
    item.save()
    return HttpResponse("!")
