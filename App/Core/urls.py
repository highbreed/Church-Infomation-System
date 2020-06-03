from . import views

from django.urls import path

app_name = "core"

urlpatterns = [
	path('', views.view_dashboard, name='dashboard_page'),
]
