from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string


from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get

from .forms import ChurchMembershipForm, FileUploadForm

# noinspection PyUnresolvedReferences
from DB.models import ChurchMember


@login_required(login_url='accounts:login')
def members_registration(request):
	if request.method == 'POST':
		registration_form = ChurchMembershipForm(request.POST, request.FILES)
		if registration_form.is_valid():
			registration_form.save()

			msg = "\nMember {} {} added Successful".format(registration_form.cleaned_data['first_name'],
														   registration_form.cleaned_data['last_name'])

			# return value when form is saved successful
			messages.success(request, msg)
			return redirect('accounts:view_members')
		else:
			messages.success(request, registration_form.errors)
			return redirect('accounts:view_members')
	else:
		registration_form = ChurchMembershipForm()
		template = 'accounts/registration_page.html'
		context = {
			'form_data': registration_form
		}
		html_form = render_to_string(
			template, context, request=request
		)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def members_view(request):
	members_qs = ChurchMember.objects.filter(active=True)  # get active members only
	template = 'accounts/members_view.html'
	context = {
		'members': members_qs
	}
	return render(request, template, context)


@login_required(login_url='accounts:login')
def members_details(request):
	pk = request.GET['post_id']
	member_qs = ChurchMember.objects.get(id=pk)
	template = 'accounts/members_details.html'
	context = {
		'member_data': member_qs,
	}
	html_form = render_to_string(template, context, request=request)
	return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def member_information_update(request, pk):
	if request.method == 'POST':
		member_instance = get_object_or_404(ChurchMember, pk=pk)
		form = ChurchMembershipForm(request.POST, request.FILES, instance=member_instance)
		if form.is_valid():
			member = form.save()
			messages.success(request, "{} information edited successful".format(member))
			return redirect('/account/view/members/')
		else:
			messages.error(request, form.errors)
			return redirect('/account/view/members/')
	else:

		member_instance = get_object_or_404(ChurchMember, pk=request.GET['post_id'])
		form = ChurchMembershipForm(instance=member_instance)
		context = {
			'form_data': form,
			'member_id': member_instance,
		}
		template = 'accounts/edit_user_form.html'

		html_form = render_to_string(template, context, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def member_information_delete(request, slug):
	if request.method == 'POST':
		member_inst = get_object_or_404(ChurchMember, id=slug)
		member_inst.delete()

		msg = "\nMember Successful Deleted"
		messages.success(request, msg)
		return redirect('/account/view/members/')
	else:
		member_inst = get_object_or_404(ChurchMember, id=request.GET['post_id'])
		msg = "\nDelete Member {} \nNB..\nThis Process is irreversible".format(member_inst)
		template = 'accounts/confirm_account_delete.html'
		prompt = {
			"data": msg,
			'member_id': member_inst.id
		}
		html_form = render_to_string(template, prompt, request=request)
		return JsonResponse({'html_response': html_form})


@login_required(login_url='accounts:login')
def register_from_excel(request):
	if request.method == "POST":
		file_form = FileUploadForm(request.POST, request.FILES)
		if file_form.is_valid():
			excel_file = file_form.cleaned_data['choose_file']

			if (str(excel_file)).split('.')[-1] == "xls":
				# read the file and loop though to get the sheets available
				file_data = xls_get(excel_file)

			elif (str(excel_file)).split('.')[-1] == "xlsx":
				file_data = xlsx_get(excel_file, column_limit=10)

			failed_entries = []
			saved_entries = 0
			if len(file_data) > 1:  # check to see the file has one sheet
				msg = '\nError Bad Excel File....\nFile Contains One Sheet...!!'
				messages.error(request, msg)
				return redirect('accounts:view_members')
			for data_obj in file_data:  # loop through each sheet
				sheet_obj = file_data[data_obj]
				sheet_len = len(sheet_obj)
				header_indexes = []
				if sheet_len > 1:  # we have data
					for header in sheet_obj[0]:  # get the headers
						if header.lower() == "first name":  # change all to lower case and map the indexes
							header_indexes.append(sheet_obj[0].index(header))
						elif header.lower() == 'middle name':
							header_indexes.append(sheet_obj[0].index(header))
						elif header.lower() == 'last name':
							header_indexes.append(sheet_obj[0].index(header))
						elif header.lower() == 'gender':
							header_indexes.append(sheet_obj[0].index(header))
						elif header.lower() == 'email':
							header_indexes.append(sheet_obj[0].index(header))
						elif header.lower() == 'residency':
							header_indexes.append(sheet_obj[0].index(header))
						elif header.lower() == 'phone number':
							header_indexes.append(sheet_obj[0].index(header))
						elif header.lower() == 'occupation':
							header_indexes.append(sheet_obj[0].index(header))
						elif header.lower() == 'citizenship':
							header_indexes.append(sheet_obj[0].index(header))
						elif header.lower() == 'marital status':
							header_indexes.append(sheet_obj[0].index(header))
						else:
							sheet_obj[0].remove(header)
					if len(header_indexes) != 10:
						msg = '\nFile Contains Bad Header Format, Check File And Try Again'
						messages.error(request, msg)
						return redirect('accounts:view_members')
					else:
						i = 1
						# loop trough each row
						while i < sheet_len:
							if len(sheet_obj[i]) != 0:
								available_row = sheet_obj[i]
								try:
									gender = available_row[header_indexes[3]]
									marital_status = available_row[header_indexes[9]]
									if len(gender) == 1:  # if gender is one character implement good variable
										if gender.lower() == 'm':
											gender = 'Male'
										elif gender.lower() == 'f':
											gender = 'Female'
										else:
											gender = 'Other'
									if len(
											marital_status) == 1:  # if marital_status is one character implement a proper variable
										if marital_status.lower() == 'm':
											marital_status = 'Married'
										elif marital_status.lower() == 'd':
											marital_status = 'Divorced'
										elif marital_status.lower() == 'w':
											marital_status = 'Widowed'
										else:
											marital_status = 'Single'

									ChurchMember.objects.create(
										first_name=available_row[header_indexes[0]],
										middle_name=available_row[header_indexes[1]],
										last_name=available_row[header_indexes[2]],
										gender=gender,
										email=available_row[header_indexes[4]],
										residency=available_row[header_indexes[5]],
										phone_number=available_row[header_indexes[6]],
										occupation=available_row[header_indexes[7]],
										citizenship=available_row[header_indexes[8]],
										marital_status=marital_status,
									)
									saved_entries += 1
								except:
									failed_entries.append(i)

							i += 1
				else:  # no data
					pass
			if len(failed_entries) == 0:
				msg = 'Success All Members Registered, Total: {}'.format(saved_entries)
				messages.success(request, msg)
				return redirect('accounts:view_members')
			else:
				msg = '\nRegitered Memebrs:{}, Failed:{}, RowsFailed:{}'.format(
					saved_entries, len(failed_entries), [x for x in failed_entries]
				)
				messages.error(request, msg)
				return redirect('accounts:view_members')
		else:
			messages.error(request, file_form.errors)
			return redirect('accounts:view_members')
	else:
		file_form = FileUploadForm()
		template = 'accounts/file_upload_form.html'
		context = {
			'form_file': file_form,
		}
		html_form = render_to_string(
			template, context, request=request
		)
		return JsonResponse({"html_response": html_form})
