from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo
from gallery.helpers import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import ListView


class GalleryView(TemplateView):
	template_name="gallery.html"

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.albums=Album.objects.filter(creator=self.user)
		return super(GalleryView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(GalleryView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

class AlbumsListView(ListView):
	template_name="albums.html"
	model=Album
	paginate_by=10

	def get_queryset(self):
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		albums=Album.objects.filter(creator__id=self.user.id)
		return albums


class PhotosListView(ListView):
	template_name="photos.html"
	model=Photo
	paginate_by=15

	def get_queryset(self):
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		photos=Photo.objects.filter(creator__id=self.user.id)
		return photos


class AlbomView(AjaxResponseMixin,JSONResponseMixin,TemplateView):
	template_name="album.html"

	def get(self,request,*args,**kwargs):
		self.album=Album.objects.get(pk=self.kwargs["pk"])
		self.photos = Photo.objects.filter(album=self.album)
		return super(AlbomView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(AlbomView,self).get_context_data(**kwargs)
		context['album'] = self.album
		context['photos'] = self.photos
		return context

	def post_ajax(self, request, *args, **kwargs):
		try:
			self.album = Album.objects.get(pk=self.kwargs["pk"])
		except Album.DoesNotExist:
			error_dict = {'message': 'Album not found.'}
			return self.render_json_response(error_dict, status=404)

		uploaded_file = request.FILES['file']
		Photo.objects.create(album=self.album, file=uploaded_file)

		response_dict = {'message': 'File uploaded successfully!',}
		return self.render_json_response(response_dict, status=200)
