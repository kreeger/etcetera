$(document).ready(function() {
  $.viewMap = {
    'install' : $([]),
    'repair' : $('#barcode_row, #equipment_row')
  };

  $('#id_work_type').change(function() {
    // hide all
    $.each($.viewMap, function() { this.hide(); });
    // show current
    $.viewMap[$(this).val()].show();
  });
});