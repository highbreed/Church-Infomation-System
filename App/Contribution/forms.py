from django import forms
# noinspection PyPackageRequirements
from dal import autocomplete

from .models import ChurchContribution, DepartmentContribution, ChurchDevelopment, \
	ChurchDevelopmentContribution, Contribution


class ChurchContributionRegForm(forms.ModelForm):
	class Meta:
		model = ChurchContribution
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'Name'}),
			'contribution_date': forms.DateInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'Date'}),
			'category': autocomplete.ModelSelect2(url='packs:contrib_category_autocomplete', attrs={
				'data-placeholder': "AutoComplete...",
				'data-minimum-input-length': 3,
			}),
			'amount': forms.NumberInput(
				attrs={'placeholder': 'Amount Contributed'}),


		}
		exclude = ['slug']


class DepartmentContributionRegForm(forms.ModelForm):
	class Meta:
		model = DepartmentContribution
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'Name of Department'}),
			'contribution_date': forms.DateInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'Department'}),
			'category': autocomplete.ModelSelect2(url='packs:contrib_category_autocomplete', attrs={
				'data-placeholder': "AutoComplete...",
				'data-minimum-input-length': 3,
			}),
			'amount': forms.NumberInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'Amount Contributed'}),
		}
		exclude = ['slug']


class ChurchDevelopmentRegForm(forms.ModelForm):
	class Meta:
		model = ChurchDevelopment
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Name'}),
			'short_description': forms.TextInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'Short Description'}),

		}


class ChurchDevelopmentContributionRegForm(forms.ModelForm):
	class Meta:
		model = ChurchDevelopmentContribution
		fields = '__all__'
		widgets = {
			'development': autocomplete.ModelSelect2(
				url='packs:church_development_autocomplete', attrs={
					'data-placeholder': "Start Typing...",
					"data-minimum-input-length": 3,
				}
			),
			'member': autocomplete.ModelSelect2(
				url='packs:members_autocomplete', attrs={
					'data-placeholder': 'Start Typing...',
					'data-minimum-input-length': 3,
				}
			),

		}


class ChurchAccountsRegForm(forms.ModelForm):
	class Meta:
		model = Contribution
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Name'}),
			'description': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Description'}),
		}
