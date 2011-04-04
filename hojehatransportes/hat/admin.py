from hat.models import Company, Region, Strike
from django.contrib import admin

class StrikeAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['company', 'region', 'description', 'canceled', 'source_link']}),
		('Strike dates', {'fields': ['start_date', 'end_date']})
	]

admin.site.register(Company)
admin.site.register(Region)
admin.site.register(Strike, StrikeAdmin)