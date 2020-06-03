from django.urls import path

from . import views


app_name = 'config'

urlpatterns = [
	path('user/settings/', views.user_settings_view, name='user_settings_view'),
	path('add/user/setting/',views.add_new_system_user, name='add_new_user'),
	path('detail/sys/user/setting/', views.detail_system_user, name='detail_system_user'),
	path('edit/sys/<str:slug>/setting/', views.edit_system_user, name='edit_system_user'),
	path('delete/sys/<str:slug>/setting/', views.delete_system_user, name='delete_system_user'),
	path('view/church/info/', views.church_information, name='church_info_view'),
	path('add/church/info/register/', views.create_church_information, name='church_info_add'),
	path('edit/<str:slug>/church/info/register/', views.edit_church_information, name='church_info_edit'),

]
