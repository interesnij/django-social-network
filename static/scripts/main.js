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

    if ($(window).width() <= 1100) {
        $('body').addClass('sidebar-left-close');
    }
});


  $.ajaxPrefilter(function( options, original_Options, jqXHR ) {options.async = true;});
  $(window).on('load', function () {
      $('.animatejack').addClass('jackInTheBox');
      $('.wrapper').css('padding-bottom', $('body > footer').outerHeight() );
      $('body > footer').css('margin-top', -( $('body > footer').outerHeight() ));
  });
