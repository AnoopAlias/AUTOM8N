jQuery(document).ready(function($) {

    $(document).ajaxStart(function() {
        $('#loader').show();
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
    $('.toast').toast({
        delay: 3000
    })
    $('[data-toggle="tooltip"]').tooltip();

    $('[data-toggle="popover"]').popover();

    $('#toastForm1').submit(function() {
        var $f = $('#toastForm1');
        var $url = "ddos_mitigate.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm2').submit(function() {
        var $f = $('#toastForm2');
        var $url = "firehol_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToastnohide").find('.toast-body').html(result)
                $("#myToastnohide").toast('show');
            }
        });
    });

    $('#toastForm3').submit(function() {
        var $f = $('#toastForm3');
        var $url = "abnormal_process_detector.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#modalForm3').submit(function() {
        var $f = $('#modalForm3');
        var $url = "abnormal_process_detector.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#modalForm4').submit(function() {
        var $f = $('#modalForm4');
        var $url = "install_borg.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#modalForm5').submit(function() {
        var $f = $('#modalForm5');
        var $url = "install_borg.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#toastForm4').submit(function() {
        var $f = $('#toastForm4');
        var $url = "fix_unison.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm5').submit(function() {
        var $f = $('#toastForm5');
        var $url = "fix_unison.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm6').submit(function() {
        var $f = $('#toastForm6');
        var $url = "set_default_php.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm7').submit(function() {
        var $f = $('#toastForm7');
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

    $('#toastForm11').submit(function() {
        var $f = $('#toastForm11');
        var $url = "save_backup_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm12').submit(function() {
        var $f = $('#toastForm12');
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

    $('#toastForm14').submit(function() {
        var $f = $('#toastForm14');
        var $url = "save_borgmatic_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm16').submit(function() {
        var $f = $('#toastForm16');
        var $url = "lock_domain_data_to_package.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm17').submit(function() {
        var $f = $('#toastForm17');
        var $url = "save_pkg_server_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm18').submit(function() {
        var $f = $('#toastForm18');
        var $url = "save_pkg_app_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToastback").find('.toast-body').html(result)
                $("#myToastback").toast('show');
            }
        });
    });

    $('#toastForm19').submit(function() {
        var $f = $('#toastForm19');
        var $url = "save_resource_limit.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm20').submit(function() {
        var $f = $('#toastForm20');
        var $url = "save_phpfpm_pool_file.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm21').submit(function() {
        var $f = $('#toastForm21');
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm22').submit(function() {
        var $f = $('#toastForm22');
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#toastForm23').submit(function() {
        var $f = $('#toastForm23');
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#restart-backends').submit(function() {
        var $f = $('#restart-backends');
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });


    $('#toastForm24').submit(function() {
        var $f = $('#toastForm24');
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

    $('#toastForm26').submit(function() {
        var $f = $('#toastForm26');
        var $url = "fix_csync2.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result){
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#ndeploy_control_branding').submit(function() {
        var $f = $('#ndeploy_control_branding');
        var $url = "save_ndeploy_branding_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#restore_branding_defaults').submit(function() {
        var $f = $('#restore_branding_defaults');
        var $url = "restore_branding_defaults.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#ndeploy_control_config').submit(function() {
        var $f = $('#ndeploy_control_config');
        var $url = "save_ndeploy_control_config.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#restore_ndeploy_control_defaults').submit(function() {
        var $f = $('#restore_ndeploy_control_defaults');
        var $url = "restore_ndeploy_control_defaults.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#easy_php_setup').submit(function() {
        var $f = $('#easy_php_setup');
        var $url = "easy_php_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#easy_netdata_setup').submit(function() {
        var $f = $('#easy_netdata_setup');
        var $url = "easy_netdata_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#clear_netdata_credentials').submit(function() {
        var $f = $('#clear_netdata_credentials');
        var $url = "easy_netdata_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#easy_glances_setup').submit(function() {
        var $f = $('#easy_glances_setup');
        var $url = "easy_glances_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#clear_glances_credentials').submit(function() {
        var $f = $('#clear_glances_credentials');
        var $url = "easy_glances_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myToast").find('.toast-body').html(result)
                $("#myToast").toast('show');
            }
        });
    });

    $('#disable_ndeploy').submit(function() {
        var $f = $('#disable_ndeploy');
        var $url = "plugin_status.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

    $('#enable_ndeploy').submit(function() {
        var $f = $('#enable_ndeploy');
        var $url = "plugin_status.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });
  
    $('#module-installer').submit(function() {
        var $f = $('#module-installer');
        var $url = "module_installer.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $("#myModal-xl").find('.modal-body').html(result)
                $("#myModal-xl").modal('show');
            }
        });
    });

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

    $('.nav a.dropdown-item').click(function (e) {
        //get selected href
        var href = $(this).attr('href');

        // show tab for all tabs that match href
        $('.nav a.dropdown-item[href="' + href + '"]').tab('show');
    })

});
