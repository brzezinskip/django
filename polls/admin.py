from django.contrib import admin
from polls.models import Poll, Choices

class ChoicesInline(admin.TabularInline):
	model = Choices
	extra = 3

class PollAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,					{'fields': ['question']}),
		('Date information', 	{'fields': ['pub_date'], 'classes': ['collapse']}),
		]
	inlines = [ChoicesInline]
	list_display = ('question', 'pub_date', 'was_published_recently')
	list_filter = ['pub_date']
	search_fields = ['question']
	date_hierarchy = 'pub_date'

admin.site.register(Poll, PollAdmin)