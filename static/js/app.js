$(document).ready(function () {
	$('[data-url]').click(function (e) {
	    document.location = $(this).data('url');
	});
});