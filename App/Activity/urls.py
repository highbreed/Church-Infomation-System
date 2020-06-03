from django.urls import path

from . import views

app_name = 'activity'

urlpatterns = [
	path('create/new/activity/', views.create_activity, name='create_activity'),
	path('view/current/activities/', views.view_activity, name='view_activity'),
	path('edit/<str:slug>/activities/', views.edit_activity, name='edit_activity'),
	path('view/details/activity/', views.activity_details, name='activity_details'),
	path('delete/<str:slug>/delete/', views.delete_activity, name='delete_activity'),
]
