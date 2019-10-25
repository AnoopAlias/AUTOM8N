jQuery(document).ready(function($) {

    // Ajax
    $(document).ajaxStart(function() {
        //$('#loader').show();
    });

    $(document).ajaxStop(function() {
        $('#loader').hide();
    });

    $(document).ajaxError(function() {
        $('#loader').hide();
    });

    $.ajaxSetup({
        cache: false
    })

    $('[data-toggle="tooltip"]').tooltip();

    $('[data-toggle="popover"]').popover();

    // Toasts & modals
    $('#myModal').on('hidden.bs.modal', function() {
        location.reload()
    });

    $('#myToast').on('hidden.bs.toast', function() {
        location.reload()
    });

    $('#myToastnohide').on('hidden.bs.toast', function() {
        location.reload()
    });

    $('#myModalback').on('hidden.bs.modal', function() {
        window.history.go(-1);
    });

    $('#myToastback').on('hidden.bs.toast', function() {
        window.history.go(-1);
    });

    $('#myModal-xl').on('hidden.bs.modal', function() {
        location.reload()
    });

    /*$('#myModal-xl-shell').on('hidden.bs.modal', function() {
        location.reload()
    });*/

    $('.toast').toast({
        delay: 3000
    })

    $('.nav a.dropdown-item').click(function (e) {
        //get selected href
        var href = $(this).attr('href');

        // Show tab for all tabs that match href
        $('.nav a.dropdown-item[href="' + href + '"]').tab('show');
    })

    // Set active tab
    $('a[data-toggle="pill"]').on('shown.bs.tab', function (e) {
        localStorage.setItem('activeTab', $(e.target).attr('href'));
    });

    var activeTab = localStorage.getItem('activeTab');
    if(activeTab){
        $('#v-pills-tab a[href="' + activeTab + '"]').tab('show');
	}

    // Set active inside tab
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        localStorage.setItem('activeTab2', $(e.target).attr('href'));
    });

    var activeTab2 = localStorage.getItem('activeTab2');
    if(activeTab){
        $('#clusterTabs a[href="' + activeTab2 + '"]').tab('show');
	}

    // Get saved data from sessionStorage
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
    $("#brand").keyup(function() {
        $(this).val($(this).val().replace(/\s/g, ""));
    });

    // We are trying to load data continuously no matter where we are in the app,
    // but let's not force scrolling when user is in terminal
    let termWindow = document.getElementById("terminal");
    let terminalActive = false;
    setInterval(function(){
        terminalActive = ($('#terminal:hover').length > 0);
        if ( !terminalActive ) {
            termWindow.scrollTop = termWindow.scrollHeight;
            $("#terminal").load('term.log');
        } else {
            $("#terminal").load('term.log');
        }
    },100)

    // General Form Validatons
    window.addEventListener('load', function() {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                } else {
                    //var $f = $('#toastForm30');
                    var $url = "save_cluster_settings.cgi?" + $(form).serialize();
                    $.ajax({
                        url: $url,
                        success: function(result) {
                            $("#myToast").find('.toast-body').html(result);
                            $("#myToast").toast('show');
                        }
                    });
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);

    // Forms
    $('#toastForm1').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "ddos_mitigate.cgi?" + $f.serialize();
        //$('#toastForm1').load('xtendweb.cgi #toastForm1 > *');
        //$('#v-pills-dos .card-body').load('xtendweb.cgi #v-pills-dos .card-body > *');
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            },
        });
    });

    $('#toastForm2').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "firehol_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToastnohide").find('.toast-body').html(result)
                $("#myToastnohide").toast('show');
            }
        });
    });

    $('#toastForm3').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "abnormal_process_detector.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#modalForm3').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "abnormal_process_detector.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#modalForm4').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "install_borg.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#modalForm5').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "install_borg.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#toastForm4').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "fix_unison.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm5').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "fix_unison.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm6').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "set_default_php.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm7').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "sync_gdnsd_zone.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $('.toastForm9-wrap').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        console.log($id);
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('.toastForm10-wrap').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm11').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_backup_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm12').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_borgmatic_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('.toastForm13-wrap').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_borgmatic_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm14').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_borgmatic_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm16').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "lock_domain_data_to_package.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm17').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_pkg_server_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm18').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_pkg_app_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToastback").find('.toast-body').html(result)
                $("#myToastback").toast('show');
            }
        });
    });

    $('#toastForm19').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_resource_limit.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm20').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm21').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm22').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm23').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#restart-backends').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm24').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "borg_restore.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('.toastForm25-wrap').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "borg_restore.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm26').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "fix_csync2.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result){
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm27').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "sync_docroots.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $('.toastForm33-wrap').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('.toastForm35-wrap').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('.toastForm37-wrap').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm38').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_cluster_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $(document).on('submit','#ndeploy_control_branding',function(e){
        var $loaderId        =   '#ndeploy-control-branding-btn';
        var $loaderText      =   'Saving...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_ndeploy_branding_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-branding .card-body').load('ndeploy_control.cgi #v-pills-branding .card-body > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#restore_branding_defaults',function(e){
        var $loaderId        =   '#restore-branding-defaults-btn';
        var $loaderText      =   'Reverting...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "restore_branding_defaults.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-branding .card-body').load('ndeploy_control.cgi #v-pills-branding .card-body > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#ndeploy_control_config',function(e){
        var $loaderId        =   '#ndeploy-control-config-btn';
        var $loaderText      =   'Saving...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_ndeploy_control_config.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-branding .card-body').load('ndeploy_control.cgi #v-pills-branding .card-body > *');
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $(document).on('submit','#restore_ndeploy_control_defaults',function(e){
        var $loaderId        =   '#restore-ndeploy-control-defaults-btn';
        var $loaderText      =   'Reverting...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "restore_ndeploy_control_defaults.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-aesthetics .card-body').load('ndeploy_control.cgi #v-pills-aesthetics .card-body > *');
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $(document).on('submit','#easy_php_setup',function(e){
        var $loaderId        =   '#easy-php-setup-btn';
        var $loaderText      =   'Upgrading...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "easy_php_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#dash_widget2').load('ndeploy_control.cgi #dash_widget2 > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $('#easy_netdata_setup').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "easy_netdata_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#clear_netdata_credentials').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "easy_netdata_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#easy_glances_setup').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "easy_glances_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#clear_glances_credentials').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "easy_glances_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    // ********************************************
    // **************************** Testing Section
    // ********************************************

    $(document).on('submit','#disable_ndeploy',function(e){
        var $loaderId        =   '#plugin-status-btn';
        var $loaderText      =   'Saving...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "plugin_status.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#dash_widget1').load('ndeploy_control.cgi #dash_widget1 > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#enable_ndeploy',function(e){
        var $loaderId        =   '#plugin-status-btn';
        var $loaderText      =   'Saving...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "plugin_status.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#dash_widget1').load('ndeploy_control.cgi #dash_widget1 > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    // ********************************************
    // *************************End Testing Section
    // ********************************************


    $(document).on('submit','#module_installer',function(e){
        var $loaderId        =   '#module-installer-btn';
        var $loaderText      =   'Saving Module Settings...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "module_installer.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-modules .card-body').load('ndeploy_control.cgi #v-pills-modules .card-body > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#autofix_simple',function(e){
        var $loaderId        =   '#autofix-simple-btn';
        var $loaderText      =   'Fixing...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "autofix_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#dash_widget3').load('ndeploy_control.cgi #dash_widget3 > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $('#autofix_force').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "autofix_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $(document).on('submit','#autofix_phpfpm',function(e){
        var $loaderId        =   '#autofix-phpfpm-btn';
        var $loaderText      =   'Fixing...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "autofix_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#dash_widget3').load('ndeploy_control.cgi #dash_widget3 > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#check_upgrades',function(e){
        var $loaderId        =   '#upgrade-control-btn';
        var $loaderText      =   'Checking...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "upgrade_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result){
                $('#dash_widget4').load('ndeploy_control.cgi #dash_widget4 > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#reinstall_application',function(e){
        var $loaderId        =   '#reinstall-application-btn';
        var $loaderText      =   'Reinstalling...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "upgrade_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#dash_widget4').load('ndeploy_control.cgi #dash_widget4 > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#upgrade_application',function(e){
        var $loaderId        =   '#upgrade-application-btn';
        var $loaderText      =   'Upgrading...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "upgrade_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#dash_widget4').load('ndeploy_control.cgi #dash_widget4 > *');
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#multi_master').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "php_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#single_master').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "php_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#chroot_on').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "php_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#chroot_off').submit(function(e) {
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "php_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

});
