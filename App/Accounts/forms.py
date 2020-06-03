from django import forms

# noinspection PyUnresolvedReferences
from DB.models import ChurchMember


class ChurchMembershipForm(forms.ModelForm):
	class Meta:
		model = ChurchMember
		fields = '__all__'
		exclude = ['active', 'username']
		widgets = {
			'first_name': forms.TextInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'First Name'}),
			'middle_name': forms.TextInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'Middle Name'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Last Name'}),
			'email': forms.EmailInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Email'}),

			'residency': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Residency'}),
			'phone_number': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
			'occupation': forms.TextInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'Occupation'}),
			'citizenship': forms.TextInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'Citizenship'}),

		}


class FileUploadForm(forms.Form):
	choose_file = forms.FileField()
