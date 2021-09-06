# Register your models here.
from django.contrib import admin
from .models import UserDonation, BhaktamberCategories, Donation_Details,Transaction_Details
from .utils import broadcast_sms
# from .views import userdata
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from admin_totals.admin import ModelAdminTotals
from django.db.models import Sum, Avg
from django.db.models.functions import Coalesce
from django_object_toolbar_admin.admin import DjangoObjectToolbarAdmin
from django.utils.html import mark_safe  # Older versions
from django.utils.html import format_html  # Newer versions


# Register your models here.


@admin.register(UserDonation)
class PersonAdmin(DjangoObjectToolbarAdmin, admin.ModelAdmin):
    list_display = ("name", "mobile_number",'adhar_number',"city",'state','address')
    list_filter = ('state', "city",)
    search_fields = ("name__startswith", "mobile_number", 'state','city')
    class Media:
        pass  # This class is imp for chained dropdown

class Transactions1Admin(admin.TabularInline):
    model = Transaction_Details
    extra=1

    fields=('received_amount','donation_date')
    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super(Transactions1Admin, self).get_formset(request, obj, **kwargs)



@admin.register(Donation_Details)
class TransactionsAdmin(ModelAdminTotals, DjangoObjectToolbarAdmin, admin.ModelAdmin):  # ,admin.ModelAdmin
    list_display = ("applicant_name", "applicant_donor_details", 'applicant_state', 'Donation_Category', 'donation_deposit_date',"donation_amount",'total_received_amount','current_received_amount','total_painding_amount', "donation_status",'custom_field')
    list_filter = ("donation_status", ('donation_date', DateRangeFilter), ('donation_deposit_date', DateRangeFilter),'Bhaktamber_category__reason', 'donor_details__state',)  #
    search_fields = ('donor_details__mobile_number','donor_details__mobile_number__startswith', 'donor_details__name__startswith', 'Bhaktamber_category__reason','donor_details__adhar_number')
    autocomplete_fields = ['donor_details',]
    list_totals = [('donation_amount', lambda field: Coalesce(Sum(field), 0)),('total_received_amount', lambda field: Coalesce(Sum(field), 0)),('total_painding_amount', lambda field: Coalesce(Sum(field), 0)),('current_received_amount', lambda field: Coalesce(Sum(field), 0)) ]  # ('donation_amount', Avg)
    inlines = [Transactions1Admin]
    class Media:
        js = [
            'admin/js/hide_attribute.js',
        ]
    def get_fields(self, request, obj=None):
        fields = super(TransactionsAdmin, self).get_fields(request, obj)
        if request.user.is_superuser:
            print(fields)
            # fields += ('approve',)
        return fields

    def save_model(self, request, obj, form, change):
        super(TransactionsAdmin, self).save_model(request, obj, form, change)
        broadcast_sms(obj)

    def custom_field(self, obj):
        return format_html(f'<a href="/temple/{obj.id}/userdata/"  target="blank">Print</a>')



# @admin.register(Transaction_Details)
# class TransactionDetails(admin.ModelAdmin):
#     list_display = ('received_amount','painding_amount','Total_Amount')

admin.site.register(BhaktamberCategories)
# admin.site.register(User)
#admin.site.register(DonationStatus)



###### Installed Libraries ########
# pip install admin-totals
# pip install django-admin-rangefilter
# pip install django-phonenumber-field
# pip install django-static-fontawesome
####pip install django-phone-field
# pip install django-object-toolbar-admin
# pip install twilio
# #pip install django-phone-field==1.8.1
#pip install phonenumbers
# pip install django-smart-selects
#pip install djangorestframework