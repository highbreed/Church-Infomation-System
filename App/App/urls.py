from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Core.urls')),
    path('account/', include('Accounts.urls')),
    path('pack/', include('UtilityPack.urls')),
    path('department/', include('Department.urls')),
    path('activities/',  include('Activity.urls')),
    path('contribution/',  include('Contribution.urls')),
    path('notification/', include('Notification.urls')),
    path('Config/', include('Configuration.urls')),
    path('messages/', include('chat.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



