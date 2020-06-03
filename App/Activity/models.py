from django.db import models


class ActivityType(models.Model):
	name = models.CharField(max_length=150, unique=True)

	def __str__(self):
		return self.name


class Activity(models.Model):
	active = models.BooleanField(default=True)
	title = models.CharField(max_length=255)
	short_description = models.CharField(max_length=255, blank=True, null=True)
	description = models.TextField()
	starts_on = models.DateTimeField(blank=True, null=True)
	ends_on = models.DateTimeField(blank=True, null=True)
	activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, blank=True, null=True)
	date_time_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	@property
	def get_status(self):
		if self.active:
			return "On going"
		return "Ended"
