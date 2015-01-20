from hojehatransportes.hat.models import Company, Region, Strike
from django.contrib import admin
from django import forms

class StrikeAdminForm(forms.ModelForm):
    class Meta:
        model = Strike
        widgets = {'description': forms.Textarea(attrs={'cols': 60, 'rows': 10})}
        
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
        
        return cleaned_data

class StrikeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Strike info', {'fields': ['company', 'region', 'description', 'canceled', 'source_link', 'submitter']}),
        ('Strike dates', {'fields': ['start_date', 'all_day', 'end_date']}),
        ('Approve', {'fields': ['approved']})
    ]

    form = StrikeAdminForm
    save_as = True

admin.site.register(Company)
admin.site.register(Region)
admin.site.register(Strike, StrikeAdmin)
