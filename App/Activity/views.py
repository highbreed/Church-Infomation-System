from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse

from .forms import ActivityRegForm
from .models import Activity


@login_required(login_url='accounts:login')
def create_activity(request):
	if request.method == 'POST':
		activity_form = ActivityRegForm(request.POST)
		if activity_form.is_valid():
			activity_form.save()

			msg = "\nSuccessful Created {} Activity".format(activity_form.cleaned_data['title'])

			messages.success(request, msg)
			return redirect('activity:view_activity')
		else:
			messages.error(request, activity_form.errors['class'])
			return redirect('activity:view_activity')
	else:
		activity_form = ActivityRegForm()
		templates = 'activity/activity_creation_page.html'

		context = {
			'form_data': activity_form,
		}

		html_form = render_to_string(templates, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def view_activity(request):
	activity_qs = Activity.objects.all()
	template = 'activity/activity_view_page.html'
	context = {
		'response_data': activity_qs,
	}

	return render(request, template, context)


@login_required(login_url='accounts:login')
def edit_activity(request, slug):
	if request.method == 'POST':
		activity_qs = get_object_or_404(Activity, id=slug)
		form_inst = ActivityRegForm(request.POST, instance=activity_qs)
		if form_inst.is_valid():
			form_inst.save()

			msg = "Successful updated {}".format(form_inst.cleaned_data['title'])
			messages.success(request, msg)
			return redirect('activity:view_activity')
		else:
			messages.success(request, form_inst.errors)
			return redirect('activity:view_activity')
	else:
		activity_qs = get_object_or_404(Activity, id=request.GET['post_id'])
		form_inst = ActivityRegForm(instance=activity_qs)

		context = {
			'activity': activity_qs,
			'form_data': form_inst,
		}
		template = 'activity/activity_edit_page.html'

		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def activity_details(request):
	activity_inst = get_object_or_404(Activity, id=request.GET['post_id'])

	templates = "activity/activity_details_page.html"
	context = {
		'member_data': activity_inst,
	}
	html_form = render_to_string(templates, context, request=request)

	return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def delete_activity(request, slug):
	if request.method == 'POST':
		member_inst = get_object_or_404(Activity, id=slug)
		member_inst.delete()

		msg = "\nActivity Successful Deleted"
		messages.success(request, msg)
		return redirect('activity:view_activity')
	else:
		member_inst = get_object_or_404(Activity, id=request.GET['post_id'])
		msg = "\nDelete Activity {} \nNB..\nThis Process is irreversible".format(member_inst)
		template = 'activity/confirm_activity_delete.html'
		prompt = {
			"data": msg,
			'member_id': member_inst.id
		}
		html_form = render_to_string(template, prompt, request=request)
		return JsonResponse({'html_response': html_form})