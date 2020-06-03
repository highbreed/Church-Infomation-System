from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .forms import NoticeCreationForm, GroupMessageSenderForm, \
	SingleMessageSenderForm, MessageGroupRegForm
from .models import Notice, ShortMessage, MessageGroup


@login_required(login_url='accounts:login')
def create_notification(request):
	if request.method == 'POST':
		notice_form = NoticeCreationForm(request.POST)
		if notice_form.is_valid():
			notice_form.save()
			msg = '\nSent  Successful'
			messages.success(request, msg)
			return redirect('core:dashboard_page')
		else:
			messages.error(request, notice_form.errors)
			return redirect('core:dashboard_page')
	else:
		notice_form = NoticeCreationForm()
		template = 'notice/notification_creation_page.html'
		context = {
			'form_data': notice_form
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def view_notification(request):
	notification_qs = get_object_or_404(Notice, id=request.GET['post_id'])
	template = 'notice/notification_view_page.html'
	context = {
		'response_data': notification_qs,
	}
	html_form = render_to_string(template, context, request=request)
	return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def edit_notification(request, slug):
	if request.method == 'POST':
		notice_inst = get_object_or_404(Notice, id=slug)
		notice_form = NoticeCreationForm(request.POST, instance=notice_inst)
		if notice_form.is_valid():
			notice_form.save()
			msg = '{} Notification Updated Successful'.format(notice_form.cleaned_data['title'])
			messages.success(request, msg)
			return redirect('core:dashboard_page')
		else:
			messages.error(request, notice_form.errors)
			return redirect('core:dashboard_page')
	else:
		notice_inst = get_object_or_404(Notice, id=request.GET['post_id'])
		notice_form = NoticeCreationForm(instance=notice_inst)
		template = 'notice/notification_edit_page.html'
		context = {
			'notice': notice_inst,
			'form_data': notice_form,
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def delete_notification(request, slug):
	if request.method == 'POST':
		member_inst = get_object_or_404(Notice, id=slug)
		member_inst.delete()

		msg = "\n Successful Deleted"
		messages.success(request, msg)
		return redirect('core:dashboard_page')
	else:
		member_inst = get_object_or_404(Notice, id=request.GET['post_id'])
		msg = "\nDelete  {} \nNB..\nThis Process is irreversible".format(member_inst)
		template = 'notice/confirm_notice_delete.html'
		prompt = {
			"data": msg,
			'member_id': member_inst.id
		}
		html_form = render_to_string(template, prompt, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def message_view(request):
	message_qs = ShortMessage.objects.filter(sender=request.user)
	context = {
		'response_data': message_qs,
	}
	template = 'message/sms_view_page.html'
	return render(request, template, context)


@login_required(login_url='accounts:login')
def message_details(request):
	qs = ShortMessage.objects.filter(sender=request.user)

	try:
		msg_obj = qs.get(id=request.GET['post_id'])
	except ObjectDoesNotExist:
		return JsonResponse(data={'status': False, 'message': 'NOT FOUND'}, status=404)
	context = {
		'response_data': msg_obj,
	}
	template = 'message/message_details.html'
	html_form = render_to_string(template, context, request=request)
	return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def delete_message(request, slug):
	qs = ShortMessage.objects.filter(sender=request.user)
	if request.method == 'POST':
		try:
			group_obj = qs.get(id=slug)
		except ObjectDoesNotExist:
			return JsonResponse(data={'status': False, 'message': 'NOT FOUND'}, status=404)
		group_obj.delete()
		msg = "\n Successful Deleted"
		messages.success(request, msg)
		return redirect('notice:message_view')
	else:
		try:
			group_obj = qs.get(id=request.GET['post_id'])
		except ObjectDoesNotExist:
			return JsonResponse(data={'status': False, 'message': 'NOT FOUND'}, status=404)
		msg = "\nDelete  {} \nNB..\nThis Process is irreversible".format(group_obj)
		template = 'message/confirm_message_delete.html'
		prompt = {
			"data": msg,
			'member_id': group_obj.id
		}
		html_form = render_to_string(template, prompt, request=request)
		return JsonResponse({'html_response': html_form})

@login_required(login_url='accounts:login')
def message_send_register(request):
	if request.method == 'POST':
		sms_register_form = SingleMessageSenderForm(request.POST)
		if sms_register_form.is_valid():
			try:
				sms_message = ShortMessage.objects.create(
					sender=request.user,
					message=sms_register_form.cleaned_data['message'],
				)
				sms_message.receivers.add(sms_register_form.cleaned_data['recipient'])
			except FieldError:
				print(FieldError)
			return redirect('notice:message_register')
		else:
			print(sms_register_form.errors)
	else:
		sms_register_form = SingleMessageSenderForm()
		template = 'message/sms_register_view.html'
		context = {
			'form_data': sms_register_form,
		}
		return render(request, template, context)


@login_required(login_url='accounts:login')
def send_group_message(request):
	if request.method == 'POST':
		group_sms_form = GroupMessageSenderForm(request.user, request.POST)
		if group_sms_form.is_valid():
			try:
				sms_message = ShortMessage.objects.create(
					sender=request.user,
					message=group_sms_form.cleaned_data['message']
				)
				for data in group_sms_form.cleaned_data['groups']:
					for member in data.members.all():
						print(member)
						sms_message.receivers.add(member)
			except:
				msg = 'Error occurred check your details and try again'
				messages.error(request, msg)
				return redirect('notice:group_msg_register')
			msg = 'Successful Sent'
			messages.success(request, msg)
			return redirect('notice:group_msg_register')
		else:
			messages.error(request, group_sms_form.errors)
			return redirect('notice:group_msg_register')
	else:
		group_sms_form = GroupMessageSenderForm(request.user)
		template = 'message/group_sms_sender.html'
		context = {
			'form_data': group_sms_form,
		}
		return render(request, template, context)


@login_required(login_url='accounts:login')
def message_groups_view(request):
	qs = MessageGroup.objects.filter(user=request.user)
	template = 'message/message_group_view.html'
	context = {
		'response_data': qs,
	}
	return render(request, template, context)


@login_required(login_url='accounts:login')
def add_message_group(request):
	if request.method == 'POST':
		message_group_form = MessageGroupRegForm(request.POST, initial={'user': request.user})
		if message_group_form.is_valid():
			message_group_form.save()
			msg = '{} Group Saved Successful'.format(message_group_form.cleaned_data['name'])
			messages.success(request, msg)
			return redirect('notice:view_message_groups')
		else:
			messages.error(request, message_group_form.errors)
			return redirect('notice:view_message_groups')
	else:
		message_group_form = MessageGroupRegForm(initial={'user': request.user})
		template = 'message/message_group_add.html'
		context = {
			'form_data': message_group_form,
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def details_message_group(request):
	qs = MessageGroup.objects.filter(user=request.user)

	try:
		group_obj = qs.get(id=request.GET['post_id'])
	except ObjectDoesNotExist:
		return JsonResponse(data={'status': False, 'message': 'NOT FOUND'}, status=404)

	template = 'message/message_group_detail.html'
	context = {
		'response_data': group_obj,
	}
	html_form = render_to_string(template, context, request=request)
	return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def edit_message_group(request, slug):
	qs = MessageGroup.objects.filter(user=request.user)
	if request.method == 'POST':
		try:
			group_obj = qs.get(id=slug)
		except ObjectDoesNotExist:
			return JsonResponse(data={'status': False, 'message': 'NOT FOUND'}, status=404)
		message_group_form = MessageGroupRegForm(request.POST, instance=group_obj)
		if message_group_form.is_valid():
			message_group_form.save()
			msg = '{} Successful Updated'.format(message_group_form.cleaned_data['name'])
			messages.success(request, msg)
			return redirect('notice:view_message_groups')
		else:
			messages.error(request, message_group_form.errors)
			return redirect('notice:view_message_groups')
	else:
		try:
			group_obj = qs.get(id=request.GET['post_id'])
		except ObjectDoesNotExist:
			return JsonResponse(data={'status': False, 'message': 'NOT FOUND'}, status=404)

		message_group_form = MessageGroupRegForm(instance=group_obj)
		template = 'message/message_group_edit.html'
		context = {
			'group_id': group_obj.id,
			'form_data': message_group_form,
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def delete_message_group(request, slug):
	qs = MessageGroup.objects.filter(user=request.user)
	if request.method == 'POST':
		try:
			group_obj = qs.get(id=slug)
		except ObjectDoesNotExist:
			return JsonResponse(data={'status': False, 'message': 'NOT FOUND'}, status=404)
		group_obj.delete()
		msg = "\n Successful Deleted"
		messages.success(request, msg)
		return redirect('notice:view_message_groups')
	else:
		try:
			group_obj = qs.get(id=request.GET['post_id'])
		except ObjectDoesNotExist:
			return JsonResponse(data={'status': False, 'message': 'NOT FOUND'}, status=404)
		msg = "\nDelete  {} \nNB..\nThis Process is irreversible".format(group_obj)
		template = 'message/confirm_message_group_delete.html'
		prompt = {
			"data": msg,
			'member_id': group_obj.id
		}
		html_form = render_to_string(template, prompt, request=request)
		return JsonResponse({'html_response': html_form})