jQuery(document).ready(function($){

	$.ajaxSetup({
    	cache: false
	})

    $('[data-toggle="tooltip"]').tooltip();

    $('[data-toggle="popover"]').popover();

    $('#modalForm1').submit(function() {
        var $f = $('#modalForm1');
        var $url = "view_log.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal-xl").find('.modal-body').html(result)
            $("#myModal-xl").modal('show');
        }});
    });

    $('#modalForm2').submit(function() {
        var $f = $('#modalForm2');
        var $url = "save_app_settings.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm3').submit(function() {
        var $f = $('#modalForm3');
        var $url = "save_app_extra_settings.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm4').submit(function() {
        var $f = $('#modalForm4');
        var $url = "reload_config.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm5').submit(function() {
        var $f = $('#modalForm5');
        var $url = "view_nginx_log.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal-xl").find('.modal-body').html(result)
            $("#myModal-xl").modal('show');
        }});
    });

    $('#modalForm6').submit(function() {
        var $f = $('#modalForm6');
        var $url = "save_app_extra_settings.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('.modalForm7-wrap').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        console.log($f.serialize());
        var $url = "subdir_delete.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm8').submit(function() {
        var $f = $('#modalForm8');
        var $url = "subdir_save_app_settings.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm9').submit(function() {
        var $f = $('#modalForm9');
        var $url = "autoswitch.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

    $('#modalForm10').submit(function() {
        var $f = $('#modalForm10');
        var $url = "dependency_installer.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal-nl").find('.modal-body').html(result)
            $("#myModal-nl").modal('show');
        }});
    });

    $('#myModal').on('hidden.bs.modal', function () {
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
