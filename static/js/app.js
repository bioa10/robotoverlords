$(document).ready(function () {
	$('[data-url]').click(function (e) {
		if (!$(e.target).is('a')) {
		    document.location = $(this).data('url');
		}
	});
});