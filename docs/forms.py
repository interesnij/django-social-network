from docs.models import DocList, Doc
from django import forms
from django.conf import settings


class DoclistForm(forms.ModelForm):

	class Meta:
		model = DocList
		fields = ['name', 'is_public', 'order']

class DocForm(forms.ModelForm):
	description = forms.CharField( label="", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))

	def clean_file(self):
		file = self.cleaned_data['file']
		try:
			if file:
				if len(file.name.split('.')) == 1:
					raise forms.ValidationError('File type is not supported')
				if file._size > settings.DOC_UPLOAD_FILE_MAX_SIZE:
					raise forms.ValidationError(_('Максимальный размер файла: %s. Ваш документ: %s') % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(file._size)))
		except:
			pass
		return file

	class Meta:
		model = Doc
		fields = ['title', 'file', 'type', 'list', ]
