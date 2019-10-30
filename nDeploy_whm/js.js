jQuery(document).ready(function($) {

    // Are we in Terminal Window?
    var terminalActive;
    
    // Poller
    var terminalUpdate;

    // Load last executed terminal data on reload and scroll to bottom after one second.
    $("#terminal .modal-body").load('term.log');
    setTimeout(function () {
        var terminalWindow = document.getElementById("terminal-panel");
        terminalWindow.scrollTop = terminalWindow.scrollHeight;
        //console.log('Terminal ready after 1 second!');
    }, 1000);

    // Ajax
    $(document).ajaxStart(function() {
        // Terminal log & scroll to bottom
        window.terminalUpdate = setInterval(function() {
            $("#terminal .modal-body").load('term.log');
            window.terminalActive = ($('#terminal-panel:hover').length > 0);
            if (!window.terminalActive) {
                var termWindow = document.getElementById("terminal-panel");
                termWindow.scrollTop = termWindow.scrollHeight;
                //console.log('Mouse not detected in Terminal');
            } else {
                //console.log('Mouse detected in Terminal');
            }
        }, 2000);
        //$('#loader').show();
    });

    $(document).ajaxStop(function() {
        clearInterval(window.terminalUpdate);
        //console.log('aJax Stop');
        //$('#loader').hide();
    });

    $(document).ajaxSuccess(function() {
        //console.log('aJax Success');
        //$('#loader').hide();
    });

    $(document).ajaxComplete(function() {
        //console.log('aJax Complete');
        //$('#loader').hide();
    });

    $(document).ajaxError(function() {
        //console.log('aJax Error');
        //$('#loader').hide();
    });

    $.ajaxSetup({
        cache: false
    });

    $('[data-toggle="tooltip"]').tooltip();

    $('[data-toggle="popover"]').popover();

    // Toasts & modals
    /*$('#myModal').on('hidden.bs.modal', function() {
        location.reload()
    });*/

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

    /*$('#myModal-xl').on('hidden.bs.modal', function() {
        location.reload()
    });

    $('#myModal-xl-shell').on('hidden.bs.modal', function() {
        location.reload()
    });*/

    $('.toast').toast({
        delay: 5000
    })

    $('.nav a.dropdown-item').click(function (e) {
        //get selected href
        var href = $(this).attr('href');

        // Show tab for all tabs that match href
        $('.nav a.dropdown-item[href="' + href + '"]').tab('show');
    })

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
    $(document).on('keyup','#brand',function(e){
        $(this).val($(this).val().replace(/\s/g, ""));
    });

    // Toggle state for Terminal
    var $modal, $apnData, $modalCon;

    // Retrieve current state
    $('#terminal').toggleClass(localStorage.minimizeClick);
    $('#main-container').addClass(localStorage.minimizePad);

    $(document).on('click','.modalMinimize',function(e){
        $modalCon = $(this).closest("#terminal").attr("id");
        $apnData = $(this).closest("#terminal");
        $modal = "#" + $modalCon;
        $($modal).toggleClass("modal-min");
        if ($($modal).hasClass("modal-min")) {
            $(this).find("i").toggleClass('fa-minus').toggleClass('fa-clone');
            $('#main-container').addClass('modal-minimized');
            localStorage.minimizeClick = "modal-min";
            localStorage.minimizePad = "modal-minimized";
        } else {
            $(this).find("i").toggleClass('fa-clone').toggleClass('fa-minus');
            $('#main-container').removeClass('modal-minimized');
            localStorage.minimizeClick = "";
            localStorage.minimizePad = "";
        };
    });

    $("button[data-dismiss='modal']").click(function() {
        $(this).closest("#terminal").removeClass("modal-min");
        $("#main-container").removeClass($apnData);
        $(this).next('.modalMinimize').find("i").removeClass('fa fa-clone').addClass('fa fa-minus');
    });

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
    $(document).on('submit','#ddos_protection_nginx_enable',function(e){
        var $loaderId        =   '#ddos-protection-nginx-enable-btn';
        var $loaderText      =   'Enabling...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "ddos_mitigate.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-dos .card-body > .no-gutters').load('xtendweb.cgi #v-pills-dos .card-body > .no-gutters > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            },
        });
    });

    $(document).on('submit','#ddos_protection_nginx_disable',function(e){
        var $loaderId        =   '#ddos-protection-nginx-disable-btn';
        var $loaderText      =   'Disabling...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "ddos_mitigate.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-dos .card-body > .no-gutters').load('xtendweb.cgi #v-pills-dos .card-body > .no-gutters > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
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

    $(document).on('submit','#default_php_autoswitch',function(e){
        var $loaderId        =   '#default-php-autoswitch-btn';
        var $loaderText      =   'Saving...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "set_default_php.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-php .card-body > .no-gutters').load('xtendweb.cgi #v-pills-php .card-body > .no-gutters > *');
                $($loaderId).html('Set Default PHP');
                $("#myToast-nl").find('.toast-body').html(result);
                $("#myToast-nl").toast('show');
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

    $(document).on('submit','#nginx_status',function(e){
        var $loaderId        =   '#nginx-status-btn';
        var $loaderText      =   'Reloading...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#nginx_status_widget').load('xtendweb.cgi #nginx_status_widget > *');
                $($loaderId).html('Reload');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#watcher_status',function(e){
        var $loaderId        =   '#watcher-status-btn';
        var $loaderText      =   'Restarting...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#watcher_status_widget').load('xtendweb.cgi #watcher_status_widget > *');
                $($loaderId).html('Restart');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#clear_caches',function(e){
        var $loaderId        =   '#clear-caches-btn';
        var $loaderText      =   'Flushing...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#clear_caches_widget').load('xtendweb.cgi #clear_caches_widget > *');
                $($loaderId).html('Flush All');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#restart_backends',function(e){
        var $loaderId        =   '#restart-backends-btn';
        var $loaderText      =   'Restarting...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "daemon_actions.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#restart_backends_widget').load('xtendweb.cgi #restart_backends_widget > *');
                $($loaderId).html('Restart');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
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
        $loaderAnimation;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "save_ndeploy_branding_settings.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-branding .card-body').load('ndeploy_control.cgi #v-pills-branding .card-body > *');
                $('#main-header').load('ndeploy_control.cgi #main-header > *');
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
        $loaderAnimation;
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
        $loaderAnimation;
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
        $loaderAnimation;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "restore_ndeploy_control_defaults.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-aesthetics .card-body').load('ndeploy_control.cgi #v-pills-aesthetics .card-body > *');
                $('#main-header').load('ndeploy_control.cgi #main-header > *');
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
        $loaderAnimation;
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

    $(document).on('submit','#easy_netdata_setup',function(e){
        var $loaderId        =   '#easy-netdata-setup-btn';
        var $loaderText      =   'Installing...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "easy_netdata_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-netdata .card-body').load('ndeploy_control.cgi #v-pills-netdata .card-body > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#clear_netdata_credentials',function(e){
        var $loaderId        =   '#clear-netdata-credentials-btn';
        var $loaderText      =   'Clearing...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "easy_netdata_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-netdata .card-body').load('ndeploy_control.cgi #v-pills-netdata .card-body > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#easy_glances_setup',function(e){
        var $loaderId        =   '#easy-glances-setup-btn';
        var $loaderText      =   'Installing...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "easy_glances_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-glances .card-body').load('ndeploy_control.cgi #v-pills-glances .card-body > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#clear_glances_credentials',function(e){
        var $loaderId        =   '#clear-glances-credentials-btn';
        var $loaderText      =   'Clearing...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "easy_glances_setup.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-glances .card-body').load('ndeploy_control.cgi #v-pills-glances .card-body > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    // ********************************************
    // **************************** Testing Section
    // ********************************************

    $(document).on('submit','#disable_ndeploy',function(e){
        var $loaderId        =   '#plugin-status-btn';
        var $loaderText      =   'Disabling...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation;
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
        var $loaderText      =   'Enabling...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation;
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
        $loaderAnimation;
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
        $loaderAnimation;
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

    $(document).on('submit','#autofix_phpfpm',function(e){
        var $loaderId        =   '#autofix-phpfpm-btn';
        var $loaderText      =   'Fixing...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation;
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
        $loaderAnimation;
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
        $loaderAnimation;
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
        $loaderAnimation;
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

    $(document).on('submit','#multi_master',function(e){
        var $loaderId        =   '#multi-master-btn';
        var $loaderText      =   'Updating...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "php_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-php_backends .card-body > .no-gutters').load('ndeploy_control.cgi #v-pills-php_backends .card-body > .no-gutters > *');
                $('#dash_widget2').load('ndeploy_control.cgi #dash_widget2 > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#single_master',function(e){
        var $loaderId        =   '#single-master-btn';
        var $loaderText      =   'Updating...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "php_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-php_backends .card-body > .no-gutters').load('ndeploy_control.cgi #v-pills-php_backends .card-body > .no-gutters > *');
                $('#dash_widget2').load('ndeploy_control.cgi #dash_widget2 > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#chroot_on',function(e){
        var $loaderId        =   '#chroot-on-btn';
        var $loaderText      =   'Enabling...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "php_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-php_backends .card-body > .no-gutters').load('ndeploy_control.cgi #v-pills-php_backends .card-body > .no-gutters > *');
                $('#dash_widget2').load('ndeploy_control.cgi #dash_widget2 > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

    $(document).on('submit','#chroot_off',function(e){
        var $loaderId        =   '#chroot-off-btn';
        var $loaderText      =   'Disabling...';
        var $loaderDisabled  =   $($loaderId).prop("disabled", true);
        var $loaderSpinner   =   $($loaderId).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;` + $loaderText);
        var $loaderAnimation =   $loaderDisabled + $loaderSpinner;
        $loaderAnimation;
        var $id = e.target.id;
        var $f = $('#' + $id);
        var $url = "php_control.cgi?" + $f.serialize();
        $.ajax({
            url: $url,
            success: function(result) {
                $('#v-pills-php_backends .card-body > .no-gutters').load('ndeploy_control.cgi #v-pills-php_backends .card-body > .no-gutters > *');
                $('#dash_widget2').load('ndeploy_control.cgi #dash_widget2 > *');
                $("#myToast-nl").find('.toast-body').html(result)
                $("#myToast-nl").toast('show');
            }
        });
    });

});
