from django.forms import ModelForm, Textarea, HiddenInput
from models import Strike

class SubmitForm(ModelForm):
    class Meta:
        model = Strike
        fields = ('description', 'company', 'start_date', 'all_day', 'end_date', 'region', 'source_link', 'submitter')
        widgets = {'description': Textarea(attrs={'cols': 60, 'rows': 10}), 'submitter': HiddenInput()}
        
    def clean(self):
        cleaned_data = self.cleaned_data
        all_day = cleaned_data.get("all_day")
        end_date = cleaned_data.get("end_date")

        if not all_day and not end_date: # If it isn't an "all day" event, we must have an end_date
            msg = u"Must have an end date or mark as an 'all day' event."

            self._errors["all_day"] = self.error_class([msg])
            self._errors["end_date"] = self.error_class([msg])

            # Clear invalid data
            del cleaned_data["all_day"]
            del cleaned_data["end_date"]
            
        if all_day:
            cleaned_data["end_date"] = cleaned_data["start_date"]
        
        return cleaned_data
