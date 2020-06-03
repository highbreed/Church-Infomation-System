from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from .forms import DepartmentRegForm, DepartmentMembershipForm
# noinspection PyUnresolvedReferences
from DB.models import Department


@login_required(login_url='accounts:login')
def create_department(request):
	if request.method == 'POST':
		reg_form = DepartmentRegForm(request.POST)
		if reg_form.is_valid():
			reg_form.save()

			msg = '\n{} Ministry Added Successful'.format(reg_form.cleaned_data['name'])
			messages.success(request, msg)
			return redirect('dep:view_department')
		else:
			messages.error(request, reg_form.errors)
			return redirect('dep:view_department')
	else:
		reg_form = DepartmentRegForm()
		template = 'department/dep_reg_page.html'
		context = {
			'form_data': reg_form
		}

		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def add_department_member(request, slug):
	if request.method == 'POST':
		dep_inst = get_object_or_404(Department, id=slug)
		membership_form = DepartmentMembershipForm(request.POST)
		if membership_form.is_valid():

			try:
				dep_inst.members_of_department.add(membership_form.cleaned_data['member_name'])
				messages.success(request, 'Successful Added {} to members'.format(membership_form.cleaned_data['member_name']))
				return redirect('dep:detail_department', slug=slug)
			except FieldError:
				messages.error(request, 'Member registration Failed try and Contact Administrator')
				return redirect('dep:detail_department', slug=slug)
		else:
			messages.error(request, membership_form.errors)
			return redirect('dep:detail_department', slug=slug)

	else:
		dep_inst = get_object_or_404(Department, id=request.GET['post_id'])
		membership_form = DepartmentMembershipForm()
		template = 'department/add_dep_member_form.html'
		context = {
			'department': dep_inst,
			'form_data': membership_form,
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def view_departments(request):
	dep_qs = Department.objects.all()
	templates = 'department/dep_view_page.html'

	context = {
		'response_data': dep_qs
	}
	return render(request, templates, context)


@login_required(login_url='accounts:login')
def edit_departments(request, slug):
	if request.method == 'POST':
		department_qs = get_object_or_404(Department, id=slug)
		dep_reg_form = DepartmentRegForm(request.POST, instance=department_qs)

		if dep_reg_form.is_valid():
			dep_reg_form.save()

			msg = "\n{} Ministry information updated Successful".format(dep_reg_form.cleaned_data['name'])
			messages.success(request, msg)
			return redirect('dep:view_department')
		else:
			messages.error(request, dep_reg_form.errors['class'])
			return redirect('dep:view_department')
	else:
		department_qs =get_object_or_404(Department, pk=request.GET['post_id'])
		dep_reg_form = DepartmentRegForm(instance=department_qs)

		context = {
			'department': department_qs,
			'form_data': dep_reg_form,
		}
		templates = 'department/dep_edit_form.html'

		html_form = render_to_string(templates, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def details_departments(request, slug):
	department_qs = get_object_or_404(Department, id=slug)
	context = {
		'department_data': department_qs,
	}
	template = 'department/dep_details_page.html'
	return render(request, template, context)


@login_required(login_url='accounts:login')
def delete_department(request, slug):
	if request.method == 'POST':
		member_inst = get_object_or_404(Department, id=slug)
		member_inst.delete()

		msg = "\nMember Successful Deleted"
		messages.success(request, msg)
		return redirect('dep:view_department')
	else:
		member_inst = get_object_or_404(Department, id=request.GET['post_id'])
		msg = "\nDelete Department {} \nNB..\nThis Process is irreversible".format(member_inst)
		template = 'department/confirm_department_delete.html'
		prompt = {
			"data": msg,
			'member_id': member_inst.id
		}
		html_form = render_to_string(template, prompt, request=request)
		return JsonResponse({'html_response': html_form})

