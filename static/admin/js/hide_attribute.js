hide_page=false;

window.addEventListener("load", function() {
    (function($) {
        django.jQuery(document).ready(function(){
            if (django.jQuery('#id_donation_status').is(':checked')) {
                django.jQuery("#id_donation_deposit_date").prop('disabled', false);
                django.jQuery("#calendarlink1").parent().css("display","")
                hide_page=false;
            } else {
                django.jQuery("#id_donation_deposit_date").prop('disabled', true);
                django.jQuery("#id_donation_deposit_date").val("");
                django.jQuery("#calendarlink1").parent().css("display","none")
                hide_page=true;
            }
            django.jQuery("#id_donation_status").click(function(){
                hide_page=!hide_page;
                if (hide_page) {
                    django.jQuery("#id_donation_deposit_date").prop('disabled', true);
                    django.jQuery("#id_donation_deposit_date").val("");
                    django.jQuery("#calendarlink1").parent().css("display","none")
                } else {
                    django.jQuery("#id_donation_deposit_date").prop('disabled', false);
                    django.jQuery("#calendarlink1").parent().css("display","")
                }
            })

        })

    })(django.jQuery);
});


