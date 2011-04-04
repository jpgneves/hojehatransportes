from django.forms import ModelForm, Textarea
from models import Strike

class SubmitForm(ModelForm):
	class Meta:
		model = Strike
		fields = ('description', 'company', 'start_date', 'end_date', 'region', 'source_link')