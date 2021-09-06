$(document).ready(function() {
    var oTable =$('#HorizontalVerticalExample').DataTable( {
//        retrieve: true,
        destroy: true,
        "scrollX": true,
        "scrollY": 300,
        "footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;

            // Remove the formatting to get integer data for summation
            var intVal = function ( i ) {
                return typeof i === 'string' ?
                    i.replace(/[\$,]/g, '')*1 :
                    typeof i === 'number' ?
                        i : 0;
            };

            // Total over all pages
            total = api
                .column(7)
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Total over this page
            DonationAmountTotal = api
                .column(7, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Total over this page
            TotalReceivedAmount = api
                .column(8, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );
            CurrentReceivedAmount = api
                .column(9, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            TotalPaindingAmount = api
                .column(10, { page: 'current'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0 );

            // Update footer
            $( api.columns(7).footer() ).html('₹'+DonationAmountTotal);
            $( api.columns(8).footer() ).html('₹'+TotalReceivedAmount);
            $( api.columns(9).footer() ).html('₹'+CurrentReceivedAmount);
            $( api.columns(10).footer() ).html('₹'+TotalPaindingAmount);

        }
    } );
} );