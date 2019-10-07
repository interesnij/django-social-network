"use strict";

(function (factory) {
	if (typeof define === 'function' && define.amd) {
		define(['jquery'], factory);
	} else if (typeof exports === 'object') {
		factory(require('jquery'));
	} else {
		factory(jQuery);
	}
}(function ($) {

	var pluses = /\+/g;

	function encode(s) {
		return config.raw ? s : encodeURIComponent(s);
	}

	function decode(s) {
		return config.raw ? s : decodeURIComponent(s);
	}

	function stringifyCookieValue(value) {
		return encode(config.json ? JSON.stringify(value) : String(value));
	}

	function parseCookieValue(s) {
		if (s.indexOf('"') === 0) {
			s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
		}
		try {
			s = decodeURIComponent(s.replace(pluses, ' '));
			return config.json ? JSON.parse(s) : s;
		} catch(e) {}
	}

	function read(s, converter) {
		var value = config.raw ? s : parseCookieValue(s);
		return $.isFunction(converter) ? converter(value) : value;
	}

	var config = $.cookie = function (key, value, options) {
		if (value !== undefined && !$.isFunction(value)) {
			options = $.extend({}, config.defaults, options);

			if (typeof options.expires === 'number') {
				var days = options.expires, t = options.expires = new Date();
				t.setTime(+t + days * 864e+5);
			}
			return (document.cookie = [
				encode(key), '=', stringifyCookieValue(value),
				options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
				options.path    ? '; path=' + options.path : '',
				options.domain  ? '; domain=' + options.domain : '',
				options.secure  ? '; secure' : ''
			].join(''));
		}

		var result = key ? undefined : {};
		var cookies = document.cookie ? document.cookie.split('; ') : [];

		for (var i = 0, l = cookies.length; i < l; i++) {
			var parts = cookies[i].split('=');
			var name = decode(parts.shift());
			var cookie = parts.join('=');

			if (key && key === name) {
				result = read(cookie, value);
				break;
			}

			if (!key && (cookie = read(cookie)) !== undefined) {
				result[name] = cookie;
			}
		}

		return result;
	};

	config.defaults = {};

	$.removeCookie = function (key, options) {
		if ($.cookie(key) === undefined) {
			return false;
		}

		$.cookie(key, '', $.extend({}, options, { expires: -1 }));
		return !$.cookie(key);
	};

}));

$(document).ready(function () {

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
