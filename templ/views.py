from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

############## For login logout reset password ################################################
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
###############################################################################################
from django.template import loader

from .models import UserDonation,  BhaktamberCategories,Donation_Details, City,Transaction_Details
from .forms import  UserDonationForm,Donation_DetailsForm,BhaktamberCategoryForm, NewUserForm , Transaction_DetailsFormSet, Transaction_DetailsForm

from .utils import broadcast_sms1
import datetime

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from bootstrap_datepicker_plus import DatePickerInput
from django.db import transaction
from django.db.models import F

###################################################################################################

###################################################################################################

### Refrence site for login logout reset::-->   https://www.ordinarycoders.com/blog/article/django-password-reset

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/donors_list")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="templ/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/donors_list")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="templ/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("/login")


############ Reset  Password ##########

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "templ/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="templ/password/password_reset.html", context={"password_reset_form":password_reset_form})




######################################################################################################
# @login_required(login_url='/login/')

class DonorsListView(ListView):
    model = UserDonation
    context_object_name = 'donorslist'
    template_name = 'templ/donatees_list.html'

class DonorsCreateView(CreateView):
    model = UserDonation
    form_class = UserDonationForm
    success_url = reverse_lazy('donors_changelist')
    template_name = 'templ/donatees.html'

class DonorsUpdateView(UpdateView):
    model = UserDonation
    form_class = UserDonationForm
    success_url = reverse_lazy('donors_changelist')
    template_name = 'templ/donatees.html'

def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('city_name')
    return render(request, 'templ/city_dropdown_list_options.html', {'cities': cities})

class DonorsDelete(DeleteView):
    model = UserDonation
    success_url = reverse_lazy('donors_changelist')
    template_name = 'templ/Donation_confirm_delete.html'

#########################################################################################################

class DonationDetailsListView(ListView):
    model = Donation_Details
    context_object_name = 'DonationDetailsList'
    template_name = 'templ/donation_details_list.html'


    # def get_queryset(self):
    #     return Donation_Details.objects.prefetch_related('donor_details').order_by('-created_at')

# class DonationDetailsCreateView(CreateView):
#     model = Donation_Details
#     form_class = Donation_DetailsForm
#     success_url = reverse_lazy('donation_details_changelist')
#     def get_form(self):
#         form = super().get_form()
#         form.fields['donation_deposit_date'].widget = DatePickerInput()
#         return form
#     template_name = 'templ/DonationDetails.html'


class DonationTransactionCreate(CreateView):
    model = Donation_Details
    fields = ['donor_details', 'Bhaktamber_category','donation_amount','current_received_amount','donation_date','donation_deposit_date',]
    success_url = reverse_lazy('donation_details_changelist')
    template_name = 'templ/DonationDetails.html'

    def get_context_data(self, **kwargs,):
        data = super(DonationTransactionCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['transaction_details'] = Transaction_DetailsFormSet(self.request.POST)
        else:
            data['transaction_details'] = Transaction_DetailsFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        transaction_details = context['transaction_details']
        with transaction.atomic():
            self.object = form.save()
            if transaction_details.is_valid():
                transaction_details.instance = self.object
                transaction_details.save()
        return super(DonationTransactionCreate, self).form_valid(form)

    def get_form(self):
        form = super().get_form()
        form.fields['donation_date'].widget = DatePickerInput()
        form.fields['donation_deposit_date'].widget = DatePickerInput()
        return form



# class DonationDetailsUpdateView(UpdateView):
#     model = Donation_Details
#     form_class = Donation_DetailsForm
#     success_url = reverse_lazy('donation_details_changelist')
#     def get_form(self):
#         form = super().get_form()
#         form.fields['donation_date'].widget = DatePickerInput()
#         form.fields['donation_deposit_date'].widget = DatePickerInput()
#         form.fields['donation_deposite_date'].widget = DatePickerInput()
#         return form
#     template_name = 'templ/DonationDetails.html'

class DonationTransactionDetail(DetailView):
    model = Donation_Details
    # fields=('__all__')
    fields = [ 'donation_amount','current_received_amount','donation_deposit_date','donation_status',]
    success_url = reverse_lazy('donation_details_changelist')
    template_name = 'templ/transaction_details.html'

    # def get_context_dataa(self, **kwargs):
    #     context = super(DonationTransactionCreate, self).get_context_dataa(**kwargs)
    #     context['transaction_details'] = Donation_Details.objects.all()
    #     return context

    def post(self, request, *args, **kwargs):
        print(request.POST)

    def get_context_data(self, **kwargs):
        data = super(DonationTransactionDetail, self).get_context_data(**kwargs)
        if self.request.POST:
            data['transaction_details'] = Transaction_DetailsFormSet(self.request.POST, instance=self.object)
        else:
            data['transaction_details'] = Transaction_DetailsFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        transaction_details = context['transaction_details']
        with transaction.atomic():
            self.object = form.save()
            if transaction_details.is_valid():
                transaction_details.instance = self.object
                transaction_details.save()
        return super(DonationTransactionDetail, self).form_valid(form)

    def get_form(self):
        form = super().get_form()
        # form.fields['donation_date'].widget = DatePickerInput()
        form.fields['Date'].widget = DatePickerInput()
        return form


class Donation_DetailsDelete(DeleteView):
    model = Donation_Details
    success_url = reverse_lazy('donation_details_changelist')
    template_name = 'templ/Donation_confirm_delete.html'


#########################################################################################################
##### PRINT FUNCTION ######

def userdata(request,obj_id):
	user_obj = Donation_Details.objects.filter(id=obj_id)
	#print(user_obj.name)
	context = {
		'user_obj': user_obj,
	}
	return render(request, 'templ/userdonation.html', context)

##########################################################################################################


class BhaktamberCategoryListView(ListView):
    model = BhaktamberCategories
    context_object_name = 'BhaktamberCategoriesList'
    template_name = 'templ/bhaktamber_category_list.html'

class BhaktamberCategoryCreateView(CreateView):
    model = BhaktamberCategories
    form_class = BhaktamberCategoryForm
    success_url = reverse_lazy('BhaktamberCategory_changelist')
    template_name = 'templ/BhaktamberCategory.html'

class BhaktamberCategoryUpdateView(UpdateView):
    model = BhaktamberCategories
    form_class = BhaktamberCategoryForm
    success_url = reverse_lazy('BhaktamberCategory_changelist')
    template_name = 'templ/BhaktamberCategory.html'


###########################################################################################################
def donation_reminder_sms(request):

	date = datetime.datetime.now().date()
	days = datetime.timedelta(1)
	date = date+days
	user_donations = UserDonation.objects.all().filter(donation_date=date)
	for user_donation in user_donations:
		broadcast_sms1(user_donation)


############       PRINT FUNCTION      ############

def userdata(request,obj_id):
	user_obj = Donation_Details.objects.filter(id=obj_id)
	#print(user_obj.name)
	context = {
		'user_obj': user_obj,
	}
	return render(request, 'templ/userdonation.html', context)

#####################################################





