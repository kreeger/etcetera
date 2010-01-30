$(function () {
	$("a.collapse-link").click(function(event) {
		event.preventDefault();
		$(this).parent().next().toggle();
		$("span.collapse-mono").text($("span.collapse-mono").text() == '+' ? '-' : '+');
	});
});