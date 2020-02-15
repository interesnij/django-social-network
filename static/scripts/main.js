"use strict";
$(document).ready(function () {
    setTimeout(function () {
        $(".loader-logo").fadeOut();
    }, 3000);

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

    $('.new').on('click', function () {
        var itemnew = $(this);
        setTimeout(function () {
            itemnew.removeClass('new');
        }, 500);
    });

    if ($(window).width() <= 1100) {
        $('body').addClass('sidebar-left-close');
    }

});

$(window).on('load', function () {
    $('.animatejack').addClass('jackInTheBox');
    $('.wrapper').css('padding-bottom', $('body > footer').outerHeight() );
    $('body > footer').css('margin-top', -( $('body > footer').outerHeight() ));
});

  $.ajaxPrefilter(function( options, original_Options, jqXHR ) {options.async = true;});
