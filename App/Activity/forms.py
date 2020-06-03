from django import forms
from dal import autocomplete

from .models import Activity


class ActivityRegForm(forms.ModelForm):
	class Meta:
		model = Activity
		fields = '__all__'
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Title'}),
			'short_description': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Short Description'}),
			'description': forms.Textarea(),
			'activity_type': autocomplete.ModelSelect2(url='packs:activity_autocomplete', attrs={
									# Only trigger autocompletion after 3 characters have been typed
									'data-minimum-input-length': 3,
								},
							)
		}
