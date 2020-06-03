from django.urls import path, re_path

from .views import ThreadView, thread_inbox

app_name = 'chat'

urlpatterns = [
	path("", thread_inbox, name='home'),
	path("<str:username>/", ThreadView.as_view()),
]