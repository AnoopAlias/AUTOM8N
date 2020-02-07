jQuery(document).ready(function($) {

    // Full URL for ajax load including params
    var $urlparam      = window.location.href;

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
    });

    // Ajax
    $(document).ajaxStart(function() {
        $("#processing").delay(1000).fadeIn(1000).show(0);
        // console.log('aJax Start');
    });

    $(document).ajaxStop(function() {
        $("#processing").delay(1000).fadeOut(1000).hide(0);
        termBottom();
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
            $("#main-container").addClass("modal-minimized");
            localStorage.minimizeClick = "modal-min";
            localStorage.minimizePad = "modal-minimized";
        } else {
            $("#main-container").removeClass("modal-minimized");
            localStorage.minimizeClick = "";
            localStorage.minimizePad = "";
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
        a = '<div class="toast toast-new" role="alert" aria-live="assertive" data-autohide="'+e+'" aria-atomic="true" data-delay="'+f+'"></div>';
        $("#toast-holder").append(a);
        $("#toast-holder .toast:last").toast("show");
    };

    // Forms
    $(document).on("submit","#ddos_protection_nginx_enable",function(e){
        var $loaderId        =   "#ddos-protection-nginx-enable-btn";
        var $loaderText      =   "Enabling...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "ddos_mitigate.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-dos .card-body > .no-gutters").load(($urlparam) + " #v-pills-dos .card-body > .no-gutters > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on('submit','#ddos_protection_nginx_disable',function(e){
        var $loaderId        =   '#ddos-protection-nginx-disable-btn';
        var $loaderText      =   'Disabling...';
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "ddos_mitigate.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-dos .card-body > .no-gutters").load(($urlparam) + " #v-pills-dos .card-body > .no-gutters > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on('submit','#ddos_protection_synproxy_enable',function(e){
        var $loaderId        =   '#ddos-protection-synproxy-enable-btn';
        var $loaderText      =   'Enabling...';
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "firehol_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-dos .card-body > .no-gutters").load(($urlparam) + " #v-pills-dos .card-body > .no-gutters > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#ddos_protection_synproxy_disable",function(e){
        var $loaderId        =   "#ddos-protection-synproxy-disable-btn";
        var $loaderText      =   "Disabling...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "firehol_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-dos .card-body > .no-gutters").load(($urlparam) + " #v-pills-dos .card-body > .no-gutters > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#cluster_soft_restart",function(e){
        var $loaderId        =   "#cluster-soft-restart-btn";
        var $loaderText      =   "Resetting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "fix_unison.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#cluster-status-info").load(($urlparam) + " #cluster-status-info > *");
                $("#cluster-reset-btns").load(($urlparam) + " #cluster-reset-btns > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#cluster_hard_reset",function(e){
        var $loaderId        =   "#cluster-hard-reset-btn";
        var $loaderText      =   "Resetting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "fix_unison.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#cluster-status-info").load(($urlparam) + " #cluster-status-info > *");
                $("#cluster-reset-btns").load(($urlparam) + " #cluster-reset-btns > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#cluster_csync2_reset",function(e){
        var $loaderId        =   "#cluster-csync2-reset-btn";
        var $loaderText      =   "Resetting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "fix_csync2.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result){
                $("#cluster-status-info").load(($urlparam) + " #cluster-status-info > *");
                $("#cluster-reset-btns").load(($urlparam) + " #cluster-reset-btns > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#default_php_autoswitch",function(e){
        var $loaderId        =   "#default-php-autoswitch-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "set_default_php.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#autoswitch-php-status").load(($urlparam) + " #autoswitch-php-status > *");
                $("#default_php_autoswitch").load(($urlparam) + " #default_php_autoswitch > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#sync_geodns_zone",function(e){
        var $loaderId        =   "#sync-geodns-zone-btn";
        var $loaderText      =   "Syncing...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "sync_gdnsd_zone.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-zone #sync_geodns_zone").load(($urlparam) + " #v-pills-zone #sync_geodns_zone > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#package_lock_disable",function(e){
        var $loaderId        =   "#package-lock-disable-btn";
        var $loaderText      =   "Disabling...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "lock_domain_data_to_package.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-map .card-body > .no-gutters").load(($urlparam) + " #v-pills-map .card-body > .no-gutters > *");
                $($loaderId).html('Enable');
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#package_lock_enable",function(e){
        var $loaderId        =   "#package-lock-enable-btn";
        var $loaderText      =   "Enabling...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "lock_domain_data_to_package.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-map .card-body > .no-gutters").load(($urlparam) + " #v-pills-map .card-body > .no-gutters > *");
                $($loaderId).html('Disable');
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#nginx_status",function(e){
        var $loaderId        =   "#nginx-status-btn";
        var $loaderText      =   "Reloading...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#nginx_status_widget").load(($urlparam) + " #nginx_status_widget > *");
                $($loaderId).html("Reload");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#watcher_status",function(e){
        var $loaderId        =   "#watcher-status-btn";
        var $loaderText      =   "Restarting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#watcher_status_widget").load(($urlparam) + " #watcher_status_widget > *");
                $($loaderId).html("Restart");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#clear_caches",function(e){
        var $loaderId        =   "#clear-caches-btn";
        var $loaderText      =   "Flushing...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#clear_caches_widget").load(($urlparam) + " #clear_caches_widget > *");
                $($loaderId).html('Flush All');
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#restart_backends",function(e){
        var $loaderId        =   "#restart-backends-btn";
        var $loaderText      =   "Restarting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#restart_backends_widget").load(($urlparam) + " #restart_backends_widget > *");
                $($loaderId).html("Restart");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#sync_web_files",function(e){
        var $loaderId        =   "#sync-web-files-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "sync_docroots.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-zone #sync_web_files").load(($urlparam) + "#v-pills-zone #sync_web_files > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#cluster_setup",function(e){
        var $loaderId        =   "#cluster-setup-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $.toast({
                    autohide: 'true',
                });
                $("#v-pills-cluster .card-body").load(($urlparam) + " #v-pills-cluster .card-body > *");
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","form[id^='delete_cluster_settings_directory-']",function(e){
        var $loaderId        =   $(this).find('button');
        var $loaderText      =   "Deleting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#home-content").load(($urlparam) + " #home-content > *");
                $("#cluster-status-info").load(($urlparam) + " #cluster-status-info > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#save_cluster_settings_directory",function(e){
        var $loaderId        =   "#save-cluster-settings-directory-btn";
        var $loaderText      =   "Adding...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#home-content").load(($urlparam) + " #home-content > *");
                $("#cluster-status-info").load(($urlparam) + " #cluster-status-info > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#deploy_playbook",function(e){
        var $loaderId        =   "#run-playbook-btn";
        var $loaderText      =   "Executing Cluster Setup Playbook...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#playbook-content").load(($urlparam) + " #playbook-content > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#save_cluster_settings_master",function(e){
        var $loaderId        =   "#save-cluster-settings-master-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#master-content").load(($urlparam) + " #master-content > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#save_cluster_settings_slave",function(e){
        var $loaderId        =   "#save-cluster-settings-slave-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#slave-content").load(($urlparam) + " #slave-content > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","form[id^='edit_ip_resource-']",function(e){
        var $loaderId        =   $(this).find('button');
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#ip-content").load(($urlparam) + " #ip-content > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#add_ip",function(e){
        var $loaderId        =   "#add-ip-btn";
        var $loaderText      =   "Adding...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#ip-add-content").load(($urlparam) + " #ip-add-content > *");
                $("#ip-content").load(($urlparam) + " #ip-content > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","form[id^='delete_ip-']",function(e){
        var $loaderId        =   $(this).find('button');
        var $loaderText      =   "Deleting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#ip-content").load(($urlparam) + " #ip-content > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#save_cluster_settings_addi_slave_add",function(e){
        var $loaderId        =   "#save-cluster-settings-addi-slave-add-btn";
        var $loaderText      =   "Adding...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#add-content").load(($urlparam) + " #add-content > *");
                $("#slave-content").load(($urlparam) + " #slave-content > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","form[id^='save_cluster_settings_slave_add-']",function(e){
        var $formId          =   $(this).attr('id');
        var $loaderId        =   '#save-cluster-settings-slave-add-btn-'+$formId.split('-')[1];
        var $loaderText      =   "Updating Slave";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#add-content").load(($urlparam) + " #add-content > *");
                $("#slave-content").load(($urlparam) + " #slave-content > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","form[id^='delete_cluster_settings_slave-']",function(e){
        var $formId          =   $(this).attr('id');
        var $loaderId        =   '#delete-cluster-settings-slave-btn-'+$formId.split('-')[1];
        var $loaderText      =   "Deleting Slave";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#slave-content").load(($urlparam) + " #slave-content > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#ndeploy_control_branding",function(e){
        var $loaderId        =   "#ndeploy-control-branding-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_ndeploy_branding_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
                window.location.reload();
            }
        });
    });

    $(document).on("submit","#restore_branding_defaults",function(e){
        var $loaderId        =   "#restore-branding-defaults-btn";
        var $loaderText      =   "Reverting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "restore_branding_defaults.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
                window.location.reload();
            }
        });
    });

    $(document).on("submit","#ndeploy_control_config",function(e){
        var $loaderId        =   "#ndeploy-control-config-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_ndeploy_control_config.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
                window.location.reload();
            }
        });
    });

    $(document).on("submit","#restore_ndeploy_control_defaults",function(e){
        var $loaderId        =   "#restore-ndeploy-control-defaults-btn";
        var $loaderText      =   "Reverting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "restore_ndeploy_control_defaults.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
                window.location.reload();
            }
        });
    });

    $(document).on("submit","#easy_php_setup",function(e){
        var $loaderId        =   "#easy-php-setup-btn";
        var $loaderText      =   "Upgrading...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "easy_php_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#php_status_widget").load(($urlparam) + " #php_status_widget > *");
                $("#v-pills-php_backends .card-body > .no-gutters").load(($urlparam) + " #v-pills-php_backends .card-body > .no-gutters > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#easy_netdata_setup",function(e){
        var $loaderId        =   "#easy-netdata-setup-btn";
        var $loaderText      =   "Installing...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "easy_netdata_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-netdata .card-body").load(($urlparam) + " #v-pills-netdata .card-body > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#clear_netdata_credentials",function(e){
        var $loaderId        =   "#clear-netdata-credentials-btn";
        var $loaderText      =   "Clearing...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "easy_netdata_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-netdata .card-body").load(($urlparam) + " #v-pills-netdata .card-body > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#easy_glances_setup",function(e){
        var $loaderId        =   "#easy-glances-setup-btn";
        var $loaderText      =   "Installing...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "easy_glances_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-glances .card-body").load(($urlparam) + " #v-pills-glances .card-body > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#clear_glances_credentials",function(e){
        var $loaderId        =   "#clear-glances-credentials-btn";
        var $loaderText      =   "Clearing...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "easy_glances_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-glances .card-body").load(($urlparam) + " #v-pills-glances .card-body > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#disable_ndeploy",function(e){
        var $loaderId        =   "#plugin-status-btn";
        var $loaderText      =   "Disabling...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "plugin_status.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#plugin_status_widget").load(($urlparam) + " #plugin_status_widget > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#enable_ndeploy",function(e){
        var $loaderId        =   "#plugin-status-btn";
        var $loaderText      =   "Enabling...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "plugin_status.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#plugin_status_widget").load(($urlparam) + " #plugin_status_widget > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#module_installer",function(e){
        var $loaderId        =   "#module-installer-btn";
        var $loaderText      =   "Saving Module Settings...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "module_installer.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-modules .card-body").load(($urlparam) + " #v-pills-modules .card-body > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#autofix_simple",function(e){
        var $loaderId        =   "#autofix-simple-btn";
        var $loaderText      =   "Fixing...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "autofix_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#fix_all_widget").load(($urlparam) + " #fix_all_widget > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#autofix_phpfpm",function(e){
        var $loaderId        =   "#autofix-phpfpm-btn";
        var $loaderText      =   "Fixing...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "autofix_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#fix_all_widget").load(($urlparam) + " #fix_all_widget > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast('show').html(result);
                $(".toast").removeClass('toast-new');
            }
        });
    });

    $(document).on("submit","#check_upgrades",function(e){
        var $loaderId        =   "#upgrade-control-btn";
        var $loaderText      =   "Checking...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "upgrade_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result){
                $("#plugin_upgrade_widget").load(($urlparam) + " #plugin_upgrade_widget > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#reinstall_application",function(e){
        var $loaderId        =   "#reinstall-application-btn";
        var $loaderText      =   "Reinstalling...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "upgrade_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#plugin_upgrade_widget").load(($urlparam) + " #plugin_upgrade_widget > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#upgrade_application",function(e){
        var $loaderId        =   "#upgrade-application-btn";
        var $loaderText      =   "Upgrading...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "upgrade_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#plugin_upgrade_widget").load(($urlparam) + " #plugin_upgrade_widget > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#multi_master",function(e){
        var $loaderId        =   "#multi-master-btn";
        var $loaderText      =   "Updating...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "php_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-php_backends .card-body > .no-gutters").load(($urlparam) + " #v-pills-php_backends .card-body > .no-gutters > *");
                $("#php_status_widget").load(($urlparam) + " #php_status_widget > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#single_master",function(e){
        var $loaderId        =   "#single-master-btn";
        var $loaderText      =   "Updating...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "php_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-php_backends .card-body > .no-gutters").load(($urlparam) + " #v-pills-php_backends .card-body > .no-gutters > *");
                $("#php_status_widget").load(($urlparam) + " #php_status_widget > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#chroot_on",function(e){
        var $loaderId        =   "#chroot-on-btn";
        var $loaderText      =   "Enabling...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "php_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-php_backends .card-body > .no-gutters").load(($urlparam) + " #v-pills-php_backends .card-body > .no-gutters > *");
                $("#php_status_widget").load(($urlparam) + " #php_status_widget > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#chroot_off",function(e){
        var $loaderId        =   "#chroot-off-btn";
        var $loaderText      =   "Disabling...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "php_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-php_backends .card-body > .no-gutters").load(($urlparam) + " #v-pills-php_backends .card-body > .no-gutters > *");
                $("#php_status_widget").load(($urlparam) + " #php_status_widget > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#check_process",function(e){
        var $loaderId        =   "#check_process_btn";
        var $loaderText      =   "Checking...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "abnormal_process_detector.cgi?" + $f.serialize();
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

    $(document).on("submit","#install_borg",function(e){
        var $loaderId        =   "#install_borg_btn";
        var $loaderText      =   "Installing...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "install_borg.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#main-container").load(($urlparam) + " #main-container > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#save_backup_settings",function(e){
        var $loaderId        =   "#save_backup_settings_btn";
        var $loaderText      =   "Saving Backup Settings...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_backup_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
                window.location.reload();
            }
        });
    });

    $(document).on("submit","#borg_add_dir",function(e){
        var $loaderId        =   "#borg_add_dir_btn";
        var $loaderText      =   "Adding...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_borgmatic_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-additional .card-body").load(($urlparam) + " #v-pills-additional .card-body > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","form[id^='borg_rm_dir-']",function(e){
        var $loaderId        =   $(this).find('button');
        var $loaderText      =   "Deleting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_borgmatic_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-additional .card-body").load(($urlparam) + " #v-pills-additional .card-body > *");
                $.toast({
                    autohide: 'true'
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#init_repo",function(e){
        var $loaderId        =   "#init_repo_btn";
        var $loaderText      =   "Initializing...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "install_borg.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-settings .card-body").load(($urlparam) + " #v-pills-settings .card-body > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#save_borg_settings",function(e){
        var $loaderId        =   "#save_borg_settings_btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_borgmatic_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#v-pills-settings .card-body").load(($urlparam) + " #v-pills-settings .card-body > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#borg_unmount_restore_point",function(e){
        var $loaderId        =   "#borg-unmount-restore-point-btn";
        var $loaderText      =   "Unmounting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "borg_restore.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#borg-restore-points").load(($urlparam) + " #borg-restore-points > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit",".borg_mount_restore_point",function(e){
        var $loaderId        =   "#borg-mount-restore-point-btn";
        var $loaderText      =   "Mounting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "borg_restore.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#borg-restore-points").load(($urlparam) + " #borg-restore-points > *");
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
            }
        });
    });

    $(document).on("submit","#cpanel_pkg_profile",function(e){
        var $loaderId        =   ".cpanel-pkg-profile-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_pkg_server_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
                window.location.reload();
            }
        });
    });

    $(document).on("submit","form[id^='php_fpm_pool_editor_save-']",function(e){
        var $formId          =   $(this).attr('id');
        var $loaderId        =   '#php-fpm-pool-editor-save-btn-'+$formId.split('-')[1];
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
                window.location.reload();
            }
        });
    });

    $(document).on("submit","form[id^='php_fpm_pool_editor_delete-']",function(e){
        var $formId          =   $(this).attr('id');
        var $loaderId        =   '#php-fpm-pool-editor-delete-btn-'+$formId.split('-')[1];
        var $loaderText      =   "Deleting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        console.log($id);
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
                window.location.reload();
            }
        });
    });

    $(document).on("submit","#add_php_pool_setting",function(e){
        var $loaderId        =   "#add-php-pool-setting-btn";
        var $loaderText      =   "Adding...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $.toast({
                    autohide: 'true',
                });
                $(".toast-new").toast("show").html(result);
                $(".toast").removeClass("toast-new");
                window.location.reload();
            }
        });
    });

    $(document).on("submit","#save_pkg_app_settings",function(e){
        var $loaderId        =   "#save-pkg-app-settings-btn";
        var $loaderText      =   "Saving...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_pkg_app_settings.cgi?" + $f.serialize();
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

    $(document).on("submit","#set_resource_limit",function(e){
        var $loaderId        =   "#set-resource-limit-btn";
        var $loaderText      =   "Setting...";
        $($loaderId).prop("disabled", true);
        $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $id = e.target.id;
        var $f = $("#" + $id);
        var $url = "save_resource_limit.cgi?" + $f.serialize();
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

});
