import random
import string

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

# noinspection PyUnresolvedReferences
from DB.models import ChurchMember, Department

USER_ROLES_CHOICES = (
	('ChairPerson', 'ChairPerson'),
	('Secretary', 'Secretary'),
	('Treasurer', 'Treasurer'),
)


class SystemUser(models.Model):
	active = models.BooleanField(default=True)
	member = models.ForeignKey(ChurchMember, on_delete=models.CASCADE)
	role = models.CharField(max_length=12, choices=USER_ROLES_CHOICES)
	group = models.ForeignKey(
		Department, on_delete=models.CASCADE, help_text='If Left Blank User Will Get System Wide Access', blank=True,
		null=True)

	def __init__(self, *args, **kwargs):
		super(SystemUser, self).__init__(*args, **kwargs)
		self.__original_role = self.role

	def __str__(self):
		return str(self.member)


def get_username_and_password(f_name, l_name):
	user_name = '{}{}'.format(f_name, l_name)
	counter = random.randint(len(user_name), (len(l_name) * random.randint(1, 100)))
	while User.objects.filter(username=user_name):
		user_name = user_name + str(counter)
		counter += 1
	user_pass = ''.join(random.choice(string.printable) for i in range(10))
	return user_name, user_pass


@receiver(post_save, sender=SystemUser)
def user_creation(sender, instance, update_fields, created, **kwargs):
	if created:
		username, password = get_username_and_password(instance.member.first_name, instance.member.last_name)
		if ' ' in password:
			password = password.replace(" ", "@")
		user = User.objects.create_user(username=username, password=password)
		# update the instance user object to reference our user
		member_qs = ChurchMember.objects.filter(id=instance.member.id)
		member_qs.update(user=user)

		# add user to group
		group, created_group = Group.objects.get_or_create(name=instance.role)
		user.groups.add(group)


@receiver(post_delete, sender=SystemUser)
def user_delete(sender, instance, **kwargs):
	user_obj = User.objects.get(username=instance.member.user)
	user_obj.delete()


class Organization(models.Model):
	active = models.BooleanField(default=False,
								 help_text="Switch to activate this settings as the Organizations Current "
										   "Settings...NB\nThis will Affect All The Systems Setting")
	name = models.CharField(max_length=250)
	address = models.CharField(max_length=255)
	location = models.CharField(max_length=255)
	pastor = models.ForeignKey(ChurchMember, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(upload_to="Organization_images", blank=True, null=True)
	contact = models.CharField(max_length=25, help_text="Official Organizations PhoneNumber", blank=True, null=True)
	email = models.EmailField(help_text="Official Organizations email", blank=True,
							  null=True)  # todo Organization default email
	logo = models.ImageField(upload_to="Organization_images", blank=True, null=True)
	history = models.TextField(blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	def save(self, force_insert=False, force_update=False, using=None,
			 update_fields=None):
		super(Organization, self).save()
		if self.active:
			Organization.objects.exclude(id=self.id).update(active=False)
