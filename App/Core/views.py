from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# noinspection PyUnresolvedReferences
from Notification.models import Notice

# noinspection PyUnresolvedReferences
from DB.models import ChurchMember


@login_required(login_url='accounts:login')
def view_dashboard(request):
	notifications_qs = Notice.objects.all()
	total_member_count = ChurchMember.objects.count()
	context = {
		'members': total_member_count,
		'response_data': notifications_qs,

	}
	template = 'dashboard/index.html'
	return render(request, template, context)
