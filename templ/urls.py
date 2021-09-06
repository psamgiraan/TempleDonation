from django.urls import path,include
from rest_framework import routers
from . import views
from django.conf.urls import url
from django.urls import path
router = routers.DefaultRouter()


urlpatterns = [

    url('', include(router.urls)),
    path('<int:obj_id>/userdata/', views.userdata, name='userdata'),
    path('donation-reminder-sms/', views.donation_reminder_sms, name='donation_reminder_sms'),

# login logout reset password -->
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path("password_reset", views.password_reset_request, name="password_reset"),

#donors creation -->
    path('donors_list/', views.DonorsListView.as_view(), name='donors_changelist'),
    path('add_donor/', views.DonorsCreateView.as_view(), name='donors_add'),
    path('<int:pk>/', views.DonorsUpdateView.as_view(), name='donors_change'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('dlt/<int:pk>', views.DonorsDelete.as_view(), name='donors_delete'),

# donation details -->
    path('donation_details/', views.DonationDetailsListView.as_view(), name='donation_details_changelist'),
    # path('add_donation/', views.DonationDetailsCreateView.as_view(), name='donation_add'),
    # path('a<int:pk>/', views.DonationDetailsUpdateView.as_view(), name='donation_change'),
    path('donation/add/', views.DonationTransactionCreate.as_view(), name='donation_addd'),
    path('donation/<int:pk>', views.DonationTransactionDetail.as_view(), name='donation-update'),
    path('delete/<int:pk>', views.Donation_DetailsDelete.as_view(), name='donation_delete'),


# bhaktamber catogry crate add update -->
    path('bhaktamber_category_list/', views.BhaktamberCategoryListView.as_view(), name='BhaktamberCategory_changelist'),
    path('add_bhaktamber/', views.BhaktamberCategoryCreateView.as_view(), name='bhaktamber_add'),
    path('b<int:pk>/', views.BhaktamberCategoryUpdateView.as_view(), name='bhaktamber_change'),


]





















