import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldError
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse

from .forms import ChurchContributionRegForm, DepartmentContributionRegForm, \
	ChurchDevelopmentRegForm, ChurchDevelopmentContributionRegForm, ChurchAccountsRegForm
from .models import ChurchContribution, DepartmentContribution, \
	ChurchDevelopment, ChurchDevelopmentContribution, Contribution


@login_required(login_url='accounts:login')
def create_church_account(request):
	if request.method == 'POST':
		accounts_form = ChurchAccountsRegForm(request.POST)
		if accounts_form.is_valid():
			accounts_form.save()

			msg = '\n{} Account Created'.format(accounts_form.cleaned_data['name'])
			messages.success(request, msg)
			return redirect('contrib:view_church_contrib')
		else:
			messages.error(request, accounts_form.errors)
			return redirect('contrib:view_church_contrib')

	else:
		accounts_form = ChurchAccountsRegForm()
		template = 'contrib/church_accounts_reg_page.html'
		context = {
			'form_data': accounts_form,
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def edit_church_account(request, slug):
	if request.method == 'POST':
		acc_inst = get_object_or_404(Contribution, id=slug)
		acc_form = ChurchAccountsRegForm(request.POST, instance=acc_inst)
		if acc_form.is_valid():
			acc_form.save()

			msg = '\n{}Edited Successful'.format(acc_form.cleaned_data['name'])
			messages.success(request, msg)
			return redirect('contrib:view_church_contrib')
		else:
			messages.error(request, acc_form.errors)
			return redirect('contrib:view_church_contrib')

	else:
		acc_inst = get_object_or_404(Contribution, id=request.GET['post_id'])
		acc_form = ChurchAccountsRegForm(instance=acc_inst)
		template = 'contrib/church_accounts_edit_page.html'
		context = {
			'acc_inst': acc_inst,
			'form_data': acc_form
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({"html_response": html_form})


@login_required(login_url='accounts:login')
def delete_church_account(request, slug):
	if request.method == 'POST':
		member_inst = get_object_or_404(Contribution, id=slug)
		member_inst.delete()

		msg = "\n Successful Deleted"
		messages.success(request, msg)
		return redirect('contrib:view_church_contrib')
	else:
		member_inst = get_object_or_404(Contribution, id=request.GET['post_id'])
		msg = "\nDelete  {} \nNB..\nThis Process is irreversible".format(member_inst)
		template = 'contrib/confirm_acct_delete.html'
		prompt = {
			"data": msg,
			'member_id': member_inst.id
		}
		html_form = render_to_string(template, prompt, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def view_church_account(request):
	church_contrib_qs = Contribution.objects.all()
	context = {
		'response_data': church_contrib_qs,
	}
	template = 'contrib/contrib_view_page.html'
	return render(request, template, context)


@login_required(login_url='accounts:login')
def detail_church_account(request, slug):
	qs = get_object_or_404(Contribution, id=slug)
	contributions = qs.churchcontribution_set.all()
	total_amount_contributed = sum([x.amount for x in contributions])
	template = 'contrib/church_account_details_page.html'
	context = {
		'data': json.dumps(qs.chart_format()['data']),
		'labels': json.dumps(qs.chart_format()['labels']),
		'total_contributed': [total_amount_contributed, (qs.total_offered - total_amount_contributed)],
		'contributions': contributions,
		'response_data': qs
	}
	return render(request, template, context)


@login_required(login_url='accounts:login')
def create_church_contribution(request, slug):
	if request.method == 'POST':
		acct_qs = get_object_or_404(Contribution, id=slug)
		contrib_form = ChurchContributionRegForm(request.POST)
		if contrib_form.is_valid():
			try:
				ChurchContribution(
					category=acct_qs,
					name=contrib_form.cleaned_data['name'],
					contribution_date=contrib_form.cleaned_data['contribution_date'],
					amount=contrib_form.cleaned_data['amount']
				).save()
			except FieldError:
				messages.error(request, "Save Failed Check form and submit again")
				return redirect('contrib:church_account_details', slug=slug)
			msg = "\n{} Added Successful".format(contrib_form.cleaned_data['name'])
			messages.success(request, msg)
			return redirect('contrib:church_account_details', slug=slug)
		else:
			messages.error(request, contrib_form.errors)
			return redirect('contrib:church_account_details', slug=slug)

	else:
		acct_qs =get_object_or_404(Contribution, id=request.GET['post_id'])
		contrib_form = ChurchContributionRegForm(initial={'category':acct_qs})
		template = 'contrib/contrib_creation_page.html'
		context = {
			'account':acct_qs,
			'form_data': contrib_form,
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def edit_church_contribution(request, slug):
	if request.method == 'POST':
		contrib_inst = get_object_or_404(ChurchContribution, id=slug)
		contrib_form = ChurchContributionRegForm(request.POST, instance=contrib_inst)
		if contrib_form.is_valid():
			contrib_form.save()

			msg = "\n{} Updated Successful".format(contrib_form.cleaned_data['name'])
			messages.success(request, msg)
			return redirect('contrib:church_account_details', slug=contrib_inst.category.id)
		else:
			messages.error(request, contrib_form.errors)
			return redirect('contrib:church_account_details', slug=contrib_inst.category.id)

	else:
		contrib_inst = get_object_or_404(ChurchContribution, id=request.GET['post_id'])
		contrib_form = ChurchContributionRegForm(instance=contrib_inst)
		context = {
			'contribution': contrib_inst,
			'form_data': contrib_form,
		}
		template = 'contrib/contrib_edit_page.html'
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def detail_church_contribution(request):
	qs = get_object_or_404(ChurchContribution, id=request.GET['post_id'])
	template = 'contrib/contrib_details_page.html'
	context = {
		'response_data': qs,
	}
	html_form = render_to_string(template, context, request=request)
	return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def delete_church_contribution(request, slug):
	if request.method == 'POST':
		member_inst = get_object_or_404(ChurchContribution, id=slug)
		member_inst.delete()

		msg = "\n Successful Deleted"
		messages.success(request, msg)
		return redirect('contrib:church_account_details', slug=member_inst.category.id)
	else:
		member_inst = get_object_or_404(ChurchContribution, id=request.GET['post_id'])
		msg = "\nDelete  {} \nNB..\nThis Process is irreversible".format(member_inst)
		template = 'contrib/confirm_contrib_delete.html'
		prompt = {
			"data": msg,
			'member_id': member_inst.id
		}
		html_form = render_to_string(template, prompt, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def create_department_contribution(request):
	if request.method == 'POST':
		contrib_form = DepartmentContributionRegForm(request.POST)
		if contrib_form.is_valid():
			contrib_form.save()

			msg = "\n{} Added Successful".format(contrib_form.cleaned_data['category'])
			messages.success(request, msg)
			return redirect('contrib:view_church_contrib')
		else:
			messages.error(request, contrib_form.errors)
			return redirect('contrib:view_church_contrib')

	else:
		contrib_form = DepartmentContributionRegForm()
		template = 'contrib/contrib_creation_page.html'
		context = {
			'form_data': contrib_form,
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def edit_department_contribution(request, slug):
	if request.method == 'POST':
		contrib_inst = get_object_or_404(DepartmentContribution, id=slug)
		contrib_form = DepartmentContributionRegForm(request.POST, instance=contrib_inst)
		if contrib_form.is_valid():
			contrib_form.save()

			msg = "\n{} Updated Successful".format(contrib_form.cleaned_data['name'])
			messages.success(request, msg)
			return redirect("contrib:view_church_contrib")
		else:
			messages.error(request, contrib_form.errors)
			return redirect("contrib:view_church_contrib")

	else:
		contrib_inst = get_object_or_404(DepartmentContribution, id=request.GET['post_id'])
		contrib_form = DepartmentContributionRegForm(instance=contrib_inst)
		context = {
			'contribution': contrib_inst,
			'form_data': contrib_form,
		}
		template = 'contrib/contrib_edit_page.html'
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def view_department_contributions(request):
	church_contrib_qs = DepartmentContribution.objects.all()
	context = {
		'response_data': church_contrib_qs,
	}
	template = 'contrib/contrib_view_page.html'
	return render(request, template, context)


@login_required(login_url='accounts:login')
def detail_department_contribution(request, slug):
	qs = get_object_or_404(DepartmentContribution, id=slug)
	template = 'contrib/contrib_details_page.html'
	context = {
		'response_data': qs,
	}
	html_form = render_to_string(template, context, request=request)
	return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def create_church_project(request):
	if request.method == 'POST':
		project_form = ChurchDevelopmentRegForm(request.POST)
		if project_form.is_valid():
			project_form.save()

			msg = '\n{} Saved Successful'.format(project_form.cleaned_data['name'])
			messages.success(request, msg)
			return redirect('contrib:view_church_project')
		else:
			messages.error(request, project_form.errors)
			return redirect('contrib:view_church_project')
	else:
		project_form = ChurchDevelopmentRegForm()
		template = 'develop/develop_create_page.html'
		context = {
			'form_data': project_form,
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def view_church_project(request):
	projects_qs = ChurchDevelopment.objects.all()
	template = 'develop/develop_view_page.html'
	context = {
		'response_data': projects_qs,
	}
	return render(request, template, context)


@login_required(login_url='accounts:login')
def edit_church_project(request, slug):
	if request.method == 'POST':
		project_inst = get_object_or_404(ChurchDevelopment, id=slug)
		project_form = ChurchDevelopmentRegForm(request.POST, instance=project_inst)
		if project_form.is_valid():
			project_form.save()

			msg = '\n{} Updated Successful'.format(project_form.cleaned_data['name'])
			messages.success(request, msg)
			return redirect('contrib:view_church_project')
		else:
			messages.error(request, project_form.errors)
			return redirect('contrib:view_church_project')
	else:
		project_inst = get_object_or_404(ChurchDevelopment, id=request.GET['post_id'])
		project_form = ChurchDevelopmentRegForm(instance=project_inst)
		template = 'develop/develop_edit_page.html'
		context = {
			'project': project_inst,
			'form_data': project_form,
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def delete_church_project(request, slug):
	if request.method == 'POST':
		member_inst = get_object_or_404(ChurchDevelopment, id=slug)
		member_inst.delete()

		msg = "\nProject Successful Deleted"
		messages.success(request, msg)
		return redirect('contrib:view_church_project')
	else:
		member_inst = get_object_or_404(ChurchDevelopment, id=request.GET['post_id'])
		msg = "\nDelete  {} \nNB..\nThis Process is irreversible".format(member_inst)
		template = 'develop/confirm_project_delete.html'
		prompt = {
			"data": msg,
			'member_id': member_inst.id
		}
		html_form = render_to_string(template, prompt, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def detail_church_project(request, slug):
	qs = get_object_or_404(ChurchDevelopment, id=slug)
	contributions = qs.churchdevelopmentcontribution_set.all()
	total_amount_contributed = sum([x.amount for x in contributions])

	template = 'develop/develop_details_page.html'
	context = {
		'response_data': qs,
		'data': json.dumps(qs.chart_format()['data']),
		'labels': json.dumps(qs.chart_format()['labels']),
		'total_contributed': [total_amount_contributed, (qs.target_amount - total_amount_contributed)],
		'contributed': total_amount_contributed,
		'contributions': contributions,
	}

	return render(request, template, context)


@login_required(login_url='accounts:login')
def create_church_project_contribution(request, slug):
	if request.method == 'POST':
		project_qs = get_object_or_404(ChurchDevelopment, id=slug)
		project_form = ChurchDevelopmentContributionRegForm(request.POST)
		if project_form.is_valid():
			ChurchDevelopmentContribution(
				development=project_qs,
				amount=project_form.cleaned_data['amount'],
				member=project_form.cleaned_data['member'],
				comment=project_form.cleaned_data['comment']
			).save()
			msg = '\n Saved Successful'
			messages.success(request, msg)
			return redirect('contrib:detail_church_project', slug=slug)
		else:
			messages.error(request, project_form.errors)
			return redirect('contrib:detail_church_project', slug=slug)
	else:
		project_qs = get_object_or_404(ChurchDevelopment, id=request.GET['post_id'])
		project_form = ChurchDevelopmentContributionRegForm(initial={'development': project_qs})
		template = 'develop/contrib_create_page.html'
		context = {
			'project': project_qs,
			'form_data': project_form,
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def view_project_contrib_church(request):
	qs = get_object_or_404(ChurchDevelopmentContribution, id=request.GET['post_id'])
	template = 'develop/view_project_contrib_page.html'
	context = {
		'response_data': qs,
	}
	html_form = render_to_string(template, context, request=request)
	return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def edit_project_contrib_church(request, slug):
	if request.method == 'POST':
		project_inst = get_object_or_404(ChurchDevelopmentContribution, id=slug)
		project_form = ChurchDevelopmentContributionRegForm(request.POST, instance=project_inst)
		if project_form.is_valid():
			project_form.save()

			msg = '\nUpdated Successful'
			messages.success(request, msg)
			return redirect('contrib:detail_church_project', slug=project_inst.development.id)
		else:
			messages.error(request, project_form.errors)
			return redirect('contrib:detail_church_project', slug=project_inst.development.id)
	else:
		project_inst = get_object_or_404(ChurchDevelopmentContribution, id=request.GET['post_id'])
		project_form = ChurchDevelopmentContributionRegForm(instance=project_inst)
		template = 'develop/project_contrib_edit_page.html'
		context = {
			'project': project_inst,
			'form_data': project_form,
		}
		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})



@login_required(login_url='accounts:login')
def delete_project_contrib_church(request, slug):
	if request.method == 'POST':
		member_inst = get_object_or_404(ChurchDevelopmentContribution, id=slug)
		member_inst.delete()

		msg = "\nContribution Successful Deleted"
		messages.success(request, msg)
		return redirect('contrib:detail_church_project', slug=member_inst.development.id)
	else:
		member_inst = get_object_or_404(ChurchDevelopmentContribution, id=request.GET['post_id'])
		msg = "\nDelete  Contribution \nNB..\nThis Process is irreversible"
		template = 'develop/confirm_church_project_contrib_delete.html'
		prompt = {
			"data": msg,
			'member_id': member_inst.id
		}
		html_form = render_to_string(template, prompt, request=request)
		return JsonResponse({'html_response': html_form})
