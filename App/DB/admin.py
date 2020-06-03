from django.contrib import admin

from . import models


admin.site.register(models.Person)
admin.site.register(models.ChurchMember)
admin.site.register(models.Department)
admin.site.register(models.BoardMember)

