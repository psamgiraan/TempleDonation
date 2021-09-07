from django.forms import ModelForm,inlineformset_factory
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import  State, City, BhaktamberCategories,UserDonation,Donation_Details, Transaction_Details
# class UserForm(ModelForm):
#     class Meta:
#         model=User
#         fields=['name','mobile_number','adhar_number','alternate_contact_number','address']


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user




class UserDonationForm(ModelForm):
    class Meta:
        model=UserDonation
        fields=['name','mobile_number','adhar_number','address', 'state','city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()


        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('city_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('city_name')

class Donation_DetailsForm(ModelForm):
    class Meta:
        model=Donation_Details
        fields = ('__all__')
        widgets ={
            'total_received_amount': forms.HiddenInput(),
            'total_painding_amount': forms.HiddenInput(),
        }
        exclude = ()

class Transaction_DetailsForm(ModelForm):
    class Meta:
        model=Transaction_Details
        fields = ('__all__')
        exclude = ()

Transaction_DetailsFormSet = inlineformset_factory(Donation_Details, Transaction_Details, form=Transaction_DetailsForm, extra=0)


class BhaktamberCategoryForm(ModelForm):
    class Meta:
        model = BhaktamberCategories
        fields = ['reason']










