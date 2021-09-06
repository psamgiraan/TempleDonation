$(document).ready(function() {
            $('#HorizontalVerticalExample').DataTable( {
//                destroy: true,
//                retrieve: true,
//                "scrollX": true,
//                "scrollY": 300,
                initComplete: function () {
                    this.api().columns('.select-filter').every( function () {
                        var column = this;
                        var select = $('<select><option value=""></option></select>')
                            .appendTo( $(column.footer()).empty() )
                            .on( 'change', function () {
                                var val = $.fn.dataTable.util.escapeRegex(
                                    $(this).val()
                                );

                                column
                                    .search( val ? '^'+val+'$' : '', true, false )
                                    .draw();
                            } );

                        column.data().unique().sort().each( function ( d, j ) {
                            select.append( '<option value="'+d+'">'+d+'</option>' )
                        } );
                    } );
                }

            } );

        } );





//    'paging': true,
//    'lengthChange': true,
//    'searching': true,
//    'ordering': true,
//    'info': true,
//    'autoWidth': true,
//    'responsive':true,

