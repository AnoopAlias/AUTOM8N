jQuery(document).ready(function($){

    $("#processing").delay(1000).fadeOut(1000).hide(0);
    // Full URL for ajax load including params
    var $urlparam      = window.location.href;

    // #terminal-panel
    var terminalPanel;

    // Force terminal scroll to bottom
    function termBottom() {
        window.terminalPanel = document.getElementById("terminal-panel");
        window.terminalPanel.scrollTop = window.terminalPanel.scrollHeight;
    }

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
        termBottom();
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
        // $("#processing").hide();
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
    var $modal, $modalCon, $apnData;

    // Retrieve current state

    if (localStorage.getItem("minimizeClick" == null )) {
        // $("#terminal").toggleClass(localStorage.minimizeClick);
        localStorage.setItem("minimizeClick", "minimized")
        $("#main-container").addClass("modal-minimized");
        $("#terminal").addClass("modal-min");
    } else {
        localStorage.getItem("minimizeClick")
        if (localStorage.getItem("minimizeClick") == "minimized") {
          $("#main-container").addClass("modal-minimized");
          $("#terminal").addClass("modal-min");
        } else {
          $("#main-container").removeClass("modal-minimized");
          $("#terminal").removeClass("modal-min");
        }
        }

    $(document).on("click",".modalMinimize",function(e){
        $modalCon = $(this).closest("#terminal").attr("id");
        $modal = "#" + $modalCon;
        $apnData = $(this).closest("#terminal");
        $($modal).toggleClass("modal-min");
        if ($($modal).hasClass("modal-min")) {
            $("#main-container").addClass("modal-minimized");
            localStorage.minimizeClick = "minimized";
        } else {
            $("#main-container").removeClass("modal-minimized");
            localStorage.minimizeClick = "maximized";
        }
    });

    $("button[data-dismiss='modal']").click(function() {
        $(this).closest("#terminal").removeClass("modal-min");
        $("#main-container").removeClass($apnData);
    });

    // Toasts
    $.toast = function(c) {
        $("#toasts-holder").length || ($("body").append('<div id="toasts-holder" aria-live="polite" aria-atomic="true"></div>'), $("#toasts-holder").append('<div id="toast-holder"></div>'), $("body").on("hidden.bs.toast", ".toast", function() {
            $(this).remove();
        }));
        e = c.autohide || "true",
        f = c.delay || 5000;
        a = '<div class="toast shadow toast-new" role="alert" aria-live="assertive" data-autohide="'+e+'" aria-atomic="true" data-delay="'+f+'"></div>';
        $("#toast-holder").append(a);
        $("#toast-holder .toast:last").toast("show");
    };

    // Forms
    $(document).on("submit","#app_backend_settings",function(e){
        var $loaderId        =   ".app-backend-settings-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_app_extra_settings.live.py?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                window.location.reload();
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#reload_nginx",function(e){
        var $loaderId        =   "#reload-nginx-btn";
        var $loaderText      =   "Reloading...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "reload_config.live.py?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-system .card-body > .no-gutters").load(($urlparam) + " #v-pills-system .card-body > .no-gutters > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#view_nginx_log",function(e){
        var $loaderId        =   "#view-nginx-log-btn";
        var $loaderText      =   "Loading...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "view_nginx_log.live.py?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                // $("#v-pills-system .card-body > .no-gutters").load(($urlparam) + " #v-pills-system .card-body > .no-gutters > *");
                window.location.reload();
                $.toast({
                    autohide: 'false',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#dependency_installer",function(e){
        var $loaderId        =   "#dependency-installer-btn";
        var $loaderText      =   "Installing...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "dependency_installer.live.py?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                // $("#v-pills-system .card-body > .btn-group").load(($urlparam) + " #v-pills-system .card-body > .btn-group > *");
                window.location.reload();
                $.toast({
                    autohide: 'false',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#view_php_log",function(e){
        var $loaderId        =   "#view-php-log-btn";
        var $loaderText      =   "Loading...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "view_log.live.py?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $.toast({
                    autohide: 'false',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
                window.location.reload();
            }
        });
    });

    $(document).on("submit","#set_upstream_configuration",function(e){
        var $loaderId        =   "#set-upstream-configuration-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_app_settings.live.py?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                window.history.back();
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","form[id^='subdirectory_delete-']",function(e){
        var $formId          =   $(this).attr('id');
        var $loaderId        =   '#subdirectory-delete-btn-'+$formId.split('-')[1];
        var $loaderText      =   "Deleting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "subdir_delete.live.py?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#subdirectory-panel").load(($urlparam) + " #subdirectory-panel > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#subdirectory_set_backend",function(e){
        var $loaderId        =   "#subdirectory-set-backend-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "subdir_save_app_settings.live.py?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                window.history.go(-1);
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#save_subdirectory_app_settings",function(e){
        var $loaderId        =   "#save-subdirectory-app-settings-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_app_extra_settings.live.py?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                window.location.reload();
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#auto_switch_nginx",function(e){
        var $loaderId        =   "#auto-switch-nginx-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "autoswitch.live.py?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $.toast({
                    autohide: 'false',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
                window.location.reload();
            }
        });
    });

    $(document).on("submit","#cluster_file_sync",function(e){
        var $loaderId        =   "#cluster-file-sync-btn";
        var $loaderText      =   "Syncing...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "cluster_filesync.live.py?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $.toast({
                    autohide: 'false',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
                window.location.reload();
            }
        });
    });

});
