from django.urls import path

from . import database_utilities

app_name = 'packs'

urlpatterns = [
	path('members-autocomplete/', database_utilities.ChurchMembersAutoComplete.as_view(

	), name='members_autocomplete'),
	path('activity-autocomplete/', database_utilities.ActivityTypeAutoComplete.as_view(
		create_field='name'), name='activity_autocomplete'),
	path('contrib-category-autocomplete/', database_utilities.ChurchContribCategoryAutoComplete.as_view(
		create_field='name'), name='contrib_category_autocomplete'),
	path('development-autocomplete/', database_utilities.ChurchDevelopmentAutoComplete.as_view(
		
	), name='church_development_autocomplete'),
	path('group_message-autocomplete/', database_utilities.MessageGroupAutoComplete.as_view(

	), name='group_message_autocomplete'),
]
