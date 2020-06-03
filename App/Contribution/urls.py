from django.urls import path

from . import views

app_name = 'contrib'

urlpatterns = [
	path('create/chr/acct/', views.create_church_account, name='create_church_account'),
	path('edit/chr/<str:slug>/acct/', views.edit_church_account, name='edit_church_account'),
	path('delete/<str:slug>/chr/account/', views.delete_church_account, name='delete_church_account'),
	path('detail/chr/<str:slug>/account/', views.detail_church_account, name='church_account_details'),
	path('create/chr/<str:slug>/acct/contrib/', views.create_church_contribution, name='create_church_contrib'),
	path('edit/<str:slug>/chr/contrib/', views.edit_church_contribution, name='edit_church_contrib'),
	path('view/chr/contrib/', views.view_church_account, name='view_church_contrib'),
	path('detail/chr/contrib/', views.detail_church_contribution, name='church_contrib_details'),
	path('create/dep/contrib/', views.create_department_contribution, name='create_dep_contrib'),
	path('edit/<str:slug>/dep/contrib/', views.edit_department_contribution, name='edit_dep_contrib'),
	path('view/dep/contrib/', views.view_department_contributions, name='view_dep_contrib'),
	path('detail/<str:slug>/dep/contrib/', views.detail_department_contribution, name='view_dep_contrib'),
	path('delete/<str:slug>/contrib/', views.delete_church_contribution, name='delete_church_contrib'),
	path('view/develop/project/', views.view_church_project, name='view_church_project'),
	path('create/chr/prj/', views.create_church_project, name='create_church_project'),
	path('edit/<str:slug>/chr/prj', views.edit_church_project, name='edit_church_project'),
	path('delete/<str:slug>/project/church/', views.delete_church_project, name='delete_church_project'),
	path('develop/<str:slug>/project/detail/', views.detail_church_project, name='detail_church_project'),
	path('create/develop/contrib/<str:slug>/project/',
		 views.create_church_project_contribution, name='create_project_contrib'),
	path('view/project/contrib/', views.view_project_contrib_church, name='detail_project_contrib_church'),
	path('edit/project/<str:slug>/contrib/',views.edit_project_contrib_church, name='edit_project_contrib_church'),
	path('delete/project/<str:slug>/contrib/', views.delete_project_contrib_church, name='delete_project_contrib_church'),
]
