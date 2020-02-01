// Call the dataTables jQuery plugin
$(document).ready(function() {
  $.ajax({
              url: 'http://localhost:63342/recruitment/web_static/data.txt',
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
