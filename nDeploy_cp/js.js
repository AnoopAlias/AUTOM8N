jQuery(document).ready(function($){
	$(function () {
  		$('[data-toggle="tooltip"]').tooltip()
	})
	// Accordion
	var active = true;

    $('#toggle-accordion').click(function () {
        if (active) {
            active = false;
            $('.panel-collapse').collapse('show');
            $('.panel-title').attr('data-toggle', '');
            $(this).text('collapse -');
        } else {
            active = true;
            $('.panel-collapse').collapse('hide');
            $('.panel-title').attr('data-toggle', 'collapse');
            $(this).text('expand +');
        }
    });

    $('#accordion').on('show.bs.collapse', function () {
        if (active) $('#accordion .in').collapse('hide');
    });
});