from django.db import models
from django.utils.text import slugify
from dateutil.relativedelta import *
import calendar

import datetime

# noinspection PyUnresolvedReferences,PyPackageRequirements
from DB.models import Department, ChurchMember


def days_converter(no_of_days):
	year = int(no_of_days / 365)
	week = (no_of_days % 365) / 7
	if isinstance(week, float):  # if its a reminder is true then convert to the nearest week
		week = int(week) + 1
	months = week / 4
	if isinstance(months, float):  # if its a reminder is true then convert to the nearest months
		months = int(months) + 2

	context_dic = {
		'year': year,
		'weeks': week,
		'months': months,
	}
	return context_dic


TYPES_OF_CONTRIBUTIONS = (
	('General Contribution', 'General Contribution'),
	('Member Contribution', 'Member Contribution'),
)


class Contribution(models.Model):
	# holds all contribution categories
	name = models.CharField(max_length=150, unique=True)
	description = models.CharField(max_length=250, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	def chart_format(self):
		contribution_qs = self.churchcontribution_set.all()
		return_months = []
		return_amount = []
		if contribution_qs:
			latest_date = contribution_qs.order_by("-id")[0]
			converted_data = days_converter((latest_date.recorded_date - self.timestamp).days)

			start_date_list = [self.timestamp]
			end_date_list = [self.timestamp + relativedelta(
				days=+calendar.monthrange(self.timestamp.year, self.timestamp.month)[1] - self.timestamp.day)]

			# loop all the dates query monthly data and append to list

			for date_data in range(converted_data['months']):

				first_start_date = start_date_list[date_data]
				first_end_month = end_date_list[date_data]
				qs = contribution_qs.filter(recorded_date__range=(first_start_date, first_end_month))

				start_date_list.append(first_end_month+relativedelta(seconds=+1))
				end_date_list.append(start_date_list[date_data+1] + relativedelta(days=+30))

				# append amount
				return_amount.append(sum([x.amount for x in qs]))

				# append month labels
				date_obj = datetime.datetime.strptime(str(first_end_month.month), "%m")
				return_months.append(date_obj.strftime("%b"))
		else:
			return_amount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			label_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
			for data in label_data:
				date_obj = datetime.datetime.strptime(str(data), "%m")
				return_months.append(date_obj.strftime("%b"))

		chart_data = {
			'labels': return_months,
			'data': return_amount,
		}
		return chart_data

	@property
	def total_offered(self):
		contributions_qs = self.churchcontribution_set.all()
		return sum([x.amount for x in contributions_qs])


class ChurchContribution(models.Model):
	# holds overall church contributions
	category = models.ForeignKey(Contribution, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	contribution_date = models.DateField(blank=True, null=True)
	amount = models.IntegerField()
	slug = models.SlugField(blank=True)
	recorded_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		slugify(self.name)
		super(ChurchContribution, self).save()


class DepartmentContribution(models.Model):
	# only holds department contributions
	name = models.CharField(max_length=255)
	contribution_date = models.DateField()
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	amount = models.IntegerField()
	slug = models.SlugField(blank=True)
	recorded_date = models.DateTimeField(auto_now_add=True)
	category = models.ForeignKey(Contribution, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		slugify(self.name)
		super(DepartmentContribution, self).save()


class ChurchDevelopment(models.Model):
	name = models.CharField(max_length=150, unique=True)
	contribution_type = models.CharField(choices=TYPES_OF_CONTRIBUTIONS, max_length=20)
	target_amount = models.IntegerField()
	short_description = models.CharField(max_length=255, blank=True, null=True)
	description = models.TextField(blank=True)
	target_date = models.DateField(blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	@property
	def total_contributions(self):
		contribution_qs = self.churchdevelopmentcontribution_set.all()
		amount = []
		for contribution in contribution_qs:
			amount.append(contribution.amount)
		return "KSh. {}".format(sum(amount))

	def chart_format(self):
		contribution_qs = self.churchdevelopmentcontribution_set.all()
		return_months = []
		return_amount = []
		if contribution_qs:
			latest_date = contribution_qs.order_by("-id")[0]
			converted_data = days_converter((latest_date.timestamp - self.timestamp).days)

			start_date_list = [self.timestamp]
			end_date_list = [self.timestamp + relativedelta(
				days=+calendar.monthrange(self.timestamp.year, self.timestamp.month)[1] - self.timestamp.day)]

			# loop all the dates query monthly data and append to list

			for date_data in range(converted_data['months']):

				first_start_date = start_date_list[date_data]
				first_end_month = end_date_list[date_data]
				qs = contribution_qs.filter(timestamp__range=(first_start_date, first_end_month))

				start_date_list.append(first_end_month+relativedelta(seconds=+1))
				end_date_list.append(start_date_list[date_data+1] + relativedelta(days=+30))

				# append amount
				return_amount.append(sum([x.amount for x in qs]))

				# append month labels
				date_obj = datetime.datetime.strptime(str(first_end_month.month), "%m")
				return_months.append(date_obj.strftime("%b"))
		else:
			return_amount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			label_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
			for data in label_data:
				date_obj = datetime.datetime.strptime(str(data), "%m")
				return_months.append(date_obj.strftime("%b"))

		chart_data = {
			'labels': return_months,
			'data': return_amount,
		}
		return chart_data


class ChurchDevelopmentContribution(models.Model):
	development = models.ForeignKey(ChurchDevelopment, on_delete=models.CASCADE)
	amount = models.IntegerField()
	member = models.ForeignKey(ChurchMember, on_delete=models.CASCADE, blank=True, null=True)
	comment = models.CharField(blank=True, null=True, max_length=255, help_text="Any comments")
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.development)
