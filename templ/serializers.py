from .models import UserDonation, BhaktamberCategories, User, Donation_Details
from rest_framework import serializers


class UserDonationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserDonation
        fields = ['name', 'mobile_number', 'address','adhar_number','state','city','adhar_number','donation_amount','donation_date','donation_deposit_date','donation_status','created_at','updated_at']
        # model = Transaction_Details
        # fields = ["applicant_name", "applicant_donor_details", 'applicant_state', 'Donation_Category', "donation_amount", "donation_status"]



       