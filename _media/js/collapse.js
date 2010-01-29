$(function () {
	$("a.collapse-link").click(function(event) {
		event.preventDefault();
		$("table#list.collapse-content").toggle();
		$("span.collapse-mono").text($("span.collapse-mono").text() == '+' ? '-' : '+');
	});
});