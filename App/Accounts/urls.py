from django.urls import path, include

from . import views

app_name = 'accounts'

urlpatterns = [
	path('add/members/', views.members_registration, name='add_members'),
	path('add/member/excel/', views.register_from_excel, name='add_member_excel'),
	path('view/members/', views.members_view, name='view_members'),
	path('details/member/',  views.members_details, name='member_details'),
	path('edit/member/<pk>/', views.member_information_update, name='edit_members'),
	path('delete/<str:slug>/member/', views.member_information_delete, name='delete_members'),
	path('auth/', include('django.contrib.auth.urls')),

]
