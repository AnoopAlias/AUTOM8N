jQuery(document).ready(function($){

	// Are we physically in Terminal Window?
    var terminalActive;

    // #terminal-panel
    var terminalPanel;

    var prevAjaxCall = "";
    // Poll for file changes using ajax
    setInterval(function() {
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function() {
            if (ajax.readyState == 4) {
                if (ajax.responseText != prevAjaxCall) {
                    $("#terminal .modal-body").load('term.log');
                    window.terminalActive = ($('#terminal-panel:hover').length > 0);
                    if ( !window.terminalActive ) {
                        // Scroll to bottom if not in terminal
                        window.terminalPanel = document.getElementById("terminal-panel");
                        window.terminalPanel.scrollTop = window.terminalPanel.scrollHeight;
                        // console.log('Mouse not detected in Terminal');
                    } else {
                        // console.log('Mouse detected in Terminal');
                    }
                    prevAjaxCall = ajax.responseText;
                }
            }
        };
        ajax.open("POST", "term.log", true);
        ajax.send();
    }, 1000);

    // General Form Validatons
    function formValidations(){
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName("needs-validation");
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener(
                "submit",
                function (event) {
                    if (form.checkValidity() === false) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add("was-validated");
                },
                false
            );
        });
    }

    $(window).on('load',function(){
        formValidations();
    });

    // Ajax
    $(document).ajaxStart(function() {
        $("#processing").delay(1000).fadeIn(1000).show(0);
        // console.log('aJax Start');
    });

    $(document).ajaxStop(function() {
        $("#processing").delay(1000).fadeOut(1000).hide(0);
        // console.log('aJax Stop');
    });

    $(document).ajaxSuccess(function() {
        // $('#processing').hide();
    });

    $(document).ajaxComplete(function() {
        // $('#processing').hide();
        formValidations();
    });

    $(document).ajaxError(function() {
        // console.log('aJax Error');
        $("#processing").hide();
    });

    $.ajaxSetup({
        cache: false
    });

    $('[data-toggle="tooltip"]').tooltip();

    $('[data-toggle="popover"]').popover();

    //window.history.go(-1);

    $('.nav a.dropdown-item').click(function (e) {
        //get selected href
        var href = $(this).attr('href');

        // Show tab for all tabs that match href
        $('.nav a.dropdown-item[href="' + href + '"]').tab('show');
    });

    // Set main active tab
    $('a[data-toggle="pill"]').on('shown.bs.tab', function (e) {
        localStorage.setItem('activeTab', $(e.target).attr('href'));
    });

    var activeTab = localStorage.getItem('activeTab');
    if(activeTab){
        $('#v-pills-tab a[href="' + activeTab + '"]').tab('show');
	}

    // Set secondary active tab
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        localStorage.setItem('activeTab2', $(e.target).attr('href'));
    });

    var activeTab2 = localStorage.getItem('activeTab2');
    if(activeTab){
        $('#clusterTabs a[href="' + activeTab2 + '"]').tab('show');
	}

    // Accordion get saved data from sessionStorage
    let selectedCollapse = sessionStorage.getItem('selectedCollapse');
    if(selectedCollapse != null) {
        $('.accordion .collapse').removeClass('show');
        $(selectedCollapse).addClass('show');
    }
    // To set, which one will be opened
    $('.accordion .btn-link').on('click', function(){
        let target = $(this).data('target');
        //Save data to sessionStorage
        sessionStorage.setItem('selectedCollapse', target);
    });

    // Remove spaces
    $(document).on("keyup","#brand",function(e){
        $(this).val($(this).val().replace(/\s/g, ""));
    });

    // Toggle state for Terminal
    var $modal, $apnData, $modalCon;

    // Retrieve current state
    $("#terminal").toggleClass(localStorage.minimizeClick);
    $("#main-container").addClass(localStorage.minimizePad);

    $(document).on("click",".modalMinimize",function(e){
        $modalCon = $(this).closest("#terminal").attr("id");
        $apnData = $(this).closest("#terminal");
        $modal = "#" + $modalCon;
        $($modal).toggleClass("modal-min");
        if ($($modal).hasClass("modal-min")) {
            $(this).find("i").toggleClass("fa-minus").toggleClass("fa-clone");
            $("#main-container").addClass("modal-minimized");
            localStorage.minimizeClick = "modal-min";
            localStorage.minimizePad = "modal-minimized";
        } else {
            $(this).find("i").toggleClass("fa-clone").toggleClass("fa-minus");
            $("#main-container").removeClass("modal-minimized");
            localStorage.minimizeClick = "";
            localStorage.minimizePad = "";
        }
    });

    $("button[data-dismiss='modal']").click(function() {
        $(this).closest("#terminal").removeClass("modal-min");
        $("#main-container").removeClass($apnData);
        $(this).next(".modalMinimize").find("i").removeClass("fa fa-clone").addClass("fa fa-minus");
    });

    // Toasts
    $.toast = function(c) {
        $("#toasts-holder").length || ($("body").append('<div id="toasts-holder" aria-live="polite" aria-atomic="true"></div>'), $("#toasts-holder").append('<div id="toast-holder"></div>'), $("body").on("hidden.bs.toast", ".toast", function() {
            $(this).remove();
        }));
        e = c.autohide || "true",
        f = c.delay || 5000;
        a = '<div class="toast toast-new" role="alert" aria-live="assertive" data-autohide="'+e+'" aria-atomic="true" data-delay="'+f+'"></div>';
        $("#toast-holder").append(a);
        $("#toast-holder .toast:last").toast("show");
    };

    $('#modalForm1').submit(function() {
        var $f = $('#modalForm1');
        var $url = "view_log.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal-xl").find('.modal-body').html(result)
            $("#myModal-xl").modal('show');
        }});
    });

    $('#toastForm2').submit(function() {
        var $f = $('#toastForm2');
        var $url = "save_app_settings.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myToastback").find('.toast-body').html(result)
            $("#myToastback").toast('show');
        }});
    });

    $('#toastForm3').submit(function() {
        var $f = $('#toastForm3');
        var $url = "save_app_extra_settings.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myToast").find('.toast-body').html(result)
            $("#myToast").toast('show');
        }});
    });

    $('#toastForm4').submit(function() {
        var $f = $('#toastForm4');
        var $url = "reload_config.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myToast").find('.toast-body').html(result)
            $("#myToast").toast('show');
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

    $('#toastForm6').submit(function() {
        var $f = $('#toastForm6');
        var $url = "save_app_extra_settings.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myToast").find('.toast-body').html(result)
            $("#myToast").toast('show');
        }});
    });

    $('.toastForm7-wrap').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "subdir_delete.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myToast").find('.toast-body').html(result)
            $("#myToast").toast('show');
        }});
    });

    $('#toastForm8').submit(function() {
        var $f = $('#toastForm8');
        var $url = "subdir_save_app_settings.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myToastback").find('.toast-body').html(result)
            $("#myToastback").toast('show');
        }});
    });

    $('#toastForm9').submit(function() {
        var $f = $('#toastForm9');
        var $url = "autoswitch.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myToast-nl").find('.toast-body').html(result)
            $("#myToast-nl").toast('show');
        }});
    });

    $('#modalForm10').submit(function() {
        var $f = $('#modalForm10');
        var $url = "dependency_installer.live.py?" + $f.serialize();
        $.ajax({url: $url, success: function(result){
            $("#myModal").find('.modal-body').html(result)
            $("#myModal").modal('show');
        }});
    });

});
