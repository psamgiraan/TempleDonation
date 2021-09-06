from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
#from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField
from smart_selects.db_fields import GroupedForeignKey, ChainedForeignKey, ChainedManyToManyField
from django.conf import settings
from twilio.rest import Client
from .utils import CITIES, state_choices


class State(models.Model):
    state_name = models.CharField( null=False, max_length=100, unique=True, )

    def __str__(self):
        return str(self.state_name)


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=200, null=False, unique=True)

    def __str__(self):
        return str(self.city_name)

# class DonationStatus(models.Model):
#     id = models.AutoField(primary_key=True)
#     status = models.CharField(max_length=100, blank=False, unique=True, )
#
#     def __str__(self):
#         return str(self.status)


# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100, default='')
#     mobile_number = PhoneNumberField(help_text='Mobile Format: +917028735596')
#
#     alternate_contact_number = PhoneNumberField(help_text='Alternate contact number')
#     address = models.CharField(max_length=100, default='')
#     adhar_number = models.CharField(max_length=50, default=None)
#     state = models.ForeignKey(State, on_delete=models.CASCADE)
#     city = ChainedForeignKey(
#         City,
#         chained_field="state",
#         chained_model_field="state",
#         show_all=False,
#         auto_choose=True,
#         default=None)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name + str(self.mobile_number)


class BhaktamberCategories(models.Model):
    id = models.AutoField(primary_key=True)
    reason = models.CharField(max_length=100, blank=False,  unique=True, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reason




class UserDonation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')

    mobile_number = PhoneNumberField(help_text='Mobile Format: +917028735596', unique=True)
    address = models.CharField(max_length=100, default='')
    adhar_number = models.CharField(max_length=12, validators=[RegexValidator(r'^\d{12,12}$', message='Enter valid AADHAAR number', code='nomatch')], unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    # city = ChainedForeignKey(
    #     City,
    #     chained_field="state",
    #     chained_model_field="state",
    #     show_all=False,
    #     auto_choose=True,
    #     default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Donaties"

    def clean(self):
        pass

    def __str__(self):
        return str(self.mobile_number)


class Donation_Details(models.Model):  #Transaction_Details
    id = models.AutoField(primary_key=True)
    donor_details = models.ForeignKey(UserDonation, on_delete=models.CASCADE, )
    Bhaktamber_category = models.ForeignKey(BhaktamberCategories, on_delete=models.CASCADE)
    amount_regex = RegexValidator(regex=r'^[1-9][0-9]*$', message="Donation amount should be 1 or > 1 Rs'.")
    donation_amount = models.IntegerField(validators=[amount_regex], default=None, blank=False)
    total_received_amount = models.FloatField(default=0,blank=True, null=True, )
    current_received_amount = models.IntegerField(validators=[amount_regex], default=None, blank=False)
    total_painding_amount = models.FloatField(default=0,blank=True, null=True, )
    donation_date = models.DateField(default=None)
    donation_status = models.CharField(max_length=100, )
    donation_deposit_date = models.DateField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add=True
    updated_at = models.DateTimeField(auto_now=True)  # auto_now=True

    class Meta:
        verbose_name_plural = "Donation_Details"


    def __str__(self):
        return str(self.donation_amount)

    def applicant_donor_details(self):
        return self.donor_details.mobile_number
    applicant_donor_details.short_description = 'Applicant Mobile Number'

    def applicant_name(self):
        return self.donor_details.name
    applicant_name.short_description = 'Applicant Name'

    def applicant_state(self):
        return self.donor_details.state
    applicant_state.short_description = 'State'

    def Donation_Category(self):
        return self.Bhaktamber_category.reason
    Donation_Category.short_description = 'Bhaktamber Category'

    def applicant_address(self):
        return self.donor_details.address
    applicant_address.short_description='Address'

    def save(self, *args, **kwargs):
        self.total_received_amount = int(self.total_received_amount + self.current_received_amount)
        self.total_painding_amount = int(self.donation_amount - self.total_received_amount)
        if self.total_received_amount==self.donation_amount:
            self.donation_status='Paid'
        elif self.total_received_amount < self.donation_amount:
            self.donation_status = 'Partialy Paid'
        elif self.total_received_amount==0:
            self.donation_status = 'Unaid'
        super().save(*args, **kwargs)

        # mobile_number = self.donor_details
        # first_name = self.applicant_name
        # donation_amount = self.current_received_amount
        # donation_status = self.donation_status
        # message_to_broadcast = (f"Thanks {first_name}, For Paying donation Of Rs. {donation_amount}.")
        # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # # mobile_number="+91"+mobile_number
        # if donation_status == 'PAID' or 'PARTIALY PAID':
        #     client.messages.create(to=mobile_number,
        #                            from_=settings.TWILIO_NUMBER,
        #                            body=message_to_broadcast)
        #     print('Message sent successfully.')
        # else:
        #     pass



class Transaction_Details(models.Model):
    donation_details = models.ForeignKey(Donation_Details, on_delete=models.CASCADE)
    # total_amount = models.ForeignKey(Donation_Details, on_delete=models.CASCADE)
    amount_regex = RegexValidator(regex=r'^[1-9][0-9]*$', message="Donation amount should be 1 or > 1 Rs'.")
    current_received_amount = models.IntegerField(validators=[amount_regex], default=None, blank=False)
    # painding_amount = models.IntegerField(validators=[amount_regex], default=None, blank=False)
    donation_deposit_date = models.DateField(default=None)




    def __str__(self):
        return str(self.received_amount)








