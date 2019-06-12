
jQuery(document).ready(function($){

		$(document).ajaxStart(function () {
        $('#wait').show();
    });
    $(document).ajaxStop(function () {
        $('#wait').hide();
    });
    $(document).ajaxError(function () {
        $('#wait').hide();
    });

	$.ajaxSetup({
	    cache: false
	})

    $('[data-toggle="tooltip"]').tooltip();

    $('[data-toggle="popover"]').popover();

    $('#modalForm1').submit(function() {
        var $f = $('#modalForm1');
        var $url = "ddos_mitigate.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm2').submit(function() {
        var $f = $('#modalForm2');
        var $url = "firehol_control.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal-xl").find('.modal-body').html(result)
            $("#myModal-xl").modal('show');
        }});
    });

    $('#modalForm3').submit(function() {
        var $f = $('#modalForm3');
        var $url = "abnormal_process_detector.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal-nl").find('.modal-body').html(result)
            $("#myModal-nl").modal('show');
        }});
    });

    $('#modalForm4').submit(function() {
        var $f = $('#modalForm4');
        var $url = "fix_unison.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm5').submit(function() {
        var $f = $('#modalForm5');
        var $url = "fix_unison.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm6').submit(function() {
        var $f = $('#modalForm6');
        var $url = "set_default_php.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm7').submit(function() {
        var $f = $('#modalForm7');
        var $url = "sync_gdnsd_zone.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal-nl").find('.modal-body').html(result)
            $("#myModal-nl").modal('show');
        }});
    });

    $('#modalForm8').submit(function() {
        var $f = $('#modalForm8');
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('.modalForm9-wrap').submit(function(e) {
				e.preventDefault();
        var $id = e.target.id;
        var $f = $('#' + $id);
        console.log($id);
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('.modalForm10-wrap').submit(function(e) {
				e.preventDefault();
        var $id = e.target.id;
        var $f = $('#' + $id);
        console.log($id);
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm11').submit(function() {
        var $f = $('#modalForm11');
        var $url = "save_backup_settings.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm12').submit(function() {
        var $f = $('#modalForm12');
        var $url = "save_borgmatic_settings.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('.modalForm13-wrap').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        console.log($f.serialize());
        var $url = "save_borgmatic_settings.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm14').submit(function() {
        var $f = $('#modalForm14');
        var $url = "save_borgmatic_settings.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm16').submit(function() {
        var $f = $('#modalForm16');
        var $url = "lock_domain_data_to_package.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm17').submit(function() {
        var $f = $('#modalForm17');
        var $url = "save_pkg_server_settings.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm18').submit(function() {
        var $f = $('#modalForm18');
        var $url = "save_pkg_app_settings.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm19').submit(function() {
        var $f = $('#modalForm19');
        var $url = "save_resource_limit.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

		$('#modalForm20').submit(function() {
        console.trace();
        var $f = $('#modalForm20');
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });


    $('#myModal').on('hidden.bs.modal', function () {
    	location.reload()
       //location.replace("xtendweb.live.py");
    });

		$('#myModal-xl').on('hidden.bs.modal', function () {
			location.reload()
			 //location.replace("xtendweb.live.py");
		});

    // btn animation for ajax updates
    $('.btn-ajax-sm').on('click', function() {
    	var $this = $(this);
		var loadingText = '<i class="spinner-grow spinner-grow-sm"><span class="sr-only">Loading</span></i>';
		if ($(this).html() !== loadingText) {
			$this.data('original-text', $(this).html());
			$this.html(loadingText);
    	}
		setTimeout(function() {
			$this.html($this.data('original-text'));
		}, 5000);
    });

    // btn-ajax animation for ajax updates
    $('.btn-ajax').on('click', function() {
    	var $this = $(this);
		var loadingText = '<i class="spinner-grow spinner-grow-sm"></i> loading...';
		if ($(this).html() !== loadingText) {
			$this.data('original-text', $(this).html());
			$this.html(loadingText);
    	}
		setTimeout(function() {
			$this.html($this.data('original-text'));
    	}, 5000);
    });

    // btn-ajax-slow animation for ajax updates
    $('.btn-ajax-slow').on('click', function() {
    	var $this = $(this);
		var loadingText = '<i class="spinner-grow spinner-grow-sm"></i> loading...';
		if ($(this).html() !== loadingText) {
			$this.data('original-text', $(this).html());
			$this.html(loadingText);
    	}
		setTimeout(function() {
			$this.html($this.data('original-text'));
    }, 20000);
    });

});
