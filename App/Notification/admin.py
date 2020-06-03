from django.contrib import admin
from .models import Notice, ShortMessage, MessageGroup


admin.site.register(Notice)
admin.site.register(ShortMessage)
admin.site.register(MessageGroup)
