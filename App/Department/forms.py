from django import forms
from dal import autocomplete

# noinspection PyUnresolvedReferences
from DB.models import Department, ChurchMember


class DepartmentRegForm(forms.ModelForm):
	class Meta:
		model = Department
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'Name of Department'}),
			'description': forms.TextInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'Description'}),
			'department_head': autocomplete.ModelSelect2(
				url='packs:members_autocomplete', attrs={
					'data-placeholder': 'Start Typing...',
					'data-minimum-input-length': 3,
				}
			),
			'department_secretary': autocomplete.ModelSelect2(
				url='packs:members_autocomplete', attrs={
					'data-placeholder': 'Start Typing...',
					'data-minimum-input-length': 3,
				}
			),
			'department_treasurer': autocomplete.ModelSelect2(
				url='packs:members_autocomplete', attrs={
					'data-placeholder': 'Start Typing...',
					'data-minimum-input-length': 3,
				}
			),
			'members_of_department': autocomplete.ModelSelect2Multiple(
				url='packs:members_autocomplete', attrs={
					'data-placeholder': 'Start Typing...',
					'data-minimum-input-length': 3,
				}
			),

		}


class DepartmentMembershipForm(forms.Form):
	member_name = forms.ModelChoiceField(queryset=ChurchMember.objects.all())

	class Meta:
		widgets = {
			'member_name': autocomplete.ModelSelect2(
				url='packs:members_autocomplete', attrs={
					'data-placeholder': 'Start Typing...',
					'data-minimum-input-length': 3,
				}
			),
		}
