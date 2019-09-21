from django.views.generic.base import TemplateView
from users.models import User, UserProfile
from posts.models import Post
from frends.models import Connect
from follows.models import Follow
from communities.models import Community
from posts.forms import PostMediumForm
from users.forms import GeneralUserForm, AboutUserForm, AvatarUserForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods



class AllUsers(ListView):
	template_name="all_users.html"
	model = User
	paginate_by = 15

	def get_queryset(self, **kwargs):
		users=User.objects.all()
		return users



class ProfileUserView(TemplateView):
	template_name = 'user.html'
	form = PostMediumForm
	form_avatar = AvatarUserForm

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.frends=Connect.objects.filter(user=self.user)
		self.frends2=Connect.objects.filter(target_user=self.user)
		self.communities=Community.objects.filter(starrers=self.user)
		self.posts=Post.objects.filter(creator=self.user,is_deleted=False)
		try:
			self.connect = Connect.objects.get(target_user=self.request.user,user=self.user)
		except:
			self.connect = None
		try:
			self.connect2 = Connect.objects.get(user=self.request.user,target_user=self.user)
		except:
			self.connect2 = None
		try:
			self.follow = Follow.objects.get(user=self.request.user,followed_user=self.user)
		except:
			self.follow = None 
		try:
			self.follow2 = Follow.objects.get(followed_user=self.request.user,user=self.user)
		except:
			self.follow2 = None

		return super(ProfileUserView,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(ProfileUserView, self).get_context_data(**kwargs)
		context['user'] = self.user
		context['posts'] = self.posts
		context['frends'] = self.frends
		context['frends2'] = self.frends2
		context['form_medium'] = self.form
		context['form_avatar'] = self.form_avatar
		context['communities'] = self.communities
		context['connect'] = self.connect
		context['connect2'] = self.connect2
		context['follow'] = self.follow
		context['follow2'] = self.follow2
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


class PostUserView(ListView):
	template_name = 'post_list.html'
	model = Post
	paginate_by = 10

	def get_queryset(self, **kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		return Post.objects.filter(creator=self.user)

class UserDesign(TemplateView):
	template_name="user_design.html"


@login_required
@require_http_methods(["GET"])
def get_thread(request):
    """Returns a list of news with the given news as parent."""
    post_id = request.GET['post']
    post = Post.objects.get(pk=post_id)
    posts_html = render_to_string("profile/post.html", {"post": post})
    thread_html = render_to_string(
        "profile/post_thread.html", {"thread": post.get_thread()})
    return JsonResponse({
        "uuid": post_id,
        "post": posts_html,
        "thread": thread_html,
    })

@login_required
@require_http_methods(["POST"])
def post_comment(request):
    """A function view to implement the post functionality with AJAX, creating
    News instances who happens to be the children and commenters of the root
    post."""
    user = request.user
    post = request.POST['reply']
    par = request.POST['parent']
    parent = Post.objects.get(pk=par)
    post = post.strip()
    if post:
        parent.reply_this(user, post)
        return JsonResponse({'comments': parent.count_thread()})

    else:
        return HttpResponseBadRequest()

@login_required
@require_http_methods(["POST"])
def update_interactions(request):
    data_point = request.POST['id_value']
    post = Post.objects.get(pk=data_point)
    data = {'likes': post.count_likers(), 'comments': post.count_thread()}
    return JsonResponse(data)
