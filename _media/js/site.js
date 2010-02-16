$(function() {
	$("input#go-back").click(function(event) {
		history.back();
	});
	$("table.list tr:odd").addClass("shaded");
	$("#list tr:odd").addClass("shaded");
});