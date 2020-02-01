// Call the dataTables jQuery plugin
$(document).ready(function() {
  $.ajax({
              url: 'http://0.0.0.0:5000/api/v1/victims',
              dataType: 'json',
              success: function(json){
                   $('#dataTable').DataTable( {
    data: json,
    columns: [
       { data: 'name' },
       { data: 'value' }
    ]
   } );

}
});
});
