$(document).ready(function() {
	$.viewMap = {
		'etc' : $('#first_name_row, #last_name_row, #department_text_row, #course_row, #phone_row, #email_row, #building_row, #room_row, #equipment_needed_row, #out_date_row, #return_date_row, #submit_row'),
		'requestor' : $('#first_name_row, #last_name_row, #department_text_row, #course_row, #phone_row, #email_row, #building_row, #room_row, #equipment_needed_row, #out_date_row, #return_date_row, #submit_row'),
		'' : $('#help_text')
	};
	
	$('#first_name_row, #last_name_row, #department_text_row, #course_row, #phone_row, #email_row, #building_row, #room_row, #equipment_needed_row, #out_date_row, #return_date_row, #submit_row').hide();

	$('#id_return_type').change(function() {
		// hide all
		$.each($.viewMap, function() { this.hide(); });
		// show current
		$.viewMap[$(this).val()].show();
		//$('#help_text').hide();
	});
});
