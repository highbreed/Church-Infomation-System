from django.urls import path

from . import views


app_name = 'dep'

urlpatterns = [
	path('add/new/dep/', views.create_department, name='create_department'),
	path('view/available/dep/', views.view_departments, name='view_department'),
	path('edit/<str:slug>/dep/', views.edit_departments, name='edit_department'),
	path('delete/<str:slug>/dep/', views.delete_department, name='delete_department'),
	path('view/<str:slug>/dep/', views.details_departments, name='detail_department'),
	path('add/dep/<str:slug>/member/', views.add_department_member, name='add_department_member'),
]
