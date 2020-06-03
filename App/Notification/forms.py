from django import forms
from django.contrib.auth.models import User

from dal import autocomplete

from .models import Notice, ShortMessage, MessageGroup

# noinspection PyUnresolvedReferences
from DB.models import ChurchMember


class NoticeCreationForm(forms.ModelForm):
	class Meta:
		model = Notice
		exclude = ['sender', 'recipients']
		widgets = {
			'title': forms.TextInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'Notification  Title'}),
			'subject': forms.TextInput(
				attrs={'class': 'form-control form-control-user', 'placeholder': 'Notification  Subject'})
		}


class GroupMessageSenderForm(forms.Form):
	groups = forms.ModelMultipleChoiceField(
		queryset=MessageGroup.objects.filter(user=1),widget=autocomplete.ModelSelect2Multiple(
		url='packs:group_message_autocomplete', attrs={
			'data-placeholder': 'Start Typing...',
			'data-minimum-input-length': 3,
		})

	)
	message = forms.CharField(max_length=500, widget=forms.Textarea)

	def __init__(self, user, *args, **kwargs):
		super(GroupMessageSenderForm, self).__init__(*args, **kwargs)
		self.fields['groups'].queryset = MessageGroup.objects.filter(user=user)


class SingleMessageSenderForm(forms.Form):
	recipient = forms.ModelChoiceField(queryset=ChurchMember.objects.all(), widget=autocomplete.ModelSelect2(
		url='packs:members_autocomplete', attrs={
			'data-placeholder': 'Start Typing...',
			'data-minimum-input-length': 3,
		}
	))
	message = forms.CharField(max_length=500, widget=forms.Textarea)


class MessageGroupRegForm(forms.ModelForm):
	class Meta:
		model = MessageGroup
		fields = '__all__'
		widgets = {
			'members': autocomplete.ModelSelect2Multiple(
				url='packs:members_autocomplete', attrs={
					'data-placeholder': 'Start Typing...',
					'data-minimum-input-length': 3,
				}),
			'user': forms.HiddenInput()
		}
