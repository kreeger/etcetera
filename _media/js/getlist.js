$(function () {
	$('input#q').keyup(function () {
		console.log(this.value);
		$.get('../service', {q:'kreeger'}, function(data) { alert(data); });
		return false;
	});
});