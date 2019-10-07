"use strict";
$(document).ready(function () {

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

    $('#hidebackdrop').on('click', function () {
        if ($(this).is(':checked') === true) {
            $('.settings-sidebar-backdrop').fadeOut();
            $('#settingalert').show();
        } else {
            $('.settings-sidebar-backdrop').fadeIn();
            $('#settingalert').hide();
        }
    });

    $.cookie("themecolor", $('#theme').attr('href'), {
        expires: 1
    });

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
    if ($.type($.cookie("stylesheetname")) != 'css/dark-grey.css' && $.cookie("stylesheetname") != 'css/dark-grey.css') {
        $('#darktheme').prop("checked", false);
    } else {
        $('#darktheme').prop("checked", true);
    }

    $('#darktheme').on('click', function () {
        if ($(this).is(':checked')) {
            var stylesheetname = "css/dark-grey.css";
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
            var stylesheetname = "css/style.css";
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

        var stylesheetname = "css/" + $(this).next().attr('data-title') + $.cookie("headerfill") + $.cookie("sidebarfill") + ".css";
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



    if ($.type($.cookie("sidebarimgrepeat")) != 'undefined' && $.cookie("sidebarimgrepeat") != '') {
        $('body .wrapper > .sidebar').css({
            'background-image': 'url(' + $.cookie("sidebarimgrepeat") + ')',
            'background-repeat': 'repeat',
            'background-size': 'auto'
        });
        $('.sidebar-image input[type="radio"]').prop("checked", false);
        $("label[data-title='" + $.cookie("sidebarimgrepeat") + "']").prev().prop("checked", true);
    }
    if ($.type($.cookie("sidebarimg")) != 'undefined' && $.cookie("sidebarimg") != '') {
        $('body .wrapper > .sidebar').css({
            'background-image': 'url(' + $.cookie("sidebarimg") + ')',
            'background-repeat': 'no-repeat',
            'background-size': '100%'
        });
        $('.sidebar-image input[type="radio"]').prop("checked", false);
        $("label[data-title='" + $.cookie("sidebarimg") + "']").prev().prop("checked", true);
    }

    $('.sidebar-image input[type="radio"]').on('click', function () {
        if ($(this).hasClass('bg-repeat') === true) {
            $.cookie("sidebarimgrepeat", $(this).next().attr('data-title'), {
                expires: 7
            });
            $.removeCookie('sidebarimg', {
                path: '/'
            });
            $('body .wrapper > .sidebar').css({
                'background-image': 'url(' + $(this).next().attr('data-title') + ')',
                'background-repeat': 'repeat',
                'background-size': 'auto'
            });
        } else {
            $.cookie("sidebarimg", $(this).next().attr('data-title'), {
                expires: 7
            });
            $.removeCookie('sidebarimgrepeat', {
                path: '/'
            });
            $('body .wrapper > .sidebar').css({
                'background-image': 'url(' + $(this).next().attr('data-title') + ')',
                'background-repeat': 'no-repeat',
                'background-size': '100%'
            });
        }
    });

    /* RTL layout */
    if ($.type($.cookie("rtl-layout")) != 'undefined' && $.cookie("rtl-layout") != '') {
        $('#rtl').prop("checked", true);
        $('body').addClass($.cookie("rtl-layout"));
    }

    $('#rtl').on('click', function () {
        if ($(this).is(':checked')) {
            $('body').addClass('rtl');
            $.cookie("rtl-layout", "rtl", {
                expires: 1
            });
        } else {
            $('body').removeClass('rtl');
            $.cookie("rtl-layout", "", {
                expires: 1
            });
            $.removeCookie('rtl-layout');
        }
    })

    /* RTL layout */
    if ($.type($.cookie("iconsibarbar-layout")) != 'undefined' && $.cookie("iconsibarbar-layout") != '') {
        $('#iconsibarbar').prop("checked", true);
        $('body').addClass($.cookie("iconsibarbar-layout"));
    }

    $('#iconsibarbar').on('click', function () {
        if ($(this).is(':checked')) {
            $('body').addClass('iconsibarbar sidebar-left-close');
            $.cookie("iconsibarbar-layout", "iconsibarbar", {
                expires: 1
            });
        } else {
            $('body').removeClass('iconsibarbar');
            $.cookie("iconsibarbar-layout", "", {
                expires: 1
            });
            $.removeCookie('iconsibarbar-layout');
        }
    });

});

$(window).on('load', function () {
    /* hide loader  */
    $('.loader').hide();
    $('.animatejack').addClass('jackInTheBox');
    $('.wrapper').css('padding-bottom', $('body > footer').outerHeight() );
    $('body > footer').css('margin-top', -( $('body > footer').outerHeight() ));
});
