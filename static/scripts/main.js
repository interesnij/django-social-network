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
        $(this).closest('.fullscreen').toggleClass('activefullscreen');
        $('body').toggleClass('body-activefullscreen');
    });


    /* full container active */
    $('#boxlayout').on('click', function () {
        if ($(this).is(':checked') === true) {
            $('body').addClass('boxed-page sidebar-left-close');
        } else {
            $('body').removeClass('boxed-page sidebar-left-close');
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

    $.cookie("themecolor", $('#theme').attr('href'), {
        expires: 1
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
    });

});

/* swiper control */
var mySwiper = new Swiper('.swiper-story', {
    slidesPerView: 'auto',
    centeredSlides: false,
    spaceBetween: 15
});
var mySwiper2 = new Swiper('.swiper-post', {
    slidesPerView: 'auto',
    centeredSlides: false,
    spaceBetween: 1,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
});

$(document).ready(function(){
    /* photos gallery */
    $('.grid').masonry({
         itemSelector: '.grid-item',
         percentPosition: true
    });


});
$(window).on("load resize", function () {
     $('.grid').masonry({
         itemSelector: '.grid-item',
         percentPosition: true
     });
 });


$(window).on('load', function () {
    /* hide loader  */
    $('.loader').hide();
    $('.animatejack').addClass('jackInTheBox');
    $('.wrapper').css('padding-bottom', $('body > footer').outerHeight() );
    $('body > footer').css('margin-top', -( $('body > footer').outerHeight() ));
});
