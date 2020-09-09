from django.views.generic import ListView
from docs.models import Doc2


class DocsView(ListView):
	template_name="docs.html"

	def get_queryset(self):
		docs = Doc2.objects.only("pk")
		return docs
