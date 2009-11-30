$(document).ready(function() {
  $.viewMap = {
    'install' : $('#coordinator_row'),
    'repair' : $('#barcode_row, #equipment_row')
  };

	$('#coordinator_row').hide();

  $('#id_work_type').change(function() {
    // hide all
    $.each($.viewMap, function() { this.hide(); });
    // show current
    $.viewMap[$(this).val()].show();
  });
});