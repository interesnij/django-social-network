from django.views.generic import ListView
from docs.models import Doc


class DocsView(ListView):
	template_name = "docs.html"

	def get_queryset(self):
		return Doc.objects.only("pk")
