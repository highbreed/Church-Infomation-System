from django.contrib import admin

from .models import ChurchContribution, Contribution, DepartmentContribution, ChurchDevelopment, ChurchDevelopmentContribution


admin.site.register(Contribution)
admin.site.register(ChurchContribution)
admin.site.register(DepartmentContribution)
admin.site.register(ChurchDevelopment)
admin.site.register(ChurchDevelopmentContribution)
