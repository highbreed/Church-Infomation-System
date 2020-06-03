from django.urls import path

from . import views

app_name = 'notice'

urlpatterns = [
	path('create/new/notice/', views.create_notification, name='notice_creation_page'),
	path('view/chr/notice/', views.view_notification, name='notice_view_page'),
	path('edit/chr/<str:slug>/notice/', views.edit_notification, name='notice_edit_page'),
	path('delete/chr/<str:slug>/notice/', views.delete_notification, name='notice_delete_page'),
	path('view/sms/message/', views.message_view, name='message_view'),
	path('details/view/message/', views.message_details, name='message_details'),
	path('delete/message/<str:slug>/register/', views.delete_message, name='delete_message'),
	path('send/message/sms/register/', views.message_send_register, name='message_register'),
	path('send/group/message/register/', views.send_group_message, name='group_msg_register'),
	path('view/message/groups/register/', views.message_groups_view, name='view_message_groups'),
	path('add/message/group/register/', views.add_message_group, name='add_message_groups'),
	path('detail/message/group/register/', views.details_message_group, name='detail_message_groups'),
	path('edit/<str:slug>/message/group/register/', views.edit_message_group, name='edit_message_group'),
	path('delete/message/<str:slug>/group/register/', views.delete_message_group, name='delete_message_group'),
]
