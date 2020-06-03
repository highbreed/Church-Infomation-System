from django.db import models
from django.contrib.auth.models import User

from . import main_database_components


class Person(models.Model):
	active = models.BooleanField(default=True)
	user = models.OneToOneField(User, on_delete=models.SET_NULL , blank=True, null=True)
	first_name = models.CharField(max_length=255)
	middle_name = models.CharField(max_length=255, blank=True, null=True)
	last_name = models.CharField(max_length=255)
	gender = models.CharField(choices=main_database_components.GenderChoices, max_length=20)
	email = models.EmailField(blank=True)
	image = models.ImageField(upload_to="Users_image", blank=True)

	def __str__(self):
		return '{} {}'.format(str(self.first_name), str(self.last_name))

	@property
	def full_name(self):
		return '{} {}'.format(str(self.first_name), str(self.last_name))


class ChurchMember(Person):
	residency = models.CharField(max_length=250, blank=True)
	phone_number = models.CharField(default="+254", blank=True, max_length=25)  # todo phone number handling
	occupation = models.CharField(max_length=250, blank=True)
	citizenship = models.CharField(max_length=150, blank=True)
	marital_status = models.CharField(choices=main_database_components.MaritalStatusChoices, max_length=10)

	def __str__(self):
		return '{} {}'.format(str(self.first_name), str(self.last_name))


class Department(models.Model):
	name = models.CharField(max_length=255, unique=True)
	description = models.CharField(max_length=255, blank=True, null=True)
	department_head = models.ForeignKey(ChurchMember, on_delete=models.CASCADE, related_name='head_of_department')
	department_secretary = models.ForeignKey(ChurchMember, on_delete=models.CASCADE, blank=True, null=True,
											 related_name='secretary')
	department_treasurer = models.ForeignKey(ChurchMember, on_delete=models.CASCADE, blank=True
											 ,null=True, related_name='department_treasurer')
	members_of_department = models.ManyToManyField(ChurchMember, blank=True, related_name='members_of_department')
	date_created = models.DateTimeField(auto_now=True)

	@property
	def get_department_heads(self):
		committee_list = [self.department_head, self.department_secretary, self.department_treasurer]
		return committee_list

	def __str__(self):
		return self.name


class BoardMember(models.Model):
	active = models.BooleanField(default=True, help_text="Current board member")
	member = models.ForeignKey(ChurchMember, on_delete=models.CASCADE)
	date_time_added = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.member)





