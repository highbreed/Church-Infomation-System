from dal import autocomplete

# noinspection PyUnresolvedReferences
from DB.models import ChurchMember, Department

# noinspection PyUnresolvedReferences
from Activity.models import ActivityType

# noinspection PyUnresolvedReferences
from Contribution.models import Contribution, ChurchDevelopment

# noinspection PyUnresolvedReferences
from Notification.models import MessageGroup


class ChurchMembersAutoComplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# todo Make sure you filter out the results depending on the visitor !

		qs = ChurchMember.objects.all()


		if self.q:
			qs = qs.filter(first_name__istartswith=self.q)

		return qs


class ActivityTypeAutoComplete(autocomplete.Select2QuerySetView):

	def get_queryset(self):
		# todo user filtering

		qs = ActivityType.objects.all()

		if self.q:
			qs = qs.filter(name__istartswith=self.q)

		return qs


class ChurchContribCategoryAutoComplete(autocomplete.Select2QuerySetView):

	def get_queryset(self):
		# todo user filtering

		qs = Contribution.objects.all()

		if self.q:
			qs = qs.filter(name__istartswith=self.q)

		return qs


class ChurchDevelopmentAutoComplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# todo user filtering
		qs = ChurchDevelopment.objects.all()

		if self.q:
			qs = qs.filter(name__istartswith=self.q)

		return qs


class MessageGroupAutoComplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		qs = MessageGroup.objects.filter(user=self.request.user)

		if self.q:
			qs = qs.filter(name__istartswith=self.q)

		return qs
