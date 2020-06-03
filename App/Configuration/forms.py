from django import forms

from dal import autocomplete

from .models import SystemUser, Organization


class SystemUserRegForm(forms.ModelForm):
	class Meta:
		model = SystemUser
		fields = '__all__'
		widgets = {
			'member': autocomplete.ModelSelect2(
				url='packs:members_autocomplete', attrs={
					'data-placeholder': 'Start Typing...',
					'data-minimum-input-length': 3,
				}
			),
		}


class OrganisationRegForm(forms.ModelForm):
	class Meta:
		model = Organization
		fields = '__all__'
		widgets = {
			'pastor': autocomplete.ModelSelect2(
				url='packs:members_autocomplete', attrs={
					'data-placeholder': 'Start Typing...',
					'data-minimum-input-length': 3,
				}),
		}
