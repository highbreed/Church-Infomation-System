from django.db import models
from django.contrib.auth.models import User

# noinspection PyUnresolvedReferences
from DB.models import ChurchMember


class Notice(models.Model):
	sender = models.ForeignKey(ChurchMember, on_delete=models.CASCADE, related_name='notice_sender', blank=True, null=True)
	recipients = models.ManyToManyField(ChurchMember, blank=True, related_name='notice_recipient')
	title = models.CharField(max_length=250)
	subject = models.CharField(max_length=255, blank=True, null=True)
	body = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


class ShortMessage(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender')
	message = models.TextField()
	receivers = models.ManyToManyField(ChurchMember, blank=True, related_name='message_receiver')
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.sender)


class MessageGroup(models.Model):
	name = models.CharField(max_length=100)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_message_group')
	members = models.ManyToManyField(ChurchMember, blank=True)

	class Meta:
		unique_together = ['user', 'name']

	def __str__(self):
		return self.name
