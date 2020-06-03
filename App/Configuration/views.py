from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse

from .forms import SystemUserRegForm, OrganisationRegForm
from .models import SystemUser, Organization


@login_required(login_url='accounts:login')
def user_settings_view(request):
	template = 'config/user_settings_view_page.html'
	sys_user_qs = SystemUser.objects.all()
	context = {
		'response_data': sys_user_qs,

	}
	return render(request, template, context)


@login_required(login_url='accounts:login')
def add_new_system_user(request):
	if request.method == 'POST':
		user_reg_form = SystemUserRegForm(request.POST)
		if user_reg_form.is_valid():
			user_reg_form.save()

			msg = '\nMember {} Successful Added To System Users with role of {}'.format(
				user_reg_form.cleaned_data['member'], user_reg_form.cleaned_data['role']
			)
			messages.success(request, msg)
			return redirect('config:user_settings_view')
		else:
			messages.error(request, user_reg_form.errors)
			return redirect('config:user_settings_view')

	else:
		user_reg_form = SystemUserRegForm()
		template = 'config/user_settings_add_page.html'
		context = {
			'form_data': user_reg_form,
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def detail_system_user(request):
	qs = get_object_or_404(SystemUser, id=request.GET['post_id'])
	template = 'config/system_user_detail_page.html'
	context = {
		'response_data': qs,
	}
	html_form = render_to_string(template, context, request=request)
	return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def edit_system_user(request, slug):
	if request.method == 'POST':
		sys_qs = get_object_or_404(SystemUser, id=slug)
		sys_form = SystemUserRegForm(request.POST, instance=sys_qs)
		if sys_form.is_valid():
			sys_form.save()

			msg = '\nUser Settings Edited Successful'
			messages.success(request, msg)
			return redirect('config:user_settings_view')
		else:
			messages.error(request, sys_form.errors)
			return redirect('config:user_settings_view')
	else:
		sys_qs = get_object_or_404(SystemUser, id=request.GET['post_id'])
		sys_form = SystemUserRegForm(instance=sys_qs)
		template = 'config/user_settings_edit_page.html'
		context = {
			'member_id': sys_qs.id,
			'form_data': sys_form,
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def delete_system_user(request, slug):
	if request.method == 'POST':
		member_inst = get_object_or_404(SystemUser, id=slug)
		member_inst.delete()

		msg = "\nActivity Successful Deleted"
		messages.success(request, msg)
		return redirect('config:user_settings_view')
	else:
		member_inst = get_object_or_404(SystemUser, id=request.GET['post_id'])
		msg = "\nDelete Activity {} \nNB..\nThis Process is irreversible".format(member_inst)
		template = 'config/confirm_user_delete.html'
		prompt = {
			"data": msg,
			'member_id': member_inst.id
		}
		html_form = render_to_string(template, prompt, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def church_information(request):
	qs = Organization.objects.filter(active=True)

	try:
		qs = qs.get(active=True)
	except ObjectDoesNotExist:
		messages.error(request, 'Church Information Unavailable')

	context = {
		'response_data': qs,
	}

	template = 'church_config/church_info_view.html'
	return render(request, template, context)


@login_required(login_url='accounts:login')
def create_church_information(request):
	if request.method == 'POST':
		church_form = OrganisationRegForm(request.POST, request.FILES)
		if church_form.is_valid():
			church_form.save()
			msg = 'Information Created Successful'
			messages.success(request, msg)
			return redirect('config:church_info_view')
		else:
			messages.error(request, church_form.errors)
			return redirect('config:church_info_view')
	else:
		church_form = OrganisationRegForm()
		context = {
			'form_data': church_form,
		}
		template = 'church_config/church_info_create_page.html'
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def edit_church_information(request, slug):
	qs = Organization.objects.filter(active=True)
	if request.method == 'POST':
		try:
			church_obj = qs.get(id=slug)
		except ObjectDoesNotExist:
			return JsonResponse(data={'status': False, 'message': 'NOT FOUND'}, status=404)

		church_form = OrganisationRegForm(request.POST, request.FILES, instance=church_obj)
		if church_form.is_valid():
			church_form.save()
			msg = 'Information Updated Successful'
			messages.success(request, msg)
			return redirect('config:church_info_view')
		else:
			messages.error(request, church_form.errors)
			return redirect('config:church_info_view')
	else:
		try:
			church_obj = qs.get(id=request.GET['post_id'])
		except ObjectDoesNotExist:
			return JsonResponse(data={'status': False, 'message': 'NOT FOUND'}, status=404)

		church_form = OrganisationRegForm(instance=church_obj)

		context = {
			'group_id': church_obj.id,
			'form_data': church_form,
		}
		template = 'church_config/church_info_edit_page.html'

		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


