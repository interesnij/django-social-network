"use strict";
$(document).ready(function () {
    /* hide loader if 3sec or more time */
    setTimeout(function () {
        $(".loader-logo").fadeOut();
    }, 3000);

    /* left sidebar open */
    $('#left-menu').on('click', function () {
        $('body').toggleClass('sidebar-left-close');
    });
    $('.sidebar-left + div.backdrop').on('click', function () {
        $('body').addClass('sidebar-left-close');
    });

    /* right sidebar open */
    $('#open-right-sidebar, #opencolorpanel').on('click', function () {
        $('body').toggleClass('sidebar-right-close');
        $('.chat-window').hide();
        $('.close-sidebar').toggleClass('active');
        $('body').addClass('sidebar-left-close');
    });

    /* right sidebar open  with setting icon on right side */
    $('.close-sidebar').on('click', function () {
        $(this).toggleClass('active');
        $('.chat-window').hide();
        $('body').toggleClass('sidebar-right-close');
    });


    /* left sidebar accordion menu */
    /* url  navigation active */
    var url = window.location;

    function menuitems() {
        var element = $('.sidebar .nav .nav-item a').filter(function () {
            return this.href == url;
            console.log(url)
        }).addClass('active').parent("li").addClass('active').closest('.nav').slideDown().addClass('in').prev().addClass('active').parent().addClass('show').closest('.nav').slideDown().addClass('in').parent().addClass('show');
    }
    menuitems();

    $('.sidebar .nav .nav-item .dropdwown-toggle').on('click', function () {
        if ($(this).hasClass('active') != true) {
            $('.sidebar .nav .nav-item .dropdwown-toggle').removeClass('active').next().slideUp();
            $(this).addClass('active').next().slideDown();
        } else {
            $(this).removeClass('active').next().slideUp();
        }
    });

    /* new message hide color */
    $('.new').on('click', function () {
        var itemnew = $(this);
        setTimeout(function () {
            itemnew.removeClass('new');
        }, 500);
    });


    /* sidebar hide below 1100px resolution  */
    if ($(window).width() <= 1100) {
        $('body').addClass('sidebar-left-close');
    }

    /* accessiblity font size change  */
    var fontsize = 16;
    $('.font-big').on('click', function () {
        fontsize = fontsize + 1;
        if (fontsize < 20) {
            $('body').css('font-size', fontsize);
            $('.font-small').attr('disabled', false);
        } else {
            $(this).attr('disabled', 'disabled');
        }
    });
    $('.font-small').on('click', function () {
        fontsize = fontsize - 1;
        if (fontsize > 13) {
            $('body').css('font-size', fontsize);
            $('.font-big').attr('disabled', false);
        } else {
            $(this).attr('disabled', 'disabled');
        }

    });


    /* flip color setting block*/
    function setIntervalX(callback, delay, repetitions) {
        var x = 0;
        var intervalID = window.setInterval(function () {
            callback();
            if (++x === repetitions) {
                window.clearInterval(intervalID);
            }
        }, delay);
    }
    setIntervalX(function () {
        $('.animateflipy').addClass('flipInY');
        setTimeout(function () {
            $('.animateflipy').removeClass('flipInY');
        }, 1000)
    }, 2000, 3);

    /* fullscreen feature */
    $('.fullscreenbtn').on('click', function () {
        $(this).closest('.fullscreen').toggleClass('activefullscreen')
    });

    /* settings sidebar backdrop close */
    $('.settings-sidebar-backdrop').on('click', function () {
        $(this).fadeOut().prev('.settings-sidebar').addClass('close-settings-sidebar-backdrop')
        $('.close-setting-sidebar').removeClass('active')
        $('body').removeClass('setting-sidebar-open');
    });
    $('.close-setting-sidebar').on('click', function () {
        if ($(this).hasClass('active') === true) {
            $('.settings-sidebar').addClass('close-settings-sidebar-backdrop')
            $(this).removeClass('active');
            $('body').removeClass('setting-sidebar-open');
            $('.settings-sidebar-backdrop').fadeOut();
        } else {
            $('.settings-sidebar').removeClass('close-settings-sidebar-backdrop')
            $(this).addClass('active');
            $('body').addClass('setting-sidebar-open');
            if ($('#hidebackdrop').is(':checked') != true) {
                $('.settings-sidebar-backdrop').fadeIn()
            }
        }
    });
    $('#hidebackdrop').on('click', function () {
        if ($(this).is(':checked') === true) {
            $('.settings-sidebar-backdrop').fadeOut();
            $('#settingalert').show();
        } else {
            $('.settings-sidebar-backdrop').fadeIn();
            $('#settingalert').hide();
        }
    });


    /* full container active */
    $('#boxlayout').on('click', function () {
        if ($(this).is(':checked') === true) {
            $('body').addClass('boxed-page sidebar-left-close');
        } else {
            $('body').removeClass('boxed-page sidebar-left-close');
        }
    });

    /* full container active */
    $('#full-width3').on('click', function () {
        if ($(this).is(':checked') === true) {
            $('#full-width2').prop('checked', true);
            $('.main-container').addClass('container-fluid').removeClass('container');
        } else {
            $('#full-width2').prop('checked', false);
            $('.main-container').removeClass('container-fluid').addClass('container');
        }
    });
    $('#full-width2').on('click', function () {
        if ($(this).is(':checked') === true) {
            $('#full-width3').prop('checked', true);
            $('.main-container').addClass('container-fluid').removeClass('container');
        } else {
            $('#full-width3').prop('checked', false);
            $('.main-container').removeClass('container-fluid').addClass('container');
        }
    });

    /* chat window minimize */
    $('.chat-minmax').on('click', function () {
        $(this).closest('.chat-window').toggleClass('active');
        $(this).toggleClass('active');
    });
    $('.chat-close').on('click', function () {
        $(this).closest('.chat-window').hide();
    });
    $('#chat-list .list-group-item').on('click', function () {
        $('.chat-minmax, .chat-window').addClass('active');
        $('.chat-window').show();
    });

    if ($('body').hasClass('boxed-page') === true) {
        $('body').addClass('sidebar-left-close');
    }



    /* theme selection and image background script*/
    $("#customRadio32img").prop('checked', true);
    $('body .wrapper > .sidebar').css({
        'background-image': 'url(img/sidebar-2.png)',
        'background-repeat': 'no-repeat',
        'background-size': 'auto'
    });

    $.cookie("themecolor", $('#theme').attr('href'), {
        expires: 1
    });

    /* sidebar fill checkbox check state */
    if ($.type($.cookie("sidebarfill")) != 'undefined' && $.cookie("sidebarfill") != '') {
        $('#sidebarfill').prop("checked", true);
    } else {
        $('#sidebarfill').prop("checked", false);
        $.cookie("sidebarfill", "", {
            expires: 1
        });
    }
    $('#sidebarfill').on('click', function () {
        $('.theme-color input[type="radio"]').prop("checked", false);
        if ($(this).is(':checked')) {
            $('#fullcolorfill').prop("checked", false);
            $.cookie("fullcolorfill", "", {
                expires: 1
            });

            $.cookie("sidebarfill", "sidebar", {
                expires: 1
            });
        } else {
            $.cookie("sidebarfill", "", {
                expires: 1
            });
        }
    });

    /* header fill checkbox check state */
    if ($.type($.cookie("headerfill")) != 'undefined' && $.cookie("headerfill") != '') {
        $('#headerfill').prop("checked", true);
    } else {
        $('#headerfill').prop("checked", false);
        $.cookie("headerfill", "", {
            expires: 1
        });
    }
    $('#headerfill').on('click', function () {
        $('.theme-color input[type="radio"]').prop("checked", false);
        if ($(this).is(':checked')) {
            $('#fullcolorfill').prop("checked", false);
            $.cookie("fullcolorfill", "", {
                expires: 1
            });

            $.cookie("headerfill", "header", {
                expires: 1
            });
        } else {
            $.cookie("headerfill", "", {
                expires: 7
            });
        }
    });

    /* full body fill checkbox check state */
    if ($.type($.cookie("fullcolorfill")) != 'undefined' && $.cookie("fullcolorfill") != '') {
        $('#fullcolorfill').prop("checked", true);
    } else {
        $('#fullcolorfill').prop("checked", false);
        $.cookie("fullcolorfill", "", {
            expires: 1
        });
    }
    $('#fullcolorfill').on('click', function () {
        $('.theme-color input[type="radio"]').prop("checked", false);
        if ($(this).is(':checked')) {
            $('#headerfill').prop("checked", false);
            $('#sidebarfill').prop("checked", false);
            $.cookie("headerfill", "", {
                expires: 7
            });
            $.cookie("sidebarfill", "", {
                expires: 1
            });

            $.cookie("fullcolorfill", "full", {
                expires: 1
            });
        } else {
            $.cookie("fullcolorfill", "", {
                expires: 1
            });
        }
    });
    if ($.type($.cookie("stylesheetname")) != 'undefined' && $.cookie("stylesheetname") != '') {
        var linkurl = $('#theme')
        $('head').append("<link id='theme' rel='stylesheet' href='" + $.cookie("stylesheetname") + "' type='text/css'>");
        $('.theme-color input[type="radio"]').prop("checked", false);
        $("label[data-title='" + $.cookie("themecolor") + "']").prev().prop("checked", true);
        setTimeout(function () {
            linkurl.remove();
        }, 1500);
    }
    if ($.type($.cookie("stylesheetname")) != '/static/styles/color/dark-grey.css' && $.cookie("stylesheetname") != '/static/styles/color/dark-grey.css') {
        $('#darktheme').prop("checked", false);
    } else {
        $('#darktheme').prop("checked", true);
    }

    $('#darktheme').on('click', function () {
        if ($(this).is(':checked')) {
            var stylesheetname = "/static/styles/color/dark-grey.css";
            $.cookie("stylesheetname", stylesheetname, {
                expires: 7
            });
            var linkurl = $('#theme')
            $('head').append("<link id='theme' rel='stylesheet' href='" + stylesheetname + "' type='text/css'>");

            $(".loader-logo").show();
            setTimeout(function () {
                $(".loader-logo").fadeOut();
                linkurl.remove();
            }, 1500);
        } else {
            var stylesheetname = "/static/styles/color/style.css";
            $.cookie("stylesheetname", stylesheetname, {
                expires: 7
            });
            var linkurl = $('#theme')
            $('head').append("<link id='theme' rel='stylesheet' href='" + stylesheetname + "' type='text/css'>");

            $(".loader-logo").show();
            setTimeout(function () {
                $(".loader-logo").fadeOut();
                linkurl.remove();
            }, 1500);
        }
    });
    $('.theme-color input[type="radio"]').on('click', function () {
        $.cookie("themecolor", $(this).next().attr('data-title'), {
            expires: 7
        });

        var stylesheetname = "/static/styles/color/" + $(this).next().attr('data-title') + $.cookie("headerfill") + $.cookie("sidebarfill") + ".css";
        $.cookie("stylesheetname", stylesheetname, {
            expires: 7
        });
        var linkurl = $('#theme')
        $('head').append("<link id='theme' rel='stylesheet' href='" + stylesheetname + "' type='text/css'>");

        $(".loader-logo").show();
        setTimeout(function () {
            $(".loader-logo").fadeOut();
            linkurl.remove();
        }, 1500);
    });

});

$(window).on('load', function () {
    /* hide loader  */
    $('.loader').hide();
    $('.animatejack').addClass('jackInTheBox');
    $('.wrapper').css('padding-bottom', $('body > footer').outerHeight() );
    $('body > footer').css('margin-top', -( $('body > footer').outerHeight() ));
});
