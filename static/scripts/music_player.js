if (! function(e) {
        function n() {}
        n.dumy = document.createElement("div"), n.trim = function(e) {
            return e.replace(/\s/gi, "")
        }, n.splitAndTrim = function(e, t) {
            for (var o = e.split(","), s = o.length, i = 0; i < s; i++) t && (o[i] = n.trim(o[i]));
            return o
        }, n.MD5 = function(e) {
            function a(e, t) {
                return e << t | e >>> 32 - t
            }

            function d(e, t) {
                var o, s, i, n, l;
                return i = 2147483648 & e, n = 2147483648 & t, l = (1073741823 & e) + (1073741823 & t), (o = 1073741824 & e) & (s = 1073741824 & t) ? 2147483648 ^ l ^ i ^ n : o | s ? 1073741824 & l ? 3221225472 ^ l ^ i ^ n : 1073741824 ^ l ^ i ^ n : l ^ i ^ n
            }

            function t(e, t, o, s, i, n, l) {
                var r;
                return e = d(e, d(d((r = t) & o | ~r & s, i), l)), d(a(e, n), t)
            }

            function o(e, t, o, s, i, n, l) {
                var r;
                return e = d(e, d(d(t & (r = s) | o & ~r, i), l)), d(a(e, n), t)
            }

            function s(e, t, o, s, i, n, l) {
                return e = d(e, d(d(t ^ o ^ s, i), l)), d(a(e, n), t)
            }

            function i(e, t, o, s, i, n, l) {
                return e = d(e, d(d(o ^ (t | ~s), i), l)), d(a(e, n), t)
            }

            function n(e) {
                var t, o = "",
                    s = "";
                for (t = 0; t <= 3; t++) o += (s = "0" + (e >>> 8 * t & 255).toString(16)).substr(s.length - 2, 2);
                return o
            }
            var l, r, u, c, h, _, f, p, m, b = Array();
            for (b = function(e) {
                    for (var t, o = e.length, s = o + 8, i = 16 * (1 + (s - s % 64) / 64), n = Array(i - 1), l = 0, r = 0; r < o;) l = r % 4 * 8, n[t = (r - r % 4) / 4] = n[t] | e.charCodeAt(r) << l, r++;
                    return l = r % 4 * 8, n[t = (r - r % 4) / 4] = n[t] | 128 << l, n[i - 2] = o << 3, n[i - 1] = o >>> 29, n
                }(e = function(e) {
                    e = e.replace(/\r\n/g, "\n");
                    for (var t = "", o = 0; o < e.length; o++) {
                        var s = e.charCodeAt(o);
                        s < 128 ? t += String.fromCharCode(s) : (127 < s && s < 2048 ? t += String.fromCharCode(s >> 6 | 192) : (t += String.fromCharCode(s >> 12 | 224), t += String.fromCharCode(s >> 6 & 63 | 128)), t += String.fromCharCode(63 & s | 128))
                    }
                    return t
                }(e)), _ = 1732584193, f = 4023233417, p = 2562383102, m = 271733878, l = 0; l < b.length; l += 16) _ = t(r = _, u = f, c = p, h = m, b[l + 0], 7, 3614090360), m = t(m, _, f, p, b[l + 1], 12, 3905402710), p = t(p, m, _, f, b[l + 2], 17, 606105819), f = t(f, p, m, _, b[l + 3], 22, 3250441966), _ = t(_, f, p, m, b[l + 4], 7, 4118548399), m = t(m, _, f, p, b[l + 5], 12, 1200080426), p = t(p, m, _, f, b[l + 6], 17, 2821735955), f = t(f, p, m, _, b[l + 7], 22, 4249261313), _ = t(_, f, p, m, b[l + 8], 7, 1770035416), m = t(m, _, f, p, b[l + 9], 12, 2336552879), p = t(p, m, _, f, b[l + 10], 17, 4294925233), f = t(f, p, m, _, b[l + 11], 22, 2304563134), _ = t(_, f, p, m, b[l + 12], 7, 1804603682), m = t(m, _, f, p, b[l + 13], 12, 4254626195), p = t(p, m, _, f, b[l + 14], 17, 2792965006), _ = o(_, f = t(f, p, m, _, b[l + 15], 22, 1236535329), p, m, b[l + 1], 5, 4129170786), m = o(m, _, f, p, b[l + 6], 9, 3225465664), p = o(p, m, _, f, b[l + 11], 14, 643717713), f = o(f, p, m, _, b[l + 0], 20, 3921069994), _ = o(_, f, p, m, b[l + 5], 5, 3593408605), m = o(m, _, f, p, b[l + 10], 9, 38016083), p = o(p, m, _, f, b[l + 15], 14, 3634488961), f = o(f, p, m, _, b[l + 4], 20, 3889429448), _ = o(_, f, p, m, b[l + 9], 5, 568446438), m = o(m, _, f, p, b[l + 14], 9, 3275163606), p = o(p, m, _, f, b[l + 3], 14, 4107603335), f = o(f, p, m, _, b[l + 8], 20, 1163531501), _ = o(_, f, p, m, b[l + 13], 5, 2850285829), m = o(m, _, f, p, b[l + 2], 9, 4243563512), p = o(p, m, _, f, b[l + 7], 14, 1735328473), _ = s(_, f = o(f, p, m, _, b[l + 12], 20, 2368359562), p, m, b[l + 5], 4, 4294588738), m = s(m, _, f, p, b[l + 8], 11, 2272392833), p = s(p, m, _, f, b[l + 11], 16, 1839030562), f = s(f, p, m, _, b[l + 14], 23, 4259657740), _ = s(_, f, p, m, b[l + 1], 4, 2763975236), m = s(m, _, f, p, b[l + 4], 11, 1272893353), p = s(p, m, _, f, b[l + 7], 16, 4139469664), f = s(f, p, m, _, b[l + 10], 23, 3200236656), _ = s(_, f, p, m, b[l + 13], 4, 681279174), m = s(m, _, f, p, b[l + 0], 11, 3936430074), p = s(p, m, _, f, b[l + 3], 16, 3572445317), f = s(f, p, m, _, b[l + 6], 23, 76029189), _ = s(_, f, p, m, b[l + 9], 4, 3654602809), m = s(m, _, f, p, b[l + 12], 11, 3873151461), p = s(p, m, _, f, b[l + 15], 16, 530742520), _ = i(_, f = s(f, p, m, _, b[l + 2], 23, 3299628645), p, m, b[l + 0], 6, 4096336452), m = i(m, _, f, p, b[l + 7], 10, 1126891415), p = i(p, m, _, f, b[l + 14], 15, 2878612391), f = i(f, p, m, _, b[l + 5], 21, 4237533241), _ = i(_, f, p, m, b[l + 12], 6, 1700485571), m = i(m, _, f, p, b[l + 3], 10, 2399980690), p = i(p, m, _, f, b[l + 10], 15, 4293915773), f = i(f, p, m, _, b[l + 1], 21, 2240044497), _ = i(_, f, p, m, b[l + 8], 6, 1873313359), m = i(m, _, f, p, b[l + 15], 10, 4264355552), p = i(p, m, _, f, b[l + 6], 15, 2734768916), f = i(f, p, m, _, b[l + 13], 21, 1309151649), _ = i(_, f, p, m, b[l + 4], 6, 4149444226), m = i(m, _, f, p, b[l + 11], 10, 3174756917), p = i(p, m, _, f, b[l + 2], 15, 718787259), f = i(f, p, m, _, b[l + 9], 21, 3951481745), _ = d(_, r), f = d(f, u), p = d(p, c), m = d(m, h);
            return (n(_) + n(f) + n(p) + n(m)).toLowerCase()
        }, n.getCanvasWithModifiedColor = function(e, t, o) {
            if (e) {
                var s, i, n = document.createElement("canvas"),
                    l = n.getContext("2d"),
                    r = null,
                    a = parseInt(t.replace(/^#/, ""), 16),
                    d = a >>> 16 & 255,
                    u = a >>> 8 & 255,
                    c = 255 & a;
                n.style.position = "absolute", n.style.left = "0px", n.style.top = "0px", n.style.margin = "0px", n.style.padding = "0px", n.style.maxWidth = "none", n.style.maxHeight = "none", n.style.border = "none", n.style.lineHeight = "1", n.style.backgroundColor = "transparent", n.style.backfaceVisibility = "hidden", n.style.webkitBackfaceVisibility = "hidden", n.style.MozBackfaceVisibility = "hidden", n.style.MozImageRendering = "optimizeSpeed", n.style.WebkitImageRendering = "optimizeSpeed", n.width = e.width, n.height = e.height, l.drawImage(e, 0, 0, e.naturalWidth, e.naturalHeight, 0, 0, e.width, e.height), i = l.getImageData(0, 0, e.width, e.height), r = l.getImageData(0, 0, e.width, e.height);
                for (var h = 0, _ = i.data.length; h < _; h += 4) 0 < r.data[h + 3] && (r.data[h] = i.data[h] / 255 * d, r.data[h + 1] = i.data[h + 1] / 255 * u, r.data[h + 2] = i.data[h + 2] / 255 * c);
                return l.globalAlpha = .5, l.putImageData(r, 0, 0), l.drawImage(n, 0, 0), o && ((s = new Image).src = n.toDataURL()), {
                    canvas: n,
                    image: s
                }
            }
        }, n.formatTime = function(e, t) {
            var o = Math.floor(e / 3600),
                s = e % 3600,
                i = Math.floor(s / 60),
                n = s % 60,
                l = Math.ceil(n);
            return i = 10 <= i ? i : "0" + i, l = 10 <= l ? l : "0" + l, isNaN(l) ? "00:00" : o || t ? "0" + o + ":" + i + ":" + l : i + ":" + l
        }, n.checkTime = function(e) {
            return !!/^(?:2[0-3]|[01][0-9]):[0-5][0-9]:[0-5][0-9]$/.test(e)
        }, n.getSecondsFromString = function(e) {
            var t = 0,
                o = 0,
                s = 0;
            if (e) return "0" == (t = (e = e.split(":"))[0])[0] && "0" != t[1] && (t = parseInt(t[1])), "00" == t && (t = 0), "0" == (o = e[1])[0] && "0" != o[1] && (o = parseInt(o[1])), "00" == o && (o = 0), secs = parseInt(e[2].replace(/,.*/gi, "")), "0" == secs[0] && "0" != secs[1] && (secs = parseInt(secs[1])), "00" == secs && (secs = 0), 0 != t && (s += 60 * t * 60), 0 != o && (s += 60 * o), s += secs
        }, n.changeCanvasHEXColor = function(e, t, o, s) {
            if (e) {
                var i, n = (t = t).getContext("2d"),
                    l = null,
                    r = parseInt(o.replace(/^#/, ""), 16),
                    a = r >>> 16 & 255,
                    d = r >>> 8 & 255,
                    u = 255 & r;
                t.width = e.width, t.height = e.height, n.drawImage(e, 0, 0, e.naturalWidth, e.naturalHeight, 0, 0, e.width, e.height), i = n.getImageData(0, 0, e.width, e.height), l = n.getImageData(0, 0, e.width, e.height);
                for (var c = 0, h = i.data.length; c < h; c += 4) 0 < l.data[c + 3] && (l.data[c] = i.data[c] / 255 * a, l.data[c + 1] = i.data[c + 1] / 255 * d, l.data[c + 2] = i.data[c + 2] / 255 * u);
                if (n.globalAlpha = .5, n.putImageData(l, 0, 0), n.drawImage(t, 0, 0), s) {
                    var _ = new Image;
                    return _.src = t.toDataURL(), _
                }
            }
        }, n.isURLEncoded = function(e) {
            try {
                if (decodeURIComponent(e) != e && -1 != e.indexOf("%")) return !0
            } catch (e) {}
            return !1
        }, n.indexOfArray = function(e, t) {
            for (var o = e.length, s = 0; s < o; s++)
                if (e[s] === t) return s;
            return -1
        }, n.randomizeArray = function(e) {
            for (var t = [], o = e.concat(), s = o.length, i = 0; i < s; i++) {
                var n = Math.floor(Math.random() * o.length);
                t.push(o[n]), o.splice(n, 1)
            }
            return t
        }, n.getCookie = function(e) {
            for (var t = e + "=", o = document.cookie.split(";"), s = 0; s < o.length; s++) {
                for (var i = o[s];
                    " " == i.charAt(0);) i = i.substring(1, i.length);
                if (0 == i.indexOf(t)) return i.substring(t.length, i.length)
            }
            return null
        }, n.parent = function(e, t) {
            for (void 0 === t && (t = 1); t-- && e;) e = e.parentNode;
            return e && 1 === e.nodeType ? e : null
        }, n.sibling = function(e, t) {
            for (; e && 0 !== t;)
                if (0 < t) {
                    if (e.nextElementSibling) e = e.nextElementSibling;
                    else
                        for (e = e.nextSibling; e && 1 !== e.nodeType; e = e.nextSibling);
                    t--
                } else {
                    if (e.previousElementSibling) e = e.previousElementSibling;
                    else
                        for (e = e.previousSibling; e && 1 !== e.nodeType; e = e.previousSibling);
                    t++
                } return e
        }, n.getChildAt = function(e, t) {
            var o = n.getChildren(e);
            return t < 0 && (t += o.length), t < 0 ? null : o[t]
        }, n.getChildById = function(e) {
            return document.getElementById(e) || void 0
        }, n.getChildren = function(e, t) {
            for (var o = [], s = e.firstChild; null != s; s = s.nextSibling) t ? o.push(s) : 1 === s.nodeType && o.push(s);
            return o
        }, n.getChildrenFromAttribute = function(e, t, o) {
            for (var s = [], i = e.firstChild; null != i; i = i.nextSibling) o && n.hasAttribute(i, t) ? s.push(i) : 1 === i.nodeType && n.hasAttribute(i, t) && s.push(i);
            return 0 == s.length ? void 0 : s
        }, n.getChildFromNodeListFromAttribute = function(e, t, o) {
            for (var s = e.firstChild; null != s; s = s.nextSibling) {
                if (o && n.hasAttribute(s, t)) return s;
                if (1 === s.nodeType && n.hasAttribute(s, t)) return s
            }
        }, n.getAttributeValue = function(e, t) {
            if (n.hasAttribute(e, t)) return e.getAttribute(t)
        }, n.hasAttribute = function(e, t) {
            return e.hasAttribute ? e.hasAttribute(t) : !!e.getAttribute(t)
        }, n.insertNodeAt = function(e, t, o) {
            var s = n.children(e);
            if (o < 0 || o > s.length) throw new Error("invalid index!");
            e.insertBefore(t, s[o])
        }, n.hasCanvas = function() {
            return Boolean(document.createElement("canvas"))
        }, n.hitTest = function(e, t, o) {
            if (!e) throw Error("Hit test target is null!");
            var s = e.getBoundingClientRect();
            return t >= s.left && t <= s.left + (s.right - s.left) && o >= s.top && o <= s.top + (s.bottom - s.top)
        }, n.getScrollOffsets = function() {
            return null != e.pageXOffset ? {
                x: e.pageXOffset,
                y: e.pageYOffset
            } : "CSS1Compat" == document.compatMode ? {
                x: document.documentElement.scrollLeft,
                y: document.documentElement.scrollTop
            } : void 0
        }, n.getViewportSize = function() {
            return n.hasPointerEvent && 1 < navigator.msMaxTouchPoints ? {
                w: document.documentElement.clientWidth || e.innerWidth,
                h: document.documentElement.clientHeight || e.innerHeight
            } : n.isMobile ? {
                w: e.innerWidth,
                h: e.innerHeight
            } : {
                w: document.documentElement.clientWidth || e.innerWidth,
                h: document.documentElement.clientHeight || e.innerHeight
            }
        }, n.getViewportMouseCoordinates = function(e) {
            var t = n.getScrollOffsets();
            return e.touches ? {
                screenX: null == e.touches[0] ? e.touches.pageX - t.x : e.touches[0].pageX - t.x,
                screenY: null == e.touches[0] ? e.touches.pageY - t.y : e.touches[0].pageY - t.y
            } : {
                screenX: null == e.clientX ? e.pageX - t.x : e.clientX,
                screenY: null == e.clientY ? e.pageY - t.y : e.clientY
            }
        }, n.hasPointerEvent = Boolean(e.navigator.msPointerEnabled) || Boolean(e.navigator.pointerEnabled), n.isMobile = function() {
            if (n.hasPointerEvent && 1 < navigator.msMaxTouchPoints || n.hasPointerEvent && 1 < navigator.maxTouchPoints) return !0;
            var e = ["android", "webos", "iphone", "ipad", "blackberry"];
            for (i in e)
                if (-1 != navigator.userAgent.toLowerCase().indexOf(String(e[i]).toLowerCase())) return !0;
            return !1
        }(), n.isAndroid = -1 != navigator.userAgent.toLowerCase().indexOf("android".toLowerCase()), n.isChrome = -1 != navigator.userAgent.toLowerCase().indexOf("chrome"), n.isSafari = -1 != navigator.userAgent.toLowerCase().indexOf("safari") && -1 == navigator.userAgent.toLowerCase().indexOf("chrome"), n.isOpera = -1 != navigator.userAgent.toLowerCase().indexOf("opera") && -1 == navigator.userAgent.toLowerCase().indexOf("chrome"), n.isFirefox = -1 != navigator.userAgent.toLowerCase().indexOf("firefox"), n.isIE = Boolean(-1 != navigator.userAgent.toLowerCase().indexOf("msie")) || Boolean(-1 != navigator.userAgent.toLowerCase().indexOf("edge")) || Boolean(!n.isIE && document.documentElement.msRequestFullscreen), n.isIE11 = Boolean(!n.isIE && document.documentElement.msRequestFullscreen), n.isIEAndLessThen9 = -1 != navigator.userAgent.toLowerCase().indexOf("msie 7") || -1 != navigator.userAgent.toLowerCase().indexOf("msie 8"), n.isIEAndLessThen10 = -1 != navigator.userAgent.toLowerCase().indexOf("msie 7") || -1 != navigator.userAgent.toLowerCase().indexOf("msie 8") || -1 != navigator.userAgent.toLowerCase().indexOf("msie 9"), n.isIE7 = -1 != navigator.userAgent.toLowerCase().indexOf("msie 7"), n.isApple = -1 != navigator.appVersion.toLowerCase().indexOf("mac"), n.hasFullScreen = n.dumy.requestFullScreen || n.dumy.mozRequestFullScreen || n.dumy.webkitRequestFullScreen || n.dumy.msieRequestFullScreen, n.onReady = function(e) {
            document.addEventListener ? document.addEventListener("DOMContentLoaded", function() {
                n.checkIfHasTransofrms(), e()
            }) : document.onreadystatechange = function() {
                n.checkIfHasTransofrms(), "complete" == document.readyState && e()
            }
        }, n.checkIfHasTransofrms = function() {
            document.documentElement.appendChild(n.dumy), n.hasTransform3d = function() {
                for (var e, t, o = ["transform", "msTransform", "WebkitTransform", "MozTransform", "OTransform", "KhtmlTransform"]; e = o.shift();)
                    if (void 0 !== n.dumy.style[e] && (n.dumy.style.position = "absolute", t = n.dumy.getBoundingClientRect().left, n.dumy.style[e] = "translate3d(500px, 0px, 0px)", 100 < (t = Math.abs(n.dumy.getBoundingClientRect().left - t)) && t < 900)) {
                        try {
                            document.documentElement.removeChild(n.dumy)
                        } catch (e) {}
                        return !0
                    } try {
                    document.documentElement.removeChild(n.dumy)
                } catch (e) {}
                return !1
            }(), n.hasTransform2d = function() {
                for (var e, t = ["transform", "msTransform", "WebkitTransform", "MozTransform", "OTransform", "KhtmlTransform"]; e = t.shift();)
                    if (void 0 !== n.dumy.style[e]) return !0;
                try {
                    document.documentElement.removeChild(n.dumy)
                } catch (e) {}
                return !1
            }(), n.isReadyMethodCalled_bl = !0
        }, n.disableElementSelection = function(e) {
            try {
                e.style.userSelect = "none"
            } catch (e) {}
            try {
                e.style.MozUserSelect = "none"
            } catch (e) {}
            try {
                e.style.webkitUserSelect = "none"
            } catch (e) {}
            try {
                e.style.khtmlUserSelect = "none"
            } catch (e) {}
            try {
                e.style.oUserSelect = "none"
            } catch (e) {}
            try {
                e.style.msUserSelect = "none"
            } catch (e) {}
            try {
                e.msUserSelect = "none"
            } catch (e) {}
            e.onselectstart = function() {
                return !1
            }
        }, n.getUrlArgs = function(e) {
            for (var t = {}, o = (e.substr(e.indexOf("?") + 1) || location.search.substring(1)).split("&"), s = 0; s < o.length; s++) {
                var i = o[s].indexOf("="),
                    n = o[s].substring(0, i),
                    l = o[s].substring(i + 1);
                l = decodeURIComponent(l), t[n] = l
            }
            return t
        }, n.isReadyMethodCalled_bl = !1, e.FWDMSPUtils = n
    }(window), !window.FWDAnimation) {
    var _fwd_gsScope = "undefined" != typeof fwd_module && fwd_module.exports && "undefined" != typeof fwd_global ? fwd_global : this || window;
    (_fwd_gsScope._fwd_gsQueue || (_fwd_gsScope._fwd_gsQueue = [])).push(function() {
            "use strict";

            function g(e, t, o, s) {
                o === s && (o = s - (s - t) / 1e6), e === t && (t = e + (o - e) / 1e6), this.a = e, this.b = t, this.c = o, this.d = s, this.da = s - e, this.ca = o - e, this.ba = t - e
            }

            function v(e, t, o, s) {
                var i = {
                        a: e
                    },
                    n = {},
                    l = {},
                    r = {
                        c: s
                    },
                    a = (e + t) / 2,
                    d = (t + o) / 2,
                    u = (o + s) / 2,
                    c = (a + d) / 2,
                    h = (d + u) / 2,
                    _ = (h - c) / 8;
                return i.b = a + (e - a) / 4, n.b = c + _, i.c = n.a = (i.b + n.b) / 2, n.c = l.a = (c + h) / 2, l.b = h - _, r.b = u + (s - u) / 4, l.c = r.a = (l.b + r.b) / 2, [i, n, l, r]
            }

            function b(e, t, o, s, i) {
                var n, l, r, a, d, u, c, h, _, f, p, m, b, g = e.length - 1,
                    S = 0,
                    y = e[0].a;
                for (n = 0; n < g; n++) l = (d = e[S]).a, r = d.d, a = e[S + 1].d, h = i ? (p = P[n], b = ((m = w[n]) + p) * t * .25 / (s ? .5 : D[n] || .5), r - ((u = r - (r - l) * (s ? .5 * t : 0 !== p ? b / p : 0)) + (((c = r + (a - r) * (s ? .5 * t : 0 !== m ? b / m : 0)) - u) * (3 * p / (p + m) + .5) / 4 || 0))) : r - ((u = r - (r - l) * t * .5) + (c = r + (a - r) * t * .5)) / 2, u += h, c += h, d.c = _ = u, d.b = 0 !== n ? y : y = d.a + .6 * (d.c - d.a), d.da = r - l, d.ca = _ - l, d.ba = y - l, o ? (f = v(l, y, _, r), e.splice(S, 1, f[0], f[1], f[2], f[3]), S += 4) : S++, y = c;
                (d = e[S]).b = y, d.c = y + .4 * (d.d - y), d.da = d.d - d.a, d.ca = d.c - d.a, d.ba = y - d.a, o && (f = v(d.a, y, d.c, d.d), e.splice(S, 1, f[0], f[1], f[2], f[3]))
            }

            function S(e, t, o, s) {
                var i, n, l, r, a, d, u = [];
                if (s)
                    for (n = (e = [s].concat(e)).length; - 1 < --n;) "string" == typeof(d = e[n][t]) && "=" === d.charAt(1) && (e[n][t] = s[t] + Number(d.charAt(0) + d.substr(2)));
                if ((i = e.length - 2) < 0) return u[0] = new g(e[0][t], 0, 0, e[i < -1 ? 0 : 1][t]), u;
                for (n = 0; n < i; n++) l = e[n][t], r = e[n + 1][t], u[n] = new g(l, 0, 0, r), o && (a = e[n + 2][t], P[n] = (P[n] || 0) + (r - l) * (r - l), w[n] = (w[n] || 0) + (a - r) * (a - r));
                return u[n] = new g(e[n][t], 0, 0, e[n + 1][t]), u
            }

            function _(e, t, o, s, i, n) {
                var l, r, a, d, u, c, h, _, f = {},
                    p = [],
                    m = n || e[0];
                for (r in i = "string" == typeof i ? "," + i + "," : ",x,y,z,left,top,right,bottom,marginTop,marginLeft,marginRight,marginBottom,paddingLeft,paddingTop,paddingRight,paddingBottom,backgroundPosition,backgroundPosition_y,", null == t && (t = 1), e[0]) p.push(r);
                if (1 < e.length) {
                    for (_ = e[e.length - 1], h = !0, l = p.length; - 1 < --l;)
                        if (r = p[l], .05 < Math.abs(m[r] - _[r])) {
                            h = !1;
                            break
                        } h && (e = e.concat(), n && e.unshift(n), e.push(e[1]), n = e[e.length - 3])
                }
                for (P.length = w.length = D.length = 0, l = p.length; - 1 < --l;) r = p[l], y[r] = -1 !== i.indexOf("," + r + ","), f[r] = S(e, r, y[r], n);
                for (l = P.length; - 1 < --l;) P[l] = Math.sqrt(P[l]), w[l] = Math.sqrt(w[l]);
                if (!s) {
                    for (l = p.length; - 1 < --l;)
                        if (y[r])
                            for (c = (a = f[p[l]]).length - 1, d = 0; d < c; d++) u = a[d + 1].da / w[d] + a[d].da / P[d] || 0, D[d] = (D[d] || 0) + u * u;
                    for (l = D.length; - 1 < --l;) D[l] = Math.sqrt(D[l])
                }
                for (l = p.length, d = o ? 4 : 1; - 1 < --l;) a = f[r = p[l]], b(a, t, o, s, y[r]), h && (a.splice(0, d), a.splice(a.length - d, d));
                return f
            }

            function f(e, t, o) {
                for (var s, i, n, l, r, a, d, u, c, h, _, f = 1 / o, p = e.length; - 1 < --p;)
                    for (n = (h = e[p]).a, l = h.d - n, r = h.c - n, a = h.b - n, s = i = 0, u = 1; u <= o; u++) s = i - (i = ((d = f * u) * d * l + 3 * (c = 1 - d) * (d * r + c * a)) * d), t[_ = p * o + u - 1] = (t[_] || 0) + s * s
            }
            var T, P, w, D, y, o, m, e, t, s;

            function a(e) {
                for (; e;) e.f || e.blob || (e.m = Math.round), e = e._next
            }
            _fwd_gsScope._gsDefine("FWDAnimation", ["core.Animation", "core.SimpleTimeline", "FWDTweenLite"], function(s, u, m) {
                function b(e) {
                    var t, o = [],
                        s = e.length;
                    for (t = 0; t !== s; o.push(e[t++]));
                    return o
                }

                function g(e, t, o) {
                    var s, i, n = e.cycle;
                    for (s in n) i = n[s], e[s] = "function" == typeof i ? i(o, t[o]) : i[o % i.length];
                    delete e.cycle
                }
                var S = function(e, t, o) {
                        m.call(this, e, t, o), this._cycle = 0, this._yoyo = !0 === this.vars.yoyo, this._repeat = this.vars.repeat || 0, this._repeatDelay = this.vars.repeatDelay || 0, this._dirty = !0, this.render = S.prototype.render
                    },
                    y = 1e-10,
                    v = m._internals,
                    P = v.isSelector,
                    T = v.isArray,
                    e = S.prototype = m.to({}, .1, {}),
                    w = [];
                S.version = "1.19.0", e.constructor = S, e.kill()._gc = !1, S.killTweensOf = S.killDelayedCallsTo = m.killTweensOf, S.getTweensOf = m.getTweensOf, S.lagSmoothing = m.lagSmoothing, S.ticker = m.ticker, S.render = m.render, e.invalidate = function() {
                    return this._yoyo = !0 === this.vars.yoyo, this._repeat = this.vars.repeat || 0, this._repeatDelay = this.vars.repeatDelay || 0, this._uncache(!0), m.prototype.invalidate.call(this)
                }, e.updateTo = function(e, t) {
                    var o, s = this.ratio,
                        i = this.vars.immediateRender || e.immediateRender;
                    for (o in t && this._startTime < this._timeline._time && (this._startTime = this._timeline._time, this._uncache(!1), this._gc ? this._enabled(!0, !1) : this._timeline.insert(this, this._startTime - this._delay)), e) this.vars[o] = e[o];
                    if (this._initted || i)
                        if (t) this._initted = !1, i && this.render(0, !0, !0);
                        else if (this._gc && this._enabled(!0, !1), this._notifyPluginsOfEnabled && this._firstPT && m._onPluginEvent("_onDisable", this), .998 < this._time / this._duration) {
                        var n = this._totalTime;
                        this.render(0, !0, !1), this._initted = !1, this.render(n, !0, !1)
                    } else if (this._initted = !1, this._init(), 0 < this._time || i)
                        for (var l, r = 1 / (1 - s), a = this._firstPT; a;) l = a.s + a.c, a.c *= r, a.s = l - a.c, a = a._next;
                    return this
                }, e.render = function(e, t, o) {
                    this._initted || 0 === this._duration && this.vars.repeat && this.invalidate();
                    var s, i, n, l, r, a, d, u, c = this._dirty ? this.totalDuration() : this._totalDuration,
                        h = this._time,
                        _ = this._totalTime,
                        f = this._cycle,
                        p = this._duration,
                        m = this._rawPrevTime;
                    if (c - 1e-7 <= e ? (this._totalTime = c, this._cycle = this._repeat, this._yoyo && 0 != (1 & this._cycle) ? (this._time = 0, this.ratio = this._ease._calcEnd ? this._ease.getRatio(0) : 0) : (this._time = p, this.ratio = this._ease._calcEnd ? this._ease.getRatio(1) : 1), this._reversed || (s = !0, i = "onComplete", o = o || this._timeline.autoRemoveChildren), 0 === p && (!this._initted && this.vars.lazy && !o || (this._startTime === this._timeline._duration && (e = 0), (m < 0 || e <= 0 && -1e-7 <= e || m === y && "isPause" !== this.data) && m !== e && (o = !0, y < m && (i = "onReverseComplete")), this._rawPrevTime = u = !t || e || m === e ? e : y))) : e < 1e-7 ? (this._totalTime = this._time = this._cycle = 0, this.ratio = this._ease._calcEnd ? this._ease.getRatio(0) : 0, (0 !== _ || 0 === p && 0 < m) && (i = "onReverseComplete", s = this._reversed), e < 0 && (this._active = !1, 0 === p && (!this._initted && this.vars.lazy && !o || (0 <= m && (o = !0), this._rawPrevTime = u = !t || e || m === e ? e : y))), this._initted || (o = !0)) : (this._totalTime = this._time = e, 0 !== this._repeat && (l = p + this._repeatDelay, this._cycle = this._totalTime / l >> 0, 0 !== this._cycle && this._cycle === this._totalTime / l && _ <= e && this._cycle--, this._time = this._totalTime - this._cycle * l, this._yoyo && 0 != (1 & this._cycle) && (this._time = p - this._time), this._time > p ? this._time = p : this._time < 0 && (this._time = 0)), this._easeType ? (r = this._time / p, (1 === (a = this._easeType) || 3 === a && .5 <= r) && (r = 1 - r), 3 === a && (r *= 2), 1 === (d = this._easePower) ? r *= r : 2 === d ? r *= r * r : 3 === d ? r *= r * r * r : 4 === d && (r *= r * r * r * r), 1 === a ? this.ratio = 1 - r : 2 === a ? this.ratio = r : this._time / p < .5 ? this.ratio = r / 2 : this.ratio = 1 - r / 2) : this.ratio = this._ease.getRatio(this._time / p)), h !== this._time || o || f !== this._cycle) {
                        if (!this._initted) {
                            if (this._init(), !this._initted || this._gc) return;
                            if (!o && this._firstPT && (!1 !== this.vars.lazy && this._duration || this.vars.lazy && !this._duration)) return this._time = h, this._totalTime = _, this._rawPrevTime = m, this._cycle = f, v.lazyTweens.push(this), void(this._lazy = [e, t]);
                            this._time && !s ? this.ratio = this._ease.getRatio(this._time / p) : s && this._ease._calcEnd && (this.ratio = this._ease.getRatio(0 === this._time ? 0 : 1))
                        }
                        for (!1 !== this._lazy && (this._lazy = !1), this._active || !this._paused && this._time !== h && 0 <= e && (this._active = !0), 0 === _ && (2 === this._initted && 0 < e && this._init(), this._startAt && (0 <= e ? this._startAt.render(e, t, o) : i = i || "_dummyGS"), this.vars.onStart && (0 === this._totalTime && 0 !== p || t || this._callback("onStart"))), n = this._firstPT; n;) {
                            if (n.f) n.t[n.p](n.c * this.ratio + n.s);
                            else {
                                var b = n.c * this.ratio + n.s;
                                "x" == n.p ? n.t.setX(b) : "y" == n.p ? n.t.setY(b) : "z" == n.p ? n.t.setZ(b) : "angleX" == n.p ? n.t.setAngleX(b) : "angleY" == n.p ? n.t.setAngleY(b) : "angleZ" == n.p ? n.t.setAngleZ(b) : "w" == n.p ? n.t.setWidth(b) : "h" == n.p ? n.t.setHeight(b) : "alpha" == n.p ? n.t.setAlpha(b) : "scale" == n.p ? n.t.setScale2(b) : n.t[n.p] = b
                            }
                            n = n._next
                        }
                        this._onUpdate && (e < 0 && this._startAt && this._startTime && this._startAt.render(e, t, o), t || this._totalTime === _ && !i || this._callback("onUpdate")), this._cycle !== f && (t || this._gc || this.vars.onRepeat && this._callback("onRepeat")), i && (this._gc && !o || (e < 0 && this._startAt && !this._onUpdate && this._startTime && this._startAt.render(e, t, o), s && (this._timeline.autoRemoveChildren && this._enabled(!1, !1), this._active = !1), !t && this.vars[i] && this._callback(i), 0 === p && this._rawPrevTime === y && u !== y && (this._rawPrevTime = 0)))
                    } else _ !== this._totalTime && this._onUpdate && (t || this._callback("onUpdate"))
                }, S.to = function(e, t, o) {
                    return new S(e, t, o)
                }, S.from = function(e, t, o) {
                    return o.runBackwards = !0, o.immediateRender = 0 != o.immediateRender, new S(e, t, o)
                }, S.fromTo = function(e, t, o, s) {
                    return s.startAt = o, s.immediateRender = 0 != s.immediateRender && 0 != o.immediateRender, new S(e, t, s)
                }, S.staggerTo = S.allTo = function(e, t, o, s, i, n, l) {
                    s = s || 0;

                    function r() {
                        o.onComplete && o.onComplete.apply(o.onCompleteScope || this, arguments), i.apply(l || o.callbackScope || this, n || w)
                    }
                    var a, d, u, c, h = 0,
                        _ = [],
                        f = o.cycle,
                        p = o.startAt && o.startAt.cycle;
                    for (T(e) || ("string" == typeof e && (e = m.selector(e) || e), P(e) && (e = b(e))), e = e || [], s < 0 && ((e = b(e)).reverse(), s *= -1), a = e.length - 1, u = 0; u <= a; u++) {
                        for (c in d = {}, o) d[c] = o[c];
                        if (f && (g(d, e, u), null != d.duration && (t = d.duration, delete d.duration)), p) {
                            for (c in p = d.startAt = {}, o.startAt) p[c] = o.startAt[c];
                            g(d.startAt, e, u)
                        }
                        d.delay = h + (d.delay || 0), u === a && i && (d.onComplete = r), _[u] = new S(e[u], t, d), h += s
                    }
                    return _
                }, S.staggerFrom = S.allFrom = function(e, t, o, s, i, n, l) {
                    return o.runBackwards = !0, o.immediateRender = 0 != o.immediateRender, S.staggerTo(e, t, o, s, i, n, l)
                }, S.staggerFromTo = S.allFromTo = function(e, t, o, s, i, n, l, r) {
                    return s.startAt = o, s.immediateRender = 0 != s.immediateRender && 0 != o.immediateRender, S.staggerTo(e, t, s, i, n, l, r)
                }, S.delayedCall = function(e, t, o, s, i) {
                    return new S(t, 0, {
                        delay: e,
                        onComplete: t,
                        onCompleteParams: o,
                        callbackScope: s,
                        onReverseComplete: t,
                        onReverseCompleteParams: o,
                        immediateRender: !1,
                        useFrames: i,
                        overwrite: 0
                    })
                }, S.set = function(e, t) {
                    return new S(e, 0, t)
                }, S.isTweening = function(e) {
                    return 0 < m.getTweensOf(e, !0).length
                };
                var n = function(e, t) {
                        for (var o = [], s = 0, i = e._first; i;) i instanceof m ? o[s++] = i : (t && (o[s++] = i), s = (o = o.concat(n(i, t))).length), i = i._next;
                        return o
                    },
                    c = S.getAllTweens = function(e) {
                        return n(s._rootTimeline, e).concat(n(s._rootFramesTimeline, e))
                    };
                S.killAll = function(e, t, o, s) {
                    null == t && (t = !0), null == o && (o = !0);
                    var i, n, l, r = c(0 != s),
                        a = r.length,
                        d = t && o && s;
                    for (l = 0; l < a; l++) n = r[l], (d || n instanceof u || (i = n.target === n.vars.onComplete) && o || t && !i) && (e ? n.totalTime(n._reversed ? 0 : n.totalDuration()) : n._enabled(!1, !1))
                }, S.killChildTweensOf = function(e, t) {
                    if (null != e) {
                        var o, s, i, n, l, r = v.tweenLookup;
                        if ("string" == typeof e && (e = m.selector(e) || e), P(e) && (e = b(e)), T(e))
                            for (n = e.length; - 1 < --n;) S.killChildTweensOf(e[n], t);
                        else {
                            for (i in o = [], r)
                                for (s = r[i].target.parentNode; s;) s === e && (o = o.concat(r[i].tweens)), s = s.parentNode;
                            for (l = o.length, n = 0; n < l; n++) t && o[n].totalTime(o[n].totalDuration()), o[n]._enabled(!1, !1)
                        }
                    }
                };

                function i(e, t, o, s) {
                    t = !1 !== t, o = !1 !== o;
                    for (var i, n, l = c(s = !1 !== s), r = t && o && s, a = l.length; - 1 < --a;) n = l[a], (r || n instanceof u || (i = n.target === n.vars.onComplete) && o || t && !i) && n.paused(e)
                }
                return S.pauseAll = function(e, t, o) {
                    i(!0, e, t, o)
                }, S.resumeAll = function(e, t, o) {
                    i(!1, e, t, o)
                }, S.globalTimeScale = function(e) {
                    var t = s._rootTimeline,
                        o = m.ticker.time;
                    return arguments.length ? (e = e || y, t._startTime = o - (o - t._startTime) * t._timeScale / e, t = s._rootFramesTimeline, o = m.ticker.frame, t._startTime = o - (o - t._startTime) * t._timeScale / e, t._timeScale = s._rootTimeline._timeScale = e, e) : t._timeScale
                }, e.progress = function(e, t) {
                    return arguments.length ? this.totalTime(this.duration() * (this._yoyo && 0 != (1 & this._cycle) ? 1 - e : e) + this._cycle * (this._duration + this._repeatDelay), t) : this._time / this.duration()
                }, e.totalProgress = function(e, t) {
                    return arguments.length ? this.totalTime(this.totalDuration() * e, t) : this._totalTime / this.totalDuration()
                }, e.time = function(e, t) {
                    return arguments.length ? (this._dirty && this.totalDuration(), e > this._duration && (e = this._duration), this._yoyo && 0 != (1 & this._cycle) ? e = this._duration - e + this._cycle * (this._duration + this._repeatDelay) : 0 !== this._repeat && (e += this._cycle * (this._duration + this._repeatDelay)), this.totalTime(e, t)) : this._time
                }, e.duration = function(e) {
                    return arguments.length ? s.prototype.duration.call(this, e) : this._duration
                }, e.totalDuration = function(e) {
                    return arguments.length ? -1 === this._repeat ? this : this.duration((e - this._repeat * this._repeatDelay) / (this._repeat + 1)) : (this._dirty && (this._totalDuration = -1 === this._repeat ? 999999999999 : this._duration * (this._repeat + 1) + this._repeatDelay * this._repeat, this._dirty = !1), this._totalDuration)
                }, e.repeat = function(e) {
                    return arguments.length ? (this._repeat = e, this._uncache(!0)) : this._repeat
                }, e.repeatDelay = function(e) {
                    return arguments.length ? (this._repeatDelay = e, this._uncache(!0)) : this._repeatDelay
                }, e.yoyo = function(e) {
                    return arguments.length ? (this._yoyo = e, this) : this._yoyo
                }, S
            }, !0), _fwd_gsScope._gsDefine("TimelineLite", ["core.Animation", "core.SimpleTimeline", "FWDTweenLite"], function(u, c, h) {
                function _(e) {
                    c.call(this, e), this._labels = {}, this.autoRemoveChildren = !0 === this.vars.autoRemoveChildren, this.smoothChildTiming = !0 === this.vars.smoothChildTiming, this._sortChildren = !0, this._onUpdate = this.vars.onUpdate;
                    var t, o, s = this.vars;
                    for (o in s) t = s[o], S(t) && -1 !== t.join("").indexOf("{self}") && (s[o] = this._swapSelfInParams(t));
                    S(s.tweens) && this.add(s.tweens, 0, s.align, s.stagger)
                }

                function f(e) {
                    var t, o = {};
                    for (t in e) o[t] = e[t];
                    return o
                }

                function p(e, t, o) {
                    var s, i, n = e.cycle;
                    for (s in n) i = n[s], e[s] = "function" == typeof i ? i.call(t[o], o) : i[o % i.length];
                    delete e.cycle
                }

                function m(e) {
                    var t, o = [],
                        s = e.length;
                    for (t = 0; t !== s; o.push(e[t++]));
                    return o
                }
                var b = 1e-10,
                    e = h._internals,
                    t = _._internals = {},
                    g = e.isSelector,
                    S = e.isArray,
                    y = e.lazyTweens,
                    v = e.lazyRender,
                    l = _fwd_gsScope._gsDefine.globals,
                    n = t.pauseCallback = function() {},
                    o = _.prototype = new c;
                return _.version = "1.19.0", o.constructor = _, o.kill()._gc = o._forcingPlayhead = o._hasPause = !1, o.to = function(e, t, o, s) {
                    var i = o.repeat && l.FWDAnimation || h;
                    return t ? this.add(new i(e, t, o), s) : this.set(e, o, s)
                }, o.from = function(e, t, o, s) {
                    return this.add((o.repeat && l.FWDAnimation || h).from(e, t, o), s)
                }, o.fromTo = function(e, t, o, s, i) {
                    var n = s.repeat && l.FWDAnimation || h;
                    return t ? this.add(n.fromTo(e, t, o, s), i) : this.set(e, s, i)
                }, o.staggerTo = function(e, t, o, s, i, n, l, r) {
                    var a, d, u = new _({
                            onComplete: n,
                            onCompleteParams: l,
                            callbackScope: r,
                            smoothChildTiming: this.smoothChildTiming
                        }),
                        c = o.cycle;
                    for ("string" == typeof e && (e = h.selector(e) || e), g(e = e || []) && (e = m(e)), (s = s || 0) < 0 && ((e = m(e)).reverse(), s *= -1), d = 0; d < e.length; d++)(a = f(o)).startAt && (a.startAt = f(a.startAt), a.startAt.cycle && p(a.startAt, e, d)), c && (p(a, e, d), null != a.duration && (t = a.duration, delete a.duration)), u.to(e[d], t, a, d * s);
                    return this.add(u, i)
                }, o.staggerFrom = function(e, t, o, s, i, n, l, r) {
                    return o.immediateRender = 0 != o.immediateRender, o.runBackwards = !0, this.staggerTo(e, t, o, s, i, n, l, r)
                }, o.staggerFromTo = function(e, t, o, s, i, n, l, r, a) {
                    return s.startAt = o, s.immediateRender = 0 != s.immediateRender && 0 != o.immediateRender, this.staggerTo(e, t, s, i, n, l, r, a)
                }, o.call = function(e, t, o, s) {
                    return this.add(h.delayedCall(0, e, t, o), s)
                }, o.set = function(e, t, o) {
                    return o = this._parseTimeOrLabel(o, 0, !0), null == t.immediateRender && (t.immediateRender = o === this._time && !this._paused), this.add(new h(e, 0, t), o)
                }, _.exportRoot = function(e, t) {
                    null == (e = e || {}).smoothChildTiming && (e.smoothChildTiming = !0);
                    var o, s, i = new _(e),
                        n = i._timeline;
                    for (null == t && (t = !0), n._remove(i, !0), i._startTime = 0, i._rawPrevTime = i._time = i._totalTime = n._time, o = n._first; o;) s = o._next, t && o instanceof h && o.target === o.vars.onComplete || i.add(o, o._startTime - o._delay), o = s;
                    return n.add(i, 0), i
                }, o.add = function(e, t, o, s) {
                    var i, n, l, r, a, d;
                    if ("number" != typeof t && (t = this._parseTimeOrLabel(t, 0, !0, e)), !(e instanceof u)) {
                        if (e instanceof Array || e && e.push && S(e)) {
                            for (o = o || "normal", s = s || 0, i = t, n = e.length, l = 0; l < n; l++) S(r = e[l]) && (r = new _({
                                tweens: r
                            })), this.add(r, i), "string" != typeof r && "function" != typeof r && ("sequence" === o ? i = r._startTime + r.totalDuration() / r._timeScale : "start" === o && (r._startTime -= r.delay())), i += s;
                            return this._uncache(!0)
                        }
                        if ("string" == typeof e) return this.addLabel(e, t);
                        if ("function" != typeof e) throw "Cannot add " + e + " into the timeline; it is not a tween, timeline, function, or string.";
                        e = h.delayedCall(0, e)
                    }
                    if (c.prototype.add.call(this, e, t), (this._gc || this._time === this._duration) && !this._paused && this._duration < this.duration())
                        for (d = (a = this).rawTime() > e._startTime; a._timeline;) d && a._timeline.smoothChildTiming ? a.totalTime(a._totalTime, !0) : a._gc && a._enabled(!0, !1), a = a._timeline;
                    return this
                }, o.remove = function(e) {
                    if (e instanceof u) {
                        this._remove(e, !1);
                        var t = e._timeline = e.vars.useFrames ? u._rootFramesTimeline : u._rootTimeline;
                        return e._startTime = (e._paused ? e._pauseTime : t._time) - (e._reversed ? e.totalDuration() - e._totalTime : e._totalTime) / e._timeScale, this
                    }
                    if (e instanceof Array || e && e.push && S(e)) {
                        for (var o = e.length; - 1 < --o;) this.remove(e[o]);
                        return this
                    }
                    return "string" == typeof e ? this.removeLabel(e) : this.kill(null, e)
                }, o._remove = function(e, t) {
                    c.prototype._remove.call(this, e, t);
                    var o = this._last;
                    return o ? this._time > o._startTime + o._totalDuration / o._timeScale && (this._time = this.duration(), this._totalTime = this._totalDuration) : this._time = this._totalTime = this._duration = this._totalDuration = 0, this
                }, o.append = function(e, t) {
                    return this.add(e, this._parseTimeOrLabel(null, t, !0, e))
                }, o.insert = o.insertMultiple = function(e, t, o, s) {
                    return this.add(e, t || 0, o, s)
                }, o.appendMultiple = function(e, t, o, s) {
                    return this.add(e, this._parseTimeOrLabel(null, t, !0, e), o, s)
                }, o.addLabel = function(e, t) {
                    return this._labels[e] = this._parseTimeOrLabel(t), this
                }, o.addPause = function(e, t, o, s) {
                    var i = h.delayedCall(0, n, o, s || this);
                    return i.vars.onComplete = i.vars.onReverseComplete = t, i.data = "isPause", this._hasPause = !0, this.add(i, e)
                }, o.removeLabel = function(e) {
                    return delete this._labels[e], this
                }, o.getLabelTime = function(e) {
                    return null != this._labels[e] ? this._labels[e] : -1
                }, o._parseTimeOrLabel = function(e, t, o, s) {
                    var i;
                    if (s instanceof u && s.timeline === this) this.remove(s);
                    else if (s && (s instanceof Array || s.push && S(s)))
                        for (i = s.length; - 1 < --i;) s[i] instanceof u && s[i].timeline === this && this.remove(s[i]);
                    if ("string" == typeof t) return this._parseTimeOrLabel(t, o && "number" == typeof e && null == this._labels[t] ? e - this.duration() : 0, o);
                    if (t = t || 0, "string" != typeof e || !isNaN(e) && null == this._labels[e]) null == e && (e = this.duration());
                    else {
                        if (-1 === (i = e.indexOf("="))) return null == this._labels[e] ? o ? this._labels[e] = this.duration() + t : t : this._labels[e] + t;
                        t = parseInt(e.charAt(i - 1) + "1", 10) * Number(e.substr(i + 1)), e = 1 < i ? this._parseTimeOrLabel(e.substr(0, i - 1), 0, o) : this.duration()
                    }
                    return Number(e) + t
                }, o.seek = function(e, t) {
                    return this.totalTime("number" == typeof e ? e : this._parseTimeOrLabel(e), !1 !== t)
                }, o.stop = function() {
                    return this.paused(!0)
                }, o.gotoAndPlay = function(e, t) {
                    return this.play(e, t)
                }, o.gotoAndStop = function(e, t) {
                    return this.pause(e, t)
                }, o.render = function(e, t, o) {
                    this._gc && this._enabled(!0, !1);
                    var s, i, n, l, r, a, d, u = this._dirty ? this.totalDuration() : this._totalDuration,
                        c = this._time,
                        h = this._startTime,
                        _ = this._timeScale,
                        f = this._paused;
                    if (u - 1e-7 <= e) this._totalTime = this._time = u, this._reversed || this._hasPausedChild() || (i = !0, l = "onComplete", r = !!this._timeline.autoRemoveChildren, 0 === this._duration && (e <= 0 && -1e-7 <= e || this._rawPrevTime < 0 || this._rawPrevTime === b) && this._rawPrevTime !== e && this._first && (r = !0, this._rawPrevTime > b && (l = "onReverseComplete"))), this._rawPrevTime = this._duration || !t || e || this._rawPrevTime === e ? e : b, e = u + 1e-4;
                    else if (e < 1e-7)
                        if (this._totalTime = this._time = 0, (0 !== c || 0 === this._duration && this._rawPrevTime !== b && (0 < this._rawPrevTime || e < 0 && 0 <= this._rawPrevTime)) && (l = "onReverseComplete", i = this._reversed), e < 0) this._active = !1, this._timeline.autoRemoveChildren && this._reversed ? (r = i = !0, l = "onReverseComplete") : 0 <= this._rawPrevTime && this._first && (r = !0), this._rawPrevTime = e;
                        else {
                            if (this._rawPrevTime = this._duration || !t || e || this._rawPrevTime === e ? e : b, 0 === e && i)
                                for (s = this._first; s && 0 === s._startTime;) s._duration || (i = !1), s = s._next;
                            e = 0, this._initted || (r = !0)
                        }
                    else {
                        if (this._hasPause && !this._forcingPlayhead && !t) {
                            if (c <= e)
                                for (s = this._first; s && s._startTime <= e && !a;) s._duration || "isPause" !== s.data || s.ratio || 0 === s._startTime && 0 === this._rawPrevTime || (a = s), s = s._next;
                            else
                                for (s = this._last; s && s._startTime >= e && !a;) s._duration || "isPause" === s.data && 0 < s._rawPrevTime && (a = s), s = s._prev;
                            a && (this._time = e = a._startTime, this._totalTime = e + this._cycle * (this._totalDuration + this._repeatDelay))
                        }
                        this._totalTime = this._time = this._rawPrevTime = e
                    }
                    if (this._time !== c && this._first || o || r || a) {
                        if (this._initted || (this._initted = !0), this._active || !this._paused && this._time !== c && 0 < e && (this._active = !0), 0 === c && this.vars.onStart && (0 === this._time && this._duration || t || this._callback("onStart")), c <= (d = this._time))
                            for (s = this._first; s && (n = s._next, d === this._time && (!this._paused || f));)(s._active || s._startTime <= d && !s._paused && !s._gc) && (a === s && this.pause(), s._reversed ? s.render((s._dirty ? s.totalDuration() : s._totalDuration) - (e - s._startTime) * s._timeScale, t, o) : s.render((e - s._startTime) * s._timeScale, t, o)), s = n;
                        else
                            for (s = this._last; s && (n = s._prev, d === this._time && (!this._paused || f));) {
                                if (s._active || s._startTime <= c && !s._paused && !s._gc) {
                                    if (a === s) {
                                        for (a = s._prev; a && a.endTime() > this._time;) a.render(a._reversed ? a.totalDuration() - (e - a._startTime) * a._timeScale : (e - a._startTime) * a._timeScale, t, o), a = a._prev;
                                        a = null, this.pause()
                                    }
                                    s._reversed ? s.render((s._dirty ? s.totalDuration() : s._totalDuration) - (e - s._startTime) * s._timeScale, t, o) : s.render((e - s._startTime) * s._timeScale, t, o)
                                }
                                s = n
                            }
                        this._onUpdate && (t || (y.length && v(), this._callback("onUpdate"))), l && (this._gc || h !== this._startTime && _ === this._timeScale || (0 === this._time || u >= this.totalDuration()) && (i && (y.length && v(), this._timeline.autoRemoveChildren && this._enabled(!1, !1), this._active = !1), !t && this.vars[l] && this._callback(l)))
                    }
                }, o._hasPausedChild = function() {
                    for (var e = this._first; e;) {
                        if (e._paused || e instanceof _ && e._hasPausedChild()) return !0;
                        e = e._next
                    }
                    return !1
                }, o.getChildren = function(e, t, o, s) {
                    s = s || -9999999999;
                    for (var i = [], n = this._first, l = 0; n;) n._startTime < s || (n instanceof h ? !1 !== t && (i[l++] = n) : (!1 !== o && (i[l++] = n), !1 !== e && (l = (i = i.concat(n.getChildren(!0, t, o))).length))), n = n._next;
                    return i
                }, o.getTweensOf = function(e, t) {
                    var o, s, i = this._gc,
                        n = [],
                        l = 0;
                    for (i && this._enabled(!0, !0), s = (o = h.getTweensOf(e)).length; - 1 < --s;)(o[s].timeline === this || t && this._contains(o[s])) && (n[l++] = o[s]);
                    return i && this._enabled(!1, !0), n
                }, o.recent = function() {
                    return this._recent
                }, o._contains = function(e) {
                    for (var t = e.timeline; t;) {
                        if (t === this) return !0;
                        t = t.timeline
                    }
                    return !1
                }, o.shiftChildren = function(e, t, o) {
                    o = o || 0;
                    for (var s, i = this._first, n = this._labels; i;) i._startTime >= o && (i._startTime += e), i = i._next;
                    if (t)
                        for (s in n) n[s] >= o && (n[s] += e);
                    return this._uncache(!0)
                }, o._kill = function(e, t) {
                    if (!e && !t) return this._enabled(!1, !1);
                    for (var o = t ? this.getTweensOf(t) : this.getChildren(!0, !0, !1), s = o.length, i = !1; - 1 < --s;) o[s]._kill(e, t) && (i = !0);
                    return i
                }, o.clear = function(e) {
                    var t = this.getChildren(!1, !0, !0),
                        o = t.length;
                    for (this._time = this._totalTime = 0; - 1 < --o;) t[o]._enabled(!1, !1);
                    return !1 !== e && (this._labels = {}), this._uncache(!0)
                }, o.invalidate = function() {
                    for (var e = this._first; e;) e.invalidate(), e = e._next;
                    return u.prototype.invalidate.call(this)
                }, o._enabled = function(e, t) {
                    if (e === this._gc)
                        for (var o = this._first; o;) o._enabled(e, !0), o = o._next;
                    return c.prototype._enabled.call(this, e, t)
                }, o.totalTime = function(e, t, o) {
                    this._forcingPlayhead = !0;
                    var s = u.prototype.totalTime.apply(this, arguments);
                    return this._forcingPlayhead = !1, s
                }, o.duration = function(e) {
                    return arguments.length ? (0 !== this.duration() && 0 !== e && this.timeScale(this._duration / e), this) : (this._dirty && this.totalDuration(), this._duration)
                }, o.totalDuration = function(e) {
                    if (arguments.length) return e && this.totalDuration() ? this.timeScale(this._totalDuration / e) : this;
                    if (this._dirty) {
                        for (var t, o, s = 0, i = this._last, n = 999999999999; i;) t = i._prev, i._dirty && i.totalDuration(), i._startTime > n && this._sortChildren && !i._paused ? this.add(i, i._startTime - i._delay) : n = i._startTime, i._startTime < 0 && !i._paused && (s -= i._startTime, this._timeline.smoothChildTiming && (this._startTime += i._startTime / this._timeScale), this.shiftChildren(-i._startTime, !1, -9999999999), n = 0), s < (o = i._startTime + i._totalDuration / i._timeScale) && (s = o), i = t;
                        this._duration = this._totalDuration = s, this._dirty = !1
                    }
                    return this._totalDuration
                }, o.paused = function(e) {
                    if (!e)
                        for (var t = this._first, o = this._time; t;) t._startTime === o && "isPause" === t.data && (t._rawPrevTime = 0), t = t._next;
                    return u.prototype.paused.apply(this, arguments)
                }, o.usesFrames = function() {
                    for (var e = this._timeline; e._timeline;) e = e._timeline;
                    return e === u._rootFramesTimeline
                }, o.rawTime = function() {
                    return this._paused ? this._totalTime : (this._timeline.rawTime() - this._startTime) * this._timeScale
                }, _
            }, !0), _fwd_gsScope._gsDefine("TimelineMax", ["TimelineLite", "FWDTweenLite", "easing.Ease"], function(t, r, e) {
                function o(e) {
                    t.call(this, e), this._repeat = this.vars.repeat || 0, this._repeatDelay = this.vars.repeatDelay || 0, this._cycle = 0, this._yoyo = !0 === this.vars.yoyo, this._dirty = !0
                }
                var B = 1e-10,
                    s = r._internals,
                    M = s.lazyTweens,
                    F = s.lazyRender,
                    a = _fwd_gsScope._gsDefine.globals,
                    d = new e(null, null, 1, 0),
                    i = o.prototype = new t;
                return i.constructor = o, i.kill()._gc = !1, o.version = "1.19.0", i.invalidate = function() {
                    return this._yoyo = !0 === this.vars.yoyo, this._repeat = this.vars.repeat || 0, this._repeatDelay = this.vars.repeatDelay || 0, this._uncache(!0), t.prototype.invalidate.call(this)
                }, i.addCallback = function(e, t, o, s) {
                    return this.add(r.delayedCall(0, e, o, s), t)
                }, i.removeCallback = function(e, t) {
                    if (e)
                        if (null == t) this._kill(null, e);
                        else
                            for (var o = this.getTweensOf(e, !1), s = o.length, i = this._parseTimeOrLabel(t); - 1 < --s;) o[s]._startTime === i && o[s]._enabled(!1, !1);
                    return this
                }, i.removePause = function(e) {
                    return this.removeCallback(t._internals.pauseCallback, e)
                }, i.tweenTo = function(e, t) {
                    t = t || {};
                    var o, s, i, n = {
                            ease: d,
                            useFrames: this.usesFrames(),
                            immediateRender: !1
                        },
                        l = t.repeat && a.FWDAnimation || r;
                    for (s in t) n[s] = t[s];
                    return n.time = this._parseTimeOrLabel(e), o = Math.abs(Number(n.time) - this._time) / this._timeScale || .001, i = new l(this, o, n), n.onStart = function() {
                        i.target.paused(!0), i.vars.time !== i.target.time() && o === i.duration() && i.duration(Math.abs(i.vars.time - i.target.time()) / i.target._timeScale), t.onStart && i._callback("onStart")
                    }, i
                }, i.tweenFromTo = function(e, t, o) {
                    o = o || {}, e = this._parseTimeOrLabel(e), o.startAt = {
                        onComplete: this.seek,
                        onCompleteParams: [e],
                        callbackScope: this
                    }, o.immediateRender = !1 !== o.immediateRender;
                    var s = this.tweenTo(t, o);
                    return s.duration(Math.abs(s.vars.time - e) / this._timeScale || .001)
                }, i.render = function(e, t, o) {
                    this._gc && this._enabled(!0, !1);
                    var s, i, n, l, r, a, d, u, c = this._dirty ? this.totalDuration() : this._totalDuration,
                        h = this._duration,
                        _ = this._time,
                        f = this._totalTime,
                        p = this._startTime,
                        m = this._timeScale,
                        b = this._rawPrevTime,
                        g = this._paused,
                        S = this._cycle;
                    if (c - 1e-7 <= e) this._locked || (this._totalTime = c, this._cycle = this._repeat), this._reversed || this._hasPausedChild() || (i = !0, l = "onComplete", r = !!this._timeline.autoRemoveChildren, 0 === this._duration && (e <= 0 && -1e-7 <= e || b < 0 || b === B) && b !== e && this._first && (r = !0, B < b && (l = "onReverseComplete"))), this._rawPrevTime = this._duration || !t || e || this._rawPrevTime === e ? e : B, this._yoyo && 0 != (1 & this._cycle) ? this._time = e = 0 : e = (this._time = h) + 1e-4;
                    else if (e < 1e-7)
                        if (this._locked || (this._totalTime = this._cycle = 0), ((this._time = 0) !== _ || 0 === h && b !== B && (0 < b || e < 0 && 0 <= b) && !this._locked) && (l = "onReverseComplete", i = this._reversed), e < 0) this._active = !1, this._timeline.autoRemoveChildren && this._reversed ? (r = i = !0, l = "onReverseComplete") : 0 <= b && this._first && (r = !0), this._rawPrevTime = e;
                        else {
                            if (this._rawPrevTime = h || !t || e || this._rawPrevTime === e ? e : B, 0 === e && i)
                                for (s = this._first; s && 0 === s._startTime;) s._duration || (i = !1), s = s._next;
                            e = 0, this._initted || (r = !0)
                        }
                    else if (0 === h && b < 0 && (r = !0), this._time = this._rawPrevTime = e, this._locked || (this._totalTime = e, 0 !== this._repeat && (a = h + this._repeatDelay, this._cycle = this._totalTime / a >> 0, 0 !== this._cycle && this._cycle === this._totalTime / a && f <= e && this._cycle--, this._time = this._totalTime - this._cycle * a, this._yoyo && 0 != (1 & this._cycle) && (this._time = h - this._time), this._time > h ? e = (this._time = h) + 1e-4 : this._time < 0 ? this._time = e = 0 : e = this._time)), this._hasPause && !this._forcingPlayhead && !t) {
                        if (_ <= (e = this._time))
                            for (s = this._first; s && s._startTime <= e && !d;) s._duration || "isPause" !== s.data || s.ratio || 0 === s._startTime && 0 === this._rawPrevTime || (d = s), s = s._next;
                        else
                            for (s = this._last; s && s._startTime >= e && !d;) s._duration || "isPause" === s.data && 0 < s._rawPrevTime && (d = s), s = s._prev;
                        d && (this._time = e = d._startTime, this._totalTime = e + this._cycle * (this._totalDuration + this._repeatDelay))
                    }
                    if (this._cycle !== S && !this._locked) {
                        var y = this._yoyo && 0 != (1 & S),
                            v = y === (this._yoyo && 0 != (1 & this._cycle)),
                            P = this._totalTime,
                            T = this._cycle,
                            w = this._rawPrevTime,
                            D = this._time;
                        if (this._totalTime = S * h, this._cycle < S ? y = !y : this._totalTime += h, this._time = _, this._rawPrevTime = 0 === h ? b - 1e-4 : b, this._cycle = S, this._locked = !0, _ = y ? 0 : h, this.render(_, t, 0 === h), t || this._gc || this.vars.onRepeat && this._callback("onRepeat"), _ !== this._time) return;
                        if (v && (_ = y ? h + 1e-4 : -1e-4, this.render(_, !0, !1)), this._locked = !1, this._paused && !g) return;
                        this._time = D, this._totalTime = P, this._cycle = T, this._rawPrevTime = w
                    }
                    if (this._time !== _ && this._first || o || r || d) {
                        if (this._initted || (this._initted = !0), this._active || !this._paused && this._totalTime !== f && 0 < e && (this._active = !0), 0 === f && this.vars.onStart && (0 === this._totalTime && this._totalDuration || t || this._callback("onStart")), _ <= (u = this._time))
                            for (s = this._first; s && (n = s._next, u === this._time && (!this._paused || g));)(s._active || s._startTime <= this._time && !s._paused && !s._gc) && (d === s && this.pause(), s._reversed ? s.render((s._dirty ? s.totalDuration() : s._totalDuration) - (e - s._startTime) * s._timeScale, t, o) : s.render((e - s._startTime) * s._timeScale, t, o)), s = n;
                        else
                            for (s = this._last; s && (n = s._prev, u === this._time && (!this._paused || g));) {
                                if (s._active || s._startTime <= _ && !s._paused && !s._gc) {
                                    if (d === s) {
                                        for (d = s._prev; d && d.endTime() > this._time;) d.render(d._reversed ? d.totalDuration() - (e - d._startTime) * d._timeScale : (e - d._startTime) * d._timeScale, t, o), d = d._prev;
                                        d = null, this.pause()
                                    }
                                    s._reversed ? s.render((s._dirty ? s.totalDuration() : s._totalDuration) - (e - s._startTime) * s._timeScale, t, o) : s.render((e - s._startTime) * s._timeScale, t, o)
                                }
                                s = n
                            }
                        this._onUpdate && (t || (M.length && F(), this._callback("onUpdate"))), l && (this._locked || this._gc || p !== this._startTime && m === this._timeScale || (0 === this._time || c >= this.totalDuration()) && (i && (M.length && F(), this._timeline.autoRemoveChildren && this._enabled(!1, !1), this._active = !1), !t && this.vars[l] && this._callback(l)))
                    } else f !== this._totalTime && this._onUpdate && (t || this._callback("onUpdate"))
                }, i.getActive = function(e, t, o) {
                    null == e && (e = !0), null == t && (t = !0), null == o && (o = !1);
                    var s, i, n = [],
                        l = this.getChildren(e, t, o),
                        r = 0,
                        a = l.length;
                    for (s = 0; s < a; s++)(i = l[s]).isActive() && (n[r++] = i);
                    return n
                }, i.getLabelAfter = function(e) {
                    e || 0 !== e && (e = this._time);
                    var t, o = this.getLabelsArray(),
                        s = o.length;
                    for (t = 0; t < s; t++)
                        if (o[t].time > e) return o[t].name;
                    return null
                }, i.getLabelBefore = function(e) {
                    null == e && (e = this._time);
                    for (var t = this.getLabelsArray(), o = t.length; - 1 < --o;)
                        if (t[o].time < e) return t[o].name;
                    return null
                }, i.getLabelsArray = function() {
                    var e, t = [],
                        o = 0;
                    for (e in this._labels) t[o++] = {
                        time: this._labels[e],
                        name: e
                    };
                    return t.sort(function(e, t) {
                        return e.time - t.time
                    }), t
                }, i.progress = function(e, t) {
                    return arguments.length ? this.totalTime(this.duration() * (this._yoyo && 0 != (1 & this._cycle) ? 1 - e : e) + this._cycle * (this._duration + this._repeatDelay), t) : this._time / this.duration()
                }, i.totalProgress = function(e, t) {
                    return arguments.length ? this.totalTime(this.totalDuration() * e, t) : this._totalTime / this.totalDuration()
                }, i.totalDuration = function(e) {
                    return arguments.length ? -1 !== this._repeat && e ? this.timeScale(this.totalDuration() / e) : this : (this._dirty && (t.prototype.totalDuration.call(this), this._totalDuration = -1 === this._repeat ? 999999999999 : this._duration * (this._repeat + 1) + this._repeatDelay * this._repeat), this._totalDuration)
                }, i.time = function(e, t) {
                    return arguments.length ? (this._dirty && this.totalDuration(), e > this._duration && (e = this._duration), this._yoyo && 0 != (1 & this._cycle) ? e = this._duration - e + this._cycle * (this._duration + this._repeatDelay) : 0 !== this._repeat && (e += this._cycle * (this._duration + this._repeatDelay)), this.totalTime(e, t)) : this._time
                }, i.repeat = function(e) {
                    return arguments.length ? (this._repeat = e, this._uncache(!0)) : this._repeat
                }, i.repeatDelay = function(e) {
                    return arguments.length ? (this._repeatDelay = e, this._uncache(!0)) : this._repeatDelay
                }, i.yoyo = function(e) {
                    return arguments.length ? (this._yoyo = e, this) : this._yoyo
                }, i.currentLabel = function(e) {
                    return arguments.length ? this.seek(e, !0) : this.getLabelBefore(this._time + 1e-8)
                }, o
            }, !0), T = 180 / Math.PI, P = [], w = [], D = [], y = {}, o = _fwd_gsScope._gsDefine.globals, m = _fwd_gsScope._gsDefine.plugin({
                propName: "bezier",
                priority: -1,
                version: "1.3.7",
                API: 2,
                fwd_global: !0,
                init: function(e, t, o) {
                    this._target = e, t instanceof Array && (t = {
                        values: t
                    }), this._func = {}, this._mod = {}, this._props = [], this._timeRes = null == t.timeResolution ? 6 : parseInt(t.timeResolution, 10);
                    var s, i, n, l, r, a = t.values || [],
                        d = {},
                        u = a[0],
                        c = t.autoRotate || o.vars.orientToBezier;
                    for (s in this._autoRotate = c ? c instanceof Array ? c : [
                            ["x", "y", "rotation", !0 === c ? 0 : Number(c) || 0]
                        ] : null, u) this._props.push(s);
                    for (n = this._props.length; - 1 < --n;) s = this._props[n], this._overwriteProps.push(s), i = this._func[s] = "function" == typeof e[s], d[s] = i ? e[s.indexOf("set") || "function" != typeof e["get" + s.substr(3)] ? s : "get" + s.substr(3)]() : parseFloat(e[s]), r || d[s] !== a[0][s] && (r = d);
                    if (this._beziers = "cubic" !== t.type && "quadratic" !== t.type && "soft" !== t.type ? _(a, isNaN(t.curviness) ? 1 : t.curviness, !1, "thruBasic" === t.type, t.correlate, r) : function(e, t, o) {
                            var s, i, n, l, r, a, d, u, c, h, _, f = {},
                                p = "cubic" === (t = t || "soft") ? 3 : 2,
                                m = "soft" === t,
                                b = [];
                            if (m && o && (e = [o].concat(e)), null == e || e.length < 1 + p) throw "invalid Bezier data";
                            for (c in e[0]) b.push(c);
                            for (a = b.length; - 1 < --a;) {
                                for (f[c = b[a]] = r = [], h = 0, u = e.length, d = 0; d < u; d++) s = null == o ? e[d][c] : "string" == typeof(_ = e[d][c]) && "=" === _.charAt(1) ? o[c] + Number(_.charAt(0) + _.substr(2)) : Number(_), m && 1 < d && d < u - 1 && (r[h++] = (s + r[h - 2]) / 2), r[h++] = s;
                                for (u = h - p + 1, d = h = 0; d < u; d += p) s = r[d], i = r[d + 1], n = r[d + 2], l = 2 == p ? 0 : r[d + 3], r[h++] = _ = 3 == p ? new g(s, i, n, l) : new g(s, (2 * i + s) / 3, (2 * i + n) / 3, n);
                                r.length = h
                            }
                            return f
                        }(a, t.type, d), this._segCount = this._beziers[s].length, this._timeRes) {
                        var h = function(e, t) {
                            var o, s, i, n, l = [],
                                r = [],
                                a = 0,
                                d = 0,
                                u = (t = t >> 0 || 6) - 1,
                                c = [],
                                h = [];
                            for (o in e) f(e[o], l, t);
                            for (i = l.length, s = 0; s < i; s++) a += Math.sqrt(l[s]), h[n = s % t] = a, n === u && (d += a, c[n = s / t >> 0] = h, r[n] = d, a = 0, h = []);
                            return {
                                length: d,
                                lengths: r,
                                segments: c
                            }
                        }(this._beziers, this._timeRes);
                        this._length = h.length, this._lengths = h.lengths, this._segments = h.segments, this._l1 = this._li = this._s1 = this._si = 0, this._l2 = this._lengths[0], this._curSeg = this._segments[0], this._s2 = this._curSeg[0], this._prec = 1 / this._curSeg.length
                    }
                    if (c = this._autoRotate)
                        for (this._initialRotations = [], c[0] instanceof Array || (this._autoRotate = c = [c]), n = c.length; - 1 < --n;) {
                            for (l = 0; l < 3; l++) s = c[n][l], this._func[s] = "function" == typeof e[s] && e[s.indexOf("set") || "function" != typeof e["get" + s.substr(3)] ? s : "get" + s.substr(3)];
                            s = c[n][2], this._initialRotations[n] = (this._func[s] ? this._func[s].call(this._target) : this._target[s]) || 0, this._overwriteProps.push(s)
                        }
                    return this._startRatio = o.vars.runBackwards ? 1 : 0, !0
                },
                set: function(e) {
                    var t, o, s, i, n, l, r, a, d, u, c = this._segCount,
                        h = this._func,
                        _ = this._target,
                        f = e !== this._startRatio;
                    if (this._timeRes) {
                        if (d = this._lengths, u = this._curSeg, e *= this._length, s = this._li, e > this._l2 && s < c - 1) {
                            for (a = c - 1; s < a && (this._l2 = d[++s]) <= e;);
                            this._l1 = d[s - 1], this._li = s, this._curSeg = u = this._segments[s], this._s2 = u[this._s1 = this._si = 0]
                        } else if (e < this._l1 && 0 < s) {
                            for (; 0 < s && (this._l1 = d[--s]) >= e;);
                            0 === s && e < this._l1 ? this._l1 = 0 : s++, this._l2 = d[s], this._li = s, this._curSeg = u = this._segments[s], this._s1 = u[(this._si = u.length - 1) - 1] || 0, this._s2 = u[this._si]
                        }
                        if (t = s, e -= this._l1, s = this._si, e > this._s2 && s < u.length - 1) {
                            for (a = u.length - 1; s < a && (this._s2 = u[++s]) <= e;);
                            this._s1 = u[s - 1], this._si = s
                        } else if (e < this._s1 && 0 < s) {
                            for (; 0 < s && (this._s1 = u[--s]) >= e;);
                            0 === s && e < this._s1 ? this._s1 = 0 : s++, this._s2 = u[s], this._si = s
                        }
                        l = (s + (e - this._s1) / (this._s2 - this._s1)) * this._prec || 0
                    } else l = (e - (t = e < 0 ? 0 : 1 <= e ? c - 1 : c * e >> 0) * (1 / c)) * c;
                    for (o = 1 - l, s = this._props.length; - 1 < --s;) i = this._props[s], r = (l * l * (n = this._beziers[i][t]).da + 3 * o * (l * n.ca + o * n.ba)) * l + n.a, this._mod[i] && (r = this._mod[i](r, _)), h[i] ? _[i](r) : "x" == i ? _.setX(r) : "y" == i ? _.setY(r) : "z" == i ? _.setZ(r) : "angleX" == i ? _.setAngleX(r) : "angleY" == i ? _.setAngleY(r) : "angleZ" == i ? _.setAngleZ(r) : "w" == i ? _.setWidth(r) : "h" == i ? _.setHeight(r) : "alpha" == i ? _.setAlpha(r) : "scale" == i ? _.setScale2(r) : _[i] = r;
                    if (this._autoRotate) {
                        var p, m, b, g, S, y, v, P = this._autoRotate;
                        for (s = P.length; - 1 < --s;) i = P[s][2], y = P[s][3] || 0, v = !0 === P[s][4] ? 1 : T, n = this._beziers[P[s][0]], p = this._beziers[P[s][1]], n && p && (n = n[t], p = p[t], m = n.a + (n.b - n.a) * l, m += ((g = n.b + (n.c - n.b) * l) - m) * l, g += (n.c + (n.d - n.c) * l - g) * l, b = p.a + (p.b - p.a) * l, b += ((S = p.b + (p.c - p.b) * l) - b) * l, S += (p.c + (p.d - p.c) * l - S) * l, r = f ? Math.atan2(S - b, g - m) * v + y : this._initialRotations[s], this._mod[i] && (r = this._mod[i](r, _)), h[i] ? _[i](r) : _[i] = r)
                    }
                }
            }), e = m.prototype, m.bezierThrough = _, m.cubicToQuadratic = v, m._autoCSS = !0, m.quadraticToCubic = function(e, t, o) {
                return new g(e, (2 * t + e) / 3, (2 * t + o) / 3, o)
            }, m._cssRegister = function() {
                var e = o.CSSPlugin;
                if (e) {
                    var t = e._internals,
                        _ = t._parseToProxy,
                        f = t._setPluginRatio,
                        p = t.CSSPropTween;
                    t._registerComplexSpecialProp("bezier", {
                        parser: function(e, t, o, s, i, n) {
                            t instanceof Array && (t = {
                                values: t
                            }), n = new m;
                            var l, r, a, d = t.values,
                                u = d.length - 1,
                                c = [],
                                h = {};
                            if (u < 0) return i;
                            for (l = 0; l <= u; l++) a = _(e, d[l], s, i, n, u !== l), c[l] = a.end;
                            for (r in t) h[r] = t[r];
                            return h.values = c, (i = new p(e, "bezier", 0, 0, a.pt, 2)).data = a, i.plugin = n, i.setRatio = f, 0 === h.autoRotate && (h.autoRotate = !0), !h.autoRotate || h.autoRotate instanceof Array || (l = !0 === h.autoRotate ? 0 : Number(h.autoRotate), h.autoRotate = null != a.end.left ? [
                                ["left", "top", "rotation", l, !1]
                            ] : null != a.end.x && [
                                ["x", "y", "rotation", l, !1]
                            ]), h.autoRotate && (s._transform || s._enableTransforms(!1), a.autoRotate = s._target._gsTransform, a.proxy.rotation = a.autoRotate.rotation || 0, s._overwriteProps.push("rotation")), n._onInitTween(a.proxy, h, s._tween), i
                        }
                    })
                }
            }, e._mod = function(e) {
                for (var t, o = this._overwriteProps, s = o.length; - 1 < --s;)(t = e[o[s]]) && "function" == typeof t && (this._mod[o[s]] = t)
            }, e._kill = function(e) {
                var t, o, s = this._props;
                for (t in this._beziers)
                    if (t in e)
                        for (delete this._beziers[t], delete this._func[t], o = s.length; - 1 < --o;) s[o] === t && s.splice(o, 1);
                if (s = this._autoRotate)
                    for (o = s.length; - 1 < --o;) e[s[o][2]] && s.splice(o, 1);
                return this._super._kill.call(this, e)
            }, _fwd_gsScope._gsDefine("plugins.CSSPlugin", ["plugins.TweenPlugin", "FWDTweenLite"], function(n, U) {
                var f, w, D, p, N = function() {
                        n.call(this, "css"), this._overwriteProps.length = 0, this.setRatio = N.prototype.setRatio
                    },
                    d = _fwd_gsScope._gsDefine.globals,
                    m = {},
                    e = N.prototype = new n("css");
                (e.constructor = N).version = "1.19.0", N.API = 2, N.defaultTransformPerspective = 0, N.defaultSkewType = "compensated", N.defaultSmoothOrigin = !0, e = "px", N.suffixMap = {
                    top: e,
                    right: e,
                    bottom: e,
                    left: e,
                    width: e,
                    height: e,
                    fontSize: e,
                    padding: e,
                    margin: e,
                    perspective: e,
                    lineHeight: ""
                };

                function l(e, t) {
                    return t.toUpperCase()
                }

                function t(e) {
                    return Z.createElementNS ? Z.createElementNS("http://www.w3.org/1999/xhtml", e) : Z.createElement(e)
                }

                function r(e) {
                    return R.test("string" == typeof e ? e : (e.currentStyle ? e.currentStyle.filter : e.style.filter) || "") ? parseFloat(RegExp.$1) / 100 : 1
                }

                function b(e) {
                    window.console && console.log(e)
                }

                function B(e, t) {
                    var o, s, i = (t = t || ee).style;
                    if (void 0 !== i[e]) return e;
                    for (e = e.charAt(0).toUpperCase() + e.substr(1), o = ["O", "Moz", "ms", "Ms", "Webkit"], s = 5; - 1 < --s && void 0 === i[o[s] + e];);
                    return 0 <= s ? (ne = "-" + (le = 3 === s ? "ms" : o[s]).toLowerCase() + "-", le + e) : null
                }

                function g(e, t) {
                    var o, s, i, n = {};
                    if (t = t || re(e, null))
                        if (o = t.length)
                            for (; - 1 < --o;) - 1 !== (i = t[o]).indexOf("-transform") && xe !== i || (n[i.replace(h, l)] = t.getPropertyValue(i));
                        else
                            for (o in t) - 1 !== o.indexOf("Transform") && Ie !== o || (n[o] = t[o]);
                    else if (t = e.currentStyle || e.style)
                        for (o in t) "string" == typeof o && void 0 === n[o] && (n[o.replace(h, l)] = t[o]);
                    return ie || (n.opacity = r(e)), s = Ge(e, t, !1), n.rotation = s.rotation, n.skewX = s.skewX, n.scaleX = s.scaleX, n.scaleY = s.scaleY, n.x = s.x, n.y = s.y, Re && (n.z = s.z, n.rotationX = s.rotationX, n.rotationY = s.rotationY, n.scaleZ = s.scaleZ), n.filters && delete n.filters, n
                }

                function S(e, t, o, s, i) {
                    var n, l, r, a = {},
                        d = e.style;
                    for (l in o) "cssText" !== l && "length" !== l && isNaN(l) && (t[l] !== (n = o[l]) || i && i[l]) && -1 === l.indexOf("Origin") && ("number" != typeof n && "string" != typeof n || (a[l] = "auto" !== n || "left" !== l && "top" !== l ? "" !== n && "auto" !== n && "none" !== n || "string" != typeof t[l] || "" === t[l].replace(u, "") ? n : 0 : ue(e, l), void 0 !== d[l] && (r = new ye(d, l, d[l], r))));
                    if (s)
                        for (l in s) "className" !== l && (a[l] = s[l]);
                    return {
                        difs: a,
                        firstMPT: r
                    }
                }

                function y(e, t, o) {
                    if ("svg" === (e.nodeName + "").toLowerCase()) return (o || re(e))[t] || 0;
                    if (e.getBBox && Ve(e)) return e.getBBox()[t] || 0;
                    var s = parseFloat("width" === t ? e.offsetWidth : e.offsetHeight),
                        i = ce[t],
                        n = i.length;
                    for (o = o || re(e, null); - 1 < --n;) s -= parseFloat(ae(e, "padding" + i[n], o, !0)) || 0, s -= parseFloat(ae(e, "border" + i[n] + "Width", o, !0)) || 0;
                    return s
                }

                function M(e, t) {
                    return "function" == typeof e && (e = e(O, E)), "string" == typeof e && "=" === e.charAt(1) ? parseInt(e.charAt(0) + "1", 10) * parseFloat(e.substr(2)) : parseFloat(e) - parseFloat(t) || 0
                }

                function F(e, t) {
                    return "function" == typeof e && (e = e(O, E)), null == e ? t : "string" == typeof e && "=" === e.charAt(1) ? parseInt(e.charAt(0) + "1", 10) * parseFloat(e.substr(2)) + t : parseFloat(e) || 0
                }

                function W(e, t, o, s) {
                    var i, n, l, r, a;
                    return "function" == typeof e && (e = e(O, E)), (r = null == e ? t : "number" == typeof e ? e : (i = 360, n = e.split("_"), l = ((a = "=" === e.charAt(1)) ? parseInt(e.charAt(0) + "1", 10) * parseFloat(n[0].substr(2)) : parseFloat(n[0])) * (-1 === e.indexOf("rad") ? 1 : Q) - (a ? 0 : t), n.length && (s && (s[o] = t + l), -1 !== e.indexOf("short") && (l %= i) !== l % 180 && (l = l < 0 ? l + i : l - i), -1 !== e.indexOf("_cw") && l < 0 ? l = (l + 3599999999640) % i - (l / i | 0) * i : -1 !== e.indexOf("ccw") && 0 < l && (l = (l - 3599999999640) % i - (l / i | 0) * i)), t + l)) < 1e-6 && -1e-6 < r && (r = 0), r
                }

                function _(e, t, o) {
                    return 255 * (6 * (e = e < 0 ? e + 1 : 1 < e ? e - 1 : e) < 1 ? t + (o - t) * e * 6 : e < .5 ? o : 3 * e < 2 ? t + (o - t) * (2 / 3 - e) * 6 : t) + .5 | 0
                }

                function s(e, t) {
                    var o, s, i, n = e.match(me) || [],
                        l = 0,
                        r = n.length ? "" : e;
                    for (o = 0; o < n.length; o++) s = n[o], l += (i = e.substr(l, e.indexOf(s, l) - l)).length + s.length, 3 === (s = pe(s, t)).length && s.push(1), r += i + (t ? "hsla(" + s[0] + "," + s[1] + "%," + s[2] + "%," + s[3] : "rgba(" + s.join(",")) + ")";
                    return r + e.substr(l)
                }
                var H, v, P, A, T, C, E, O, o, i, k = /(?:\-|\.|\b)(\d|\.|e\-)+/g,
                    L = /(?:\d|\-\d|\.\d|\-\.\d|\+=\d|\-=\d|\+=.\d|\-=\.\d)+/g,
                    I = /(?:\+=|\-=|\-|\b)[\d\-\.]+[a-zA-Z0-9]*(?:%|\b)/gi,
                    u = /(?![+-]?\d*\.?\d+|[+-]|e[+-]\d+)[^0-9]/g,
                    x = /(?:\d|\-|\+|=|#|\.)*/g,
                    R = /opacity *= *([^)]*)/i,
                    Y = /opacity:([^;]*)/i,
                    a = /alpha\(opacity *=.+?\)/i,
                    X = /^(rgb|hsl)/,
                    c = /([A-Z])/g,
                    h = /-([a-z])/gi,
                    V = /(^(?:url\(\"|url\())|(?:(\"\))$|\)$)/gi,
                    j = /(?:Left|Right|Width)/i,
                    z = /(M11|M12|M21|M22)=[\d\-\.e]+/gi,
                    G = /progid\:DXImageTransform\.Microsoft\.Matrix\(.+?\)/i,
                    q = /,(?=[^\)]*(?:\(|$))/gi,
                    K = /[\s,\(]/i,
                    J = Math.PI / 180,
                    Q = 180 / Math.PI,
                    $ = {},
                    Z = document,
                    ee = t("div"),
                    te = t("img"),
                    oe = N._internals = {
                        _specialProps: m
                    },
                    se = navigator.userAgent,
                    ie = (o = se.indexOf("Android"), i = t("a"), P = -1 !== se.indexOf("Safari") && -1 === se.indexOf("Chrome") && (-1 === o || 3 < Number(se.substr(o + 8, 1))), T = P && Number(se.substr(se.indexOf("Version/") + 8, 1)) < 6, A = -1 !== se.indexOf("Firefox"), (/MSIE ([0-9]{1,}[\.0-9]{0,})/.exec(se) || /Trident\/.*rv:([0-9]{1,}[\.0-9]{0,})/.exec(se)) && (C = parseFloat(RegExp.$1)), !!i && (i.style.cssText = "top:1px;opacity:.55;", /^0.55/.test(i.style.opacity))),
                    ne = "",
                    le = "",
                    re = Z.defaultView ? Z.defaultView.getComputedStyle : function() {},
                    ae = N.getStyle = function(e, t, o, s, i) {
                        var n;
                        return ie || "opacity" !== t ? (!s && e.style[t] ? n = e.style[t] : (o = o || re(e)) ? n = o[t] || o.getPropertyValue(t) || o.getPropertyValue(t.replace(c, "-$1").toLowerCase()) : e.currentStyle && (n = e.currentStyle[t]), null == i || n && "none" !== n && "auto" !== n && "auto auto" !== n ? n : i) : r(e)
                    },
                    de = oe.convertToPixels = function(e, t, o, s, i) {
                        if ("px" === s || !s) return o;
                        if ("auto" === s || !o) return 0;
                        var n, l, r, a = j.test(t),
                            d = e,
                            u = ee.style,
                            c = o < 0,
                            h = 1 === o;
                        if (c && (o = -o), h && (o *= 100), "%" === s && -1 !== t.indexOf("border")) n = o / 100 * (a ? e.clientWidth : e.clientHeight);
                        else {
                            if (u.cssText = "border:0 solid red;position:" + ae(e, "position") + ";line-height:0;", "%" !== s && d.appendChild && "v" !== s.charAt(0) && "rem" !== s) u[a ? "borderLeftWidth" : "borderTopWidth"] = o + s;
                            else {
                                if (l = (d = e.parentNode || Z.body)._gsCache, r = U.ticker.frame, l && a && l.time === r) return l.width * o / 100;
                                u[a ? "width" : "height"] = o + s
                            }
                            d.appendChild(ee), n = parseFloat(ee[a ? "offsetWidth" : "offsetHeight"]), d.removeChild(ee), a && "%" === s && !1 !== N.cacheWidths && ((l = d._gsCache = d._gsCache || {}).time = r, l.width = n / o * 100), 0 !== n || i || (n = de(e, t, o, s, !0))
                        }
                        return h && (n /= 100), c ? -n : n
                    },
                    ue = oe.calculateOffset = function(e, t, o) {
                        if ("absolute" !== ae(e, "position", o)) return 0;
                        var s = "left" === t ? "Left" : "Top",
                            i = ae(e, "margin" + s, o);
                        return e["offset" + s] - (de(e, t, parseFloat(i), i.replace(x, "")) || 0)
                    },
                    ce = {
                        width: ["Left", "Right"],
                        height: ["Top", "Bottom"]
                    },
                    he = ["marginLeft", "marginRight", "marginTop", "marginBottom"],
                    _e = function(e, t) {
                        if ("contain" === e || "auto" === e || "auto auto" === e) return e + " ";
                        null != e && "" !== e || (e = "0 0");
                        var o, s = e.split(" "),
                            i = -1 !== e.indexOf("left") ? "0%" : -1 !== e.indexOf("right") ? "100%" : s[0],
                            n = -1 !== e.indexOf("top") ? "0%" : -1 !== e.indexOf("bottom") ? "100%" : s[1];
                        if (3 < s.length && !t) {
                            for (s = e.split(", ").join(",").split(","), e = [], o = 0; o < s.length; o++) e.push(_e(s[o]));
                            return e.join(",")
                        }
                        return null == n ? n = "center" === i ? "50%" : "0" : "center" === n && (n = "50%"), ("center" === i || isNaN(parseFloat(i)) && -1 === (i + "").indexOf("=")) && (i = "50%"), e = i + " " + n + (2 < s.length ? " " + s[2] : ""), t && (t.oxp = -1 !== i.indexOf("%"), t.oyp = -1 !== n.indexOf("%"), t.oxr = "=" === i.charAt(1), t.oyr = "=" === n.charAt(1), t.ox = parseFloat(i.replace(u, "")), t.oy = parseFloat(n.replace(u, "")), t.v = e), t || e
                    },
                    fe = {
                        aqua: [0, 255, 255],
                        lime: [0, 255, 0],
                        silver: [192, 192, 192],
                        black: [0, 0, 0],
                        maroon: [128, 0, 0],
                        teal: [0, 128, 128],
                        blue: [0, 0, 255],
                        navy: [0, 0, 128],
                        white: [255, 255, 255],
                        fuchsia: [255, 0, 255],
                        olive: [128, 128, 0],
                        yellow: [255, 255, 0],
                        orange: [255, 165, 0],
                        gray: [128, 128, 128],
                        purple: [128, 0, 128],
                        green: [0, 128, 0],
                        red: [255, 0, 0],
                        pink: [255, 192, 203],
                        cyan: [0, 255, 255],
                        transparent: [255, 255, 255, 0]
                    },
                    pe = N.parseColor = function(e, t) {
                        var o, s, i, n, l, r, a, d, u, c, h;
                        if (e)
                            if ("number" == typeof e) o = [e >> 16, e >> 8 & 255, 255 & e];
                            else {
                                if ("," === e.charAt(e.length - 1) && (e = e.substr(0, e.length - 1)), fe[e]) o = fe[e];
                                else if ("#" === e.charAt(0)) 4 === e.length && (e = "#" + (s = e.charAt(1)) + s + (i = e.charAt(2)) + i + (n = e.charAt(3)) + n), o = [(e = parseInt(e.substr(1), 16)) >> 16, e >> 8 & 255, 255 & e];
                                else if ("hsl" === e.substr(0, 3))
                                    if (o = h = e.match(k), t) {
                                        if (-1 !== e.indexOf("=")) return e.match(L)
                                    } else l = Number(o[0]) % 360 / 360, r = Number(o[1]) / 100, s = 2 * (a = Number(o[2]) / 100) - (i = a <= .5 ? a * (r + 1) : a + r - a * r), 3 < o.length && (o[3] = Number(e[3])), o[0] = _(l + 1 / 3, s, i), o[1] = _(l, s, i), o[2] = _(l - 1 / 3, s, i);
                                else o = e.match(k) || fe.transparent;
                                o[0] = Number(o[0]), o[1] = Number(o[1]), o[2] = Number(o[2]), 3 < o.length && (o[3] = Number(o[3]))
                            }
                        else o = fe.black;
                        return t && !h && (s = o[0] / 255, i = o[1] / 255, n = o[2] / 255, a = ((d = Math.max(s, i, n)) + (u = Math.min(s, i, n))) / 2, d === u ? l = r = 0 : (c = d - u, r = .5 < a ? c / (2 - d - u) : c / (d + u), l = d === s ? (i - n) / c + (i < n ? 6 : 0) : d === i ? (n - s) / c + 2 : (s - i) / c + 4, l *= 60), o[0] = l + .5 | 0, o[1] = 100 * r + .5 | 0, o[2] = 100 * a + .5 | 0), o
                    },
                    me = "(?:\\b(?:(?:rgb|rgba|hsl|hsla)\\(.+?\\))|\\B#(?:[0-9a-f]{3}){1,2}\\b";
                for (e in fe) me += "|" + e + "\\b";
                me = new RegExp(me + ")", "gi"), N.colorStringFilter = function(e) {
                    var t, o = e[0] + e[1];
                    me.test(o) && (t = -1 !== o.indexOf("hsl(") || -1 !== o.indexOf("hsla("), e[0] = s(e[0], t), e[1] = s(e[1], t)), me.lastIndex = 0
                }, U.defaultStringFilter || (U.defaultStringFilter = N.colorStringFilter);

                function be(e, t, n, l) {
                    if (null == e) return function(e) {
                        return e
                    };
                    var r, a = t ? (e.match(me) || [""])[0] : "",
                        d = e.split(a).join("").match(I) || [],
                        u = e.substr(0, e.indexOf(d[0])),
                        c = ")" === e.charAt(e.length - 1) ? ")" : "",
                        h = -1 !== e.indexOf(" ") ? " " : ",",
                        _ = d.length,
                        f = 0 < _ ? d[0].replace(k, "") : "";
                    return _ ? r = t ? function(e) {
                        var t, o, s, i;
                        if ("number" == typeof e) e += f;
                        else if (l && q.test(e)) {
                            for (i = e.replace(q, "|").split("|"), s = 0; s < i.length; s++) i[s] = r(i[s]);
                            return i.join(",")
                        }
                        if (t = (e.match(me) || [a])[0], s = (o = e.split(t).join("").match(I) || []).length, _ > s--)
                            for (; ++s < _;) o[s] = n ? o[(s - 1) / 2 | 0] : d[s];
                        return u + o.join(h) + h + t + c + (-1 !== e.indexOf("inset") ? " inset" : "")
                    } : function(e) {
                        var t, o, s;
                        if ("number" == typeof e) e += f;
                        else if (l && q.test(e)) {
                            for (o = e.replace(q, "|").split("|"), s = 0; s < o.length; s++) o[s] = r(o[s]);
                            return o.join(",")
                        }
                        if (s = (t = e.match(I) || []).length, _ > s--)
                            for (; ++s < _;) t[s] = n ? t[(s - 1) / 2 | 0] : d[s];
                        return u + t.join(h) + c
                    } : function(e) {
                        return e
                    }
                }

                function ge(d) {
                    return d = d.split(","),
                        function(e, t, o, s, i, n, l) {
                            var r, a = (t + "").split(" ");
                            for (l = {}, r = 0; r < 4; r++) l[d[r]] = a[r] = a[r] || a[(r - 1) / 2 >> 0];
                            return s.parse(e, l, i, n)
                        }
                }
                oe._setPluginRatio = function(e) {
                    this.plugin.setRatio(e);
                    for (var t, o, s, i, n, l = this.data, r = l.proxy, a = l.firstMPT; a;) t = r[a.v], a.r ? t = Math.round(t) : t < 1e-6 && -1e-6 < t && (t = 0), a.t[a.p] = t, a = a._next;
                    if (l.autoRotate && (l.autoRotate.rotation = l.mod ? l.mod(r.rotation, this.t) : r.rotation), 1 === e || 0 === e)
                        for (a = l.firstMPT, n = 1 === e ? "e" : "b"; a;) {
                            if ((o = a.t).type) {
                                if (1 === o.type) {
                                    for (i = o.xs0 + o.s + o.xs1, s = 1; s < o.l; s++) i += o["xn" + s] + o["xs" + (s + 1)];
                                    o[n] = i
                                }
                            } else o[n] = o.s + o.xs0;
                            a = a._next
                        }
                };

                function Se(e, t, o, s, i, n) {
                    var l = new ve(e, t, o, s - o, i, -1, n);
                    return l.b = o, l.e = l.xs0 = s, l
                }
                var ye = function(e, t, o, s, i) {
                        this.t = e, this.p = t, this.v = o, this.r = i, s && ((s._prev = this)._next = s)
                    },
                    ve = (oe._parseToProxy = function(e, t, o, s, i, n) {
                        var l, r, a, d, u, c = s,
                            h = {},
                            _ = {},
                            f = o._transform,
                            p = $;
                        for (o._transform = null, $ = t, s = u = o.parse(e, t, s, i), $ = p, n && (o._transform = f, c && (c._prev = null, c._prev && (c._prev._next = null))); s && s !== c;) {
                            if (s.type <= 1 && (_[r = s.p] = s.s + s.c, h[r] = s.s, n || (d = new ye(s, "s", r, d, s.r), s.c = 0), 1 === s.type))
                                for (l = s.l; 0 < --l;) a = "xn" + l, _[r = s.p + "_" + a] = s.data[a], h[r] = s[a], n || (d = new ye(s, a, r, d, s.rxp[a]));
                            s = s._next
                        }
                        return {
                            proxy: h,
                            end: _,
                            firstMPT: d,
                            pt: u
                        }
                    }, oe.CSSPropTween = function(e, t, o, s, i, n, l, r, a, d, u) {
                        this.t = e, this.p = t, this.s = o, this.c = s, this.n = l || t, e instanceof ve || p.push(this.n), this.r = r, this.type = n || 0, a && (this.pr = a, f = !0), this.b = void 0 === d ? o : d, this.e = void 0 === u ? o + s : u, i && ((this._next = i)._prev = this)
                    }),
                    Pe = N.parseComplex = function(e, t, o, s, i, n, l, r, a, d) {
                        o = o || n || "", "function" == typeof s && (s = s(O, E)), l = new ve(e, t, 0, 0, l, d ? 2 : 1, null, !1, r, o, s), s += "", i && me.test(s + o) && (s = [o, s], N.colorStringFilter(s), o = s[0], s = s[1]);
                        var u, c, h, _, f, p, m, b, g, S, y, v, P, T = o.split(", ").join(",").split(" "),
                            w = s.split(", ").join(",").split(" "),
                            D = T.length,
                            B = !1 !== H;
                        for (-1 === s.indexOf(",") && -1 === o.indexOf(",") || (T = T.join(" ").replace(q, ", ").split(" "), w = w.join(" ").replace(q, ", ").split(" "), D = T.length), D !== w.length && (D = (T = (n || "").split(" ")).length), l.plugin = a, l.setRatio = d, u = me.lastIndex = 0; u < D; u++)
                            if (_ = T[u], f = w[u], (b = parseFloat(_)) || 0 === b) l.appendXtra("", b, M(f, b), f.replace(L, ""), B && -1 !== f.indexOf("px"), !0);
                            else if (i && me.test(_)) v = ")" + ((v = f.indexOf(")") + 1) ? f.substr(v) : ""), P = -1 !== f.indexOf("hsl") && ie, _ = pe(_, P), f = pe(f, P), (g = 6 < _.length + f.length) && !ie && 0 === f[3] ? (l["xs" + l.l] += l.l ? " transparent" : "transparent", l.e = l.e.split(w[u]).join("transparent")) : (ie || (g = !1), P ? l.appendXtra(g ? "hsla(" : "hsl(", _[0], M(f[0], _[0]), ",", !1, !0).appendXtra("", _[1], M(f[1], _[1]), "%,", !1).appendXtra("", _[2], M(f[2], _[2]), g ? "%," : "%" + v, !1) : l.appendXtra(g ? "rgba(" : "rgb(", _[0], f[0] - _[0], ",", !0, !0).appendXtra("", _[1], f[1] - _[1], ",", !0).appendXtra("", _[2], f[2] - _[2], g ? "," : v, !0), g && (_ = _.length < 4 ? 1 : _[3], l.appendXtra("", _, (f.length < 4 ? 1 : f[3]) - _, v, !1))), me.lastIndex = 0;
                        else if (p = _.match(k)) {
                            if (!(m = f.match(L)) || m.length !== p.length) return l;
                            for (c = h = 0; c < p.length; c++) y = p[c], S = _.indexOf(y, h), l.appendXtra(_.substr(h, S - h), Number(y), M(m[c], y), "", B && "px" === _.substr(S + y.length, 2), 0 === c), h = S + y.length;
                            l["xs" + l.l] += _.substr(h)
                        } else l["xs" + l.l] += l.l || l["xs" + l.l] ? " " + f : f;
                        if (-1 !== s.indexOf("=") && l.data) {
                            for (v = l.xs0 + l.data.s, u = 1; u < l.l; u++) v += l["xs" + u] + l.data["xn" + u];
                            l.e = v + l["xs" + u]
                        }
                        return l.l || (l.type = -1, l.xs0 = l.e), l.xfirst || l
                    },
                    Te = 9;
                for ((e = ve.prototype).l = e.pr = 0; 0 < --Te;) e["xn" + Te] = 0, e["xs" + Te] = "";
                e.xs0 = "", e._next = e._prev = e.xfirst = e.data = e.plugin = e.setRatio = e.rxp = null, e.appendXtra = function(e, t, o, s, i, n) {
                    var l = this,
                        r = l.l;
                    return l["xs" + r] += n && (r || l["xs" + r]) ? " " + e : e || "", o || 0 === r || l.plugin ? (l.l++, l.type = l.setRatio ? 2 : 1, l["xs" + l.l] = s || "", 0 < r ? (l.data["xn" + r] = t + o, l.rxp["xn" + r] = i, l["xn" + r] = t, l.plugin || (l.xfirst = new ve(l, "xn" + r, t, o, l.xfirst || l, 0, l.n, i, l.pr), l.xfirst.xs0 = 0)) : (l.data = {
                        s: t + o
                    }, l.rxp = {}, l.s = t, l.c = o, l.r = i), l) : (l["xs" + r] += t + (s || ""), l)
                };

                function we(e, t) {
                    t = t || {}, this.p = t.prefix && B(e) || e, m[e] = m[this.p] = this, this.format = t.formatter || be(t.defaultValue, t.color, t.collapsible, t.multi), t.parser && (this.parse = t.parser), this.clrs = t.color, this.multi = t.multi, this.keyword = t.keyword, this.dflt = t.defaultValue, this.pr = t.priority || 0
                }
                var De = oe._registerComplexSpecialProp = function(e, t, o) {
                        "object" != typeof t && (t = {
                            parser: o
                        });
                        var s, i = e.split(","),
                            n = t.defaultValue;
                        for (o = o || [n], s = 0; s < i.length; s++) t.prefix = 0 === s && t.prefix, t.defaultValue = o[s] || n, new we(i[s], t)
                    },
                    Be = oe._registerPluginProp = function(e) {
                        if (!m[e]) {
                            var a = e.charAt(0).toUpperCase() + e.substr(1) + "Plugin";
                            De(e, {
                                parser: function(e, t, o, s, i, n, l) {
                                    var r = d.com.greensock.plugins[a];
                                    return r ? (r._cssRegister(), m[o].parse(e, t, o, s, i, n, l)) : (b("Error: " + a + " js file not loaded."), i)
                                }
                            })
                        }
                    };
                (e = we.prototype).parseComplex = function(e, t, o, s, i, n) {
                    var l, r, a, d, u, c, h = this.keyword;
                    if (this.multi && (q.test(o) || q.test(t) ? (r = t.replace(q, "|").split("|"), a = o.replace(q, "|").split("|")) : h && (r = [t], a = [o])), a) {
                        for (d = a.length > r.length ? a.length : r.length, l = 0; l < d; l++) t = r[l] = r[l] || this.dflt, o = a[l] = a[l] || this.dflt, h && (u = t.indexOf(h)) !== (c = o.indexOf(h)) && (-1 === c ? r[l] = r[l].split(h).join("") : -1 === u && (r[l] += " " + h));
                        t = r.join(", "), o = a.join(", ")
                    }
                    return Pe(e, this.p, t, o, this.clrs, this.dflt, s, this.pr, i, n)
                }, e.parse = function(e, t, o, s, i, n, l) {
                    return this.parseComplex(e.style, this.format(ae(e, this.p, D, !1, this.dflt)), this.format(t), i, n)
                }, N.registerSpecialProp = function(e, a, d) {
                    De(e, {
                        parser: function(e, t, o, s, i, n, l) {
                            var r = new ve(e, o, 0, 0, i, 2, o, !1, d);
                            return r.plugin = n, r.setRatio = a(e, t, s._tween, o), r
                        },
                        priority: d
                    })
                }, N.useSVGTransformAttr = P || A;

                function Me(e, t, o) {
                    var s, i = Z.createElementNS("http://www.w3.org/2000/svg", e),
                        n = /([a-z])([A-Z])/g;
                    for (s in o) i.setAttributeNS(null, s.replace(n, "$1-$2").toLowerCase(), o[s]);
                    return t.appendChild(i), i
                }

                function Fe(e, t, o, s, i, n) {
                    var l, r, a, d, u, c, h, _, f, p, m, b, g, S, y = e._gsTransform,
                        v = ze(e, !0);
                    y && (g = y.xOrigin, S = y.yOrigin), (!s || (l = s.split(" ")).length < 2) && (h = e.getBBox(), l = [(-1 !== (t = _e(t).split(" "))[0].indexOf("%") ? parseFloat(t[0]) / 100 * h.width : parseFloat(t[0])) + h.x, (-1 !== t[1].indexOf("%") ? parseFloat(t[1]) / 100 * h.height : parseFloat(t[1])) + h.y]), o.xOrigin = d = parseFloat(l[0]), o.yOrigin = u = parseFloat(l[1]), s && v !== je && (c = v[0], h = v[1], _ = v[2], f = v[3], p = v[4], r = d * (f / (b = c * f - h * _)) + u * (-_ / b) + (_ * (m = v[5]) - f * p) / b, a = d * (-h / b) + u * (c / b) - (c * m - h * p) / b, d = o.xOrigin = l[0] = r, u = o.yOrigin = l[1] = a), y && (n && (o.xOffset = y.xOffset, o.yOffset = y.yOffset, y = o), i || !1 !== i && !1 !== N.defaultSmoothOrigin ? (r = d - g, a = u - S, y.xOffset += r * v[0] + a * v[2] - r, y.yOffset += r * v[1] + a * v[3] - a) : y.xOffset = y.yOffset = 0), n || e.setAttribute("data-svg-origin", l.join(" "))
                }

                function We(e) {
                    var t, o, s = this.data,
                        i = -s.rotation * J,
                        n = i + s.skewX * J,
                        l = 1e5,
                        r = (Math.cos(i) * s.scaleX * l | 0) / l,
                        a = (Math.sin(i) * s.scaleX * l | 0) / l,
                        d = (Math.sin(n) * -s.scaleY * l | 0) / l,
                        u = (Math.cos(n) * s.scaleY * l | 0) / l,
                        c = this.t.style,
                        h = this.t.currentStyle;
                    if (h) {
                        o = a, a = -d, d = -o, t = h.filter, c.filter = "";
                        var _, f, p = this.t.offsetWidth,
                            m = this.t.offsetHeight,
                            b = "absolute" !== h.position,
                            g = "progid:DXImageTransform.Microsoft.Matrix(M11=" + r + ", M12=" + a + ", M21=" + d + ", M22=" + u,
                            S = s.x + p * s.xPercent / 100,
                            y = s.y + m * s.yPercent / 100;
                        if (null != s.ox && (S += (_ = (s.oxp ? p * s.ox * .01 : s.ox) - p / 2) - (_ * r + (f = (s.oyp ? m * s.oy * .01 : s.oy) - m / 2) * a), y += f - (_ * d + f * u)), g += b ? ", Dx=" + ((_ = p / 2) - (_ * r + (f = m / 2) * a) + S) + ", Dy=" + (f - (_ * d + f * u) + y) + ")" : ", sizingMethod='auto expand')", -1 !== t.indexOf("DXImageTransform.Microsoft.Matrix(") ? c.filter = t.replace(G, g) : c.filter = g + " " + t, 0 !== e && 1 !== e || 1 == r && 0 === a && 0 === d && 1 == u && (b && -1 === g.indexOf("Dx=0, Dy=0") || R.test(t) && 100 !== parseFloat(RegExp.$1) || -1 === t.indexOf(t.indexOf("Alpha")) && c.removeAttribute("filter")), !b) {
                            var v, P, T, w = C < 8 ? 1 : -1;
                            for (_ = s.ieOffsetX || 0, f = s.ieOffsetY || 0, s.ieOffsetX = Math.round((p - ((r < 0 ? -r : r) * p + (a < 0 ? -a : a) * m)) / 2 + S), s.ieOffsetY = Math.round((m - ((u < 0 ? -u : u) * m + (d < 0 ? -d : d) * p)) / 2 + y), Te = 0; Te < 4; Te++) T = (o = -1 !== (v = h[P = he[Te]]).indexOf("px") ? parseFloat(v) : de(this.t, P, parseFloat(v), v.replace(x, "")) || 0) !== s[P] ? Te < 2 ? -s.ieOffsetX : -s.ieOffsetY : Te < 2 ? _ - s.ieOffsetX : f - s.ieOffsetY, c[P] = (s[P] = Math.round(o - T * (0 === Te || 2 === Te ? 1 : w))) + "px"
                        }
                    }
                }
                var He, Ce, Ee, Oe, ke, Le = "scaleX,scaleY,scaleZ,x,y,z,skewX,skewY,rotation,rotationX,rotationY,perspective,xPercent,yPercent".split(","),
                    Ie = B("transform"),
                    xe = ne + "transform",
                    Ae = B("transformOrigin"),
                    Re = null !== B("perspective"),
                    Ue = oe.Transform = function() {
                        this.perspective = parseFloat(N.defaultTransformPerspective) || 0, this.force3D = !(!1 === N.defaultForce3D || !Re) && (N.defaultForce3D || "auto")
                    },
                    Ne = window.SVGElement,
                    Ye = Z.documentElement,
                    Xe = (ke = C || /Android/i.test(se) && !window.chrome, Z.createElementNS && !ke && (Ce = Me("svg", Ye), Oe = (Ee = Me("rect", Ce, {
                        width: 100,
                        height: 50,
                        x: 100
                    })).getBoundingClientRect().width, Ee.style[Ae] = "50% 50%", Ee.style[Ie] = "scaleX(0.5)", ke = Oe === Ee.getBoundingClientRect().width && !(A && Re), Ye.removeChild(Ce)), ke),
                    Ve = function(e) {
                        return !!(Ne && e.getBBox && e.getCTM && function(e) {
                            try {
                                return e.getBBox()
                            } catch (e) {}
                        }(e) && (!e.parentNode || e.parentNode.getBBox && e.parentNode.getCTM))
                    },
                    je = [1, 0, 0, 1, 0, 0],
                    ze = function(e, t) {
                        var o, s, i, n, l, r, a = e._gsTransform || new Ue,
                            d = e.style;
                        if (Ie ? s = ae(e, xe, null, !0) : e.currentStyle && (s = (s = e.currentStyle.filter.match(z)) && 4 === s.length ? [s[0].substr(4), Number(s[2].substr(4)), Number(s[1].substr(4)), s[3].substr(4), a.x || 0, a.y || 0].join(",") : ""), (o = !s || "none" === s || "matrix(1, 0, 0, 1, 0, 0)" === s) && Ie && ((r = "none" === re(e).display) || !e.parentNode) && (r && (n = d.display, d.display = "block"), e.parentNode || (l = 1, Ye.appendChild(e)), o = !(s = ae(e, xe, null, !0)) || "none" === s || "matrix(1, 0, 0, 1, 0, 0)" === s, n ? d.display = n : r && Qe(d, "display"), l && Ye.removeChild(e)), (a.svg || e.getBBox && Ve(e)) && (o && -1 !== (d[Ie] + "").indexOf("matrix") && (s = d[Ie], o = 0), i = e.getAttribute("transform"), o && i && (-1 !== i.indexOf("matrix") ? (s = i, o = 0) : -1 !== i.indexOf("translate") && (s = "matrix(1,0,0,1," + i.match(/(?:\-|\b)[\d\-\.e]+\b/gi).join(",") + ")", o = 0))), o) return je;
                        for (i = (s || "").match(k) || [], Te = i.length; - 1 < --Te;) n = Number(i[Te]), i[Te] = (l = n - (n |= 0)) ? (1e5 * l + (l < 0 ? -.5 : .5) | 0) / 1e5 + n : n;
                        return t && 6 < i.length ? [i[0], i[1], i[4], i[5], i[12], i[13]] : i
                    },
                    Ge = oe.getTransform = function(e, t, o, s) {
                        if (e._gsTransform && o && !s) return e._gsTransform;
                        var i, n, l, r, a, d, u = o && e._gsTransform || new Ue,
                            c = u.scaleX < 0,
                            h = Re && (parseFloat(ae(e, Ae, t, !1, "0 0 0").split(" ")[2]) || u.zOrigin) || 0,
                            _ = parseFloat(N.defaultTransformPerspective) || 0;
                        if (u.svg = !(!e.getBBox || !Ve(e)), u.svg && (Fe(e, ae(e, Ae, t, !1, "50% 50%") + "", u, e.getAttribute("data-svg-origin")), He = N.useSVGTransformAttr || Xe), (i = ze(e)) !== je) {
                            if (16 === i.length) {
                                var f, p, m, b, g, S = i[0],
                                    y = i[1],
                                    v = i[2],
                                    P = i[3],
                                    T = i[4],
                                    w = i[5],
                                    D = i[6],
                                    B = i[7],
                                    M = i[8],
                                    F = i[9],
                                    W = i[10],
                                    H = i[12],
                                    C = i[13],
                                    E = i[14],
                                    O = i[11],
                                    k = Math.atan2(D, W);
                                u.zOrigin && (H = M * (E = -u.zOrigin) - i[12], C = F * E - i[13], E = W * E + u.zOrigin - i[14]), u.rotationX = k * Q, k && (f = T * (b = Math.cos(-k)) + M * (g = Math.sin(-k)), p = w * b + F * g, m = D * b + W * g, M = T * -g + M * b, F = w * -g + F * b, W = D * -g + W * b, O = B * -g + O * b, T = f, w = p, D = m), k = Math.atan2(-v, W), u.rotationY = k * Q, k && (p = y * (b = Math.cos(-k)) - F * (g = Math.sin(-k)), m = v * b - W * g, F = y * g + F * b, W = v * g + W * b, O = P * g + O * b, S = f = S * b - M * g, y = p, v = m), k = Math.atan2(y, S), u.rotation = k * Q, k && (S = S * (b = Math.cos(-k)) + T * (g = Math.sin(-k)), p = y * b + w * g, w = y * -g + w * b, D = v * -g + D * b, y = p), u.rotationX && 359.9 < Math.abs(u.rotationX) + Math.abs(u.rotation) && (u.rotationX = u.rotation = 0, u.rotationY = 180 - u.rotationY), u.scaleX = (1e5 * Math.sqrt(S * S + y * y) + .5 | 0) / 1e5, u.scaleY = (1e5 * Math.sqrt(w * w + F * F) + .5 | 0) / 1e5, u.scaleZ = (1e5 * Math.sqrt(D * D + W * W) + .5 | 0) / 1e5, u.rotationX || u.rotationY ? u.skewX = 0 : (u.skewX = T || w ? Math.atan2(T, w) * Q + u.rotation : u.skewX || 0, 90 < Math.abs(u.skewX) && Math.abs(u.skewX) < 270 && (c ? (u.scaleX *= -1, u.skewX += u.rotation <= 0 ? 180 : -180, u.rotation += u.rotation <= 0 ? 180 : -180) : (u.scaleY *= -1, u.skewX += u.skewX <= 0 ? 180 : -180))), u.perspective = O ? 1 / (O < 0 ? -O : O) : 0, u.x = H, u.y = C, u.z = E, u.svg && (u.x -= u.xOrigin - (u.xOrigin * S - u.yOrigin * T), u.y -= u.yOrigin - (u.yOrigin * y - u.xOrigin * w))
                            } else if (!Re || s || !i.length || u.x !== i[4] || u.y !== i[5] || !u.rotationX && !u.rotationY) {
                                var L = 6 <= i.length,
                                    I = L ? i[0] : 1,
                                    x = i[1] || 0,
                                    A = i[2] || 0,
                                    R = L ? i[3] : 1;
                                u.x = i[4] || 0, u.y = i[5] || 0, l = Math.sqrt(I * I + x * x), r = Math.sqrt(R * R + A * A), a = I || x ? Math.atan2(x, I) * Q : u.rotation || 0, d = A || R ? Math.atan2(A, R) * Q + a : u.skewX || 0, 90 < Math.abs(d) && Math.abs(d) < 270 && (c ? (l *= -1, d += a <= 0 ? 180 : -180, a += a <= 0 ? 180 : -180) : (r *= -1, d += d <= 0 ? 180 : -180)), u.scaleX = l, u.scaleY = r, u.rotation = a, u.skewX = d, Re && (u.rotationX = u.rotationY = u.z = 0, u.perspective = _, u.scaleZ = 1), u.svg && (u.x -= u.xOrigin - (u.xOrigin * I + u.yOrigin * A), u.y -= u.yOrigin - (u.xOrigin * x + u.yOrigin * R))
                            }
                            for (n in u.zOrigin = h, u) u[n] < 2e-5 && -2e-5 < u[n] && (u[n] = 0)
                        }
                        return o && (e._gsTransform = u).svg && (He && e.style[Ie] ? U.delayedCall(.001, function() {
                            Qe(e.style, Ie)
                        }) : !He && e.getAttribute("transform") && U.delayedCall(.001, function() {
                            e.removeAttribute("transform")
                        })), u
                    },
                    qe = oe.set3DTransformRatio = oe.setTransformRatio = function(e) {
                        var t, o, s, i, n, l, r, a, d, u, c, h, _, f, p, m, b, g, S, y, v, P, T, w = this.data,
                            D = this.t.style,
                            B = w.rotation,
                            M = w.rotationX,
                            F = w.rotationY,
                            W = w.scaleX,
                            H = w.scaleY,
                            C = w.scaleZ,
                            E = w.x,
                            O = w.y,
                            k = w.z,
                            L = w.svg,
                            I = w.perspective,
                            x = w.force3D;
                        if (!((1 !== e && 0 !== e || "auto" !== x || this.tween._totalTime !== this.tween._totalDuration && this.tween._totalTime) && x || k || I || F || M || 1 !== C) || He && L || !Re) B || w.skewX || L ? (B *= J, P = w.skewX * J, T = 1e5, t = Math.cos(B) * W, i = Math.sin(B) * W, o = Math.sin(B - P) * -H, n = Math.cos(B - P) * H, P && "simple" === w.skewType && (b = Math.tan(P - w.skewY * J), o *= b = Math.sqrt(1 + b * b), n *= b, w.skewY && (b = Math.tan(w.skewY * J), t *= b = Math.sqrt(1 + b * b), i *= b)), L && (E += w.xOrigin - (w.xOrigin * t + w.yOrigin * o) + w.xOffset, O += w.yOrigin - (w.xOrigin * i + w.yOrigin * n) + w.yOffset, He && (w.xPercent || w.yPercent) && (f = this.t.getBBox(), E += .01 * w.xPercent * f.width, O += .01 * w.yPercent * f.height), E < (f = 1e-6) && -f < E && (E = 0), O < f && -f < O && (O = 0)), S = (t * T | 0) / T + "," + (i * T | 0) / T + "," + (o * T | 0) / T + "," + (n * T | 0) / T + "," + E + "," + O + ")", L && He ? this.t.setAttribute("transform", "matrix(" + S) : D[Ie] = (w.xPercent || w.yPercent ? "translate(" + w.xPercent + "%," + w.yPercent + "%) matrix(" : "matrix(") + S) : D[Ie] = (w.xPercent || w.yPercent ? "translate(" + w.xPercent + "%," + w.yPercent + "%) matrix(" : "matrix(") + W + ",0,0," + H + "," + E + "," + O + ")";
                        else {
                            if (A && (W < (f = 1e-4) && -f < W && (W = C = 2e-5), H < f && -f < H && (H = C = 2e-5), !I || w.z || w.rotationX || w.rotationY || (I = 0)), B || w.skewX) B *= J, p = t = Math.cos(B), m = i = Math.sin(B), w.skewX && (B -= w.skewX * J, p = Math.cos(B), m = Math.sin(B), "simple" === w.skewType && (b = Math.tan((w.skewX - w.skewY) * J), p *= b = Math.sqrt(1 + b * b), m *= b, w.skewY && (b = Math.tan(w.skewY * J), t *= b = Math.sqrt(1 + b * b), i *= b))), o = -m, n = p;
                            else {
                                if (!(F || M || 1 !== C || I || L)) return void(D[Ie] = (w.xPercent || w.yPercent ? "translate(" + w.xPercent + "%," + w.yPercent + "%) translate3d(" : "translate3d(") + E + "px," + O + "px," + k + "px)" + (1 !== W || 1 !== H ? " scale(" + W + "," + H + ")" : ""));
                                t = n = 1, o = i = 0
                            }
                            d = 1, s = l = r = a = u = c = 0, h = I ? -1 / I : 0, _ = w.zOrigin, f = 1e-6, y = ",", v = "0", (B = F * J) && (p = Math.cos(B), u = h * (r = -(m = Math.sin(B))), s = t * m, l = i * m, h *= d = p, t *= p, i *= p), (B = M * J) && (b = o * (p = Math.cos(B)) + s * (m = Math.sin(B)), g = n * p + l * m, a = d * m, c = h * m, s = o * -m + s * p, l = n * -m + l * p, d *= p, h *= p, o = b, n = g), 1 !== C && (s *= C, l *= C, d *= C, h *= C), 1 !== H && (o *= H, n *= H, a *= H, c *= H), 1 !== W && (t *= W, i *= W, r *= W, u *= W), (_ || L) && (_ && (E += s * -_, O += l * -_, k += d * -_ + _), L && (E += w.xOrigin - (w.xOrigin * t + w.yOrigin * o) + w.xOffset, O += w.yOrigin - (w.xOrigin * i + w.yOrigin * n) + w.yOffset), E < f && -f < E && (E = v), O < f && -f < O && (O = v), k < f && -f < k && (k = 0)), S = w.xPercent || w.yPercent ? "translate(" + w.xPercent + "%," + w.yPercent + "%) matrix3d(" : "matrix3d(", S += (t < f && -f < t ? v : t) + y + (i < f && -f < i ? v : i) + y + (r < f && -f < r ? v : r), S += y + (u < f && -f < u ? v : u) + y + (o < f && -f < o ? v : o) + y + (n < f && -f < n ? v : n), M || F || 1 !== C ? (S += y + (a < f && -f < a ? v : a) + y + (c < f && -f < c ? v : c) + y + (s < f && -f < s ? v : s), S += y + (l < f && -f < l ? v : l) + y + (d < f && -f < d ? v : d) + y + (h < f && -f < h ? v : h) + y) : S += ",0,0,0,0,1,0,", S += E + y + O + y + k + y + (I ? 1 + -k / I : 1) + ")", D[Ie] = S
                        }
                    };
                (e = Ue.prototype).x = e.y = e.z = e.skewX = e.skewY = e.rotation = e.rotationX = e.rotationY = e.zOrigin = e.xPercent = e.yPercent = e.xOffset = e.yOffset = 0, e.scaleX = e.scaleY = e.scaleZ = 1, De("transform,scale,scaleX,scaleY,scaleZ,x,y,z,rotation,rotationX,rotationY,rotationZ,skewX,skewY,shortRotation,shortRotationX,shortRotationY,shortRotationZ,transformOrigin,svgOrigin,transformPerspective,directionalRotation,parseTransform,force3D,skewType,xPercent,yPercent,smoothOrigin", {
                    parser: function(e, t, o, s, i, n, l) {
                        if (s._lastParsedTransform === l) return i;
                        var r;
                        "function" == typeof(s._lastParsedTransform = l)[o] && (r = l[o], l[o] = t);
                        var a, d, u, c, h, _, f, p, m, b = e._gsTransform,
                            g = e.style,
                            S = Le.length,
                            y = l,
                            v = {},
                            P = "transformOrigin",
                            T = Ge(e, D, !0, y.parseTransform),
                            w = y.transform && ("function" == typeof y.transform ? y.transform(O, E) : y.transform);
                        if (s._transform = T, w && "string" == typeof w && Ie)(d = ee.style)[Ie] = w, d.display = "block", d.position = "absolute", Z.body.appendChild(ee), a = Ge(ee, null, !1), T.svg && (_ = T.xOrigin, f = T.yOrigin, a.x -= T.xOffset, a.y -= T.yOffset, (y.transformOrigin || y.svgOrigin) && (w = {}, Fe(e, _e(y.transformOrigin), w, y.svgOrigin, y.smoothOrigin, !0), _ = w.xOrigin, f = w.yOrigin, a.x -= w.xOffset - T.xOffset, a.y -= w.yOffset - T.yOffset), (_ || f) && (p = ze(ee, !0), a.x -= _ - (_ * p[0] + f * p[2]), a.y -= f - (_ * p[1] + f * p[3]))), Z.body.removeChild(ee), a.perspective || (a.perspective = T.perspective), null != y.xPercent && (a.xPercent = F(y.xPercent, T.xPercent)), null != y.yPercent && (a.yPercent = F(y.yPercent, T.yPercent));
                        else if ("object" == typeof y) {
                            if (a = {
                                    scaleX: F(null != y.scaleX ? y.scaleX : y.scale, T.scaleX),
                                    scaleY: F(null != y.scaleY ? y.scaleY : y.scale, T.scaleY),
                                    scaleZ: F(y.scaleZ, T.scaleZ),
                                    x: F(y.x, T.x),
                                    y: F(y.y, T.y),
                                    z: F(y.z, T.z),
                                    xPercent: F(y.xPercent, T.xPercent),
                                    yPercent: F(y.yPercent, T.yPercent),
                                    perspective: F(y.transformPerspective, T.perspective)
                                }, null != (h = y.directionalRotation))
                                if ("object" == typeof h)
                                    for (d in h) y[d] = h[d];
                                else y.rotation = h;
                            "string" == typeof y.x && -1 !== y.x.indexOf("%") && (a.x = 0, a.xPercent = F(y.x, T.xPercent)), "string" == typeof y.y && -1 !== y.y.indexOf("%") && (a.y = 0, a.yPercent = F(y.y, T.yPercent)), a.rotation = W("rotation" in y ? y.rotation : "shortRotation" in y ? y.shortRotation + "_short" : "rotationZ" in y ? y.rotationZ : T.rotation - T.skewY, T.rotation - T.skewY, "rotation", v), Re && (a.rotationX = W("rotationX" in y ? y.rotationX : "shortRotationX" in y ? y.shortRotationX + "_short" : T.rotationX || 0, T.rotationX, "rotationX", v), a.rotationY = W("rotationY" in y ? y.rotationY : "shortRotationY" in y ? y.shortRotationY + "_short" : T.rotationY || 0, T.rotationY, "rotationY", v)), a.skewX = W(y.skewX, T.skewX - T.skewY), (a.skewY = W(y.skewY, T.skewY)) && (a.skewX += a.skewY, a.rotation += a.skewY)
                        }
                        for (Re && null != y.force3D && (T.force3D = y.force3D, c = !0), T.skewType = y.skewType || T.skewType || N.defaultSkewType, (u = T.force3D || T.z || T.rotationX || T.rotationY || a.z || a.rotationX || a.rotationY || a.perspective) || null == y.scale || (a.scaleZ = 1); - 1 < --S;)(1e-6 < (w = a[m = Le[S]] - T[m]) || w < -1e-6 || null != y[m] || null != $[m]) && (c = !0, i = new ve(T, m, T[m], w, i), m in v && (i.e = v[m]), i.xs0 = 0, i.plugin = n, s._overwriteProps.push(i.n));
                        return w = y.transformOrigin, T.svg && (w || y.svgOrigin) && (_ = T.xOffset, f = T.yOffset, Fe(e, _e(w), a, y.svgOrigin, y.smoothOrigin), i = Se(T, "xOrigin", (b ? T : a).xOrigin, a.xOrigin, i, P), i = Se(T, "yOrigin", (b ? T : a).yOrigin, a.yOrigin, i, P), _ === T.xOffset && f === T.yOffset || (i = Se(T, "xOffset", b ? _ : T.xOffset, T.xOffset, i, P), i = Se(T, "yOffset", b ? f : T.yOffset, T.yOffset, i, P)), w = He ? null : "0px 0px"), (w || Re && u && T.zOrigin) && (Ie ? (c = !0, m = Ae, w = (w || ae(e, m, D, !1, "50% 50%")) + "", (i = new ve(g, m, 0, 0, i, -1, P)).b = g[m], i.plugin = n, Re ? (d = T.zOrigin, w = w.split(" "), T.zOrigin = (2 < w.length && (0 === d || "0px" !== w[2]) ? parseFloat(w[2]) : d) || 0, i.xs0 = i.e = w[0] + " " + (w[1] || "50%") + " 0px", (i = new ve(T, "zOrigin", 0, 0, i, -1, i.n)).b = d, i.xs0 = i.e = T.zOrigin) : i.xs0 = i.e = w) : _e(w + "", T)), c && (s._transformType = T.svg && He || !u && 3 !== this._transformType ? 2 : 3), r && (l[o] = r), i
                    },
                    prefix: !0
                }), De("boxShadow", {
                    defaultValue: "0px 0px 0px 0px #999",
                    prefix: !0,
                    color: !0,
                    multi: !0,
                    keyword: "inset"
                }), De("borderRadius", {
                    defaultValue: "0px",
                    parser: function(e, t, o, s, i, n) {
                        t = this.format(t);
                        var l, r, a, d, u, c, h, _, f, p, m, b, g, S, y, v, P = ["borderTopLeftRadius", "borderTopRightRadius", "borderBottomRightRadius", "borderBottomLeftRadius"],
                            T = e.style;
                        for (f = parseFloat(e.offsetWidth), p = parseFloat(e.offsetHeight), l = t.split(" "), r = 0; r < P.length; r++) this.p.indexOf("border") && (P[r] = B(P[r])), -1 !== (u = d = ae(e, P[r], D, !1, "0px")).indexOf(" ") && (u = (d = u.split(" "))[0], d = d[1]), c = a = l[r], h = parseFloat(u), b = u.substr((h + "").length), "" === (m = (g = "=" === c.charAt(1)) ? (_ = parseInt(c.charAt(0) + "1", 10), c = c.substr(2), _ *= parseFloat(c), c.substr((_ + "").length - (_ < 0 ? 1 : 0)) || "") : (_ = parseFloat(c), c.substr((_ + "").length))) && (m = w[o] || b), m !== b && (S = de(e, "borderLeft", h, b), y = de(e, "borderTop", h, b), d = "%" === m ? (u = S / f * 100 + "%", y / p * 100 + "%") : "em" === m ? (u = S / (v = de(e, "borderLeft", 1, "em")) + "em", y / v + "em") : (u = S + "px", y + "px"), g && (c = parseFloat(u) + _ + m, a = parseFloat(d) + _ + m)), i = Pe(T, P[r], u + " " + d, c + " " + a, !1, "0px", i);
                        return i
                    },
                    prefix: !0,
                    formatter: be("0px 0px 0px 0px", !1, !0)
                }), De("borderBottomLeftRadius,borderBottomRightRadius,borderTopLeftRadius,borderTopRightRadius", {
                    defaultValue: "0px",
                    parser: function(e, t, o, s, i, n) {
                        return Pe(e.style, o, this.format(ae(e, o, D, !1, "0px 0px")), this.format(t), !1, "0px", i)
                    },
                    prefix: !0,
                    formatter: be("0px 0px", !1, !0)
                }), De("backgroundPosition", {
                    defaultValue: "0 0",
                    parser: function(e, t, o, s, i, n) {
                        var l, r, a, d, u, c, h = "background-position",
                            _ = D || re(e, null),
                            f = this.format((_ ? C ? _.getPropertyValue(h + "-x") + " " + _.getPropertyValue(h + "-y") : _.getPropertyValue(h) : e.currentStyle.backgroundPositionX + " " + e.currentStyle.backgroundPositionY) || "0 0"),
                            p = this.format(t);
                        if (-1 !== f.indexOf("%") != (-1 !== p.indexOf("%")) && p.split(",").length < 2 && (c = ae(e, "backgroundImage").replace(V, "")) && "none" !== c) {
                            for (l = f.split(" "), r = p.split(" "), te.setAttribute("src", c), a = 2; - 1 < --a;)(d = -1 !== (f = l[a]).indexOf("%")) != (-1 !== r[a].indexOf("%")) && (u = 0 === a ? e.offsetWidth - te.width : e.offsetHeight - te.height, l[a] = d ? parseFloat(f) / 100 * u + "px" : parseFloat(f) / u * 100 + "%");
                            f = l.join(" ")
                        }
                        return this.parseComplex(e.style, f, p, i, n)
                    },
                    formatter: _e
                }), De("backgroundSize", {
                    defaultValue: "0 0",
                    formatter: function(e) {
                        return _e(-1 === (e += "").indexOf(" ") ? e + " " + e : e)
                    }
                }), De("perspective", {
                    defaultValue: "0px",
                    prefix: !0
                }), De("perspectiveOrigin", {
                    defaultValue: "50% 50%",
                    prefix: !0
                }), De("transformStyle", {
                    prefix: !0
                }), De("backfaceVisibility", {
                    prefix: !0
                }), De("userSelect", {
                    prefix: !0
                }), De("margin", {
                    parser: ge("marginTop,marginRight,marginBottom,marginLeft")
                }), De("padding", {
                    parser: ge("paddingTop,paddingRight,paddingBottom,paddingLeft")
                }), De("clip", {
                    defaultValue: "rect(0px,0px,0px,0px)",
                    parser: function(e, t, o, s, i, n) {
                        var l, r, a;
                        return t = C < 9 ? (r = e.currentStyle, a = C < 8 ? " " : ",", l = "rect(" + r.clipTop + a + r.clipRight + a + r.clipBottom + a + r.clipLeft + ")", this.format(t).split(",").join(a)) : (l = this.format(ae(e, this.p, D, !1, this.dflt)), this.format(t)), this.parseComplex(e.style, l, t, i, n)
                    }
                }), De("textShadow", {
                    defaultValue: "0px 0px 0px #999",
                    color: !0,
                    multi: !0
                }), De("autoRound,strictUnits", {
                    parser: function(e, t, o, s, i) {
                        return i
                    }
                }), De("border", {
                    defaultValue: "0px solid #000",
                    parser: function(e, t, o, s, i, n) {
                        var l = ae(e, "borderTopWidth", D, !1, "0px"),
                            r = this.format(t).split(" "),
                            a = r[0].replace(x, "");
                        return "px" !== a && (l = parseFloat(l) / de(e, "borderTopWidth", 1, a) + a), this.parseComplex(e.style, this.format(l + " " + ae(e, "borderTopStyle", D, !1, "solid") + " " + ae(e, "borderTopColor", D, !1, "#000")), r.join(" "), i, n)
                    },
                    color: !0,
                    formatter: function(e) {
                        var t = e.split(" ");
                        return t[0] + " " + (t[1] || "solid") + " " + (e.match(me) || ["#000"])[0]
                    }
                }), De("borderWidth", {
                    parser: ge("borderTopWidth,borderRightWidth,borderBottomWidth,borderLeftWidth")
                }), De("float,cssFloat,styleFloat", {
                    parser: function(e, t, o, s, i, n) {
                        var l = e.style,
                            r = "cssFloat" in l ? "cssFloat" : "styleFloat";
                        return new ve(l, r, 0, 0, i, -1, o, !1, 0, l[r], t)
                    }
                });

                function Ke(e) {
                    var t, o = this.t,
                        s = o.filter || ae(this.data, "filter") || "",
                        i = this.s + this.c * e | 0;
                    100 == i && (t = -1 === s.indexOf("atrix(") && -1 === s.indexOf("radient(") && -1 === s.indexOf("oader(") ? (o.removeAttribute("filter"), !ae(this.data, "filter")) : (o.filter = s.replace(a, ""), !0)), t || (this.xn1 && (o.filter = s = s || "alpha(opacity=" + i + ")"), -1 === s.indexOf("pacity") ? 0 == i && this.xn1 || (o.filter = s + " alpha(opacity=" + i + ")") : o.filter = s.replace(R, "opacity=" + i))
                }
                De("opacity,alpha,autoAlpha", {
                    defaultValue: "1",
                    parser: function(e, t, o, s, i, n) {
                        var l = parseFloat(ae(e, "opacity", D, !1, "1")),
                            r = e.style,
                            a = "autoAlpha" === o;
                        return "string" == typeof t && "=" === t.charAt(1) && (t = ("-" === t.charAt(0) ? -1 : 1) * parseFloat(t.substr(2)) + l), a && 1 === l && "hidden" === ae(e, "visibility", D) && 0 !== t && (l = 0), ie ? i = new ve(r, "opacity", l, t - l, i) : ((i = new ve(r, "opacity", 100 * l, 100 * (t - l), i)).xn1 = a ? 1 : 0, r.zoom = 1, i.type = 2, i.b = "alpha(opacity=" + i.s + ")", i.e = "alpha(opacity=" + (i.s + i.c) + ")", i.data = e, i.plugin = n, i.setRatio = Ke), a && ((i = new ve(r, "visibility", 0, 0, i, -1, null, !1, 0, 0 !== l ? "inherit" : "hidden", 0 === t ? "hidden" : "inherit")).xs0 = "inherit", s._overwriteProps.push(i.n), s._overwriteProps.push(o)), i
                    }
                });

                function Je(e) {
                    if (this.t._gsClassPT = this, 1 === e || 0 === e) {
                        this.t.setAttribute("class", 0 === e ? this.b : this.e);
                        for (var t = this.data, o = this.t.style; t;) t.v ? o[t.p] = t.v : Qe(o, t.p), t = t._next;
                        1 === e && this.t._gsClassPT === this && (this.t._gsClassPT = null)
                    } else this.t.getAttribute("class") !== this.e && this.t.setAttribute("class", this.e)
                }
                var Qe = function(e, t) {
                    t && (e.removeProperty ? ("ms" !== t.substr(0, 2) && "webkit" !== t.substr(0, 6) || (t = "-" + t), e.removeProperty(t.replace(c, "-$1").toLowerCase())) : e.removeAttribute(t))
                };
                De("className", {
                    parser: function(e, t, o, s, i, n, l) {
                        var r, a, d, u, c, h = e.getAttribute("class") || "",
                            _ = e.style.cssText;
                        if ((i = s._classNamePT = new ve(e, o, 0, 0, i, 2)).setRatio = Je, i.pr = -11, f = !0, i.b = h, a = g(e, D), d = e._gsClassPT) {
                            for (u = {}, c = d.data; c;) u[c.p] = 1, c = c._next;
                            d.setRatio(1)
                        }
                        return (e._gsClassPT = i).e = "=" !== t.charAt(1) ? t : h.replace(new RegExp("(?:\\s|^)" + t.substr(2) + "(?![\\w-])"), "") + ("+" === t.charAt(0) ? " " + t.substr(2) : ""), e.setAttribute("class", i.e), r = S(e, a, g(e), l, u), e.setAttribute("class", h), i.data = r.firstMPT, e.style.cssText = _, i = i.xfirst = s.parse(e, r.difs, i, n)
                    }
                });

                function $e(e) {
                    if ((1 === e || 0 === e) && this.data._totalTime === this.data._totalDuration && "isFromStart" !== this.data.data) {
                        var t, o, s, i, n, l = this.t.style,
                            r = m.transform.parse;
                        if ("all" === this.e) i = !(l.cssText = "");
                        else
                            for (s = (t = this.e.split(" ").join("").split(",")).length; - 1 < --s;) o = t[s], m[o] && (m[o].parse === r ? i = !0 : o = "transformOrigin" === o ? Ae : m[o].p), Qe(l, o);
                        i && (Qe(l, Ie), (n = this.t._gsTransform) && (n.svg && (this.t.removeAttribute("data-svg-origin"), this.t.removeAttribute("transform")), delete this.t._gsTransform))
                    }
                }
                for (De("clearProps", {
                        parser: function(e, t, o, s, i) {
                            return (i = new ve(e, o, 0, 0, i, 2)).setRatio = $e, i.e = t, i.pr = -10, i.data = s._tween, f = !0, i
                        }
                    }), e = "bezier,throwProps,physicsProps,physics2D".split(","), Te = e.length; Te--;) Be(e[Te]);
                (e = N.prototype)._firstPT = e._lastParsedTransform = e._transform = null, e._onInitTween = function(e, t, o, s) {
                    if (!e.nodeType) return !1;
                    this._target = E = e, this._tween = o, this._vars = t, O = s, H = t.autoRound, f = !1, w = t.suffixMap || N.suffixMap, D = re(e, ""), p = this._overwriteProps;
                    var i, n, l, r, a, d, u, c, h, _ = e.style;
                    if (v && "" === _.zIndex && ("auto" !== (i = ae(e, "zIndex", D)) && "" !== i || this._addLazySet(_, "zIndex", 0)), "string" == typeof t && (r = _.cssText, i = g(e, D), _.cssText = r + ";" + t, i = S(e, i, g(e)).difs, !ie && Y.test(t) && (i.opacity = parseFloat(RegExp.$1)), t = i, _.cssText = r), t.className ? this._firstPT = n = m.className.parse(e, t.className, "className", this, null, null, t) : this._firstPT = n = this.parse(e, t, null), this._transformType) {
                        for (h = 3 === this._transformType, Ie ? P && (v = !0, "" === _.zIndex && ("auto" !== (u = ae(e, "zIndex", D)) && "" !== u || this._addLazySet(_, "zIndex", 0)), T && this._addLazySet(_, "WebkitBackfaceVisibility", this._vars.WebkitBackfaceVisibility || (h ? "visible" : "hidden"))) : _.zoom = 1, l = n; l && l._next;) l = l._next;
                        c = new ve(e, "transform", 0, 0, null, 2), this._linkCSSP(c, null, l), c.setRatio = Ie ? qe : We, c.data = this._transform || Ge(e, D, !0), c.tween = o, c.pr = -1, p.pop()
                    }
                    if (f) {
                        for (; n;) {
                            for (d = n._next, l = r; l && l.pr > n.pr;) l = l._next;
                            (n._prev = l ? l._prev : a) ? n._prev._next = n: r = n, (n._next = l) ? l._prev = n : a = n, n = d
                        }
                        this._firstPT = r
                    }
                    return !0
                }, e.parse = function(e, t, o, s) {
                    var i, n, l, r, a, d, u, c, h, _, f = e.style;
                    for (i in t) "function" == typeof(d = t[i]) && (d = d(O, E)), (n = m[i]) ? o = n.parse(e, d, i, this, o, s, t) : (a = ae(e, i, D) + "", h = "string" == typeof d, "color" === i || "fill" === i || "stroke" === i || -1 !== i.indexOf("Color") || h && X.test(d) ? (h || (d = (3 < (d = pe(d)).length ? "rgba(" : "rgb(") + d.join(",") + ")"), o = Pe(f, i, a, d, !0, "transparent", o, 0, s)) : h && K.test(d) ? o = Pe(f, i, a, d, !0, null, o, 0, s) : (u = (l = parseFloat(a)) || 0 === l ? a.substr((l + "").length) : "", "" !== a && "auto" !== a || (u = "width" === i || "height" === i ? (l = y(e, i, D), "px") : "left" === i || "top" === i ? (l = ue(e, i, D), "px") : (l = "opacity" !== i ? 0 : 1, "")), "" === (c = (_ = h && "=" === d.charAt(1)) ? (r = parseInt(d.charAt(0) + "1", 10), d = d.substr(2), r *= parseFloat(d), d.replace(x, "")) : (r = parseFloat(d), h ? d.replace(x, "") : "")) && (c = i in w ? w[i] : u), d = r || 0 === r ? (_ ? r + l : r) + c : t[i], u !== c && "" !== c && (r || 0 === r) && l && (l = de(e, i, l, u), "%" === c ? (l /= de(e, i, 100, "%") / 100, !0 !== t.strictUnits && (a = l + "%")) : "em" === c || "rem" === c || "vw" === c || "vh" === c ? l /= de(e, i, 1, c) : "px" !== c && (r = de(e, i, r, c), c = "px"), _ && (!r && 0 !== r || (d = r + l + c))), _ && (r += l), !l && 0 !== l || !r && 0 !== r ? void 0 !== f[i] && (d || d + "" != "NaN" && null != d) ? (o = new ve(f, i, r || l || 0, 0, o, -1, i, !1, 0, a, d)).xs0 = "none" !== d || "display" !== i && -1 === i.indexOf("Style") ? d : a : b("invalid " + i + " tween value: " + t[i]) : (o = new ve(f, i, l, r - l, o, 0, i, !1 !== H && ("px" === c || "zIndex" === i), 0, a, d)).xs0 = c)), s && o && !o.plugin && (o.plugin = s);
                    return o
                }, e.setRatio = function(e) {
                    var t, o, s, i = this._firstPT;
                    if (1 !== e || this._tween._time !== this._tween._duration && 0 !== this._tween._time)
                        if (e || this._tween._time !== this._tween._duration && 0 !== this._tween._time || -1e-6 === this._tween._rawPrevTime)
                            for (; i;) {
                                if (t = i.c * e + i.s, i.r ? t = Math.round(t) : t < 1e-6 && -1e-6 < t && (t = 0), i.type)
                                    if (1 === i.type)
                                        if (2 === (s = i.l)) i.t[i.p] = i.xs0 + t + i.xs1 + i.xn1 + i.xs2;
                                        else if (3 === s) i.t[i.p] = i.xs0 + t + i.xs1 + i.xn1 + i.xs2 + i.xn2 + i.xs3;
                                else if (4 === s) i.t[i.p] = i.xs0 + t + i.xs1 + i.xn1 + i.xs2 + i.xn2 + i.xs3 + i.xn3 + i.xs4;
                                else if (5 === s) i.t[i.p] = i.xs0 + t + i.xs1 + i.xn1 + i.xs2 + i.xn2 + i.xs3 + i.xn3 + i.xs4 + i.xn4 + i.xs5;
                                else {
                                    for (o = i.xs0 + t + i.xs1, s = 1; s < i.l; s++) o += i["xn" + s] + i["xs" + (s + 1)];
                                    i.t[i.p] = o
                                } else -1 === i.type ? i.t[i.p] = i.xs0 : i.setRatio && i.setRatio(e);
                                else i.t[i.p] = t + i.xs0;
                                i = i._next
                            } else
                                for (; i;) 2 !== i.type ? i.t[i.p] = i.b : i.setRatio(e), i = i._next;
                        else
                            for (; i;) {
                                if (2 !== i.type)
                                    if (i.r && -1 !== i.type)
                                        if (t = Math.round(i.s + i.c), i.type) {
                                            if (1 === i.type) {
                                                for (s = i.l, o = i.xs0 + t + i.xs1, s = 1; s < i.l; s++) o += i["xn" + s] + i["xs" + (s + 1)];
                                                i.t[i.p] = o
                                            }
                                        } else i.t[i.p] = t + i.xs0;
                                else i.t[i.p] = i.e;
                                else i.setRatio(e);
                                i = i._next
                            }
                }, e._enableTransforms = function(e) {
                    this._transform = this._transform || Ge(this._target, D, !0), this._transformType = this._transform.svg && He || !e && 3 !== this._transformType ? 2 : 3
                };

                function Ze(e) {
                    this.t[this.p] = this.e, this.data._linkCSSP(this, this._next, null, !0)
                }
                e._addLazySet = function(e, t, o) {
                    var s = this._firstPT = new ve(e, t, 0, 0, this._firstPT, 2);
                    s.e = o, s.setRatio = Ze, s.data = this
                }, e._linkCSSP = function(e, t, o, s) {
                    return e && (t && (t._prev = e), e._next && (e._next._prev = e._prev), e._prev ? e._prev._next = e._next : this._firstPT === e && (this._firstPT = e._next, s = !0), o ? o._next = e : s || null !== this._firstPT || (this._firstPT = e), e._next = t, e._prev = o), e
                }, e._mod = function(e) {
                    for (var t = this._firstPT; t;) "function" == typeof e[t.p] && e[t.p] === Math.round && (t.r = 1), t = t._next
                }, e._kill = function(e) {
                    var t, o, s, i = e;
                    if (e.autoAlpha || e.alpha) {
                        for (o in i = {}, e) i[o] = e[o];
                        i.opacity = 1, i.autoAlpha && (i.visibility = 1)
                    }
                    for (e.className && (t = this._classNamePT) && ((s = t.xfirst) && s._prev ? this._linkCSSP(s._prev, t._next, s._prev._prev) : s === this._firstPT && (this._firstPT = t._next), t._next && this._linkCSSP(t._next, t._next._next, s._prev), this._classNamePT = null), t = this._firstPT; t;) t.plugin && t.plugin !== o && t.plugin._kill && (t.plugin._kill(e), o = t.plugin), t = t._next;
                    return n.prototype._kill.call(this, i)
                };
                var et = function(e, t, o) {
                    var s, i, n, l;
                    if (e.slice)
                        for (i = e.length; - 1 < --i;) et(e[i], t, o);
                    else
                        for (i = (s = e.childNodes).length; - 1 < --i;) l = (n = s[i]).type, n.style && (t.push(g(n)), o && o.push(n)), 1 !== l && 9 !== l && 11 !== l || !n.childNodes.length || et(n, t, o)
                };
                return N.cascadeTo = function(e, t, o) {
                    var s, i, n, l, r = U.to(e, t, o),
                        a = [r],
                        d = [],
                        u = [],
                        c = [],
                        h = U._internals.reservedProps;
                    for (e = r._targets || r.target, et(e, d, c), r.render(t, !0, !0), et(e, u), r.render(0, !0, !0), r._enabled(!0), s = c.length; - 1 < --s;)
                        if ((i = S(c[s], d[s], u[s])).firstMPT) {
                            for (n in i = i.difs, o) h[n] && (i[n] = o[n]);
                            for (n in l = {}, i) l[n] = d[s][n];
                            a.push(U.fromTo(c[s], t, l, i))
                        } return a
                }, n.activate([N]), N
            }, !0), t = _fwd_gsScope._gsDefine.plugin({
                propName: "roundProps",
                version: "1.6.0",
                priority: -1,
                API: 2,
                init: function(e, t, o) {
                    return this._tween = o, !0
                }
            }), (s = t.prototype)._onInitAllProps = function() {
                for (var e, t, o, s = this._tween, i = s.vars.roundProps.join ? s.vars.roundProps : s.vars.roundProps.split(","), n = i.length, l = {}, r = s._propLookup.roundProps; - 1 < --n;) l[i[n]] = Math.round;
                for (n = i.length; - 1 < --n;)
                    for (e = i[n], t = s._firstPT; t;) o = t._next, t.pg ? t.t._mod(l) : t.n === e && (2 === t.f && t.t ? a(t.t._firstPT) : (this._add(t.t, e, t.s, t.c), o && (o._prev = t._prev), t._prev ? t._prev._next = o : s._firstPT === t && (s._firstPT = o), t._next = t._prev = null, s._propLookup[e] = r)), t = o;
                return !1
            }, s._add = function(e, t, o, s) {
                this._addTween(e, t, o, o + s, t, Math.round), this._overwriteProps.push(t)
            }, _fwd_gsScope._gsDefine.plugin({
                propName: "attr",
                API: 2,
                version: "0.6.0",
                init: function(e, t, o, s) {
                    var i, n;
                    if ("function" != typeof e.setAttribute) return !1;
                    for (i in t) "function" == typeof(n = t[i]) && (n = n(s, e)), this._addTween(e, "setAttribute", e.getAttribute(i) + "", n + "", i, !1, i), this._overwriteProps.push(i);
                    return !0
                }
            }), _fwd_gsScope._gsDefine.plugin({
                propName: "directionalRotation",
                version: "0.3.0",
                API: 2,
                init: function(e, t, o, s) {
                    "object" != typeof t && (t = {
                        rotation: t
                    }), this.finals = {};
                    var i, n, l, r, a, d, u = !0 === t.useRadians ? 2 * Math.PI : 360;
                    for (i in t) "useRadians" !== i && ("function" == typeof(r = t[i]) && (r = r(s, e)), n = (d = (r + "").split("_"))[0], l = parseFloat("function" != typeof e[i] ? e[i] : e[i.indexOf("set") || "function" != typeof e["get" + i.substr(3)] ? i : "get" + i.substr(3)]()), a = (r = this.finals[i] = "string" == typeof n && "=" === n.charAt(1) ? l + parseInt(n.charAt(0) + "1", 10) * Number(n.substr(2)) : Number(n) || 0) - l, d.length && (-1 !== (n = d.join("_")).indexOf("short") && (a %= u) !== a % (u / 2) && (a = a < 0 ? a + u : a - u), -1 !== n.indexOf("_cw") && a < 0 ? a = (a + 9999999999 * u) % u - (a / u | 0) * u : -1 !== n.indexOf("ccw") && 0 < a && (a = (a - 9999999999 * u) % u - (a / u | 0) * u)), (1e-6 < a || a < -1e-6) && (this._addTween(e, i, l, l + a, i), this._overwriteProps.push(i)));
                    return !0
                },
                set: function(e) {
                    var t;
                    if (1 !== e) this._super.setRatio.call(this, e);
                    else
                        for (t = this._firstPT; t;) t.f ? t.t[t.p](this.finals[t.p]) : t.t[t.p] = this.finals[t.p], t = t._next
                }
            })._autoCSS = !0, _fwd_gsScope._gsDefine("easing.Back", ["easing.Ease"], function(m) {
                function e(e, t) {
                    var o = u("easing." + e, function() {}, !0),
                        s = o.prototype = new m;
                    return s.constructor = o, s.getRatio = t, o
                }

                function t(e, t, o, s, i) {
                    var n = u("easing." + e, {
                        easeOut: new t,
                        easeIn: new o,
                        easeInOut: new s
                    }, !0);
                    return c(n, e), n
                }

                function b(e, t, o) {
                    this.t = e, this.v = t, o && (((this.next = o).prev = this).c = o.v - t, this.gap = o.t - e)
                }

                function o(e, t) {
                    var o = u("easing." + e, function(e) {
                            this._p1 = e || 0 === e ? e : 1.70158, this._p2 = 1.525 * this._p1
                        }, !0),
                        s = o.prototype = new m;
                    return s.constructor = o, s.getRatio = t, s.config = function(e) {
                        return new o(e)
                    }, o
                }
                var s, i, n, l = _fwd_gsScope.GreenSockGlobals || _fwd_gsScope,
                    r = l.com.greensock,
                    a = 2 * Math.PI,
                    d = Math.PI / 2,
                    u = r._class,
                    c = m.register || function() {},
                    h = t("Back", o("BackOut", function(e) {
                        return --e * e * ((this._p1 + 1) * e + this._p1) + 1
                    }), o("BackIn", function(e) {
                        return e * e * ((this._p1 + 1) * e - this._p1)
                    }), o("BackInOut", function(e) {
                        return (e *= 2) < 1 ? .5 * e * e * ((this._p2 + 1) * e - this._p2) : .5 * ((e -= 2) * e * ((this._p2 + 1) * e + this._p2) + 2)
                    })),
                    _ = u("easing.SlowMo", function(e, t, o) {
                        t = t || 0 === t ? t : .7, null == e ? e = .7 : 1 < e && (e = 1), this._p = 1 !== e ? t : 0, this._p1 = (1 - e) / 2, this._p2 = e, this._p3 = this._p1 + this._p2, this._calcEnd = !0 === o
                    }, !0),
                    f = _.prototype = new m;
                return f.constructor = _, f.getRatio = function(e) {
                    var t = e + (.5 - e) * this._p;
                    return e < this._p1 ? this._calcEnd ? 1 - (e = 1 - e / this._p1) * e : t - (e = 1 - e / this._p1) * e * e * e * t : e > this._p3 ? this._calcEnd ? 1 - (e = (e - this._p3) / this._p1) * e : t + (e - t) * (e = (e - this._p3) / this._p1) * e * e * e : this._calcEnd ? 1 : t
                }, _.ease = new _(.7, .7), f.config = _.config = function(e, t, o) {
                    return new _(e, t, o)
                }, (f = (s = u("easing.SteppedEase", function(e) {
                    e = e || 1, this._p1 = 1 / e, this._p2 = e + 1
                }, !0)).prototype = new m).constructor = s, f.getRatio = function(e) {
                    return e < 0 ? e = 0 : 1 <= e && (e = .999999999), (this._p2 * e >> 0) * this._p1
                }, f.config = s.config = function(e) {
                    return new s(e)
                }, (f = (i = u("easing.RoughEase", function(e) {
                    for (var t, o, s, i, n, l, r = (e = e || {}).taper || "none", a = [], d = 0, u = 0 | (e.points || 20), c = u, h = !1 !== e.randomize, _ = !0 === e.clamp, f = e.template instanceof m ? e.template : null, p = "number" == typeof e.strength ? .4 * e.strength : .4; - 1 < --c;) t = h ? Math.random() : 1 / u * c, o = f ? f.getRatio(t) : t, s = "none" === r ? p : "out" === r ? (i = 1 - t) * i * p : "in" === r ? t * t * p : t < .5 ? (i = 2 * t) * i * .5 * p : (i = 2 * (1 - t)) * i * .5 * p, h ? o += Math.random() * s - .5 * s : c % 2 ? o += .5 * s : o -= .5 * s, _ && (1 < o ? o = 1 : o < 0 && (o = 0)), a[d++] = {
                        x: t,
                        y: o
                    };
                    for (a.sort(function(e, t) {
                            return e.x - t.x
                        }), l = new b(1, 1, null), c = u; - 1 < --c;) n = a[c], l = new b(n.x, n.y, l);
                    this._prev = new b(0, 0, 0 !== l.t ? l : l.next)
                }, !0)).prototype = new m).constructor = i, f.getRatio = function(e) {
                    var t = this._prev;
                    if (e > t.t) {
                        for (; t.next && e >= t.t;) t = t.next;
                        t = t.prev
                    } else
                        for (; t.prev && e <= t.t;) t = t.prev;
                    return (this._prev = t).v + (e - t.t) / t.gap * t.c
                }, f.config = function(e) {
                    return new i(e)
                }, i.ease = new i, t("Bounce", e("BounceOut", function(e) {
                    return e < 1 / 2.75 ? 7.5625 * e * e : e < 2 / 2.75 ? 7.5625 * (e -= 1.5 / 2.75) * e + .75 : e < 2.5 / 2.75 ? 7.5625 * (e -= 2.25 / 2.75) * e + .9375 : 7.5625 * (e -= 2.625 / 2.75) * e + .984375
                }), e("BounceIn", function(e) {
                    return (e = 1 - e) < 1 / 2.75 ? 1 - 7.5625 * e * e : e < 2 / 2.75 ? 1 - (7.5625 * (e -= 1.5 / 2.75) * e + .75) : e < 2.5 / 2.75 ? 1 - (7.5625 * (e -= 2.25 / 2.75) * e + .9375) : 1 - (7.5625 * (e -= 2.625 / 2.75) * e + .984375)
                }), e("BounceInOut", function(e) {
                    var t = e < .5;
                    return (e = t ? 1 - 2 * e : 2 * e - 1) < 1 / 2.75 ? e *= 7.5625 * e : e = e < 2 / 2.75 ? 7.5625 * (e -= 1.5 / 2.75) * e + .75 : e < 2.5 / 2.75 ? 7.5625 * (e -= 2.25 / 2.75) * e + .9375 : 7.5625 * (e -= 2.625 / 2.75) * e + .984375, t ? .5 * (1 - e) : .5 * e + .5
                })), t("Circ", e("CircOut", function(e) {
                    return Math.sqrt(1 - --e * e)
                }), e("CircIn", function(e) {
                    return -(Math.sqrt(1 - e * e) - 1)
                }), e("CircInOut", function(e) {
                    return (e *= 2) < 1 ? -.5 * (Math.sqrt(1 - e * e) - 1) : .5 * (Math.sqrt(1 - (e -= 2) * e) + 1)
                })), t("Elastic", (n = function(e, t, o) {
                    var s = u("easing." + e, function(e, t) {
                            this._p1 = 1 <= e ? e : 1, this._p2 = (t || o) / (e < 1 ? e : 1), this._p3 = this._p2 / a * (Math.asin(1 / this._p1) || 0), this._p2 = a / this._p2
                        }, !0),
                        i = s.prototype = new m;
                    return i.constructor = s, i.getRatio = t, i.config = function(e, t) {
                        return new s(e, t)
                    }, s
                })("ElasticOut", function(e) {
                    return this._p1 * Math.pow(2, -10 * e) * Math.sin((e - this._p3) * this._p2) + 1
                }, .3), n("ElasticIn", function(e) {
                    return -this._p1 * Math.pow(2, 10 * --e) * Math.sin((e - this._p3) * this._p2)
                }, .3), n("ElasticInOut", function(e) {
                    return (e *= 2) < 1 ? this._p1 * Math.pow(2, 10 * --e) * Math.sin((e - this._p3) * this._p2) * -.5 : this._p1 * Math.pow(2, -10 * --e) * Math.sin((e - this._p3) * this._p2) * .5 + 1
                }, .45)), t("Expo", e("ExpoOut", function(e) {
                    return 1 - Math.pow(2, -10 * e)
                }), e("ExpoIn", function(e) {
                    return Math.pow(2, 10 * (e - 1)) - .001
                }), e("ExpoInOut", function(e) {
                    return (e *= 2) < 1 ? .5 * Math.pow(2, 10 * (e - 1)) : .5 * (2 - Math.pow(2, -10 * (e - 1)))
                })), t("Sine", e("SineOut", function(e) {
                    return Math.sin(e * d)
                }), e("SineIn", function(e) {
                    return 1 - Math.cos(e * d)
                }), e("SineInOut", function(e) {
                    return -.5 * (Math.cos(Math.PI * e) - 1)
                })), u("easing.EaseLookup", {
                    find: function(e) {
                        return m.map[e]
                    }
                }, !0), c(l.SlowMo, "SlowMo", "ease,"), c(i, "RoughEase", "ease,"), c(s, "SteppedEase", "ease,"), h
            }, !0)
        }), _fwd_gsScope._gsDefine && _fwd_gsScope._fwd_gsQueue.pop()(),
        function(_, f) {
            "use strict";
            var p = {},
                m = _.GreenSockGlobals = _.GreenSockGlobals || _;
            if (!m.FWDTweenLite) {
                var e, t, o, b, g, s, i, S = function(e) {
                        var t, o = e.split("."),
                            s = m;
                        for (t = 0; t < o.length; t++) s[o[t]] = s = s[o[t]] || {};
                        return s
                    },
                    c = S("com.greensock"),
                    y = 1e-10,
                    a = function(e) {
                        var t, o = [],
                            s = e.length;
                        for (t = 0; t !== s; o.push(e[t++]));
                        return o
                    },
                    v = function() {},
                    P = (s = Object.prototype.toString, i = s.call([]), function(e) {
                        return null != e && (e instanceof Array || "object" == typeof e && !!e.push && s.call(e) === i)
                    }),
                    T = {},
                    w = function(a, d, u, c) {
                        this.sc = T[a] ? T[a].sc : [], (T[a] = this).gsClass = null, this.func = u;
                        var h = [];
                        this.check = function(e) {
                            for (var t, o, s, i, n, l = d.length, r = l; - 1 < --l;)(t = T[d[l]] || new w(d[l], [])).gsClass ? (h[l] = t.gsClass, r--) : e && t.sc.push(this);
                            if (0 === r && u) {
                                if (s = (o = ("com.greensock." + a).split(".")).pop(), i = S(o.join("."))[s] = this.gsClass = u.apply(u, h), c)
                                    if (m[s] = p[s] = i, !(n = "undefined" != typeof fwd_module && fwd_module.exports) && "function" == typeof define && define.amd) define((_.GreenSockAMDPath ? _.GreenSockAMDPath + "/" : "") + a.split(".").pop(), [], function() {
                                        return i
                                    });
                                    else if (n)
                                    if (a === f)
                                        for (l in fwd_module.exports = p[f] = i, p) i[l] = p[l];
                                    else p[f] && (p[f][s] = i);
                                for (l = 0; l < this.sc.length; l++) this.sc[l].check()
                            }
                        }, this.check(!0)
                    },
                    n = _._gsDefine = function(e, t, o, s) {
                        return new w(e, t, o, s)
                    },
                    h = c._class = function(e, t, o) {
                        return t = t || function() {}, n(e, [], function() {
                            return t
                        }, o), t
                    };
                n.globals = m;
                var l = [0, 0, 1, 1],
                    D = h("easing.Ease", function(e, t, o, s) {
                        this._func = e, this._type = o || 0, this._power = s || 0, this._params = t ? l.concat(t) : l
                    }, !0),
                    B = D.map = {},
                    r = D.register = function(e, t, o, s) {
                        for (var i, n, l, r, a = t.split(","), d = a.length, u = (o || "easeIn,easeOut,easeInOut").split(","); - 1 < --d;)
                            for (n = a[d], i = s ? h("easing." + n, null, !0) : c.easing[n] || {}, l = u.length; - 1 < --l;) r = u[l], B[n + "." + r] = B[r + n] = i[r] = e.getRatio ? e : e[r] || new e
                    };
                for ((o = D.prototype)._calcEnd = !1, o.getRatio = function(e) {
                        if (this._func) return this._params[0] = e, this._func.apply(null, this._params);
                        var t = this._type,
                            o = this._power,
                            s = 1 === t ? 1 - e : 2 === t ? e : e < .5 ? 2 * e : 2 * (1 - e);
                        return 1 === o ? s *= s : 2 === o ? s *= s * s : 3 === o ? s *= s * s * s : 4 === o && (s *= s * s * s * s), 1 === t ? 1 - s : 2 === t ? s : e < .5 ? s / 2 : 1 - s / 2
                    }, t = (e = ["Linear", "Quad", "Cubic", "Quart", "Quint,Strong"]).length; - 1 < --t;) o = e[t] + ",Power" + t, r(new D(null, null, 1, t), o, "easeOut", !0), r(new D(null, null, 2, t), o, "easeIn" + (0 === t ? ",easeNone" : "")), r(new D(null, null, 3, t), o, "easeInOut");
                B.linear = c.easing.Linear.easeIn, B.swing = c.easing.Quad.easeInOut;
                var M = h("events.EventDispatcher", function(e) {
                    this._listeners = {}, this._eventTarget = e || this
                });
                (o = M.prototype).addEventListener = function(e, t, o, s, i) {
                    i = i || 0;
                    var n, l, r = this._listeners[e],
                        a = 0;
                    for (this !== b || g || b.wake(), null == r && (this._listeners[e] = r = []), l = r.length; - 1 < --l;)(n = r[l]).c === t && n.s === o ? r.splice(l, 1) : 0 === a && n.pr < i && (a = l + 1);
                    r.splice(a, 0, {
                        c: t,
                        s: o,
                        up: s,
                        pr: i
                    })
                }, o.removeEventListener = function(e, t) {
                    var o, s = this._listeners[e];
                    if (s)
                        for (o = s.length; - 1 < --o;)
                            if (s[o].c === t) return void s.splice(o, 1)
                }, o.dispatchEvent = function(e) {
                    var t, o, s, i = this._listeners[e];
                    if (i)
                        for (1 < (t = i.length) && (i = i.slice(0)), o = this._eventTarget; - 1 < --t;)(s = i[t]) && (s.up ? s.c.call(s.s || o, {
                            type: e,
                            target: o
                        }) : s.c.call(s.s || o))
                };
                var F = _.requestAnimationFrame,
                    W = _.cancelAnimationFrame,
                    H = Date.now || function() {
                        return (new Date).getTime()
                    },
                    C = H();
                for (t = (e = ["ms", "moz", "webkit", "o"]).length; - 1 < --t && !F;) F = _[e[t] + "RequestAnimationFrame"], W = _[e[t] + "CancelAnimationFrame"] || _[e[t] + "CancelRequestAnimationFrame"];
                h("Ticker", function(e, t) {
                    var i, n, l, r, a, d = this,
                        u = H(),
                        o = !(!1 === t || !F) && "auto",
                        c = 500,
                        h = 33,
                        _ = function(e) {
                            var t, o, s = H() - C;
                            c < s && (u += s - h), C += s, d.time = (C - u) / 1e3, t = d.time - a, (!i || 0 < t || !0 === e) && (d.frame++, a += t + (r <= t ? .004 : r - t), o = !0), !0 !== e && (l = n(_)), o && d.dispatchEvent("tick")
                        };
                    M.call(d), d.time = d.frame = 0, d.tick = function() {
                        _(!0)
                    }, d.lagSmoothing = function(e, t) {
                        c = e || 1e10, h = Math.min(t, c, 0)
                    }, d.sleep = function() {
                        null != l && (o && W ? W(l) : clearTimeout(l), n = v, l = null, d === b && (g = !1))
                    }, d.wake = function(e) {
                        null !== l ? d.sleep() : e ? u += -C + (C = H()) : 10 < d.frame && (C = H() - c + 5), n = 0 === i ? v : o && F ? F : function(e) {
                            return setTimeout(e, 1e3 * (a - d.time) + 1 | 0)
                        }, d === b && (g = !0), _(2)
                    }, d.fps = function(e) {
                        if (!arguments.length) return i;
                        r = 1 / ((i = e) || 60), a = this.time + r, d.wake()
                    }, d.useRAF = function(e) {
                        if (!arguments.length) return o;
                        d.sleep(), o = e, d.fps(i)
                    }, d.fps(e), setTimeout(function() {
                        "auto" === o && d.frame < 5 && "hidden" !== document.visibilityState && d.useRAF(!1)
                    }, 1500)
                }), (o = c.Ticker.prototype = new c.events.EventDispatcher).constructor = c.Ticker;
                var d = h("core.Animation", function(e, t) {
                    if (this.vars = t = t || {}, this._duration = this._totalDuration = e || 0, this._delay = Number(t.delay) || 0, this._timeScale = 1, this._active = !0 === t.immediateRender, this.data = t.data, this._reversed = !0 === t.reversed, q) {
                        g || b.wake();
                        var o = this.vars.useFrames ? G : q;
                        o.add(this, o._time), this.vars.paused && this.paused(!0)
                    }
                });
                b = d.ticker = new c.Ticker, (o = d.prototype)._dirty = o._gc = o._initted = o._paused = !1, o._totalTime = o._time = 0, o._rawPrevTime = -1, o._next = o._last = o._onUpdate = o._timeline = o.timeline = null, o._paused = !1;
                var u = function() {
                    g && 2e3 < H() - C && b.wake(), setTimeout(u, 2e3)
                };
                u(), o.play = function(e, t) {
                    return null != e && this.seek(e, t), this.reversed(!1).paused(!1)
                }, o.pause = function(e, t) {
                    return null != e && this.seek(e, t), this.paused(!0)
                }, o.resume = function(e, t) {
                    return null != e && this.seek(e, t), this.paused(!1)
                }, o.seek = function(e, t) {
                    return this.totalTime(Number(e), !1 !== t)
                }, o.restart = function(e, t) {
                    return this.reversed(!1).paused(!1).totalTime(e ? -this._delay : 0, !1 !== t, !0)
                }, o.reverse = function(e, t) {
                    return null != e && this.seek(e || this.totalDuration(), t), this.reversed(!0).paused(!1)
                }, o.render = function(e, t, o) {}, o.invalidate = function() {
                    return this._time = this._totalTime = 0, this._initted = this._gc = !1, this._rawPrevTime = -1, !this._gc && this.timeline || this._enabled(!0), this
                }, o.isActive = function() {
                    var e, t = this._timeline,
                        o = this._startTime;
                    return !t || !this._gc && !this._paused && t.isActive() && (e = t.rawTime()) >= o && e < o + this.totalDuration() / this._timeScale
                }, o._enabled = function(e, t) {
                    return g || b.wake(), this._gc = !e, this._active = this.isActive(), !0 !== t && (e && !this.timeline ? this._timeline.add(this, this._startTime - this._delay) : !e && this.timeline && this._timeline._remove(this, !0)), !1
                }, o._kill = function(e, t) {
                    return this._enabled(!1, !1)
                }, o.kill = function(e, t) {
                    return this._kill(e, t), this
                }, o._uncache = function(e) {
                    for (var t = e ? this : this.timeline; t;) t._dirty = !0, t = t.timeline;
                    return this
                }, o._swapSelfInParams = function(e) {
                    for (var t = e.length, o = e.concat(); - 1 < --t;) "{self}" === e[t] && (o[t] = this);
                    return o
                }, o._callback = function(e) {
                    var t = this.vars,
                        o = t[e],
                        s = t[e + "Params"],
                        i = t[e + "Scope"] || t.callbackScope || this;
                    switch (s ? s.length : 0) {
                        case 0:
                            o.call(i);
                            break;
                        case 1:
                            o.call(i, s[0]);
                            break;
                        case 2:
                            o.call(i, s[0], s[1]);
                            break;
                        default:
                            o.apply(i, s)
                    }
                }, o.eventCallback = function(e, t, o, s) {
                    if ("on" === (e || "").substr(0, 2)) {
                        var i = this.vars;
                        if (1 === arguments.length) return i[e];
                        null == t ? delete i[e] : (i[e] = t, i[e + "Params"] = P(o) && -1 !== o.join("").indexOf("{self}") ? this._swapSelfInParams(o) : o, i[e + "Scope"] = s), "onUpdate" === e && (this._onUpdate = t)
                    }
                    return this
                }, o.delay = function(e) {
                    return arguments.length ? (this._timeline.smoothChildTiming && this.startTime(this._startTime + e - this._delay), this._delay = e, this) : this._delay
                }, o.duration = function(e) {
                    return arguments.length ? (this._duration = this._totalDuration = e, this._uncache(!0), this._timeline.smoothChildTiming && 0 < this._time && this._time < this._duration && 0 !== e && this.totalTime(this._totalTime * (e / this._duration), !0), this) : (this._dirty = !1, this._duration)
                }, o.totalDuration = function(e) {
                    return this._dirty = !1, arguments.length ? this.duration(e) : this._totalDuration
                }, o.time = function(e, t) {
                    return arguments.length ? (this._dirty && this.totalDuration(), this.totalTime(e > this._duration ? this._duration : e, t)) : this._time
                }, o.totalTime = function(e, t, o) {
                    if (g || b.wake(), !arguments.length) return this._totalTime;
                    if (this._timeline) {
                        if (e < 0 && !o && (e += this.totalDuration()), this._timeline.smoothChildTiming) {
                            this._dirty && this.totalDuration();
                            var s = this._totalDuration,
                                i = this._timeline;
                            if (s < e && !o && (e = s), this._startTime = (this._paused ? this._pauseTime : i._time) - (this._reversed ? s - e : e) / this._timeScale, i._dirty || this._uncache(!1), i._timeline)
                                for (; i._timeline;) i._timeline._time !== (i._startTime + i._totalTime) / i._timeScale && i.totalTime(i._totalTime, !0), i = i._timeline
                        }
                        this._gc && this._enabled(!0, !1), this._totalTime === e && 0 !== this._duration || (L.length && J(), this.render(e, t, !1), L.length && J())
                    }
                    return this
                }, o.progress = o.totalProgress = function(e, t) {
                    var o = this.duration();
                    return arguments.length ? this.totalTime(o * e, t) : o ? this._time / o : this.ratio
                }, o.startTime = function(e) {
                    return arguments.length ? (e !== this._startTime && (this._startTime = e, this.timeline && this.timeline._sortChildren && this.timeline.add(this, e - this._delay)), this) : this._startTime
                }, o.endTime = function(e) {
                    return this._startTime + (0 != e ? this.totalDuration() : this.duration()) / this._timeScale
                }, o.timeScale = function(e) {
                    if (!arguments.length) return this._timeScale;
                    if (e = e || y, this._timeline && this._timeline.smoothChildTiming) {
                        var t = this._pauseTime,
                            o = t || 0 === t ? t : this._timeline.totalTime();
                        this._startTime = o - (o - this._startTime) * this._timeScale / e
                    }
                    return this._timeScale = e, this._uncache(!1)
                }, o.reversed = function(e) {
                    return arguments.length ? (e != this._reversed && (this._reversed = e, this.totalTime(this._timeline && !this._timeline.smoothChildTiming ? this.totalDuration() - this._totalTime : this._totalTime, !0)), this) : this._reversed
                }, o.paused = function(e) {
                    if (!arguments.length) return this._paused;
                    var t, o, s = this._timeline;
                    return e != this._paused && s && (g || e || b.wake(), o = (t = s.rawTime()) - this._pauseTime, !e && s.smoothChildTiming && (this._startTime += o, this._uncache(!1)), this._pauseTime = e ? t : null, this._paused = e, this._active = this.isActive(), !e && 0 != o && this._initted && this.duration() && (t = s.smoothChildTiming ? this._totalTime : (t - this._startTime) / this._timeScale, this.render(t, t === this._totalTime, !0))), this._gc && !e && this._enabled(!0, !1), this
                };
                var E = h("core.SimpleTimeline", function(e) {
                    d.call(this, 0, e), this.autoRemoveChildren = this.smoothChildTiming = !0
                });
                (o = E.prototype = new d).constructor = E, o.kill()._gc = !1, o._first = o._last = o._recent = null, o._sortChildren = !1, o.add = o.insert = function(e, t, o, s) {
                    var i, n;
                    if (e._startTime = Number(t || 0) + e._delay, e._paused && this !== e._timeline && (e._pauseTime = e._startTime + (this.rawTime() - e._startTime) / e._timeScale), e.timeline && e.timeline._remove(e, !0), e.timeline = e._timeline = this, e._gc && e._enabled(!0, !0), i = this._last, this._sortChildren)
                        for (n = e._startTime; i && i._startTime > n;) i = i._prev;
                    return i ? (e._next = i._next, i._next = e) : (e._next = this._first, this._first = e), e._next ? e._next._prev = e : this._last = e, e._prev = i, this._recent = e, this._timeline && this._uncache(!0), this
                }, o._remove = function(e, t) {
                    return e.timeline === this && (t || e._enabled(!1, !0), e._prev ? e._prev._next = e._next : this._first === e && (this._first = e._next), e._next ? e._next._prev = e._prev : this._last === e && (this._last = e._prev), e._next = e._prev = e.timeline = null, e === this._recent && (this._recent = this._last), this._timeline && this._uncache(!0)), this
                }, o.render = function(e, t, o) {
                    var s, i = this._first;
                    for (this._totalTime = this._time = this._rawPrevTime = e; i;) s = i._next, (i._active || e >= i._startTime && !i._paused) && (i._reversed ? i.render((i._dirty ? i.totalDuration() : i._totalDuration) - (e - i._startTime) * i._timeScale, t, o) : i.render((e - i._startTime) * i._timeScale, t, o)), i = s
                }, o.rawTime = function() {
                    return g || b.wake(), this._totalTime
                };
                var O = h("FWDTweenLite", function(e, t, o) {
                        if (d.call(this, t, o), this.render = O.prototype.render, null == e) throw "Cannot tween a null target.";
                        this.target = e = "string" != typeof e ? e : O.selector(e) || e;
                        var s, i, n, l = e.jquery || e.length && e !== _ && e[0] && (e[0] === _ || e[0].nodeType && e[0].style && !e.nodeType),
                            r = this.vars.overwrite;
                        if (this._overwrite = r = null == r ? z[O.defaultOverwrite] : "number" == typeof r ? r >> 0 : z[r], (l || e instanceof Array || e.push && P(e)) && "number" != typeof e[0])
                            for (this._targets = n = a(e), this._propLookup = [], this._siblings = [], s = 0; s < n.length; s++)(i = n[s]) ? "string" != typeof i ? i.length && i !== _ && i[0] && (i[0] === _ || i[0].nodeType && i[0].style && !i.nodeType) ? (n.splice(s--, 1), this._targets = n = n.concat(a(i))) : (this._siblings[s] = Q(i, this, !1), 1 === r && 1 < this._siblings[s].length && Z(i, this, null, 1, this._siblings[s])) : "string" == typeof(i = n[s--] = O.selector(i)) && n.splice(s + 1, 1) : n.splice(s--, 1);
                        else this._propLookup = {}, this._siblings = Q(e, this, !1), 1 === r && 1 < this._siblings.length && Z(e, this, null, 1, this._siblings);
                        (this.vars.immediateRender || 0 === t && 0 === this._delay && !1 !== this.vars.immediateRender) && (this._time = -y, this.render(Math.min(0, -this._delay)))
                    }, !0),
                    k = function(e) {
                        return e && e.length && e !== _ && e[0] && (e[0] === _ || e[0].nodeType && e[0].style && !e.nodeType)
                    };
                (o = O.prototype = new d).constructor = O, o.kill()._gc = !1, o.ratio = 0, o._firstPT = o._targets = o._overwrittenProps = o._startAt = null, o._notifyPluginsOfEnabled = o._lazy = !1, O.version = "1.19.0", O.defaultEase = o._ease = new D(null, null, 1, 1), O.defaultOverwrite = "auto", O.ticker = b, O.autoSleep = 120, O.lagSmoothing = function(e, t) {
                    b.lagSmoothing(e, t)
                }, O.selector = _.$ || _.jQuery || function(e) {
                    var t = _.$ || _.jQuery;
                    return t ? (O.selector = t)(e) : "undefined" == typeof document ? e : document.querySelectorAll ? document.querySelectorAll(e) : document.getElementById("#" === e.charAt(0) ? e.substr(1) : e)
                };
                var L = [],
                    I = {},
                    x = /(?:(-|-=|\+=)?\d*\.?\d*(?:e[\-+]?\d+)?)[0-9]/gi,
                    A = function(e) {
                        for (var t, o = this._firstPT; o;) t = o.blob ? e ? this.join("") : this.start : o.c * e + o.s, o.m ? t = o.m(t, this._target || o.t) : t < 1e-6 && -1e-6 < t && (t = 0), o.f ? o.fp ? o.t[o.p](o.fp, t) : o.t[o.p](t) : o.t[o.p] = t, o = o._next
                    },
                    R = function(e, t, o, s) {
                        var i, n, l, r, a, d, u, c = [e, t],
                            h = 0,
                            _ = "",
                            f = 0;
                        for (c.start = e, o && (o(c), e = c[0], t = c[1]), c.length = 0, i = e.match(x) || [], n = t.match(x) || [], s && (s._next = null, s.blob = 1, c._firstPT = c._applyPT = s), a = n.length, r = 0; r < a; r++) u = n[r], _ += (d = t.substr(h, t.indexOf(u, h) - h)) || !r ? d : ",", h += d.length, f ? f = (f + 1) % 5 : "rgba(" === d.substr(-5) && (f = 1), u === i[r] || i.length <= r ? _ += u : (_ && (c.push(_), _ = ""), l = parseFloat(i[r]), c.push(l), c._firstPT = {
                            _next: c._firstPT,
                            t: c,
                            p: c.length - 1,
                            s: l,
                            c: ("=" === u.charAt(1) ? parseInt(u.charAt(0) + "1", 10) * parseFloat(u.substr(2)) : parseFloat(u) - l) || 0,
                            f: 0,
                            m: f && f < 4 ? Math.round : 0
                        }), h += u.length;
                        return (_ += t.substr(h)) && c.push(_), c.setRatio = A, c
                    },
                    U = function(e, t, o, s, i, n, l, r, a) {
                        "function" == typeof s && (s = s(a || 0, e));
                        var d, u = "get" === o ? e[t] : o,
                            c = typeof e[t],
                            h = "string" == typeof s && "=" === s.charAt(1),
                            _ = {
                                t: e,
                                p: t,
                                s: u,
                                f: "function" == c,
                                pg: 0,
                                n: i || t,
                                m: n ? "function" == typeof n ? n : Math.round : 0,
                                pr: 0,
                                c: h ? parseInt(s.charAt(0) + "1", 10) * parseFloat(s.substr(2)) : parseFloat(s) - u || 0
                            };
                        if ("number" != c && ("function" == c && "get" === o && (d = t.indexOf("set") || "function" != typeof e["get" + t.substr(3)] ? t : "get" + t.substr(3), _.s = u = l ? e[d](l) : e[d]()), "string" == typeof u && (l || isNaN(u)) ? (_.fp = l, _ = {
                                t: R(u, s, r || O.defaultStringFilter, _),
                                p: "setRatio",
                                s: 0,
                                c: 1,
                                f: 2,
                                pg: 0,
                                n: i || t,
                                pr: 0,
                                m: 0
                            }) : h || (_.s = parseFloat(u), _.c = parseFloat(s) - _.s || 0)), _.c) return (_._next = this._firstPT) && (_._next._prev = _), this._firstPT = _
                    },
                    N = O._internals = {
                        isArray: P,
                        isSelector: k,
                        lazyTweens: L,
                        blobDif: R
                    },
                    Y = O._plugins = {},
                    X = N.tweenLookup = {},
                    V = 0,
                    j = N.reservedProps = {
                        ease: 1,
                        delay: 1,
                        overwrite: 1,
                        onComplete: 1,
                        onCompleteParams: 1,
                        onCompleteScope: 1,
                        useFrames: 1,
                        runBackwards: 1,
                        startAt: 1,
                        onUpdate: 1,
                        onUpdateParams: 1,
                        onUpdateScope: 1,
                        onStart: 1,
                        onStartParams: 1,
                        onStartScope: 1,
                        onReverseComplete: 1,
                        onReverseCompleteParams: 1,
                        onReverseCompleteScope: 1,
                        onRepeat: 1,
                        onRepeatParams: 1,
                        onRepeatScope: 1,
                        easeParams: 1,
                        yoyo: 1,
                        immediateRender: 1,
                        repeat: 1,
                        repeatDelay: 1,
                        data: 1,
                        paused: 1,
                        reversed: 1,
                        autoCSS: 1,
                        lazy: 1,
                        onOverwrite: 1,
                        callbackScope: 1,
                        stringFilter: 1,
                        id: 1
                    },
                    z = {
                        none: 0,
                        all: 1,
                        auto: 2,
                        concurrent: 3,
                        allOnStart: 4,
                        preexisting: 5,
                        true: 1,
                        false: 0
                    },
                    G = d._rootFramesTimeline = new E,
                    q = d._rootTimeline = new E,
                    K = 30,
                    J = N.lazyRender = function() {
                        var e, t = L.length;
                        for (I = {}; - 1 < --t;)(e = L[t]) && !1 !== e._lazy && (e.render(e._lazy[0], e._lazy[1], !0), e._lazy = !1);
                        L.length = 0
                    };
                q._startTime = b.time, G._startTime = b.frame, q._active = G._active = !0, setTimeout(J, 1), d._updateRoot = O.render = function() {
                    var e, t, o;
                    if (L.length && J(), q.render((b.time - q._startTime) * q._timeScale, !1, !1), G.render((b.frame - G._startTime) * G._timeScale, !1, !1), L.length && J(), b.frame >= K) {
                        for (o in K = b.frame + (parseInt(O.autoSleep, 10) || 120), X) {
                            for (e = (t = X[o].tweens).length; - 1 < --e;) t[e]._gc && t.splice(e, 1);
                            0 === t.length && delete X[o]
                        }
                        if ((!(o = q._first) || o._paused) && O.autoSleep && !G._first && 1 === b._listeners.tick.length) {
                            for (; o && o._paused;) o = o._next;
                            o || b.sleep()
                        }
                    }
                }, b.addEventListener("tick", d._updateRoot);
                var Q = function(e, t, o) {
                        var s, i, n = e._gsTweenID;
                        if (X[n || (e._gsTweenID = n = "t" + V++)] || (X[n] = {
                                target: e,
                                tweens: []
                            }), t && ((s = X[n].tweens)[i = s.length] = t, o))
                            for (; - 1 < --i;) s[i] === t && s.splice(i, 1);
                        return X[n].tweens
                    },
                    $ = function(e, t, o, s) {
                        var i, n, l = e.vars.onOverwrite;
                        return l && (i = l(e, t, o, s)), (l = O.onOverwrite) && (n = l(e, t, o, s)), !1 !== i && !1 !== n
                    },
                    Z = function(e, t, o, s, i) {
                        var n, l, r, a;
                        if (1 === s || 4 <= s) {
                            for (a = i.length, n = 0; n < a; n++)
                                if ((r = i[n]) !== t) r._gc || r._kill(null, e, t) && (l = !0);
                                else if (5 === s) break;
                            return l
                        }
                        var d, u = t._startTime + y,
                            c = [],
                            h = 0,
                            _ = 0 === t._duration;
                        for (n = i.length; - 1 < --n;)(r = i[n]) === t || r._gc || r._paused || (r._timeline !== t._timeline ? (d = d || ee(t, 0, _), 0 === ee(r, d, _) && (c[h++] = r)) : r._startTime <= u && r._startTime + r.totalDuration() / r._timeScale > u && ((_ || !r._initted) && u - r._startTime <= 2e-10 || (c[h++] = r)));
                        for (n = h; - 1 < --n;)
                            if (r = c[n], 2 === s && r._kill(o, e, t) && (l = !0), 2 !== s || !r._firstPT && r._initted) {
                                if (2 !== s && !$(r, t)) continue;
                                r._enabled(!1, !1) && (l = !0)
                            } return l
                    },
                    ee = function(e, t, o) {
                        for (var s = e._timeline, i = s._timeScale, n = e._startTime; s._timeline;) {
                            if (n += s._startTime, i *= s._timeScale, s._paused) return -100;
                            s = s._timeline
                        }
                        return t < (n /= i) ? n - t : o && n === t || !e._initted && n - t < 2 * y ? y : (n += e.totalDuration() / e._timeScale / i) > t + y ? 0 : n - t - y
                    };
                o._init = function() {
                    var e, t, o, s, i, n, l = this.vars,
                        r = this._overwrittenProps,
                        a = this._duration,
                        d = !!l.immediateRender,
                        u = l.ease;
                    if (l.startAt) {
                        for (s in this._startAt && (this._startAt.render(-1, !0), this._startAt.kill()), i = {}, l.startAt) i[s] = l.startAt[s];
                        if (i.overwrite = !1, i.immediateRender = !0, i.lazy = d && !1 !== l.lazy, i.startAt = i.delay = null, this._startAt = O.to(this.target, 0, i), d)
                            if (0 < this._time) this._startAt = null;
                            else if (0 !== a) return
                    } else if (l.runBackwards && 0 !== a)
                        if (this._startAt) this._startAt.render(-1, !0), this._startAt.kill(), this._startAt = null;
                        else {
                            for (s in 0 !== this._time && (d = !1), o = {}, l) j[s] && "autoCSS" !== s || (o[s] = l[s]);
                            if (o.overwrite = 0, o.data = "isFromStart", o.lazy = d && !1 !== l.lazy, o.immediateRender = d, this._startAt = O.to(this.target, 0, o), d) {
                                if (0 === this._time) return
                            } else this._startAt._init(), this._startAt._enabled(!1), this.vars.immediateRender && (this._startAt = null)
                        } if (this._ease = u = u ? u instanceof D ? u : "function" == typeof u ? new D(u, l.easeParams) : B[u] || O.defaultEase : O.defaultEase, l.easeParams instanceof Array && u.config && (this._ease = u.config.apply(u, l.easeParams)), this._easeType = this._ease._type, this._easePower = this._ease._power, this._firstPT = null, this._targets)
                        for (n = this._targets.length, e = 0; e < n; e++) this._initProps(this._targets[e], this._propLookup[e] = {}, this._siblings[e], r ? r[e] : null, e) && (t = !0);
                    else t = this._initProps(this.target, this._propLookup, this._siblings, r, 0);
                    if (t && O._onPluginEvent("_onInitAllProps", this), r && (this._firstPT || "function" != typeof this.target && this._enabled(!1, !1)), l.runBackwards)
                        for (o = this._firstPT; o;) o.s += o.c, o.c = -o.c, o = o._next;
                    this._onUpdate = l.onUpdate, this._initted = !0
                }, o._initProps = function(e, t, o, s, i) {
                    var n, l, r, a, d, u;
                    if (null == e) return !1;
                    for (n in I[e._gsTweenID] && J(), this.vars.css || e.style && e !== _ && e.nodeType && Y.css && !1 !== this.vars.autoCSS && function(e, t) {
                            var o, s = {};
                            for (o in e) j[o] || o in t && "transform" !== o && "x" !== o && "y" !== o && "width" !== o && "height" !== o && "className" !== o && "border" !== o || !(!Y[o] || Y[o] && Y[o]._autoCSS) || (s[o] = e[o], delete e[o]);
                            e.css = s
                        }(this.vars, e), this.vars)
                        if (u = this.vars[n], j[n]) u && (u instanceof Array || u.push && P(u)) && -1 !== u.join("").indexOf("{self}") && (this.vars[n] = u = this._swapSelfInParams(u, this));
                        else if (Y[n] && (a = new Y[n])._onInitTween(e, this.vars[n], this, i)) {
                        for (this._firstPT = d = {
                                _next: this._firstPT,
                                t: a,
                                p: "setRatio",
                                s: 0,
                                c: 1,
                                f: 1,
                                n: n,
                                pg: 1,
                                pr: a._priority,
                                m: 0
                            }, l = a._overwriteProps.length; - 1 < --l;) t[a._overwriteProps[l]] = this._firstPT;
                        (a._priority || a._onInitAllProps) && (r = !0), (a._onDisable || a._onEnable) && (this._notifyPluginsOfEnabled = !0), d._next && (d._next._prev = d)
                    } else t[n] = U.call(this, e, n, "get", u, n, 0, null, this.vars.stringFilter, i);
                    return s && this._kill(s, e) ? this._initProps(e, t, o, s, i) : 1 < this._overwrite && this._firstPT && 1 < o.length && Z(e, this, t, this._overwrite, o) ? (this._kill(t, e), this._initProps(e, t, o, s, i)) : (this._firstPT && (!1 !== this.vars.lazy && this._duration || this.vars.lazy && !this._duration) && (I[e._gsTweenID] = !0), r)
                }, o.render = function(e, t, o) {
                    var s, i, n, l, r = this._time,
                        a = this._duration,
                        d = this._rawPrevTime;
                    if (a - 1e-7 <= e) this._totalTime = this._time = a, this.ratio = this._ease._calcEnd ? this._ease.getRatio(1) : 1, this._reversed || (s = !0, i = "onComplete", o = o || this._timeline.autoRemoveChildren), 0 === a && (!this._initted && this.vars.lazy && !o || (this._startTime === this._timeline._duration && (e = 0), (d < 0 || e <= 0 && -1e-7 <= e || d === y && "isPause" !== this.data) && d !== e && (o = !0, y < d && (i = "onReverseComplete")), this._rawPrevTime = l = !t || e || d === e ? e : y));
                    else if (e < 1e-7) this._totalTime = this._time = 0, this.ratio = this._ease._calcEnd ? this._ease.getRatio(0) : 0, (0 !== r || 0 === a && 0 < d) && (i = "onReverseComplete", s = this._reversed), e < 0 && (this._active = !1, 0 === a && (!this._initted && this.vars.lazy && !o || (0 <= d && (d !== y || "isPause" !== this.data) && (o = !0), this._rawPrevTime = l = !t || e || d === e ? e : y))), this._initted || (o = !0);
                    else if (this._totalTime = this._time = e, this._easeType) {
                        var u = e / a,
                            c = this._easeType,
                            h = this._easePower;
                        (1 === c || 3 === c && .5 <= u) && (u = 1 - u), 3 === c && (u *= 2), 1 === h ? u *= u : 2 === h ? u *= u * u : 3 === h ? u *= u * u * u : 4 === h && (u *= u * u * u * u), this.ratio = 1 === c ? 1 - u : 2 === c ? u : e / a < .5 ? u / 2 : 1 - u / 2
                    } else this.ratio = this._ease.getRatio(e / a);
                    if (this._time !== r || o) {
                        if (!this._initted) {
                            if (this._init(), !this._initted || this._gc) return;
                            if (!o && this._firstPT && (!1 !== this.vars.lazy && this._duration || this.vars.lazy && !this._duration)) return this._time = this._totalTime = r, this._rawPrevTime = d, L.push(this), void(this._lazy = [e, t]);
                            this._time && !s ? this.ratio = this._ease.getRatio(this._time / a) : s && this._ease._calcEnd && (this.ratio = this._ease.getRatio(0 === this._time ? 0 : 1))
                        }
                        for (!1 !== this._lazy && (this._lazy = !1), this._active || !this._paused && this._time !== r && 0 <= e && (this._active = !0), 0 === r && (this._startAt && (0 <= e ? this._startAt.render(e, t, o) : i = i || "_dummyGS"), this.vars.onStart && (0 === this._time && 0 !== a || t || this._callback("onStart"))), n = this._firstPT; n;) n.f ? n.t[n.p](n.c * this.ratio + n.s) : n.t[n.p] = n.c * this.ratio + n.s, n = n._next;
                        this._onUpdate && (e < 0 && this._startAt && -1e-4 !== e && this._startAt.render(e, t, o), t || (this._time !== r || s || o) && this._callback("onUpdate")), i && (this._gc && !o || (e < 0 && this._startAt && !this._onUpdate && -1e-4 !== e && this._startAt.render(e, t, o), s && (this._timeline.autoRemoveChildren && this._enabled(!1, !1), this._active = !1), !t && this.vars[i] && this._callback(i), 0 === a && this._rawPrevTime === y && l !== y && (this._rawPrevTime = 0)))
                    }
                }, o._kill = function(e, t, o) {
                    if ("all" === e && (e = null), null == e && (null == t || t === this.target)) return this._lazy = !1, this._enabled(!1, !1);
                    t = "string" != typeof t ? t || this._targets || this.target : O.selector(t) || t;
                    var s, i, n, l, r, a, d, u, c, h = o && this._time && o._startTime === this._startTime && this._timeline === o._timeline;
                    if ((P(t) || k(t)) && "number" != typeof t[0])
                        for (s = t.length; - 1 < --s;) this._kill(e, t[s], o) && (a = !0);
                    else {
                        if (this._targets) {
                            for (s = this._targets.length; - 1 < --s;)
                                if (t === this._targets[s]) {
                                    r = this._propLookup[s] || {}, this._overwrittenProps = this._overwrittenProps || [], i = this._overwrittenProps[s] = e ? this._overwrittenProps[s] || {} : "all";
                                    break
                                }
                        } else {
                            if (t !== this.target) return !1;
                            r = this._propLookup, i = this._overwrittenProps = e ? this._overwrittenProps || {} : "all"
                        }
                        if (r) {
                            if (d = e || r, u = e !== i && "all" !== i && e !== r && ("object" != typeof e || !e._tempKill), o && (O.onOverwrite || this.vars.onOverwrite)) {
                                for (n in d) r[n] && (c = c || []).push(n);
                                if ((c || !e) && !$(this, o, t, c)) return !1
                            }
                            for (n in d)(l = r[n]) && (h && (l.f ? l.t[l.p](l.s) : l.t[l.p] = l.s, a = !0), l.pg && l.t._kill(d) && (a = !0), l.pg && 0 !== l.t._overwriteProps.length || (l._prev ? l._prev._next = l._next : l === this._firstPT && (this._firstPT = l._next), l._next && (l._next._prev = l._prev), l._next = l._prev = null), delete r[n]), u && (i[n] = 1);
                            !this._firstPT && this._initted && this._enabled(!1, !1)
                        }
                    }
                    return a
                }, o.invalidate = function() {
                    return this._notifyPluginsOfEnabled && O._onPluginEvent("_onDisable", this), this._firstPT = this._overwrittenProps = this._startAt = this._onUpdate = null, this._notifyPluginsOfEnabled = this._active = this._lazy = !1, this._propLookup = this._targets ? {} : [], d.prototype.invalidate.call(this), this.vars.immediateRender && (this._time = -y, this.render(Math.min(0, -this._delay))), this
                }, o._enabled = function(e, t) {
                    if (g || b.wake(), e && this._gc) {
                        var o, s = this._targets;
                        if (s)
                            for (o = s.length; - 1 < --o;) this._siblings[o] = Q(s[o], this, !0);
                        else this._siblings = Q(this.target, this, !0)
                    }
                    return d.prototype._enabled.call(this, e, t), !(!this._notifyPluginsOfEnabled || !this._firstPT) && O._onPluginEvent(e ? "_onEnable" : "_onDisable", this)
                }, O.to = function(e, t, o) {
                    return new O(e, t, o)
                }, O.from = function(e, t, o) {
                    return o.runBackwards = !0, o.immediateRender = 0 != o.immediateRender, new O(e, t, o)
                }, O.fromTo = function(e, t, o, s) {
                    return s.startAt = o, s.immediateRender = 0 != s.immediateRender && 0 != o.immediateRender, new O(e, t, s)
                }, O.delayedCall = function(e, t, o, s, i) {
                    return new O(t, 0, {
                        delay: e,
                        onComplete: t,
                        onCompleteParams: o,
                        callbackScope: s,
                        onReverseComplete: t,
                        onReverseCompleteParams: o,
                        immediateRender: !1,
                        lazy: !1,
                        useFrames: i,
                        overwrite: 0
                    })
                }, O.set = function(e, t) {
                    return new O(e, 0, t)
                }, O.getTweensOf = function(e, t) {
                    if (null == e) return [];
                    var o, s, i, n;
                    if (e = "string" != typeof e ? e : O.selector(e) || e, (P(e) || k(e)) && "number" != typeof e[0]) {
                        for (o = e.length, s = []; - 1 < --o;) s = s.concat(O.getTweensOf(e[o], t));
                        for (o = s.length; - 1 < --o;)
                            for (n = s[o], i = o; - 1 < --i;) n === s[i] && s.splice(o, 1)
                    } else
                        for (o = (s = Q(e).concat()).length; - 1 < --o;)(s[o]._gc || t && !s[o].isActive()) && s.splice(o, 1);
                    return s
                }, O.killTweensOf = O.killDelayedCallsTo = function(e, t, o) {
                    "object" == typeof t && (o = t, t = !1);
                    for (var s = O.getTweensOf(e, t), i = s.length; - 1 < --i;) s[i]._kill(o, e)
                };
                var te = h("plugins.TweenPlugin", function(e, t) {
                    this._overwriteProps = (e || "").split(","), this._propName = this._overwriteProps[0], this._priority = t || 0, this._super = te.prototype
                }, !0);
                if (o = te.prototype, te.version = "1.19.0", te.API = 2, o._firstPT = null, o._addTween = U, o.setRatio = A, o._kill = function(e) {
                        var t, o = this._overwriteProps,
                            s = this._firstPT;
                        if (null != e[this._propName]) this._overwriteProps = [];
                        else
                            for (t = o.length; - 1 < --t;) null != e[o[t]] && o.splice(t, 1);
                        for (; s;) null != e[s.n] && (s._next && (s._next._prev = s._prev), s._prev ? (s._prev._next = s._next, s._prev = null) : this._firstPT === s && (this._firstPT = s._next)), s = s._next;
                        return !1
                    }, o._mod = o._roundProps = function(e) {
                        for (var t, o = this._firstPT; o;)(t = e[this._propName] || null != o.n && e[o.n.split(this._propName + "_").join("")]) && "function" == typeof t && (2 === o.f ? o.t._applyPT.m = t : o.m = t), o = o._next
                    }, O._onPluginEvent = function(e, t) {
                        var o, s, i, n, l, r = t._firstPT;
                        if ("_onInitAllProps" === e) {
                            for (; r;) {
                                for (l = r._next, s = i; s && s.pr > r.pr;) s = s._next;
                                (r._prev = s ? s._prev : n) ? r._prev._next = r: i = r, (r._next = s) ? s._prev = r : n = r, r = l
                            }
                            r = t._firstPT = i
                        }
                        for (; r;) r.pg && "function" == typeof r.t[e] && r.t[e]() && (o = !0), r = r._next;
                        return o
                    }, te.activate = function(e) {
                        for (var t = e.length; - 1 < --t;) e[t].API === te.API && (Y[(new e[t])._propName] = e[t]);
                        return !0
                    }, n.plugin = function(e) {
                        if (!(e && e.propName && e.init && e.API)) throw "illegal plugin definition.";
                        var t, o = e.propName,
                            s = e.priority || 0,
                            i = e.overwriteProps,
                            n = {
                                init: "_onInitTween",
                                set: "setRatio",
                                kill: "_kill",
                                round: "_mod",
                                mod: "_mod",
                                initAll: "_onInitAllProps"
                            },
                            l = h("plugins." + o.charAt(0).toUpperCase() + o.substr(1) + "Plugin", function() {
                                te.call(this, o, s), this._overwriteProps = i || []
                            }, !0 === e.fwd_global),
                            r = l.prototype = new te(o);
                        for (t in (r.constructor = l).API = e.API, n) "function" == typeof e[t] && (r[n[t]] = e[t]);
                        return l.version = e.version, te.activate([l]), l
                    }, e = _._fwd_gsQueue) {
                    for (t = 0; t < e.length; t++) e[t]();
                    for (o in T) T[o].func || _.console.log("GSAP encountered missing dependency: " + o)
                }
                g = !1
            }
        }("undefined" != typeof fwd_module && fwd_module.exports && "undefined" != typeof fwd_global ? fwd_global : this || window, "FWDAnimation")
}
if (! function(e) {
        var t = function() {
            var i = this;
            t.prototype;
            this.main_do = null, this.init = function() {
                this.setupScreen(), e.onerror = this.showError, this.screen.style.zIndex = 100000009, setTimeout(this.addConsoleToDom, 100), setInterval(this.position, 100)
            }, this.position = function() {
                var e = FWDMSPUtils.getScrollOffsets();
                i.setX(e.x + 200), i.setY(e.y)
            }, this.addConsoleToDom = function() {
                -1 != navigator.userAgent.toLowerCase().indexOf("msie 7") ? document.getElementsByTagName("body")[0].appendChild(i.screen) : document.documentElement.appendChild(i.screen)
            }, this.setupScreen = function() {
                this.main_do = new FWDMSPDisplayObject("div", "absolute"), this.main_do.setOverflow("auto"), this.main_do.setWidth(200), this.main_do.setHeight(300), this.setWidth(200), this.setHeight(300), this.main_do.setBkColor("#FFFFFF"), this.addChild(this.main_do)
            }, this.showError = function(e, t, o) {
                var s = i.main_do.getInnerHTML() + "<br>JavaScript error: " + e + " on line " + o + " for " + t;
                i.main_do.setInnerHTML(s), i.main_do.screen.scrollTop = i.main_do.screen.scrollHeight
            }, this.log = function(e) {
                var t = i.main_do.getInnerHTML() + "<br>" + e;
                i.main_do.setInnerHTML(t), i.main_do.getScreen().scrollTop = 1e4
            }, this.init()
        };
        t.setPrototype = function() {
            t.prototype = new FWDMSPDisplayObject("div", "absolute")
        }, t.prototype = null, e.FWDConsole = t
    }(window), void 0 === asual) var asual = {};
void 0 === asual.util && (asual.util = {}), asual.util.Browser = new function() {
    var e = navigator.userAgent.toLowerCase(),
        t = /webkit/.test(e),
        o = /opera/.test(e),
        s = /msie/.test(e) && !/opera/.test(e),
        i = /mozilla/.test(e) && !/(compatible|webkit)/.test(e),
        n = parseFloat(s ? e.substr(e.indexOf("msie") + 4) : (e.match(/.+(?:rv|it|ra|ie)[\/: ]([\d.]+)/) || [0, "0"])[1]);
    this.toString = function() {
        return "[class Browser]"
    }, this.getVersion = function() {
        return n
    }, this.isMSIE = function() {
        return s
    }, this.isSafari = function() {
        return t
    }, this.isOpera = function() {
        return o
    }, this.isMozilla = function() {
        return i
    }
}, asual.util.Events = new function() {
    var n = "DOMContentLoaded",
        t = "onstop",
        o = window,
        s = document,
        l = [],
        i = asual.util,
        e = i.Browser,
        r = e.isMSIE(),
        a = e.isSafari();
    this.toString = function() {
        return "[class Events]"
    }, this.addListener = function(e, t, o) {
        l.push({
            o: e,
            t: t,
            l: o
        }), t == n && (r || a) || (e.addEventListener ? e.addEventListener(t, o, !1) : e.attachEvent && e.attachEvent("on" + t, o))
    }, this.removeListener = function(e, t, o) {
        for (var s, i = 0; s = l[i]; i++)
            if (s.o == e && s.t == t && s.l == o) {
                l.splice(i, 1);
                break
            } t == n && (r || a) || (e.removeEventListener ? e.removeEventListener(t, o, !1) : e.detachEvent && e.detachEvent("on" + t, o))
    };

    function d() {
        for (var e, t = 0; e = l[t]; t++) e.t != n && i.Events.removeListener(e.o, e.t, e.l)
    }(r || a) && function() {
        try {
            (r && s.body || !/loaded|complete/.test(s.readyState)) && s.documentElement.doScroll("left")
        } catch (e) {
            return setTimeout(arguments.callee, 0)
        }
        for (var e, t = 0; e = l[t]; t++) e.t == n && e.l.call(null)
    }(), r && o.attachEvent && o.attachEvent("onbeforeunload", function() {
        if ("interactive" == s.readyState) {
            function e() {
                s.detachEvent(t, e), d()
            }
            s.attachEvent(t, e), o.setTimeout(function() {
                s.detachEvent(t, e)
            }, 0)
        }
    }), this.addListener(o, "unload", d)
}, asual.util.Functions = new function() {
    this.toString = function() {
        return "[class Functions]"
    }, this.bind = function(e, t, o) {
        for (var s, i = 2, n = []; s = arguments[i]; i++) n.push(s);
        return function() {
            return e.apply(t, n)
        }
    }
};
var FWDAddressEvent = function(e) {
    this.toString = function() {
        return "[object FWDAddressEvent]"
    }, this.type = e, this.target = [FWDAddress][0], this.value = FWDAddress.getValue(), this.path = FWDAddress.getPath(), this.pathNames = FWDAddress.getPathNames(), this.parameters = {};
    for (var t = FWDAddress.getParameterNames(), o = 0, s = t.length; o < s; o++) this.parameters[t[o]] = FWDAddress.getParameter(t[o]);
    this.parameterNames = t
};
FWDAddressEvent.INIT = "init", FWDAddressEvent.CHANGE = "change", FWDAddressEvent.INTERNAL_CHANGE = "internalChange", FWDAddressEvent.EXTERNAL_CHANGE = "externalChange";
var FWDAddress = new function() {
        var _getHash = function() {
                var e = _l.href.indexOf("#");
                return -1 != e ? _ec(_dc(_l.href.substr(e + 1))) : ""
            },
            _getWindow = function() {
                try {
                    return top.document, top
                } catch (e) {
                    return window
                }
            },
            _strictCheck = function(e, t) {
                return _opts.strict && (e = t ? "/" != e.substr(0, 1) ? "/" + e : e : "" == e ? "/" : e), e
            },
            _ieLocal = function(e, t) {
                return _msie && "file:" == _l.protocol ? t ? _value.replace(/\?/, "%3F") : _value.replace(/%253F/, "?") : e
            },
            _searchScript = function(e) {
                if (e.childNodes)
                    for (var t, o = 0, s = e.childNodes.length; o < s; o++)
                        if (e.childNodes[o].src && (_url = String(e.childNodes[o].src)), t = _searchScript(e.childNodes[o])) return t
            },
            _titleCheck = function() {
                _d.title != _title && -1 != _d.title.indexOf("#") && (_d.title = _title)
            },
            _listen = function() {
                if (!_silent) {
                    var e = _getHash(),
                        t = !(_value == e);
                    _safari && _version < 523 ? _length != _h.length && (_length = _h.length, typeof _stack[_length - 1] != UNDEFINED && (_value = _stack[_length - 1]), _update.call(this, !1)) : _msie && t ? _version < 7 ? _l.reload() : this.setValue(e) : t && (_value = e, _update.call(this, !1)), _msie && _titleCheck.call(this)
                }
            },
            _bodyClick = function(e) {
                if (0 < _popup.length) {
                    var popup = window.open(_popup[0], _popup[1], eval(_popup[2]));
                    typeof _popup[3] != UNDEFINED && eval(_popup[3])
                }
                _popup = []
            },
            _swfChange = function() {
                for (var e, t, o = 0, s = FWDAddress.getValue(), i = "setFWDAddressValue"; e = _ids[o]; o++)
                    if (t = document.getElementById(e))
                        if (t.parentNode && typeof t.parentNode.so != UNDEFINED) t.parentNode.so.call(i, s);
                        else {
                            if (!t || typeof t[i] == UNDEFINED) {
                                var n = t.getElementsByTagName("object"),
                                    l = t.getElementsByTagName("embed");
                                t = n[0] && typeof n[0][i] != UNDEFINED ? n[0] : l[0] && typeof l[0][i] != UNDEFINED ? l[0] : null
                            }
                            t && t[i](s)
                        }
                else(t = document[e]) && typeof t[i] != UNDEFINED && t[i](s)
            },
            _jsDispatch = function(e) {
                this.dispatchEvent(new FWDAddressEvent(e)), typeof this["on" + (e = e.substr(0, 1).toUpperCase() + e.substr(1))] == FUNCTION && this["on" + e]()
            },
            _jsInit = function() {
                _util.Browser.isSafari() && _d.body.addEventListener("click", _bodyClick), _jsDispatch.call(this, "init")
            },
            _jsChange = function() {
                _swfChange(), _jsDispatch.call(this, "change")
            },
            _update = function(e) {
                _jsChange.call(this), e ? _jsDispatch.call(this, "internalChange") : _jsDispatch.call(this, "externalChange"), _st(_functions.bind(_track, this), 10)
            },
            _track = function() {
                var e = (_l.pathname + (/\/$/.test(_l.pathname) ? "" : "/") + this.getValue()).replace(/\/\//, "/").replace(/^\/$/, ""),
                    t = _t[_opts.tracker];
                typeof t == FUNCTION ? t(e) : typeof _t.pageTracker != UNDEFINED && typeof _t.pageTracker._trackPageview == FUNCTION ? _t.pageTracker._trackPageview(e) : typeof _t.urchinTracker == FUNCTION && _t.urchinTracker(e)
            },
            _htmlWrite = function() {
                var e = _frame.contentWindow.document;
                e.open(), e.write("<html><head><title>" + _d.title + "</title><script>var " + ID + ' = "' + _getHash() + '";<\/script></head></html>'), e.close()
            },
            _htmlLoad = function() {
                var e = _frame.contentWindow;
                e.location.href;
                (_value = typeof e[ID] != UNDEFINED ? e[ID] : "") != _getHash() && (_update.call(FWDAddress, !1), _l.hash = _ieLocal(_value, TRUE))
            },
            _load = function() {
                if (!_loaded) {
                    if (_loaded = TRUE, _msie && _version < 8) {
                        var e = _d.getElementsByTagName("frameset")[0];
                        _frame = _d.createElement((e ? "" : "i") + "frame"), e ? (e.insertAdjacentElement("beforeEnd", _frame), e[e.cols ? "cols" : "rows"] += ",0", _frame.src = "javascript:false", _frame.noResize = !0, _frame.frameBorder = _frame.frameSpacing = 0) : (_frame.src = "javascript:false", _frame.style.display = "none", _d.body.insertAdjacentElement("afterBegin", _frame)), _st(function() {
                            _events.addListener(_frame, "load", _htmlLoad), typeof _frame.contentWindow[ID] == UNDEFINED && _htmlWrite()
                        }, 50)
                    } else _safari && (_version < 418 && (_d.body.innerHTML += '<form id="' + ID + '" style="position:absolute;top:-9999px;" method="get"></form>', _form = _d.getElementById(ID)), typeof _l[ID] == UNDEFINED && (_l[ID] = {}), typeof _l[ID][_l.pathname] != UNDEFINED && (_stack = _l[ID][_l.pathname].split(",")));
                    _st(_functions.bind(function() {
                        _jsInit.call(this), _jsChange.call(this), _track.call(this)
                    }, this), 1), _msie && 8 <= _version ? (_d.body.onhashchange = _functions.bind(_listen, this), _si(_functions.bind(_titleCheck, this), 50)) : _si(_functions.bind(_listen, this), 50)
                }
            },
            ID = "swfaddress",
            FUNCTION = "function",
            UNDEFINED = "undefined",
            TRUE = !0,
            FALSE = !1,
            _util = asual.util,
            _browser = _util.Browser,
            _events = _util.Events,
            _functions = _util.Functions,
            _version = _browser.getVersion(),
            _msie = _browser.isMSIE(),
            _mozilla = _browser.isMozilla(),
            _opera = _browser.isOpera(),
            _safari = _browser.isSafari(),
            _supported = FALSE,
            _t = _getWindow(),
            _d = _t.document,
            _h = _t.history,
            _l = _t.location,
            _si = setInterval,
            _st = setTimeout,
            _dc = decodeURI,
            _ec = encodeURI,
            _frame, _form, _url, _title = _d.title,
            _length = _h.length,
            _silent = FALSE,
            _loaded = FALSE,
            _justset = TRUE,
            _juststart = TRUE,
            _ref = this,
            _stack = [],
            _ids = [],
            _popup = [],
            _listeners = {},
            _value = _getHash(),
            _opts = {
                history: TRUE,
                strict: TRUE
            };
        if (_msie && _d.documentMode && _d.documentMode != _version && (_version = 8 != _d.documentMode ? 7 : 8), _supported = _mozilla && 1 <= _version || _msie && 6 <= _version || _opera && 9.5 <= _version || _safari && 312 <= _version, _supported) {
            _opera && (history.navigationMode = "compatible");
            for (var i = 1; i < _length; i++) _stack.push("");
            _stack.push(_getHash()), _msie && _l.hash != _getHash() && (_l.hash = "#" + _ieLocal(_getHash(), TRUE)), _searchScript(document);
            var _qi = _url ? _url.indexOf("?") : -1;
            if (-1 != _qi)
                for (var param, params = _url.substr(_qi + 1).split("&"), i = 0, p; p = params[i]; i++) param = p.split("="), /^(history|strict)$/.test(param[0]) && (_opts[param[0]] = isNaN(param[1]) ? /^(true|yes)$/i.test(param[1]) : 0 != parseInt(param[1])), /^tracker$/.test(param[0]) && (_opts[param[0]] = param[1]);
            _msie && _titleCheck.call(this), window == _t && _events.addListener(document, "DOMContentLoaded", _functions.bind(_load, this)), _events.addListener(_t, "load", _functions.bind(_load, this))
        } else !_supported && -1 != _l.href.indexOf("#") || _safari && _version < 418 && -1 != _l.href.indexOf("#") && "" != _l.search ? (_d.open(), _d.write('<html><head><meta http-equiv="refresh" content="0;url=' + _l.href.substr(0, _l.href.indexOf("#")) + '" /></head></html>'), _d.close()) : _track();
        this.toString = function() {
                return "[class FWDAddress]"
            }, this.back = function() {
                _h.back()
            }, this.forward = function() {
                _h.forward()
            }, this.up = function() {
                var e = this.getPath();
                this.setValue(e.substr(0, e.lastIndexOf("/", e.length - 2) + ("/" == e.substr(e.length - 1) ? 1 : 0)))
            }, this.go = function(e) {
                _h.go(e)
            }, this.href = function(e, t) {
                "_self" == (t = typeof t != UNDEFINED ? t : "_self") ? self.location.href = e: "_top" == t ? _l.href = e : "_blank" == t ? window.open(e) : _t.frames[t].location.href = e
            }, this.popup = function(url, name, options, handler) {
                try {
                    var popup = window.open(url, name, eval(options));
                    typeof handler != UNDEFINED && eval(handler)
                } catch (e) {}
                _popup = arguments
            }, this.getIds = function() {
                return _ids
            }, this.getId = function(e) {
                return _ids[0]
            }, this.setId = function(e) {
                _ids[0] = e
            }, this.addId = function(e) {
                this.removeId(e), _ids.push(e)
            }, this.removeId = function(e) {
                for (var t = 0; t < _ids.length; t++)
                    if (e == _ids[t]) {
                        _ids.splice(t, 1);
                        break
                    }
            }, this.addEventListener = function(e, t) {
                typeof _listeners[e] == UNDEFINED && (_listeners[e] = []), _listeners[e].push(t)
            }, this.removeEventListener = function(e, t) {
                if (typeof _listeners[e] != UNDEFINED) {
                    for (var o, s = 0;
                        (o = _listeners[e][s]) && o != t; s++);
                    _listeners[e].splice(s, 1)
                }
            }, this.dispatchEvent = function(e) {
                if (this.hasEventListener(e.type)) {
                    e.target = this;
                    for (var t, o = 0; t = _listeners[e.type][o]; o++) t(e);
                    return TRUE
                }
                return FALSE
            }, this.hasEventListener = function(e) {
                return typeof _listeners[e] != UNDEFINED && 0 < _listeners[e].length
            }, this.getBaseURL = function() {
                var e = _l.href;
                return -1 != e.indexOf("#") && (e = e.substr(0, e.indexOf("#"))), "/" == e.substr(e.length - 1) && (e = e.substr(0, e.length - 1)), e
            }, this.getStrict = function() {
                return _opts.strict
            }, this.setStrict = function(e) {
                _opts.strict = e
            }, this.getHistory = function() {
                return _opts.history
            }, this.setHistory = function(e) {
                _opts.history = e
            }, this.getTracker = function() {
                return _opts.tracker
            }, this.setTracker = function(e) {
                _opts.tracker = e
            }, this.getTitle = function() {
                return _d.title
            }, this.setTitle = function(e) {
                if (!_supported) return null;
                typeof e != UNDEFINED && ("null" == e && (e = ""), e = _dc(e), _st(function() {
                    _title = _d.title = e, _juststart && _frame && _frame.contentWindow && _frame.contentWindow.document && (_frame.contentWindow.document.title = e, _juststart = FALSE), !_justset && _mozilla && _l.replace(-1 != _l.href.indexOf("#") ? _l.href : _l.href + "#"), _justset = FALSE
                }, 10))
            }, this.getStatus = function() {
                return _t.status
            }, this.setStatus = function(e) {
                if (!_supported) return null;
                if (typeof e != UNDEFINED && ("null" == e && (e = ""), e = _dc(e), !_safari)) {
                    if ("/" == (e = _strictCheck("null" != e ? e : "", TRUE)) && (e = ""), !/http(s)?:\/\//.test(e)) {
                        var t = _l.href.indexOf("#");
                        e = (-1 == t ? _l.href : _l.href.substr(0, t)) + "#" + e
                    }
                    _t.status = e
                }
            }, this.resetStatus = function() {
                _t.status = ""
            }, this.getValue = function() {
                return _supported ? _dc(_strictCheck(_ieLocal(_value, FALSE), FALSE)) : null
            }, this.setValue = function(e) {
                if (!_supported) return null;
                if (typeof e != UNDEFINED && ("null" == e && (e = ""), "/" == (e = _ec(_dc(_strictCheck(e, TRUE)))) && (e = ""), _value != e)) {
                    if (_value = e, _silent = _justset = TRUE, _update.call(FWDAddress, !0), _stack[_h.length] = _value, _safari)
                        if (_opts.history)
                            if (_l[ID][_l.pathname] = _stack.toString(), _length = _h.length + 1, _version < 418) "" == _l.search && (_form.action = "#" + _value, _form.submit());
                            else if (_version < 523 || "" == _value) {
                        var t = _d.createEvent("MouseEvents");
                        t.initEvent("click", TRUE, TRUE);
                        var o = _d.createElement("a");
                        o.href = "#" + _value, o.dispatchEvent(t)
                    } else _l.hash = "#" + _value;
                    else _l.replace("#" + _value);
                    else _value != _getHash() && (_opts.history ? _l.hash = "#" + _dc(_ieLocal(_value, TRUE)) : _l.replace("#" + _dc(_value)));
                    _msie && _version < 8 && _opts.history && _st(_htmlWrite, 50), _safari ? _st(function() {
                        _silent = FALSE
                    }, 1) : _silent = FALSE
                }
            }, this.getPath = function() {
                var e = this.getValue();
                return -1 != e.indexOf("?") ? e.split("?")[0] : -1 != e.indexOf("#") ? e.split("#")[0] : e
            }, this.getPathNames = function() {
                var e = this.getPath(),
                    t = e.split("/");
                return "/" != e.substr(0, 1) && 0 != e.length || t.splice(0, 1), "/" == e.substr(e.length - 1, 1) && t.splice(t.length - 1, 1), t
            }, this.getQueryString = function() {
                var e = this.getValue(),
                    t = e.indexOf("?");
                if (-1 != t && t < e.length) return e.substr(t + 1)
            }, this.getParameter = function(e) {
                var t = this.getValue(),
                    o = t.indexOf("?");
                if (-1 != o) {
                    for (var s, i = (t = t.substr(o + 1)).split("&"), n = i.length, l = []; n--;)(s = i[n].split("="))[0] == e && l.push(s[1]);
                    if (0 != l.length) return 1 != l.length ? l : l[0]
                }
            }, this.getParameterNames = function() {
                var e = this.getValue(),
                    t = e.indexOf("?"),
                    o = [];
                if (-1 != t && "" != (e = e.substr(t + 1)) && -1 != e.indexOf("="))
                    for (var s = e.split("&"), i = 0; i < s.length;) o.push(s[i].split("=")[0]), i++;
                return o
            }, this.onInit = null, this.onChange = null, this.onInternalChange = null, this.onExternalChange = null,
            function() {
                var o;
                if (typeof FlashObject != UNDEFINED && (SWFObject = FlashObject), typeof SWFObject != UNDEFINED && SWFObject.prototype && SWFObject.prototype.write) {
                    var t = SWFObject.prototype.write;
                    SWFObject.prototype.write = function() {
                        var e;
                        return o = arguments, this.getAttribute("version").major < 8 && (this.addVariable("$swfaddress", FWDAddress.getValue()), ("string" == typeof o[0] ? document.getElementById(o[0]) : o[0]).so = this), (e = t.apply(this, o)) && _ref.addId(this.getAttribute("id")), e
                    }
                }
                if (typeof swfobject != UNDEFINED) {
                    var e = swfobject.registerObject;
                    swfobject.registerObject = function() {
                        o = arguments, e.apply(this, o), _ref.addId(o[0])
                    };
                    var s = swfobject.createSWF;
                    swfobject.createSWF = function() {
                        o = arguments;
                        var e = s.apply(this, o);
                        return e && _ref.addId(o[0].id), e
                    };
                    var i = swfobject.embedSWF;
                    swfobject.embedSWF = function() {
                        typeof(o = arguments)[8] == UNDEFINED && (o[8] = {}), typeof o[8].id == UNDEFINED && (o[8].id = o[1]), i.apply(this, o), _ref.addId(o[8].id)
                    }
                }
                if (typeof UFO != UNDEFINED) {
                    var n = UFO.create;
                    UFO.create = function() {
                        o = arguments, n.apply(this, o), _ref.addId(o[0].id)
                    }
                }
                if (typeof AC_FL_RunContent != UNDEFINED) {
                    var l = AC_FL_RunContent;
                    AC_FL_RunContent = function() {
                        o = arguments, l.apply(this, o);
                        for (var e = 0, t = o.length; e < t; e++) "id" == o[e] && _ref.addId(o[e + 1])
                    }
                }
            }()
    },
    FWDFlashTest = function() {
        var u = "undefined",
            c = "object",
            h = "Shockwave Flash",
            _ = "application/x-shockwave-flash",
            f = window,
            p = document,
            m = navigator,
            s = function() {
                var e = typeof p.getElementById != u && typeof p.getElementsByTagName != u && typeof p.createElement != u,
                    t = m.userAgent.toLowerCase(),
                    o = m.platform.toLowerCase(),
                    s = /win/.test(o || t),
                    i = /mac/.test(o || t),
                    n = !!/webkit/.test(t) && parseFloat(t.replace(/^.*webkit\/(\d+(\.\d+)?).*$/, "$1")),
                    l = !1,
                    r = [0, 0, 0],
                    a = null;
                if (typeof m.plugins != u && typeof m.plugins[h] == c) !(a = m.plugins[h].description) || typeof m.mimeTypes != u && m.mimeTypes[_] && !m.mimeTypes[_].enabledPlugin || (l = !!0, a = a.replace(/^.*\s+(\S+\s+\S+$)/, "$1"), r[0] = parseInt(a.replace(/^(.*)\..*$/, "$1"), 10), r[1] = parseInt(a.replace(/^.*\.(.*)\s.*$/, "$1"), 10), r[2] = /[a-zA-Z]/.test(a) ? parseInt(a.replace(/^.*[a-zA-Z]+(.*)$/, "$1"), 10) : 0);
                else if (typeof f.ActiveXObject != u) try {
                    var d = new ActiveXObject("ShockwaveFlash.ShockwaveFlash");
                    d && (a = d.GetVariable("$version")) && (l = !0, a = a.split(" ")[1].split(","), r = [parseInt(a[0], 10), parseInt(a[1], 10), parseInt(a[2], 10)])
                } catch (e) {}
                return {
                    w3: e,
                    pv: r,
                    wk: n,
                    ie: l,
                    win: s,
                    mac: i
                }
            }();

        function e(e) {
            var t = s.pv,
                o = e.split(".");
            return o[0] = parseInt(o[0], 10), o[1] = parseInt(o[1], 10) || 0, o[2] = parseInt(o[2], 10) || 0, t[0] > o[0] || t[0] == o[0] && t[1] > o[1] || t[0] == o[0] && t[1] == o[1] && t[2] >= o[2]
        }
        return {
            hasFlashPlayerVersion: e
        }
    }();

function A(t, e, o) {
    var s = e || 0,
        i = 0;
    "string" == typeof t ? (i = o || t.length, this.a = function(e) {
        return 255 & t.charCodeAt(e + s)
    }) : "unknown" == typeof t && (i = o || IEBinary_getLength(t), this.a = function(e) {
        return IEBinary_getByteAt(t, e + s)
    }), this.l = function(e, t) {
        for (var o = Array(t), s = 0; s < t; s++) o[s] = this.a(e + s);
        return o
    }, this.h = function() {
        return i
    }, this.d = function(e, t) {
        return 0 != (this.a(e) & 1 << t)
    }, this.w = function(e) {
        return (e = (this.a(e + 1) << 8) + this.a(e)) < 0 && (e += 65536), e
    }, this.i = function(e) {
        var t = this.a(e);
        return (t = (((t << 8) + this.a(e + 1) << 8) + this.a(e + 2) << 8) + (e = this.a(e + 3))) < 0 && (t += 4294967296), t
    }, this.o = function(e) {
        var t = this.a(e);
        return (t = ((t << 8) + this.a(e + 1) << 8) + (e = this.a(e + 2))) < 0 && (t += 16777216), t
    }, this.c = function(e, t) {
        for (var o = [], s = e, i = 0; s < e + t; s++, i++) o[i] = String.fromCharCode(this.a(s));
        return o.join("")
    }, this.e = function(e, t, o) {
        switch (e = this.l(e, t), o.toLowerCase()) {
            case "utf-16":
            case "utf-16le":
            case "utf-16be":
                t = o;
                var s, i = 0,
                    n = 1;
                o = 0, s = Math.min(s || e.length, e.length), 254 == e[0] && 255 == e[1] ? (t = !0, i = 2) : 255 == e[0] && 254 == e[1] && (t = !1, i = 2), t && (n = 0, o = 1), t = [];
                for (var l = 0; i < s; l++) {
                    var r = e[i + n],
                        a = (r << 8) + e[i + o];
                    i = i + 2;
                    if (0 == a) break;
                    r < 216 || 224 <= r ? t[l] = String.fromCharCode(a) : (r = (e[i + n] << 8) + e[i + o], i += 2, t[l] = String.fromCharCode(a, r))
                }(e = new String(t.join(""))).g = i;
                break;
            case "utf-8":
                for (s = 0, i = Math.min(i || e.length, e.length), 239 == e[0] && 187 == e[1] && 191 == e[2] && (s = 3), n = [], o = 0; s < i && 0 != (t = e[s++]); o++) t < 128 ? n[o] = String.fromCharCode(t) : 194 <= t && t < 224 ? (l = e[s++], n[o] = String.fromCharCode(((31 & t) << 6) + (63 & l))) : 224 <= t && t < 240 ? (l = e[s++], a = e[s++], n[o] = String.fromCharCode(((255 & t) << 12) + ((63 & l) << 6) + (63 & a))) : 240 <= t && t < 245 && (t = ((7 & t) << 18) + ((63 & (l = e[s++])) << 12) + ((63 & (a = e[s++])) << 6) + (63 & (r = e[s++])) - 65536, n[o] = String.fromCharCode(55296 + (t >> 10), 56320 + (1023 & t)));
                (e = new String(n.join(""))).g = s;
                break;
            default:
                for (i = [], n = n || e.length, s = 0; s < n && 0 != (o = e[s++]);) i[s - 1] = String.fromCharCode(o);
                (e = new String(i.join(""))).g = s
        }
        return e
    }, this.f = function(e, t) {
        t()
    }
}

function B(t, o, p) {
    function m() {
        var e = null;
        return window.XMLHttpRequest ? e = new XMLHttpRequest : window.ActiveXObject && (e = new ActiveXObject("Microsoft.XMLHTTP")), e
    }

    function s(u, c) {
        var h, o;

        function s(e) {
            var t = ~~(e[0] / h) - o;
            return t < 0 && (t = 0), (e = 1 + ~~(e[1] / h) + o) >= blockTotal && (e = blockTotal - 1), [t, e]
        }

        function i(o, s) {
            for (; f[o[0]];)
                if (o[0]++, o[0] > o[1]) return void(s && s());
            for (; f[o[1]];)
                if (o[1]--, o[0] > o[1]) return void(s && s());
            var e, t, i, n, l, r, a, d = [o[0] * h, (o[1] + 1) * h - 1];
            e = u, t = function(e) {
                parseInt(e.getResponseHeader("Content-Length"), 10) == c && (o[0] = 0, o[1] = blockTotal - 1, d[0] = 0, d[1] = c - 1), e = {
                    data: e.N || e.responseText,
                    offset: d[0]
                };
                for (var t = o[0]; t <= o[1]; t++) f[t] = e;
                s && s()
            }, i = p, n = d, l = _, r = !!s, (a = m()) ? (void 0 === r && (r = !0), t && (void 0 !== a.onload ? a.onload = function() {
                "200" == a.status || "206" == a.status ? (a.fileSize = l || a.getResponseHeader("Content-Length"), t(a)) : i && i(), a = null
            } : a.onreadystatechange = function() {
                4 == a.readyState && ("200" == a.status || "206" == a.status ? (a.fileSize = l || a.getResponseHeader("Content-Length"), t(a)) : i && i(), a = null)
            }), a.open("GET", e, r), a.overrideMimeType && a.overrideMimeType("text/plain; charset=x-user-defined"), n && a.setRequestHeader("Range", "bytes=" + n[0] + "-" + n[1]), a.setRequestHeader("If-Modified-Since", "Sat, 1 Jan 1970 00:00:00 GMT"), a.send(null)) : i && i()
        }
        var _, e = new A("", 0, c),
            f = [];
        for (var t in o = void 0 === o ? 0 : o, blockTotal = 1 + ~~((c - 1) / (h = h || 2048)), e) e.hasOwnProperty(t) && "function" == typeof e[t] && (this[t] = e[t]);
        this.a = function(e) {
            var t;
            return i(s([e, e])), "string" == typeof(t = f[~~(e / h)]).data ? 255 & t.data.charCodeAt(e - t.offset) : "unknown" == typeof t.data ? IEBinary_getByteAt(t.data, e - t.offset) : void 0
        }, this.f = function(e, t) {
            i(s(e), t)
        }
    }
    var e, i, n;
    e = t, i = function(e) {
        e = parseInt(e.getResponseHeader("Content-Length"), 10) || -1, o(new s(t, e))
    }, (n = m()) && (i && (void 0 !== n.onload ? n.onload = function() {
        "200" == n.status && i(this), n = null
    } : n.onreadystatechange = function() {
        4 == n.readyState && ("200" == n.status && i(this), n = null)
    }), n.open("HEAD", e, !0), n.send(null))
}
document.write("<script type='text/vbscript'>\r\nFunction IEBinary_getByteAt(strBinary, iOffset)\r\n\tIEBinary_getByteAt = AscB(MidB(strBinary,iOffset+1,1))\r\nEnd Function\r\nFunction IEBinary_getLength(strBinary)\r\n\tIEBinary_getLength = LenB(strBinary)\r\nEnd Function\r\n<\/script>\r\n"),
    function(e) {
        e.FileAPIReader = function(s, i) {
            return function(e, t) {
                var o = i || new FileReader;
                o.onload = function(e) {
                    t(new A(e.target.result))
                }, o.readAsBinaryString(s)
            }
        }
    }(this),
    function(e) {
        var t = e.p = {},
            a = {},
            o = [0, 7];
        t.t = function(e) {
            delete a[e]
        }, t.s = function() {
            a = {}
        }, t.B = function(n, l, r) {
            ((r = r || {}).dataReader || B)(n, function(i) {
                i.f(o, function() {
                    var s = "ftypM4A" == i.c(4, 7) ? ID4 : "ID3" == i.c(0, 3) ? ID3v2 : ID3v1;
                    s.m(i, function() {
                        var e, t = r.tags,
                            o = s.n(i, t);
                        t = a[n] || {};
                        for (e in o) o.hasOwnProperty(e) && (t[e] = o[e]);
                        a[n] = t, l && l()
                    })
                })
            })
        }, t.v = function(e) {
            if (!a[e]) return null;
            var t, o = {};
            for (t in a[e]) a[e].hasOwnProperty(t) && (o[t] = a[e][t]);
            return o
        }, t.A = function(e, t) {
            return a[e] ? a[e][t] : null
        }, e.ID3 = e.p, t.loadTags = t.B, t.getAllTags = t.v, t.getTag = t.A, t.clearTags = t.t, t.clearAll = t.s
    }(this),
    function(e) {
        var t = e.q = {},
            a = "Blues;Classic Rock;Country;Dance;Disco;Funk;Grunge;Hip-Hop;Jazz;Metal;New Age;Oldies;Other;Pop;R&B;Rap;Reggae;Rock;Techno;Industrial;Alternative;Ska;Death Metal;Pranks;Soundtrack;Euro-Techno;Ambient;Trip-Hop;Vocal;Jazz+Funk;Fusion;Trance;Classical;Instrumental;Acid;House;Game;Sound Clip;Gospel;Noise;AlternRock;Bass;Soul;Punk;Space;Meditative;Instrumental Pop;Instrumental Rock;Ethnic;Gothic;Darkwave;Techno-Industrial;Electronic;Pop-Folk;Eurodance;Dream;Southern Rock;Comedy;Cult;Gangsta;Top 40;Christian Rap;Pop/Funk;Jungle;Native American;Cabaret;New Wave;Psychadelic;Rave;Showtunes;Trailer;Lo-Fi;Tribal;Acid Punk;Acid Jazz;Polka;Retro;Musical;Rock & Roll;Hard Rock;Folk;Folk-Rock;National Folk;Swing;Fast Fusion;Bebob;Latin;Revival;Celtic;Bluegrass;Avantgarde;Gothic Rock;Progressive Rock;Psychedelic Rock;Symphonic Rock;Slow Rock;Big Band;Chorus;Easy Listening;Acoustic;Humour;Speech;Chanson;Opera;Chamber Music;Sonata;Symphony;Booty Bass;Primus;Porn Groove;Satire;Slow Jam;Club;Tango;Samba;Folklore;Ballad;Power Ballad;Rhythmic Soul;Freestyle;Duet;Punk Rock;Drum Solo;Acapella;Euro-House;Dance Hall".split(";");
        t.m = function(e, t) {
            var o = e.h();
            e.f([o - 128 - 1, o], t)
        }, t.n = function(e) {
            var t = e.h() - 128;
            if ("TAG" != e.c(t, 3)) return {};
            var o = e.c(3 + t, 30).replace(/\0/g, ""),
                s = e.c(33 + t, 30).replace(/\0/g, ""),
                i = e.c(63 + t, 30).replace(/\0/g, ""),
                n = e.c(93 + t, 4).replace(/\0/g, "");
            if (0 == e.a(97 + t + 28)) var l = e.c(97 + t, 28).replace(/\0/g, ""),
                r = e.a(97 + t + 29);
            else l = "", r = 0;
            return {
                version: "1.1",
                title: o,
                artist: s,
                album: i,
                year: n,
                comment: l,
                track: r,
                genre: (e = e.a(97 + t + 30)) < 255 ? a[e] : ""
            }
        }, e.ID3v1 = e.q
    }(this),
    function(e) {
        function g(e, t) {
            var o = t.a(e),
                s = t.a(e + 1),
                i = t.a(e + 2);
            return 127 & t.a(e + 3) | (127 & i) << 7 | (127 & s) << 14 | (127 & o) << 21
        }
        var S = e.D = {};
        S.b = {}, S.frames = {
            BUF: "Recommended buffer size",
            CNT: "Play counter",
            COM: "Comments",
            CRA: "Audio encryption",
            CRM: "Encrypted meta frame",
            ETC: "Event timing codes",
            EQU: "Equalization",
            GEO: "General encapsulated object",
            IPL: "Involved people list",
            LNK: "Linked information",
            MCI: "Music CD Identifier",
            MLL: "MPEG location lookup table",
            PIC: "Attached picture",
            POP: "Popularimeter",
            REV: "Reverb",
            RVA: "Relative volume adjustment",
            SLT: "Synchronized lyric/text",
            STC: "Synced tempo codes",
            TAL: "Album/Movie/Show title",
            TBP: "BPM (Beats Per Minute)",
            TCM: "Composer",
            TCO: "Content type",
            TCR: "Copyright message",
            TDA: "Date",
            TDY: "Playlist delay",
            TEN: "Encoded by",
            TFT: "File type",
            TIM: "Time",
            TKE: "Initial key",
            TLA: "Language(s)",
            TLE: "Length",
            TMT: "Media type",
            TOA: "Original artist(s)/performer(s)",
            TOF: "Original filename",
            TOL: "Original Lyricist(s)/text writer(s)",
            TOR: "Original release year",
            TOT: "Original album/Movie/Show title",
            TP1: "Lead artist(s)/Lead performer(s)/Soloist(s)/Performing group",
            TP2: "Band/Orchestra/Accompaniment",
            TP3: "Conductor/Performer refinement",
            TP4: "Interpreted, remixed, or otherwise modified by",
            TPA: "Part of a set",
            TPB: "Publisher",
            TRC: "ISRC (International Standard Recording Code)",
            TRD: "Recording dates",
            TRK: "Track number/Position in set",
            TSI: "Size",
            TSS: "Software/hardware and settings used for encoding",
            TT1: "Content group description",
            TT2: "Title/Songname/Content description",
            TT3: "Subtitle/Description refinement",
            TXT: "Lyricist/text writer",
            TXX: "User defined text information frame",
            TYE: "Year",
            UFI: "Unique file identifier",
            ULT: "Unsychronized lyric/text transcription",
            WAF: "Official audio file webpage",
            WAR: "Official artist/performer webpage",
            WAS: "Official audio source webpage",
            WCM: "Commercial information",
            WCP: "Copyright/Legal information",
            WPB: "Publishers official webpage",
            WXX: "User defined URL link frame",
            AENC: "Audio encryption",
            APIC: "Attached picture",
            COMM: "Comments",
            COMR: "Commercial frame",
            ENCR: "Encryption method registration",
            EQUA: "Equalization",
            ETCO: "Event timing codes",
            GEOB: "General encapsulated object",
            GRID: "Group identification registration",
            IPLS: "Involved people list",
            LINK: "Linked information",
            MCDI: "Music CD identifier",
            MLLT: "MPEG location lookup table",
            OWNE: "Ownership frame",
            PRIV: "Private frame",
            PCNT: "Play counter",
            POPM: "Popularimeter",
            POSS: "Position synchronisation frame",
            RBUF: "Recommended buffer size",
            RVAD: "Relative volume adjustment",
            RVRB: "Reverb",
            SYLT: "Synchronized lyric/text",
            SYTC: "Synchronized tempo codes",
            TALB: "Album/Movie/Show title",
            TBPM: "BPM (beats per minute)",
            TCOM: "Composer",
            TCON: "Content type",
            TCOP: "Copyright message",
            TDAT: "Date",
            TDLY: "Playlist delay",
            TENC: "Encoded by",
            TEXT: "Lyricist/Text writer",
            TFLT: "File type",
            TIME: "Time",
            TIT1: "Content group description",
            TIT2: "Title/songname/content description",
            TIT3: "Subtitle/Description refinement",
            TKEY: "Initial key",
            TLAN: "Language(s)",
            TLEN: "Length",
            TMED: "Media type",
            TOAL: "Original album/movie/show title",
            TOFN: "Original filename",
            TOLY: "Original lyricist(s)/text writer(s)",
            TOPE: "Original artist(s)/performer(s)",
            TORY: "Original release year",
            TOWN: "File owner/licensee",
            TPE1: "Lead performer(s)/Soloist(s)",
            TPE2: "Band/orchestra/accompaniment",
            TPE3: "Conductor/performer refinement",
            TPE4: "Interpreted, remixed, or otherwise modified by",
            TPOS: "Part of a set",
            TPUB: "Publisher",
            TRCK: "Track number/Position in set",
            TRDA: "Recording dates",
            TRSN: "Internet radio station name",
            TRSO: "Internet radio station owner",
            TSIZ: "Size",
            TSRC: "ISRC (international standard recording code)",
            TSSE: "Software/Hardware and settings used for encoding",
            TYER: "Year",
            TXXX: "User defined text information frame",
            UFID: "Unique file identifier",
            USER: "Terms of use",
            USLT: "Unsychronized lyric/text transcription",
            WCOM: "Commercial information",
            WCOP: "Copyright/Legal information",
            WOAF: "Official audio file webpage",
            WOAR: "Official artist/performer webpage",
            WOAS: "Official audio source webpage",
            WORS: "Official internet radio station homepage",
            WPAY: "Payment",
            WPUB: "Publishers official webpage",
            WXXX: "User defined URL link frame"
        };
        var y = {
                title: ["TIT2", "TT2"],
                artist: ["TPE1", "TP1"],
                album: ["TALB", "TAL"],
                year: ["TYER", "TYE"],
                comment: ["COMM", "COM"],
                track: ["TRCK", "TRK"],
                genre: ["TCON", "TCO"],
                picture: ["APIC", "PIC"],
                lyrics: ["USLT", "ULT"]
            },
            v = ["title", "artist", "album", "track"];
        S.m = function(e, t) {
            e.f([0, g(6, e)], t)
        }, S.n = function(e, t) {
            var o = 0;
            if (4 < (d = e.a(o + 3))) return {
                version: ">2.4"
            };
            var s = e.a(o + 4),
                i = e.d(o + 5, 7),
                n = e.d(o + 5, 6),
                l = e.d(o + 5, 5),
                r = g(o + 6, e);
            o += 10;
            if (n) o = o + ((c = e.i(o)) + 4);
            var a, d = {
                version: "2." + d + "." + s,
                major: d,
                revision: s,
                flags: {
                    unsynchronisation: i,
                    extended_header: n,
                    experimental_indicator: l
                },
                size: r
            };
            if (i) a = {};
            else {
                r = r - 10, i = e, s = t, n = {}, l = d.major;
                for (var u, c = [], h = 0; u = (s || v)[h]; h++) c = c.concat(y[u] || [u]);
                for (s = c; o < r;) {
                    h = i, u = o;
                    var _ = c = null;
                    switch (l) {
                        case 2:
                            a = h.c(u, 3);
                            var f = h.o(u + 3),
                                p = 6;
                            break;
                        case 3:
                            a = h.c(u, 4), f = h.i(u + 4), p = 10;
                            break;
                        case 4:
                            a = h.c(u, 4), f = g(u + 4, h), p = 10
                    }
                    if ("" == a) break;
                    o += p + f, s.indexOf(a) < 0 || (2 < l && (_ = {
                        message: {
                            P: h.d(u + 8, 6),
                            I: h.d(u + 8, 5),
                            M: h.d(u + 8, 4)
                        },
                        k: {
                            K: h.d(u + 8 + 1, 7),
                            F: h.d(u + 8 + 1, 3),
                            H: h.d(u + 8 + 1, 2),
                            C: h.d(u + 8 + 1, 1),
                            u: h.d(u + 8 + 1, 0)
                        }
                    }), u += p, _ && _.k.u && (g(u, h), u += 4, f -= 4), _ && _.k.C || (a in S.b ? c = S.b[a] : "T" == a[0] && (c = S.b["T*"]), c = c ? c(u, f, h, _) : void 0, c = {
                        id: a,
                        size: f,
                        description: a in S.frames ? S.frames[a] : "Unknown",
                        data: c
                    }, a in n ? (n[a].id && (n[a] = [n[a]]), n[a].push(c)) : n[a] = c))
                }
                a = n
            }
            for (var m in y)
                if (y.hasOwnProperty(m)) {
                    e: {
                        for ("string" == typeof(f = y[m]) && (f = [f]), o = void(p = 0); o = f[p]; p++)
                            if (o in a) {
                                e = a[o].data;
                                break e
                            } e = void 0
                    }
                    e && (d[m] = e)
                } for (var b in a) a.hasOwnProperty(b) && (d[b] = a[b]);
            return d
        }, e.ID3v2 = S
    }(this),
    function() {
        function r(e) {
            var t;
            switch (e) {
                case 0:
                    t = "iso-8859-1";
                    break;
                case 1:
                    t = "utf-16";
                    break;
                case 2:
                    t = "utf-16be";
                    break;
                case 3:
                    t = "utf-8"
            }
            return t
        }
        var a = "32x32 pixels 'file icon' (PNG only);Other file icon;Cover (front);Cover (back);Leaflet page;Media (e.g. lable side of CD);Lead artist/lead performer/soloist;Artist/performer;Conductor;Band/Orchestra;Composer;Lyricist/text writer;Recording Location;During recording;During performance;Movie/video screen capture;A bright coloured fish;Illustration;Band/artist logotype;Publisher/Studio logotype".split(";");
        ID3v2.b.APIC = function(e, t, o, s, i) {
            i = i || "3", s = e;
            var n = r(o.a(e));
            switch (i) {
                case "2":
                    var l = o.c(e + 1, 3);
                    e += 4;
                    break;
                case "3":
                case "4":
                    e += 1 + (l = o.e(e + 1, t - (e - s), n)).g
            }
            return i = o.a(e, 1), i = a[i], e += 1 + (n = o.e(e + 1, t - (e - s), n)).g, {
                format: l.toString(),
                type: i,
                description: n.toString(),
                data: o.l(e, s + t - e)
            }
        }, ID3v2.b.COMM = function(e, t, o) {
            var s = e,
                i = r(o.a(e)),
                n = o.c(e + 1, 3),
                l = o.e(e + 4, t - 4, i);
            return e += 4 + l.g, e = o.e(e, s + t - e, i), {
                language: n,
                O: l.toString(),
                text: e.toString()
            }
        }, ID3v2.b.COM = ID3v2.b.COMM, ID3v2.b.PIC = function(e, t, o, s) {
            return ID3v2.b.APIC(e, t, o, s, "2")
        }, ID3v2.b.PCNT = function(e, t, o) {
            return o.J(e)
        }, ID3v2.b.CNT = ID3v2.b.PCNT, ID3v2.b["T*"] = function(e, t, o) {
            var s = r(o.a(e));
            return o.e(e + 1, t - 1, s).toString()
        }, ID3v2.b.TCON = function(e, t, o) {
            return ID3v2.b["T*"].apply(this, arguments).replace(/^\(\d+\)/, "")
        }, ID3v2.b.TCO = ID3v2.b.TCON, ID3v2.b.USLT = function(e, t, o) {
            var s = e,
                i = r(o.a(e)),
                n = o.c(e + 1, 3),
                l = o.e(e + 4, t - 4, i);
            return e += 4 + l.g, e = o.e(e, s + t - e, i), {
                language: n,
                G: l.toString(),
                L: e.toString()
            }
        }, ID3v2.b.ULT = ID3v2.b.USLT
    }(),
    function(e) {
        var _ = e.r = {};
        _.types = {
            0: "uint8",
            1: "text",
            13: "jpeg",
            14: "png",
            21: "uint8"
        }, _.j = {
            "Â©alb": ["album"],
            "Â©art": ["artist"],
            "Â©ART": ["artist"],
            aART: ["artist"],
            "Â©day": ["year"],
            "Â©nam": ["title"],
            "Â©gen": ["genre"],
            trkn: ["track"],
            "Â©wrt": ["composer"],
            "Â©too": ["encoder"],
            cprt: ["copyright"],
            covr: ["picture"],
            "Â©grp": ["grouping"],
            keyw: ["keyword"],
            "Â©lyr": ["lyrics"],
            "Â©cmt": ["comment"],
            tmpo: ["tempo"],
            cpil: ["compilation"],
            disk: ["disc"]
        }, _.m = function(e, t) {
            e.f([0, 7], function() {
                ! function e(t, o, s, i) {
                    var n = t.i(o);
                    if (0 == n) i();
                    else {
                        var l = t.c(o + 4, 4); - 1 < ["moov", "udta", "meta", "ilst"].indexOf(l) ? ("meta" == l && (o += 4), t.f([o + 8, o + 8 + 8], function() {
                            e(t, o + 8, n - 8, i)
                        })) : t.f([o + (l in _.j ? 0 : n), o + n + 8], function() {
                            e(t, o + n, s, i)
                        })
                    }
                }(e, 0, e.h(), t)
            })
        }, _.n = function(e) {
            var t = {};
            return function e(t, o, s, i, n) {
                n = void 0 === n ? "" : n + "  ";
                for (var l = s; l < s + i;) {
                    var r = o.i(l);
                    if (0 == r) break;
                    var a = o.c(l + 4, 4);
                    if (-1 < ["moov", "udta", "meta", "ilst"].indexOf(a)) {
                        "meta" == a && (l += 4), e(t, o, l + 8, r - 8, n);
                        break
                    }
                    if (_.j[a]) {
                        var d = o.o(l + 16 + 1),
                            u = _.j[a];
                        if (d = _.types[d], "trkn" == a) t[u[0]] = o.a(l + 16 + 11), t.count = o.a(l + 16 + 13);
                        else {
                            a = l + 16 + 4 + 4;
                            var c, h = r - 16 - 4 - 4;
                            switch (d) {
                                case "text":
                                    c = o.e(a, h, "UTF-8");
                                    break;
                                case "uint8":
                                    c = o.w(a);
                                    break;
                                case "jpeg":
                                case "png":
                                    c = {
                                        k: "image/" + d,
                                        data: o.l(a, h)
                                    }
                            }
                            t[u[0]] = "comment" === u[0] ? {
                                text: c
                            } : c
                        }
                    }
                    l += r
                }
            }(t, e, 0, e.h()), t
        }, e.ID4 = e.r
    }(this),
    function(a) {
        var e = navigator.platform,
            t = !1;
        if ("iPad" != e && "iPhone" != e || (t = !0), t) {
            var o = !1;
            if (-1 != navigator.userAgent.indexOf("6") && (o = !0), o) {
                var s = {},
                    i = {},
                    n = a.setTimeout,
                    d = a.setInterval,
                    l = a.clearTimeout,
                    r = a.clearInterval;
                a.setTimeout = function() {
                    return u(n, s, arguments)
                }, a.setInterval = function() {
                    return u(d, i, arguments)
                }, a.clearTimeout = function(e) {
                    var t = s[e];
                    t && (delete s[e], l(t.id))
                }, a.clearInterval = function(e) {
                    var t = i[e];
                    t && (delete i[e], r(t.id))
                }, a.addEventListener("scroll", function() {
                    var e;
                    for (e in s) c(n, l, s, e);
                    for (e in i) c(d, r, i, e)
                })
            }
        }

        function u(e, t, o) {
            var s, i = o[0],
                n = e === d;
            return o[0] = function() {
                i && (i.apply(a, arguments), n || (delete t[s], i = null))
            }, s = e.apply(a, o), t[s] = {
                args: o,
                created: Date.now(),
                cb: i,
                id: s
            }, s
        }

        function c(e, t, o, s) {
            var i = o[s];
            if (i) {
                var n = e === d;
                if (t(i.id), !n) {
                    var l = i.args[1],
                        r = Date.now() - i.created;
                    r < 0 && (r = 0), (l -= r) < 0 && (l = 0), i.args[1] = l
                }
                i.args[0] = function() {
                    i.cb && (i.cb.apply(a, arguments), n || (delete o[s], i.cb = null))
                }, i.created = Date.now(), i.id = e.apply(a, i.args)
            }
        }
    }(window),
    function() {
        var s, _, e;
        s = ("undefined" != typeof window && null !== window ? window.DOMParser : void 0) || ("function" == typeof require ? require("xmldom").DOMParser : void 0) || function() {}, _ = function(e, t) {
            var o, s, i, n, l, r, a, d, u, c, h;
            if (e.hasChildNodes())
                for (l = d = 0, c = (n = e.childNodes).length; 0 <= c ? d < c : c < d; l = 0 <= c ? ++d : --d)
                    if (i = (s = n[l]).nodeName, /REF/i.test(i)) {
                        for (a = u = 0, h = (o = s.attributes).length; 0 <= h ? u < h : h < u; a = 0 <= h ? ++u : --u)
                            if (r = o[a].nodeName.match(/HREF/i)) {
                                t.push({
                                    file: s.getAttribute(r[0]).trim()
                                });
                                break
                            }
                    } else "#text" !== i && _(s, t);
            return null
        }, e = function(e) {
            var t, o;
            return o = [], (t = (new s).parseFromString(e, "text/xml").documentElement) && _(t, o), o
        }, ("undefined" != typeof module && null !== module ? module.exports : window).ASX = {
            name: "asx",
            parse: e
        }
    }.call(this),
    function() {
        var o, s, i, n, e, l;
        o = /:(?:(-?\d+),(.+)\s*-\s*(.+)|(.+))\n(.+)/, n = function(e) {
            var t;
            return (t = e.match(o)) && 6 === t.length ? {
                length: t[1] || 0,
                artist: t[2] || "",
                title: t[4] || t[3],
                file: t[5].trim()
            } : void 0
        }, l = function(e) {
            return {
                file: e.trim()
            }
        }, i = function(e) {
            return !!e.trim().length
        }, s = function(e) {
            return "#" !== e[0]
        }, e = function(e) {
            var t;
            return t = (e = e.replace(/\r/g, "")).search("\n"), "#EXTM3U" === e.substr(0, t) ? e.substr(t).split("\n#").filter(i).map(n) : e.split("\n").filter(i).filter(s).map(l)
        }, ("undefined" != typeof module && null !== module ? module.exports : window).M3U = {
            name: "m3u",
            parse: e
        }
    }.call(this),
    function() {
        var d, e;
        d = /(file|title|length)(\d+)=(.+)\r?/i, e = function(e) {
            var t, o, s, i, n, l, r, a;
            for (i = [], l = 0, r = (a = e.trim().split("\n")).length; l < r; l++)(s = a[l].match(d)) && 4 === s.length && (s[0], o = s[1], t = s[2], n = s[3], i[t] || (i[t] = {}), i[t][o.toLowerCase()] = n);
            return i.filter(function(e) {
                return null != e
            })
        }, ("undefined" != typeof module && null !== module ? module.exports : window).PLS = {
            name: "pls",
            parse: e
        }
    }.call(this),
    function(window) {
        var FWDMSP = function(props) {
                var self = this;
                if (FWDMSP.instaces_ar.push(this), self.mainFolderPath_str = props.mainFolderPath, self.mainFolderPath_str.lastIndexOf("/") + 1 != self.mainFolderPath_str.length && (self.mainFolderPath_str += "/"), this.skinPath_str = props.skinPath, self.skinPath_str.lastIndexOf("/") + 1 != self.skinPath_str.length && (self.skinPath_str += "/"), this.warningIconPath_str = self.mainFolderPath_str + this.skinPath_str + "warningIcon.png", this.useYoutube_bl = props.useYoutube || "no", this.useYoutube_bl = "yes" == self.useYoutube_bl, this.useVideo_bl = props.useVideo || "no", this.useVideo_bl = "yes" == self.useVideo_bl, this.instanceName_str = props.instanceName, this.instanceName_str) {
                    if (window[this.instanceName_str]) alert("FWDMSP instance name " + this.instanceName_str + " is already defined and contains a different instance reference, set a different instance name.");
                    else if (window[this.instanceName_str] = this, this.listeners = {
                            events_ar: []
                        }, window[this.instanceName_str].addListener = function() {}, !document.cookie || -1 == document.cookie.indexOf("FWDMSP=" + self.instanceName_str) || self.isMobile_bl) {
                        var recoverDecodingErrorDate, recoverSwapAudioCodecDate;
                        if (self.init = function() {
                                if (FWDTweenLite.ticker.useRAF(!1), this.props_obj = props, this.props_obj) {
                                    this.position_str = self.props_obj.verticalPosition, this.position_str || (this.position_str = FWDMSP.POSITION_TOP), "bottom" == this.position_str ? this.position_str = FWDMSP.POSITION_BOTTOM : this.position_str = FWDMSP.POSITION_TOP, this.horizontalPosition_str = self.props_obj.horizontalPosition, this.horizontalPosition_str || (this.horizontalPosition_str = FWDMSP.CENTER), "center" == this.horizontalPosition_str ? this.horizontalPosition_str = FWDMSP.CENTER : "left" == this.horizontalPosition_str ? this.horizontalPosition_str = FWDMSP.LEFT : "right" == this.horizontalPosition_str ? this.horizontalPosition_str = FWDMSP.RIGHT : this.horizontalPosition_str = FWDMSP.CENTER, this.stageContainer = document.createElement("div"), this.stageContainer.style.position = "fixed", self.stageContainer.style.width = "100%", FWDMSPUtils.isIEAndLessThen9 ? this.stageContainer.style.zIndex = "21474836" : this.stageContainer.style.zIndex = "21474835", this.stageContainer.style.overflow = "visible", self.stageContainer.style.height = "0px", FWDMSPUtils.isIE ? document.getElementsByTagName("body")[0].appendChild(this.stageContainer) : document.documentElement.appendChild(this.stageContainer), this.popupWindow, this.ws = null, this.so = null, this.data = null, this.opener_do = null, this.customContextMenu_do = null, this.info_do = null, this.main_do = null, this.background_do = null, this.preloader_do = null, this.controller_do = null, this.categories_do = null, this.playlist_do = null, this.audioScreen_do = null, this.flash_do = null, this.flashObject = null, this.facebookShare = null, this.flashObjectMarkup_str = null, this.popupWindowBackgroundColor = this.props_obj.popupWindowBackgroundColor || "#000000", this.prevCatId = -1, this.catId = -1, this.id = -1, this.prevId = -1, this.totalAudio = 0, this.stageWidth = 0, this.stageHeight = 0, this.maxWidth = self.props_obj.maxWidth || 2e3, this.maxHeight = 0, this.prevAddToHeight = -1, this.lastPercentPlayed = 0, this.popupWindowWidth = self.props_obj.popupWindowWidth || 500, this.popupWindowHeight = self.props_obj.popupWindowHeight || 400, FWDMSPUtils.isIE && (this.popupWindowHeight -= 3), this.resizeHandlerId_to, this.resizeHandler2Id_to, this.hidePreloaderId_to, this.orientationChangeId_to, this.showCatWidthDelayId_to, this.showPlaylistWithDelayId_to, this.disablePlaylistForAWhileId_to, this.allowToResizeAndPosition_bl = !1, this.isAPIReady_bl = !1, this.isPlaylistLoaded_bl = !1, this.isFlashScreenReady_bl = !1, this.orintationChangeComplete_bl = !0, this.animate_bl = !1, this.isFirstPlaylistLoaded_bl = !1, this.scrubbedFirstTimeInPopup_bl = !1, this.showedFirstTime_bl = !1, self.isPlaylistShowed_bl = !1, this.useDeepLinking_bl = self.props_obj.useDeepLinking, this.useDeepLinking_bl = "yes" == self.useDeepLinking_bl, this.showMainBackground_bl = "no" != self.props_obj.showMainBackground, this.openInPopup_bl = !1, this.isMobile_bl = FWDMSPUtils.isMobile, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent;
                                    try {
                                        window.opener && window.opener[this.instanceName_str] && window.opener[this.instanceName_str].instanceName_str == this.instanceName_str && (this.openInPopup_bl = !0, this.popupWindow = window.opener[this.instanceName_str], window.opener[this.instanceName_str].removeAndDisablePlayer(), self.isMobile_bl || (document.cookie = "FWDMSP=" + self.instanceName_str + "; expires=Thu, 18 Dec 2030 12:00:00 UTC; path=/", window.onbeforeunload = function(e) {
                                            document.cookie = "FWDMSP=; expires=Thu, 01-Jan-70 00:00:01 GMT; path=/"
                                        }))
                                    } catch (e) {}
                                    var e, t, o, s, i;
                                    self.googleAnalyticsTrackingCode = self.props_obj.googleAnalyticsTrackingCode, !window.ga && self.googleAnalyticsTrackingCode ? (e = window, t = document, o = "ga", e.GoogleAnalyticsObject = o, e.ga = e.ga || function() {
                                        (e.ga.q = e.ga.q || []).push(arguments)
                                    }, e.ga.l = 1 * new Date, s = t.createElement("script"), i = t.getElementsByTagName("script")[0], s.async = 1, s.src = "https://www.google-analytics.com/analytics.js", i.parentNode.insertBefore(s, i), ga("create", self.googleAnalyticsTrackingCode, "auto"), ga("send", "pageview")) : window.ga && self.googleAnalyticsTrackingCode && (ga("create", self.googleAnalyticsTrackingCode, "auto"), ga("send", "pageview")), this.setupMainDo(), this.startResizeHandler(), this.setupInfo(), this.setupData()
                                } else alert("FWDMSP constructor properties object is not defined!")
                            }, this.popup = function() {
                                if (!self.popupWindow || self.popupWindow.closed) {
                                    FWDMSP.isOpenedInPopup = self.instanceName_str;
                                    var e = screen.width / 2 - self.popupWindowWidth / 2,
                                        t = screen.height / 2 - self.popupWindowHeight / 2,
                                        o = "no";
                                    FWDMSPUtils.isSafari && (o = "yes");
                                    try {
                                        FWDMSPUtils.isMobile ? self.popupWindow = window.open(location.href, self.instanceName_str) : self.popupWindow = window.open(location.href, self.instanceName_str, "location=" + o + ", width=" + self.popupWindowWidth + ", height=" + self.popupWindowHeight + ", top=" + t + ", left=" + e), self.popupWindow && (self.stageContainer.style.display = "none", self.preloader_do && self.preloader_do.hide(!1), self.data.closeData(), self.stop(), self.isAPIReady_bl = !1), self.stopResizeHandler(), self.dispatchEvent(FWDMSP.POPUP)
                                    } catch (e) {}
                                }
                            }, this.removeAndDisablePlayer = function() {
                                self.stageContainer.style.display = "none"
                            }, self.setupMainDo = function() {
                                self.showMainBackground_bl && (self.background_do = new FWDMSPDisplayObject("div"), self.background_do.getStyle().width = "100%"), self.main_do = new FWDMSPDisplayObject("div"), self.main_do.getStyle().msTouchAction = "none", self.main_do.getStyle().webkitTapHighlightColor = "rgba(0, 0, 0, 0)", self.main_do.setBackfaceVisibility(), (!FWDMSPUtils.isMobile || FWDMSPUtils.isMobile && FWDMSPUtils.hasPointerEvent) && self.main_do.setSelectable(!1), self.openInPopup_bl ? (document.documentElement.appendChild(self.main_do.screen), self.stageContainer.style.position = "absolute", document.documentElement.style.overflow = "hidden", document.documentElement.style.backgroundColor = self.popupWindowBackgroundColor, self.main_do.setBkColor(self.popupWindowBackgroundColor), FWDMSPUtils.isIEAndLessThen9 ? this.main_do.getStyle().zIndex = "2147483631" : this.main_do.getStyle().zIndex = "99999999991", FWDMSPUtils.isIE ? document.getElementsByTagName("body")[0].appendChild(self.main_do.screen) : document.getElementsByTagName("body")[0].style.display = "none", self.main_do.setHeight(3e3)) : (self.background_do && self.stageContainer.appendChild(self.background_do.screen), self.stageContainer.appendChild(self.main_do.screen))
                            }, self.setupInfo = function() {
                                FWDMSPInfo.setPrototype(), self.info_do = new FWDMSPInfo(self, self.warningIconPath_str), FWDMSPUtils.isIEAndLessThen9 ? self.info_do.getStyle().zIndex = "2147483632" : self.info_do.getStyle().zIndex = "99999999992"
                            }, self.startResizeHandler = function() {
                                window.addEventListener ? (window.addEventListener("resize", self.onResizeHandler), FWDMSPUtils.isAndroid && window.addEventListener("orientationchange", self.orientationChange)) : window.attachEvent && window.attachEvent("onresize", self.onResizeHandler)
                            }, self.stopResizeHandler = function() {
                                clearTimeout(self.resizeHandlerId_to), clearTimeout(self.resizeHandler2Id_to), clearTimeout(self.orientationChangeId_to), window.removeEventListener ? (window.removeEventListener("resize", self.onResizeHandler), window.removeEventListener("orientationchange", self.orientationChange)) : window.detachEvent && window.detachEvent("onresize", self.onResizeHandler)
                            }, self.onScrollHandler = function() {
                                self.onResizeHandler()
                            }, self.onResizeHandler = function(e) {
                                self.resizeHandler()
                            }, this.orientationChange = function() {
                                self.orintationChangeComplete_bl = !1, clearTimeout(self.resizeHandlerId_to), clearTimeout(self.resizeHandler2Id_to), clearTimeout(self.orientationChangeId_to), self.orientationChangeId_to = setTimeout(function() {
                                    self.orintationChangeComplete_bl = !0, self.resizeHandler(!0)
                                }, 1e3), self.stageContainer.style.left = "-5000px", self.preloader_do && self.preloader_do.setX(-5e3)
                            }, self.resizeHandler = function(e, t) {
                                self.orintationChangeComplete_bl && (self.ws = FWDMSPUtils.getViewportSize(), self.stageWidth = document.documentElement.offsetWidth, self.stageContainer.style.left = "0px", self.stageWidth > self.maxWidth && !self.openInPopup_bl && (self.stageWidth = self.maxWidth), self.controller_do && (self.maxHeight = self.controller_do.h), self.stageHeight = self.maxHeight, self.main_do.setWidth(self.stageWidth), self.preloader_do && self.positionPreloader(), self.controller_do && self.controller_do.resizeAndPosition(e), self.categories_do && self.categories_do.resizeAndPosition(), self.playlist_do && self.playlist_do.resizeAndPosition(), self.isFirstPlaylistLoaded_bl && self.setStageContainerFinalHeightAndPosition(!1), self.info_do && self.info_do.isShowed_bl && self.info_do.positionAndResize(), self.atb_do && self.atb_do.isShowed_bl && self.atb_do.positionAndResize(), self.shareWindow_do && self.shareWindow_do.isShowed_bl && self.shareWindow_do.positionAndResize(), self.passWindow_do && self.passWindow_do.isShowed_bl && self.passWindow_do.positionAndResize(), self.playbackRateWindow_do && self.playbackRateWindow_do.isShowed_bl && self.playbackRateWindow_do.positionAndResize(), self.positionVideoHolder())
                            }, this.setStageContainerFinalHeightAndPosition = function(e) {
                                if (self.ws || (self.ws = FWDMSPUtils.getViewportSize()), self.controller_do && self.allowToResizeAndPosition_bl) {
                                    if (self.openInPopup_bl) return self.main_do.setX(0), self.main_do.setY(0), self.main_do.getStyle().width = "100%", self.main_do.setHeight(self.ws.h), self.controller_do.setX(0), FWDAnimation.killTweensOf(self.controller_do), e ? 0 != self.controller_do.y && FWDAnimation.to(self.controller_do, .8, {
                                        y: 0,
                                        ease: Expo.easeInOut
                                    }) : self.controller_do.setY(0), self.isFullScreen_bl || self.controller_do.setY(0), void(self.playlist_do && (FWDAnimation.killTweensOf(self.playlist_do), self.playlist_do.setX(0), self.playlist_do.setY(self.controller_do.h)));
                                    clearTimeout(self.showPlaylistWithDelayId_to), self.playlist_do && self.playlist_do.isShowed_bl && (addToHeight = self.playlist_do.h), self.position_str == FWDMSP.POSITION_TOP ? self.playlist_do ? (self.background_do && self.background_do.setHeight(self.playlist_do.h + self.controller_do.h), self.playlist_do.setY(0), self.isFullScreen_bl ? self.controller_do.setY(0) : self.controller_do.setY(self.playlist_do.h), self.main_do.setHeight(self.playlist_do.h + self.controller_do.h)) : (self.background_do && self.background_do.setHeight(self.controller_do.h), self.controller_do.setY(0), self.main_do.setHeight(self.controller_do.h)) : self.playlist_do ? (self.background_do && self.background_do.setHeight(self.playlist_do.h + self.controller_do.h + 150), self.playlist_do.setY(self.controller_do.h), self.controller_do.setY(0), self.main_do.setHeight(self.playlist_do.h + self.controller_do.h)) : (self.background_do && self.background_do.setHeight(self.controller_do.h), self.controller_do.setY(0), self.main_do.setHeight(self.controller_do.h)), self.horizontalPosition_str == FWDMSP.LEFT ? (self.main_do.setX(0), self.opener_do && ("right" == self.data.openerAlignment_str ? self.opener_do.setX(Math.round(self.stageWidth - self.opener_do.w)) : self.opener_do.setX(0))) : self.horizontalPosition_str == FWDMSP.CENTER ? (self.main_do.setX(Math.round((self.ws.w - self.stageWidth) / 2)), self.opener_do && ("right" == self.data.openerAlignment_str ? self.opener_do.setX(parseInt((self.ws.w - self.stageWidth) / 2) + self.stageWidth - self.opener_do.w) : self.opener_do.setX(self.main_do.x))) : self.horizontalPosition_str == FWDMSP.RIGHT && (self.main_do.setX(Math.round(self.ws.w - self.stageWidth)), "right" == self.data.openerAlignment_str ? self.opener_do.setX(Math.round(self.ws.w - self.opener_do.w)) : self.opener_do.setX(Math.round(self.ws.w - self.stageWidth))), FWDAnimation.killTweensOf(self.stageContainer), self.background_do && FWDAnimation.killTweensOf(self.background_do), FWDAnimation.killTweensOf(self.controller_do), FWDAnimation.killTweensOf(self.opener_do), self.center(), e ? self.position_str == FWDMSP.POSITION_TOP ? self.playlist_do && self.playlist_do.isShowed_bl && self.controller_do.isShowed_bl ? (FWDAnimation.to(self.stageContainer, .8, {
                                        css: {
                                            top: 0
                                        },
                                        ease: Expo.easeInOut
                                    }), FWDAnimation.to(self.opener_do, .8, {
                                        y: self.playlist_do.h + self.controller_do.h,
                                        ease: Expo.easeInOut
                                    })) : self.controller_do.isShowed_bl && self.playlist_do ? (FWDAnimation.to(self.stageContainer, .8, {
                                        css: {
                                            top: -self.playlist_do.h
                                        },
                                        ease: Expo.easeInOut
                                    }), FWDAnimation.to(self.opener_do, .8, {
                                        y: self.playlist_do.h + self.controller_do.h,
                                        ease: Expo.easeInOut
                                    })) : !self.controller_do.isShowed_bl && self.playlist_do ? (FWDAnimation.to(self.stageContainer, .8, {
                                        css: {
                                            top: -self.playlist_do.h - self.controller_do.h
                                        },
                                        ease: Expo.easeInOut
                                    }), FWDAnimation.to(self.opener_do, .8, {
                                        y: self.playlist_do.h + self.controller_do.h,
                                        ease: Expo.easeInOut,
                                        onComplete: self.moveWheyLeft
                                    })) : (self.controller_do.isShowed_bl ? FWDAnimation.to(self.stageContainer, .8, {
                                        css: {
                                            top: 0
                                        },
                                        ease: Expo.easeInOut
                                    }) : FWDAnimation.to(self.stageContainer, .8, {
                                        css: {
                                            top: -self.controller_do.h
                                        },
                                        ease: Expo.easeInOut
                                    }), FWDAnimation.to(self.opener_do, .8, {
                                        y: self.controller_do.h,
                                        ease: Expo.easeInOut
                                    })) : (self.playlist_do && self.playlist_do.isShowed_bl && self.controller_do.isShowed_bl ? FWDAnimation.to(self.stageContainer, .8, {
                                        css: {
                                            top: self.ws.h - self.controller_do.h - self.playlist_do.h
                                        },
                                        ease: Expo.easeInOut
                                    }) : self.controller_do.isShowed_bl && self.playlist_do ? FWDAnimation.to(self.stageContainer, .8, {
                                        css: {
                                            top: self.ws.h - self.controller_do.h
                                        },
                                        ease: Expo.easeInOut
                                    }) : self.controller_do.isShowed_bl ? FWDAnimation.to(self.stageContainer, .8, {
                                        css: {
                                            top: self.ws.h - self.controller_do.h
                                        },
                                        ease: Expo.easeInOut
                                    }) : self.controller_do.isShowed_bl ? FWDAnimation.to(self.stageContainer, .8, {
                                        css: {
                                            top: 0
                                        },
                                        ease: Expo.easeInOut
                                    }) : FWDAnimation.to(self.stageContainer, .8, {
                                        css: {
                                            top: self.ws.h
                                        },
                                        ease: Expo.easeInOut,
                                        onComplete: self.moveWheyLeft
                                    }), FWDAnimation.to(self.opener_do, .8, {
                                        y: -self.opener_do.h,
                                        ease: Expo.easeInOut
                                    })) : self.position_str == FWDMSP.POSITION_TOP ? self.playlist_do && self.playlist_do.isShowed_bl && self.controller_do.isShowed_bl ? (self.stageContainer.style.top = "0px", self.opener_do.setY(self.playlist_do.h + self.controller_do.h)) : self.controller_do.isShowed_bl && self.playlist_do ? (self.stageContainer.style.top = -self.playlist_do.h + "px", self.opener_do.setY(self.playlist_do.h + self.controller_do.h)) : !self.controller_do.isShowed_bl && self.playlist_do ? (self.stageContainer.style.top = -self.playlist_do.h - self.controller_do.h + "px", self.opener_do.setY(self.playlist_do.h + self.controller_do.h)) : self.controller_do.isShowed_bl ? (self.stageContainer.style.top = "0px", self.opener_do.setY(self.controller_do.h)) : (self.stageContainer.style.top = -self.controller_do.h + "px", self.opener_do.setY(self.controller_do.h), self.moveWheyLeft()) : (self.playlist_do && self.playlist_do.isShowed_bl && self.controller_do.isShowed_bl ? self.stageContainer.style.top = self.ws.h - self.controller_do.h - self.playlist_do.h + "px" : self.controller_do.isShowed_bl && self.playlist_do ? self.stageContainer.style.top = self.ws.h - self.controller_do.h + "px" : self.controller_do.isShowed_bl ? self.stageContainer.style.top = self.ws.h - self.controller_do.h + "px" : (self.stageContainer.style.top = self.ws.h + "px", self.moveWheyLeft()), self.opener_do.setY(-self.opener_do.h))
                                }
                            }, this.moveWheyLeft = function() {
                                self.main_do.setX(-5e3), self.background_do && self.background_do.setWidth(0)
                            }, this.center = function() {
                                self.isFullScreen_bl && self.main_do.setX(0), self.background_do && (self.background_do.getStyle().width = "100%")
                            }, this.setupContextMenu = function() {
                                self.customContextMenu_do = new FWDMSPContextMenu(self.main_do, self.data.rightClickContextMenu_str)
                            }, this.setupMainInstances = function() {
                                self.controller_do || (FWDMSP.hasHTML5Audio && self.setupAudioScreen(), self.data.showPlaylistsButtonAndPlaylists_bl && self.setupCategories(), self.data.showPlayListButtonAndPlaylist_bl && self.setupPlaylist(), self.setupController(), self.setupVideosHolder(), self.setupHider(), self.useYoutube_bl && self.setupYoutubePlayer(), self.setupVideoScreen(), self.data.showShareButton_bl && self.setupShareWindow(), self.data.showPlaybackRateButton_bl && self.setupPlaybackRateWindow(), self.setupPasswordWindow(), self.setupOpener(), self.controller_do.resizeAndPosition(), self.data.addKeyboardSupport_bl && self.addKeyboardSupport())
                            }, this.setInputs = function() {
                                for (var e = document.querySelectorAll("input"), t = 0; t < e.length; t++) self.hasPointerEvent_bl ? e[t].addEventListener("pointerdown", self.inputFocusInHandler) : e[t].addEventListener && (e[t].addEventListener("mousedown", self.inputFocusInHandler), e[t].addEventListener("touchstart", self.inputFocusInHandler))
                            }, this.inputFocusInHandler = function(e) {
                                self.curInput = e.target, setTimeout(function() {
                                    self.hasPointerEvent_bl ? window.addEventListener("pointerdown", self.inputFocusOutHandler) : window.addEventListener && (window.addEventListener("mousedown", self.inputFocusOutHandler), window.addEventListener("touchstart", self.inputFocusOutHandler)), FWDMSP.isSearchedFocused_bl = !0
                                }, 50)
                            }, this.inputFocusOutHandler = function(e) {
                                var t = FWDUVPUtils.getViewportMouseCoordinates(e);
                                if (!FWDUVPUtils.hitTest(self.curInput, t.screenX, t.screenY)) return self.hasPointerEvent_bl ? window.removeEventListener("pointerdown", self.inputFocusOutHandler) : window.removeEventListener && (window.removeEventListener("mousedown", self.inputFocusOutHandler), window.removeEventListener("touchstart", self.inputFocusOutHandler)), void(FWDMSP.isSearchedFocused_bl = !1)
                            }, this.addKeyboardSupport = function() {
                                self.setInputs(), document.addEventListener("keydown", this.onKeyDownHandler), document.addEventListener("keyup", this.onKeyUpHandler)
                            }, this.onKeyDownHandler = function(e) {
                                if (!self.isSpaceDown_bl && self.hasStartedToPlay_bl && !FWDMSP.isSearchedFocused_bl && (self.isSpaceDown_bl = !0, e.preventDefault && e.preventDefault(), self == FWDMSP.keyboardCurInstance)) {
                                    if (32 == e.keyCode) {
                                        if (self.audioType_str == FWDMSP.YOUTUBE) {
                                            if (!self.ytb_do.isSafeToBeControlled_bl) return;
                                            self.ytb_do.togglePlayPause()
                                        } else if (self.audioType_str != FWDMSP.VIDEO && self.audioType_str != FWDMSP.HLS || !self.videoScreen_do) {
                                            if (!self.audioScreen_do.isSafeToBeControlled_bl) return;
                                            self.audioScreen_do.togglePlayPause()
                                        } else {
                                            if (!self.videoScreen_do.isSafeToBeControlled_bl) return;
                                            self.videoScreen_do && self.videoScreen_do.togglePlayPause()
                                        }
                                        return e.preventDefault && e.preventDefault(), !1
                                    }
                                    if (77 == e.keyCode) 0 != self.volume && (self.lastVolume = self.volume), 0 != self.volume ? self.volume = 0 : self.volume = self.lastVolume, self.setVolume(self.volume);
                                    else if (38 == e.keyCode) self.volume += .1, 1 < self.volume && (self.volume = 1), self.setVolume(self.volume);
                                    else if (40 == e.keyCode) self.volume -= .1, self.volume < 0 && (self.volume = 0), self.setVolume(self.volume);
                                    else if (77 == e.keyCode) self.volume < 0 && (self.volume = 0), self.setVolume(self.volume);
                                    else if (39 != e.keyCode || self.isAdd_bl) {
                                        if (37 == e.keyCode && !self.isAdd_bl) {
                                            5 == (t = self.getCurrentTime()).length && (t = "00:" + t), 7 == t.length && (t = "0" + t), t = FWDMSPUtils.getSecondsFromString(t), t -= 5, 5 == (t = FWDMSPUtils.formatTime(t)).length && (t = "00:" + t), 7 == t.length && (t = "0" + t), self.scrubbAtTime(t)
                                        }
                                    } else {
                                        var t;
                                        5 == (t = self.getCurrentTime()).length && (t = "00:" + t), 7 == t.length && (t = "0" + t), t = FWDMSPUtils.getSecondsFromString(t), t += 5, 5 == (t = FWDMSPUtils.formatTime(t)).length && (t = "00:" + t), 7 == t.length && (t = "0" + t), self.scrubbAtTime(t)
                                    }
                                }
                            }, this.onKeyUpHandler = function(e) {
                                self.isSpaceDown_bl = !1
                            }, this.setupAopw = function() {
                                FWDMSPOPWindow.setPrototype(), self.popw_do = new FWDMSPOPWindow(self.data, self)
                            }, this.setupPasswordWindow = function() {
                                FWDMSPPassword.setPrototype(), self.passWindow_do = new FWDMSPPassword(self.data, self), self.passWindow_do.addListener(FWDMSPPassword.CORRECT, self.passordCorrect)
                            }, this.passordCorrect = function() {
                                self.passWindow_do.hide(), self.hasPassedPassowrd_bl = !0, self.play()
                            }, this.setupShareWindow = function() {
                                FWDMSPShareWindow.setPrototype(), self.shareWindow_do = new FWDMSPShareWindow(self.data, self), self.shareWindow_do.addListener(FWDMSPShareWindow.HIDE_COMPLETE, self.shareWindowHideCompleteHandler)
                            }, this.shareWindowHideCompleteHandler = function() {
                                self.controller_do && !self.isMobile_bl && (self.controller_do.shareButton_do.isDisabled_bl = !1, self.controller_do.shareButton_do.setNormalState())
                            }, this.setupAtbWindow = function() {
                                FWDMSPATB.setPrototype(), self.atb_do = new FWDMSPATB(self.controller_do, self), self.atb_do.addListener(FWDMSPATB.HIDE_COMPLETE, self.atbWindowHideCompleteHandler)
                            }, this.atbWindowHideCompleteHandler = function() {
                                self.controller_do && !self.isMobile_bl && (self.controller_do.atbButton_do.isDisabled_bl = !1, self.controller_do.atbButton_do.setNormalState())
                            }, this.setupPlaybackRateWindow = function() {
                                FWDMSPPlaybackRateWindow.setPrototype(), self.playbackRateWindow_do = new FWDMSPPlaybackRateWindow(self.data, self), self.playbackRateWindow_do.addListener(FWDMSPPlaybackRateWindow.HIDE_COMPLETE, self.playbackRateWindowHideCompleteHandler), self.playbackRateWindow_do.addListener(FWDMSPPlaybackRateWindow.SET_PLAYBACK_RATE, self.playbackRateWindowSetPlaybackRateHandler)
                            }, this.playbackRateWindowHideCompleteHandler = function() {
                                self.controller_do && !self.isMobile_bl && (self.controller_do.playbackRateButton_do.isDisabled_bl = !1, self.controller_do.playbackRateButton_do.setNormalState())
                            }, this.playbackRateWindowSetPlaybackRateHandler = function(e) {
                                self.setPlaybackRate(e.rate)
                            }, this.setupVideoScreen = function() {
                                FWDMSPVideoScreen.setPrototype(), self.videoScreen_do = new FWDMSPVideoScreen(self, self.data.volume), self.videoScreen_do.addListener(FWDMSPVideoScreen.ERROR, self.audioScreenErrorHandler), self.videoScreen_do.addListener(FWDMSPVideoScreen.SAFE_TO_SCRUBB, self.audioScreenSafeToScrubbHandler), self.videoScreen_do.addListener(FWDMSPVideoScreen.STOP, self.audioScreenStopHandler), self.videoScreen_do.addListener(FWDMSPVideoScreen.PLAY, self.audioScreenPlayHandler), self.videoScreen_do.addListener(FWDMSPVideoScreen.PAUSE, self.audioScreenPauseHandler), self.videoScreen_do.addListener(FWDMSPVideoScreen.UPDATE, self.audioScreenUpdateHandler), self.videoScreen_do.addListener(FWDMSPVideoScreen.UPDATE_TIME, self.audioScreenUpdateTimeHandler), self.videoScreen_do.addListener(FWDMSPVideoScreen.LOAD_PROGRESS, self.audioScreenLoadProgressHandler), self.videoScreen_do.addListener(FWDMSPVideoScreen.PLAY_COMPLETE, self.audioScreenPlayCompleteHandler), self.videosHolder_do.addChild(self.videoScreen_do)
                            }, this.setupYoutubePlayer = function() {
                                -1 != location.protocol.indexOf("file:") && (FWDMSPUtils.isOpera || FWDMSPUtils.isIE) || (FWDMSPYoutubeScreen.setPrototype(), self.ytb_do = new FWDMSPYoutubeScreen(self, self.data.volume), self.ytb_do.addListener(FWDMSPYoutubeScreen.READY, self.youtubeReadyHandler), self.ytb_do.addListener(FWDMSPAudioScreen.ERROR, self.audioScreenErrorHandler), self.ytb_do.addListener(FWDMSPYoutubeScreen.SAFE_TO_SCRUBB, self.audioScreenSafeToScrubbHandler), self.ytb_do.addListener(FWDMSPYoutubeScreen.STOP, self.audioScreenStopHandler), self.ytb_do.addListener(FWDMSPYoutubeScreen.PLAY, self.audioScreenPlayHandler), self.ytb_do.addListener(FWDMSPYoutubeScreen.PAUSE, self.audioScreenPauseHandler), self.ytb_do.addListener(FWDMSPYoutubeScreen.UPDATE, self.audioScreenUpdateHandler), self.ytb_do.addListener(FWDMSPYoutubeScreen.UPDATE_TIME, self.audioScreenUpdateTimeHandler), self.ytb_do.addListener(FWDMSPYoutubeScreen.LOAD_PROGRESS, self.audioScreenLoadProgressHandler), self.ytb_do.addListener(FWDMSPYoutubeScreen.PLAY_COMPLETE, self.audioScreenPlayCompleteHandler), self.videosHolder_do.addChild(self.ytb_do))
                            }, this.youtubeReadyHandler = function(e) {}, this.setupContinousPlayback = function() {
                                self.data.useContinuousPlayback_bl && (self.ppPplayedOnce = !1, window.onbeforeunload = function(e) {
                                    var t = new Date;
                                    t.setTime(t.getTime() + 2e4);
                                    var o, s = 0;
                                    self.audioType_str == FWDMSP.YOUTUBE && self.ytb_do ? self.ytb_do && (s = self.ytb_do.lastPercentPlayed, o = self.ytb_do.isPlaying_bl) : self.audioType_str == FWDMSP.VIDEO && self.videoScreen_do ? self.videoScreen_do && (s = self.videoScreen_do.lastPercentPlayed, o = self.videoScreen_do.isPlaying_bl) : self.audioScreen_do && (s = self.audioScreen_do.lastPercentPlayed, o = self.audioScreen_do.isPlaying_bl), document.cookie = "FWDMSPusePP=true; expires=" + t.toGMTString() + ", 01-Jan-70 00:00:01 GMT; path=/", document.cookie = "FWDMSPVolume=" + self.volume + "; expires=" + t.toGMTString() + ", 01-Jan-70 00:00:01 GMT; path=/", document.cookie = "FWDMSPpp=" + s + "; expires=" + t.toGMTString() + ", 01-Jan-70 00:00:01 GMT; path=/", document.cookie = "FWDMSPppPlay=" + o + "; expires=" + t.toGMTString() + ", 01-Jan-70 00:00:01 GMT; path=/", document.cookie = "FWDMSPcatId=" + self.catId + "; expires=" + t.toGMTString() + ", 01-Jan-70 00:00:01 GMT; path=/", document.cookie = "FWDMSPid=" + self.id + "; expires=" + t.toGMTString() + ", 01-Jan-70 00:00:01 GMT; path=/"
                                })
                            }, this.setupData = function() {
                                FWDMSPAudioData.setPrototype(), self.data = new FWDMSPAudioData(self.props_obj, self.rootElement_el, self), self.data.useYoutube_bl = self.useYoutube_bl, self.data.addListener(FWDMSPAudioData.UPDATE_IMAGE, self.onImageUpdate), self.data.addListener(FWDMSPAudioData.PRELOADER_LOAD_DONE, self.onPreloaderLoadDone), self.data.addListener(FWDMSPAudioData.SOUNDCLOUD_TRACK_READY, self.onSoundClooudReady), self.data.addListener(FWDMSPAudioData.RADIO_TRACK_READY, self.onRadioReady), self.data.addListener(FWDMSPAudioData.RADIO_TRACK_UPDATE, self.onRadioTrackUpdate), self.data.addListener(FWDMSPAudioData.LOAD_ERROR, self.dataLoadError), self.data.addListener(FWDMSPAudioData.SKIN_LOAD_COMPLETE, self.dataSkinLoadComplete), self.data.addListener(FWDMSPAudioData.PLAYLIST_LOAD_COMPLETE, self.dataPlayListLoadComplete)
                            }, self.onImageUpdate = function(e) {
                                self.controller_do.loadThumb(e.image)
                            }, self.onRadioReady = function(e) {
                                self.isShoutcast_bl || self.isIcecast_bl ? (self.radioSource_str = e.source, self.data.playlist_ar[self.id].title = e.songTitle, self.controller_do.setTitle(e.songTitle), self.prevAudioPath != self.audioPath && (self.setSource(), self.isPlaylistItemClicked_bl && self.play(), self.prevAudioPath = self.audioPath)) : self.data.closeJsonPLoader()
                            }, self.onRadioTrackUpdate = function(e) {
                                self.curTitle = e.songTitle, self.curTitle != self.prevTitle && (self.controller_do.setTitle(e.songTitle), self.prevTitle = self.curTitle)
                            }, self.onSoundClooudReady = function(e) {
                                self.data.playlist_ar[self.id].source = e.source, self.setSource(), self.isPlaylistItemClicked_bl && self.play()
                            }, self.onPreloaderLoadDone = function() {
                                !self.data.useContinuousPlayback_bl && !self.data.autoPlay_bl || FWDMSP.iFrame || !FWDMSPUtils.isChrome || FWDMSPUtils.isMobile || (FWDMSP.iFrame = document.createElement("iframe"), FWDMSP.iFrame.src = self.data.mainFolderPath_str + "audio/silent.mp3", FWDMSP.iFrame.style.position = "absolute", FWDMSP.iFrame.style.top = "-500px", document.documentElement.appendChild(FWDMSP.iFrame)), self.maxHeight = 32, self.usePlaylistsSelectBox_bl = self.data.usePlaylistsSelectBox_bl, self.background_do && (self.background_do.getStyle().background = "url('" + self.data.skinPath_str + "main-background.png')"), self.setupPreloader(), !self.isMobile_bl && self.data.showContextMenu_bl && self.setupContextMenu(), self.resizeHandler(), self.main_do.setHeight(self.stageHeight), self.openInPopup_bl && self.main_do.setHeight(3e3)
                            }, self.dataLoadError = function(e) {
                                self.maxHeight = 120, self.preloader_do && self.preloader_do.hide(!1), self.main_do.addChild(self.info_do), self.info_do.showText(e.text), self.controller_do || (self.ws || (self.ws = FWDMSPUtils.getViewportSize()), self.position_str == FWDMSP.POSITION_TOP ? self.stageContainer.style.top = "0px" : self.stageContainer.style.top = self.ws.h - self.maxHeight + "px", self.main_do.setHeight(self.maxHeight)), self.resizeHandler(), self.dispatchEvent(FWDMSP.ERROR, {
                                    error: e.text
                                })
                            }, self.dataSkinLoadComplete = function() {
                                self.animate_bl = self.data.animate_bl, self.openInPopup_bl && (self.data.showPopupButton_bl = !1), self.lastVolume = self.volume = self.data.volume, self.setupContinousPlayback(), self.initPlaylist()
                            }, self.initPlaylist = function() {
                                self.useDeepLinking_bl ? setTimeout(function() {
                                    self.setupDL()
                                }, 200) : (FWDMSPUtils.getCookie("FWDMSPusePP") ? (self.catId = FWDMSPUtils.getCookie("FWDMSPcatId"), self.id = FWDMSPUtils.getCookie("FWDMSPid")) : self.openInPopup_bl ? (self.catId = self.popupWindow.catId, self.id = self.popupWindow.id) : (self.catId = self.data.startAtPlaylist, self.id = self.data.startAtTrack), self.loadInternalPlaylist())
                            }, this.dataPlayListLoadComplete = function() {
                                self.isAPIReady_bl || self.dispatchEvent(FWDMSP.READY), self.data.randomizePlaylist_bl && (self.data.playlist_ar = FWDMSPUtils.randomizeArray(self.data.playlist_ar)), self.isAPIReady_bl = !0, self.isPlaylistLoaded_bl = !0, self.data.startAtRandomTrack_bl && (self.id = Math.max(0, parseInt(Math.random() * self.data.playlist_ar.length) - 1), self.startAtTrack = self.id, self.useDeepLinking_bl && (self.preventFWDDLchange_bl = !0, FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id), setTimeout(function() {
                                    self.preventFWDDLchange_bl = !1
                                }, 250))), self.setupMainInstances(), self.updatePlaylist(), self.dispatchEvent(FWDMSP.LOAD_PLAYLIST_COMPLETE)
                            }, this.updatePlaylist = function() {
                                if (self.main_do && self.main_do.contains(self.info_do) && self.main_do.removeChild(self.info_do), self.id > self.data.playlist_ar.length && (self.id = 0), self.data.playlist_ar && (self.videoNameGa = self.data.playlist_ar[self.id].titleText, self.videoCat = self.data.cats_ar[self.catId].playlistsName), self.preloader_do.hide(!0), self.prevId = -1, self.totalAudio = self.data.playlist_ar.length, self.controller_do.enableControllerWhileLoadingPlaylist(), self.controller_do.cleanThumbnails(!0), self.playlist_do && (self.playlist_do.updatePlaylist(self.data.playlist_ar), self.playlist_do.resizeAndPosition(), self.playlist_do.isShowed_bl && self.controller_do.setPlaylistButtonState("selected")), self.openInPopup_bl && self.popupWindow.audioScreen_do && (self.lastPercentPlayed = self.popupWindow.audioScreen_do.lastPercentPlayed), self.playlist_do && self.playlist_do.comboBox_do && self.playlist_do.comboBox_do.setButtonsStateBasedOnId(self.catId), self.setSource(), (self.data.autoPlay_bl || self.data.playTrackAfterPlaylistLoad_bl) && setTimeout(self.play, 1e3), self.openInPopup_bl && !self.showedFirstTime_bl ? (self.controller_do.setY(-self.controller_do.h), self.playlist_do && self.playlist_do.setY(-self.playlist_do.h)) : self.playlist_do && self.playlist_do.setY(-self.playlist_do.h + self.controller_do.h), self.setStageContainerFinalHeightAndPosition(!0), self.openInPopup_bl) return clearTimeout(self.showPlaylistWithDelayId_to), self.showedFirstTime_bl ? self.showPlaylistWithDelayId_to = setTimeout(function() {
                                    self.setStageContainerFinalHeightAndPosition(!0)
                                }, 100) : self.showPlaylistWithDelayId_to = setTimeout(function() {
                                    self.setStageContainerFinalHeightAndPosition(!0)
                                }, 900), self.showedFirstTime_bl = !0, void(self.allowToResizeAndPosition_bl = !0);
                                self.allowToResizeAndPosition_bl = !0, self.position_str == FWDMSP.POSITION_TOP ? self.playlist_do && self.controller_do.isShowed_bl ? self.showedFirstTime_bl ? (self.stageContainer.style.top = -self.playlist_do.h + "px", self.opener_do.setY(self.controller_do.h + self.playlist_do.h)) : (self.stageContainer.style.top = -self.controller_do.h - self.playlist_do.h + "px", self.opener_do.setY(self.controller_do.h + self.playlist_do.h - self.opener_do.h)) : self.controller_do.isShowed_bl ? self.playlist_do ? (self.stageContainer.style.top = self.controller_do.h + "px", self.opener_do.setY(self.controller_do.h + self.playlist_do.h - self.opener_do.h)) : self.showedFirstTime_bl || (self.stageContainer.style.top = -self.controller_do.h + "px", self.opener_do.setY(self.controller_do.h - self.opener_do.h)) : self.playlist_do ? (self.stageContainer.style.top = -self.controller_do.h - self.playlist_do.h + "px", self.opener_do.setY(0)) : self.showedFirstTime_bl ? (self.stageContainer.style.top = -self.controller_do.h + "px", self.opener_do.setY(0)) : (self.stageContainer.style.top = -self.controller_do.h + "px", self.opener_do.setY(-self.opener_do.h)) : self.controller_do.isShowed_bl || self.playlist_do && self.controller_do.isShowed_bl ? self.showedFirstTime_bl ? (self.stageContainer.style.top = self.ws.h - self.controller_do.h + "px", self.opener_do.setY(-self.opener_do.h)) : (self.stageContainer.style.top = self.ws.h + "px", self.opener_do.setY(0)) : self.showedFirstTime_bl ? (self.stageContainer.style.top = self.ws.h + "px", self.opener_do.setY(-self.opener_do.h)) : (self.stageContainer.style.top = self.ws.h + "px", self.opener_do.setY(0)), clearTimeout(self.showPlaylistWithDelayId_to), self.showPlaylistWithDelayId_to = setTimeout(function() {
                                    self.setStageContainerFinalHeightAndPosition(!0)
                                }, 900), self.showedFirstTime_bl = !0
                            }, this.loadInternalPlaylist = function() {
                                self.isPlaylistLoaded_bl = !1, self.data.loadPlaylist(self.catId), self.isPlaylistItemClicked_bl = !1, self.stop(), self.playbackRateWindow_do && self.playbackRateWindow_do.hide(), self.shareWindow_do && self.shareWindow_do.hide(), self.preloader_do.show(!0), self.controller_do && (self.controller_do.disableControllerWhileLoadingPlaylist(), self.controller_do.loadThumb()), self.hider && (self.hider.reset(), self.hider.stop()), self.playlist_do && self.playlist_do.destroyPlaylist(), self.positionPreloader(), self.setStageContainerFinalHeightAndPosition(!1), self.dispatchEvent(FWDMSP.START_TO_LOAD_PLAYLIST)
                            }, this.setupDL = function() {
                                self.setOnceDL = !0, self.dlChangeHandler(), FWDAddress.onChange = self.dlChangeHandler
                            }, this.dlChangeHandler = function() {
                                var e = !1;
                                if (!self.preventFWDDLchange_bl)
                                    if (self.categories_do && self.categories_do.isOnDOM_bl) self.categories_do.hide();
                                    else {
                                        if (self.catId = parseInt(FWDAddress.getParameter("catid")), self.id = parseInt(FWDAddress.getParameter("trackid")), "true" == FWDMSPUtils.getCookie("FWDMSPusePP") && self.setOnceDL && -1 == location.hash.indexOf("catid=")) return self.catId = FWDMSPUtils.getCookie("FWDMSPcatId"), self.id = FWDMSPUtils.getCookie("FWDMSPid"), self.setOnceDL = !1, void(location.hash = self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id);
                                        (void 0 === self.catId || void 0 === self.id || isNaN(self.catId) || isNaN(self.id)) && (self.catId = self.data.startAtPlaylist, self.id = self.data.startAtTrack, e = !0), (self.catId < 0 || self.catId > self.data.totalCategories - 1 && !e) && (self.catId = self.data.startAtPlaylist, self.id = self.data.startAtTrack, e = !0), self.data.playlist_ar && (self.id < 0 && !e ? (self.id = self.data.startAtTrack, e = !0) : self.prevCatId == self.catId && self.id > self.data.playlist_ar.length - 1 && !e && (self.id = self.data.playlist_ar.length - 1, e = !0)), e ? location.hash = self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id : self.prevCatId != self.catId ? (self.loadInternalPlaylist(), self.prevCatId = self.catId) : (self.isPlaylistItemClicked_bl = !0, self.setSource(!1), self.changeHLS_bl = !0, self.isShoutcast_bl || self.isIcecast_bl || self.play())
                                    }
                            }, this.setupPreloader = function() {
                                FWDMSPPreloader.setPrototype(), self.preloader_do = new FWDMSPPreloader(self.data.preloaderPath_str, 53, 34, 30, 80), self.preloader_do.addListener(FWDMSPPreloader.HIDE_COMPLETE, self.preloaderHideComplete), FWDMSPUtils.isIEAndLessThen9 ? self.preloader_do.getStyle().zIndex = "2147483633" : self.preloader_do.getStyle().zIndex = "99999999993", self.preloader_do.setPosition("fixed"), self.preloader_do.setForFixedPosition(), self.preloader_do.show(!0), document.documentElement.appendChild(self.preloader_do.screen)
                            }, this.positionPreloader = function() {
                                self.preloader_do.setX(parseInt((self.ws.w - self.preloader_do.w) / 2)), self.openInPopup_bl ? self.controller_do ? self.preloader_do.setY(parseInt((self.controller_do.h - self.preloader_do.h) / 2)) : self.preloader_do.setY(0) : self.position_str == FWDMSP.POSITION_TOP ? self.controller_do && !self.controller_do.isShowed_bl ? self.preloader_do.setY(-200) : self.controller_do ? self.preloader_do.setY(parseInt((self.controller_do.h - self.preloader_do.h) / 2)) : self.preloader_do.setY(parseInt((self.stageHeight - self.preloader_do.h) / 2)) : self.controller_do && !self.controller_do.isShowed_bl ? self.preloader_do.setY(self.ws.h) : self.controller_do ? self.preloader_do.setY(self.ws.h - self.controller_do.h + parseInt((self.controller_do.h - self.preloader_do.h) / 2)) : self.preloader_do.setY(self.ws.h - self.preloader_do.h)
                            }, this.preloaderHideComplete = function() {
                                self.controller_do.show(), self.opener_do.show(), self.playlist_do && self.playlist_do.show(), self.isFirstPlaylistLoaded_bl = !0, self.allowToResizeAndPosition_bl = !0, self.animate_bl || self.setStageContainerFinalHeightAndPosition(!1)
                            }, this.setupOpener = function() {
                                FWDMSPOpener.setPrototype(), self.opener_do = new FWDMSPOpener(self.data, self.position_str, self.controller_do.isShowed_bl), FWDMSPUtils.isIEAndLessThen9 ? self.opener_do.getStyle().zIndex = "2147483634" : self.opener_do.getStyle().zIndex = "99999999994", self.opener_do.setX(-1e3), self.controller_do.isShowed_bl ? self.opener_do.showCloseButton() : self.opener_do.showOpenButton(), self.opener_do.addListener(FWDMSPOpener.SHOW, self.openerShowHandler), self.opener_do.addListener(FWDMSPOpener.HIDE, self.openerHideHandler), self.opener_do.addListener(FWDMSPController.PLAY, self.controllerOnPlayHandler), self.opener_do.addListener(FWDMSPController.PAUSE, self.controllerOnPauseHandler), self.data.showOpener_bl && self.stageContainer.appendChild(self.opener_do.screen)
                            }, this.openerShowHandler = function() {
                                self.showPlayer()
                            }, this.openerHideHandler = function() {
                                self.hidePlayer()
                            }, this.setupCategories = function() {
                                FWDMSPCategories.setPrototype(), self.categories_do = new FWDMSPCategories(self.data), FWDMSPUtils.isIEAndLessThen9 ? self.categories_do.getStyle().zIndex = "2147483635" : self.categories_do.getStyle().zIndex = "99999999995", self.categories_do.addListener(FWDMSPCategories.HIDE_COMPLETE, self.categoriesHideCompleteHandler), self.data.showPlaylistsByDefault_bl && (self.showCatWidthDelayId_to = setTimeout(function() {
                                    self.showCategories()
                                }, 1400))
                            }, this.categoriesHideCompleteHandler = function(e) {
                                if (self.controller_do.setCategoriesButtonState("unselected"), self.customContextMenu_do && self.customContextMenu_do.updateParent(self.main_do), self.useDeepLinking_bl) self.categories_do.id != self.catId && (self.catId = self.categories_do.id, self.id = 0, FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id));
                                else {
                                    if (self.catId == self.categories_do.id) return;
                                    self.catId = self.categories_do.id, self.id = 0, self.loadInternalPlaylist(self.catId)
                                }
                            }, this.setupPlaylist = function() {
                                FWDMSPPlaylist.setPrototype(), self.playlist_do = new FWDMSPPlaylist(self.data, self), self.playlist_do.addListener(FWDMSPPlaylist.CHANGE_PLAYLIST, self.playlistChangePlaylistHandler), self.playlist_do.addListener(FWDMSPPlaylistItem.MOUSE_UP, self.palylistItemOnUpHandler), self.playlist_do.addListener(FWDMSPPlaylistItem.DOWNLOAD, self.palylistItemDownloadHandler), self.playlist_do.addListener(FWDMSPPlaylistItem.BUY, self.palylistItemBuyHandler), self.playlist_do.addListener(FWDMSPPlaylist.UPDATE_TRACK_TITLE_if_FOLDER, self.palylistUpdateFolderTrackTitle), self.main_do.addChild(self.playlist_do)
                            }, this.playlistChangePlaylistHandler = function(e) {
                                if (self.controller_do.setCategoriesButtonState("unselected"), self.customContextMenu_do && self.customContextMenu_do.updateParent(self.main_do), self.useDeepLinking_bl) e.id != self.catId && (self.catId = e.id, self.id = 0, FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id));
                                else {
                                    if (self.catId == e.id) return;
                                    self.catId = e.id, self.id = 0, self.loadInternalPlaylist(self.catId)
                                }
                            }, this.palylistItemOnUpHandler = function(e) {
                                self.isPlaylistItemClicked_bl = !0, e.id == self.id ? self.audioType_str == FWDMSP.AUDIO && self.audioScreen_do.isPlaying_bl ? self.pause() : self.audioType_str != FWDMSP.AUDIO || self.audioScreen_do.isStopped_bl && !self.audioScreen_do.isStopped_bl ? self.audioType_str != FWDMSP.VIDEO && self.audioType_str != FWDMSP.HLS || !self.videoScreen_do.isPlaying_bl ? self.audioType_str != FWDMSP.VIDEO && self.audioType_str != FWDMSP.HLS || self.videoScreen_do.isStopped_bl ? self.audioType_str == FWDMSP.YOUTUBE && self.ytb_do.isPlaying_bl ? self.pause() : self.audioType_str != FWDMSP.YOUTUBE || self.ytb_do.isStopped_bl || self.play() : self.play() : self.pause() : self.play() : self.useDeepLinking_bl && self.id != e.id ? (FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + e.id), self.id = e.id) : (self.id = e.id, self.setSource(!0), self.changeHLS_bl = !0, self.autioType_str != FWDMSP.HLS && self.play()), self.data.playlist_ar && (self.videoNameGa = self.data.playlist_ar[self.id].titleText, self.videoCat = self.data.cats_ar[self.catId].playlistsName)
                            }, this.palylistItemDownloadHandler = function(e) {
                                self.downloadMP3(e.id)
                            }, this.palylistUpdateFolderTrackTitle = function(e) {
                                self.controller_do.setTitle(e.title)
                            }, this.palylistItemBuyHandler = function(e) {
                                self.buy(e.id)
                            }, this.setupController = function() {
                                FWDMSPController.setPrototype(), self.controller_do = new FWDMSPController(self.data, self), self.controller_do.addListener(FWDMSPController.POPUP, self.controllerOnPopupHandler), self.controller_do.addListener(FWDMSPController.PLAY, self.controllerOnPlayHandler), self.controller_do.addListener(FWDMSPController.PLAY_NEXT, self.controllerPlayNextHandler), self.controller_do.addListener(FWDMSPController.PLAY_PREV, self.controllerPlayPrevHandler), self.controller_do.addListener(FWDMSPController.PAUSE, self.controllerOnPauseHandler), self.controller_do.addListener(FWDMSPController.CHANGE_VOLUME, self.controllerChangeVolumeHandler), self.controller_do.addListener(FWDMSPController.VOLUME_START_TO_SCRUB, self.volumeStartToScrubbHandler), self.controller_do.addListener(FWDMSPController.VOLUME_STOP_TO_SCRUB, self.volumeStopToScrubbHandler), self.controller_do.addListener(FWDMSPController.START_TO_SCRUB, self.controllerStartToScrubbHandler), self.controller_do.addListener(FWDMSPController.SCRUB, self.controllerScrubbHandler), self.controller_do.addListener(FWDMSPController.SCRUB_PLAYLIST_ITEM, self.controllerPlaylistItemScrubbHandler), self.controller_do.addListener(FWDMSPController.STOP_TO_SCRUB, self.controllerStopToScrubbHandler), self.controller_do.addListener(FWDMSPController.SHOW_CATEGORIES, self.showCategoriesHandler), self.controller_do.addListener(FWDMSPController.SHOW_PLAYLIST, self.showPlaylistHandler), self.controller_do.addListener(FWDMSPController.HIDE_PLAYLIST, self.hidePlaylistHandler), self.controller_do.addListener(FWDMSPController.ENABLE_LOOP, self.enableLoopHandler), self.controller_do.addListener(FWDMSPController.DISABLE_LOOP, self.disableLoopHandler), self.controller_do.addListener(FWDMSPController.DOWNLOAD_MP3, self.controllerButtonDownloadMp3Handler), self.controller_do.addListener(FWDMSPController.ENABLE_SHUFFLE, self.enableShuffleHandler), self.controller_do.addListener(FWDMSPController.DISABLE_SHUFFLE, self.disableShuffleHandler), self.controller_do.addListener(FWDMSPController.BUY, self.controllerButtonBuyHandler), self.controller_do.addListener(FWDMSPController.FACEBOOK_SHARE, self.facebookShareHandler), self.controller_do.addListener(FWDMSPController.SHOW_PLAYBACKRATE, self.showPlaybacrateWindowHandler), self.controller_do.addListener(FWDMSPController.SHOW_ATOB, self.showAtobWindowHandler), self.main_do.addChild(self.controller_do), self.openInPopup_bl && self.data.showPlaylistsButtonAndPlaylists_bl && (self.controller_do.setPlaylistButtonState("selected"), self.controller_do.playlistButton_do && self.controller_do.playlistButton_do.disableForGood())
                            }, this.controllerOnPopupHandler = function() {
                                self.popup()
                            }, this.controllerOnPlayHandler = function(e) {
                                self.play()
                            }, this.controllerPlayNextHandler = function(e) {
                                self.isPlaylistItemClicked_bl = !0, self.data.shuffle_bl ? self.playShuffle() : self.playNext()
                            }, this.controllerPlayPrevHandler = function(e) {
                                self.isPlaylistItemClicked_bl = !0, self.data.shuffle_bl ? self.playShuffle() : self.playPrev()
                            }, this.controllerOnPauseHandler = function(e) {
                                self.isPlaylistItemClicked_bl = !0, self.pause()
                            }, this.volumeStartToScrubbHandler = function(e) {
                                self.playlist_do && self.playlist_do.showDisable()
                            }, this.volumeStopToScrubbHandler = function(e) {
                                self.playlist_do && self.playlist_do.hideDisable()
                            }, this.controllerStartToScrubbHandler = function(e) {
                                self.playlist_do && self.playlist_do.showDisable(), self.audioType_str == FWDMSP.YOUTUBE && self.ytb_do ? self.ytb_do.startToScrub() : self.audioType_str == FWDMSP.VIDEO && self.videoScreen_do ? self.videoScreen_do.startToScrub() : FWDMSP.hasHTML5Audio ? self.audioScreen_do.startToScrub() : self.isFlashScreenReady_bl && (FWDMSP.pauseAllAudio(self), self.flashObject.startToScrub())
                            }, this.controllerScrubbHandler = function(e) {
                                self.audioType_str == FWDMSP.YOUTUBE && self.ytb_do ? self.ytb_do.scrub(e.percent) : self.audioType_str == FWDMSP.VIDEO && self.videoScreen_do ? self.videoScreen_do.scrub(e.percent) : FWDMSP.hasHTML5Audio ? self.audioScreen_do.scrub(e.percent) : self.isFlashScreenReady_bl && self.flashObject.scrub(e.percent)
                            }, this.controllerPlaylistItemScrubbHandler = function(e) {
                                self.playlist_do && self.playlist_do.updateCurItemProgress(e.percent)
                            }, this.controllerStopToScrubbHandler = function(e) {
                                self.playlist_do && self.playlist_do.hideDisable(), self.audioType_str == FWDMSP.YOUTUBE && self.ytb_do ? self.ytb_do.stopToScrub() : self.audioType_str == FWDMSP.VIDEO && self.videoScreen_do ? self.videoScreen_do.stopToScrub() : FWDMSP.hasHTML5Audio ? self.audioScreen_do.stopToScrub() : self.isFlashScreenReady_bl && self.flashObject.stopToScrub()
                            }, this.controllerChangeVolumeHandler = function(e) {
                                self.setVolume(e.percent)
                            }, this.showCategoriesHandler = function(e) {
                                self.showCategories(), self.controller_do.setCategoriesButtonState("selected")
                            }, this.showPlaylistHandler = function(e) {
                                self.showPlaylist()
                            }, this.hidePlaylistHandler = function(e) {
                                self.hidePlaylist()
                            }, this.enableLoopHandler = function(e) {
                                self.data.loop_bl = !0, self.data.shuffle_bl = !1, self.controller_do.setLoopStateButton("selected"), self.controller_do.setShuffleButtonState("unselected")
                            }, this.disableLoopHandler = function(e) {
                                self.data.loop_bl = !1, self.controller_do.setLoopStateButton("unselected")
                            }, this.enableShuffleHandler = function(e) {
                                self.data.shuffle_bl = !0, self.data.loop_bl = !1, self.controller_do.setShuffleButtonState("selected"), self.controller_do.setLoopStateButton("unselected")
                            }, this.controllerButtonDownloadMp3Handler = function(e) {
                                self.downloadMP3()
                            }, this.disableShuffleHandler = function(e) {
                                self.data.shuffle_bl = !1, self.controller_do.setShuffleButtonState("unselected")
                            }, this.facebookShareHandler = function(e) {
                                self.resizeHandler(), self.shareWindow_do.show(), self.controller_do && !self.isMobile_bl && (self.controller_do.shareButton_do.setSelectedState(), self.controller_do.shareButton_do.isDisabled_bl = !0)
                            }, this.showPlaybacrateWindowHandler = function(e) {
                                self.resizeHandler(), self.playbackRateWindow_do.show(), self.controller_do && !self.isMobile_bl && (self.controller_do.playbackRateButton_do.setSelectedState(), self.controller_do.playbackRateButton_do.isDisabled_bl = !0)
                            }, this.showAtobWindowHandler = function(e) {
                                self.resizeHandler(), self.atb_do.positionAndResize(), self.atb_do.show(!0), self.controller_do && !self.isMobile_bl && (self.controller_do.atbButton_do.setSelectedState(), self.controller_do.atbButton_do.isDisabled_bl = !0)
                            }, this.controllerButtonBuyHandler = function() {
                                self.buy()
                            }, this.setupAudioScreen = function() {
                                FWDMSPAudioScreen.setPrototype(), self.audioScreen_do = new FWDMSPAudioScreen(self.data.volume, self.data.autoPlay_bl, self.data.loop_bl), self.audioScreen_do.addListener(FWDMSPAudioScreen.ERROR, self.audioScreenErrorHandler), self.audioScreen_do.addListener(FWDMSPAudioScreen.START, self.audioScreenSatrtHandler), self.audioScreen_do.addListener(FWDMSPAudioScreen.SAFE_TO_SCRUBB, self.audioScreenSafeToScrubbHandler), self.audioScreen_do.addListener(FWDMSPAudioScreen.STOP, self.audioScreenStopHandler), self.audioScreen_do.addListener(FWDMSPAudioScreen.PLAY, self.audioScreenPlayHandler), self.audioScreen_do.addListener(FWDMSPAudioScreen.PAUSE, self.audioScreenPauseHandler), self.audioScreen_do.addListener(FWDMSPAudioScreen.UPDATE, self.audioScreenUpdateHandler), self.audioScreen_do.addListener(FWDMSPAudioScreen.UPDATE_TIME, self.audioScreenUpdateTimeHandler), self.audioScreen_do.addListener(FWDMSPAudioScreen.LOAD_PROGRESS, self.audioScreenLoadProgressHandler), self.audioScreen_do.addListener(FWDMSPAudioScreen.PLAY_COMPLETE, self.audioScreenPlayCompleteHandler), self.useOnlyAPI_bl ? document.documentElement.appendChild(self.audioScreen_do.screen) : self.main_do.addChild(self.audioScreen_do)
                            }, this.audioScreenErrorHandler = function(e) {
                                var t; - 1 == e.text.indexOf(">null<") && (t = FWDMSP.hasHTML5Audio ? e.text : e, self.main_do && self.main_do.addChild(self.info_do), self.info_do && self.info_do.showText(t), self.position_str == FWDMSP.POSITION_TOP && self.playlist_do && (self.info_do.setY(self.playlist_do.h), self.info_do.setHeight(self.controller_do.h)), self.hider && (self.hider.reset(), self.hider.stop()), self.dispatchEvent(FWDMSP.ERROR, {
                                    error: t
                                }))
                            }, this.audioScreenSatrtHandler = function() {
                                self.dispatchEvent(FWDMSP.START)
                            }, this.audioScreenSafeToScrubbHandler = function() {
                                self.controller_do && self.controller_do.enableMainScrubber(), FWDMSPUtils.getCookie("FWDMSPusePP") && !self.playedOnceCP_bl && (self.setVolume(Number(FWDMSPUtils.getCookie("FWDMSPVolume"))), setTimeout(function() {
                                    self.scrub(Number(FWDMSPUtils.getCookie("FWDMSPpp")))
                                }, 200)), self.playedOnceCP_bl = !0
                            }, this.audioScreenStopHandler = function(e) {
                                self.main_do && self.main_do.contains(self.info_do) && self.main_do.removeChild(self.info_do), self.opener_do && self.opener_do.showPlayButton(), self.controller_do && (self.controller_do.showPlayButton(), self.controller_do.stopEqulizer(), self.controller_do.disableMainScrubber()), self.hider && (self.hider.reset(), self.hider.stop()), self.dispatchEvent(FWDMSP.STOP)
                            }, this.sendGAPlayedEvent = function() {
                                if (window.ga && self.videoNameGa && self.videoNameGa != self.prevVideoNameGa) {
                                    var e = "trackName:" + self.videoNameGa;
                                    ga("send", {
                                        hitType: "event",
                                        eventCategory: self.videoCat,
                                        eventAction: "played",
                                        eventLabel: e,
                                        nonInteraction: !0
                                    })
                                }
                                self.prevVideoNameGa = self.videoNameGa
                            }, this.audioScreenPlayHandler = function() {
                                self.sendGAPlayedEvent(), (FWDMSP.keyboardCurInstance = self).controller_do && (self.controller_do.showPauseButton(), self.controller_do.startEqulizer()), self.opener_do && self.opener_do.showPauseButton(), self.playlist_do && self.playlist_do.setCurItemPauseState(), self.largePlayButton_do && self.largePlayButton_do.hide(), self.hider && self.isFullScreen_bl && self.hider.start(), self.openInPopup_bl && setTimeout(function() {
                                    self.scrubbedFirstTimeInPopup_bl || self.scrub(self.lastPercentPlayed), self.scrubbedFirstTimeInPopup_bl = !0
                                }, 600), self.hasStartedToPlay_bl || self.data.playlist_ar[self.id].startAtTime && self.scrubbAtTime(self.data.playlist_ar[self.id].startAtTime), setTimeout(function() {
                                    self.isPlaylistItemClicked_bl = !1
                                }, 500), self.ppPplayedOnce = !0, self.hasStartedToPlay_bl = !0, self.dispatchEvent(FWDMSP.PLAY)
                            }, this.audioScreenPauseHandler = function() {
                                self.isPlaying_bl = !1, self.opener_do && self.opener_do.showPlayButton(), self.largePlayButton_do && self.isFullScreen_bl && self.largePlayButton_do.show(), self.hider && (self.hider.reset(), self.hider.stop()), !FWDMSPUtils.isIphone && self.largePlayButton_do && self.isFullScreen_bl && (self.audioType_str == FWDMSP.VIDEO ? self.largePlayButton_do && self.isFullScreen_bl && self.largePlayButton_do.show() : self.audioType_str != FWDMSP.YOUTUBE || self.isMobile_bl || self.largePlayButton_do && self.isFullScreen_bl && self.largePlayButton_do.show()), self.showCursor(), self.controller_do && (self.controller_do.showPlayButton(), self.controller_do.stopEqulizer()), self.playlist_do && self.playlist_do.setCurItemPlayState(), self.dispatchEvent(FWDMSP.PAUSE)
                            }, this.audioScreenUpdateHandler = function(e) {
                                var t;
                                t = FWDMSP.hasHTML5Audio ? e.percent : e, self.controller_do && self.controller_do.updateMainScrubber(t), self.playlist_do && self.playlist_do.updateCurItemProgress(t), self.dispatchEvent(FWDMSP.UPDATE, {
                                    percent: t
                                })
                            }, this.audioScreenUpdateTimeHandler = function(e, t) {
                                if (self.prevSeconds != e.seconds && (self.totalTimePlayed += 1), self.totalTimeInSeconds = e.totalTimeInSeconds, self.curTimeInSecond = e.seconds, self.totalTime = e.totalTime, self.curTime = e.curTime, self.prevSeconds = e.seconds, self.totalPercentPlayed = self.totalTimePlayed / e.totalTimeInSeconds, isFinite(self.totalPercentPlayed) || (self.totalPercentPlayed = 0), self.controller_do && !self.controller_do.isMainScrubberScrubbing_bl && self.atb_do && self.atb_do.isShowed_bl && !self.atb_do.scrub) {
                                    var o = self.totalTimeInSeconds * self.atb_do.pa,
                                        s = self.totalTimeInSeconds * self.atb_do.pb;
                                    self.prevCurTimeInSeconds != self.curTimeInSecond && (self.prevCurTimeInSeconds = self.curTimeInSecond, self.curTimeInSecond < o ? self.scrub(self.atb_do.pa) : self.curTimeInSecond > s && self.scrub(self.atb_do.pa))
                                }
                                var i, n;
                                FWDMSP.hasHTML5Audio ? (i = e.curTime, n = e.totalTime) : (i = e, (n = t).length > i.length && (i = parseInt(n.substring(0, 1)) - 1 + ":" + i)), self.controller_do && self.controller_do.updateTime(i, n), FWDMSPUtils.getSecondsFromString(self.data.playlist_ar[self.id].stopAtTime) <= e.seconds && self.stop(), 5 < n.length ? self.totalDuration = FWDMSPUtils.getSecondsFromString(n) : self.totalDuration = FWDMSPUtils.getSecondsFromString("00:" + n), self.dispatchEvent(FWDMSP.UPDATE_TIME, {
                                    curTime: i,
                                    totalTime: n
                                })
                            }, this.audioScreenLoadProgressHandler = function(e) {
                                FWDMSP.hasHTML5Audio ? self.controller_do && self.controller_do.updatePreloaderBar(e.percent) : self.controller_do && self.controller_do.updatePreloaderBar(e)
                            }, this.audioScreenPlayCompleteHandler = function() {
                                self.data.playlist_ar && (self.videoNameGa = self.data.playlist_ar[self.id].titleText, self.videoCat = self.data.cats_ar[self.catId]), FWDMSP.hasHTML5Audio && (self.data.loop_bl ? "hls_flash" == self.audioType_str ? setTimeout(function() {
                                    self.scrub(0), self.resume()
                                }, 50) : (self.scrub(0), self.play()) : self.data.shuffle_bl ? self.playShuffle() : 1 == self.playlist_do.items_ar.length ? (self.stop(), self.playlist_do && self.playlist_do.updateCurItemProgress(0)) : self.playNext()), self.dispatchEvent(FWDMSP.PLAY_COMPLETE)
                            }, this.loadID3IfPlaylistDisabled = function() {
                                var o = self.data.playlist_ar[self.id].source;
                                "..." == self.data.playlist_ar[self.id].title && (o = o + "?rand=" + parseInt(99999999 * Math.random()), ID3.loadTags(o, function() {
                                    var e = self.data.playlist_ar[self.id],
                                        t = ID3.getAllTags(o);
                                    e.title = t.artist + " - " + t.title, e.titleText = e.title, self.controller_do.setTitle(e.title)
                                }))
                            }, this.setSource = function(e) {
                                if (self.stop(!0), FWDMSPUtils.getCookie("FWDMSPusePP") && !self.playedOnceCP_bl && self.setVolume(Number(FWDMSPUtils.getCookie("FWDMSPVolume"))), self.data.playVideoOnlyWhenLoggedIn_bl && !self.data.isLoggedIn_bl) return self.main_do.addChild(self.info_do), self.info_do.showText(self.data.loggedInMessage_str), void(self.info_do.allowToRemove_bl = !1);
                                if (self.useYoutube_bl && self.ytb_do && !self.ytb_do.isReady_bl) setTimeout(self.setSource, 200);
                                else {
                                    if (e && (self.itemClicked = e), self.passWindow_do && self.passWindow_do.hide(), self.id < 0 ? self.id = 0 : self.id > self.totalAudio - 1 && (self.id = self.totalAudio - 1), self.audioPath = self.data.playlist_ar[self.id].source, self.isShoutcast_bl = self.data.playlist_ar[self.id].isShoutcast_bl, self.isIcecast_bl = self.data.playlist_ar[self.id].isIcecast_bl, self.data.shoutcastVersion = self.data.playlist_ar[self.id].shoutcastVersion, !self.isShoutcastLoaded_bl && self.isShoutcast_bl && self.prevAudioPath != self.audioPath) return self.isShoutcastLoaded_bl = !0, self.playlist_do && self.playlist_do.activateItems(self.id, self.itemClicked), self.resizeHandler(), void self.data.getShoutcastRadioNameAndStream(self.audioPath);
                                    if (!self.isIcecastLoaded_bl && self.isIcecast_bl && self.prevAudioPath != self.audioPath) return self.isIcecastLoaded_bl = !0, self.playlist_do && self.playlist_do.activateItems(self.id, self.itemClicked), self.resizeHandler(), void self.data.getIcecastRadioNameAndStream(self.audioPath);
                                    var t;
                                    if ((self.isShoutcast_bl || self.isIcecast_bl) && (self.audioPath = self.radioSource_str), self.prevAudioPath = self.audioPath, self.data.playlist_ar[self.id].controlerThumbnailPath && self.controller_do.loadThumb(self.data.playlist_ar[self.id].controlerThumbnailPath), self.data.playlist_ar[self.id].title && self.controller_do.setTitle(self.data.playlist_ar[self.id].title), (self.isShoutcast_bl || self.isIcecast_bl) && (self.audioPath = self.radioSource_str), self.stop(), self.isShoutcast_bl = self.data.playlist_ar[self.id].isShoutcast_bl, self.isIcecast_bl = self.data.playlist_ar[self.id].isIcecast_bl, self.videoPosterPath = self.data.playlist_ar[self.id].videoPosterPath, -1 != self.audioPath.indexOf("soundcloud.") && -1 == self.audioPath.indexOf("https://api.soundcloud.") ? (self.data.getSoundcloudUrl(self.audioPath), self.isLoadingSoundcloudTrack_bl = !0, self.audioType_str = FWDMSP.AUDIO) : (self.audioType_str = FWDMSP.AUDIO, self.isLoadingSoundcloudTrack_bl = !1), self.finalAudioPath_str = self.audioPath, -1 == self.audioPath.indexOf(".") && self.useYoutube_bl ? self.audioType_str = FWDMSP.YOUTUBE : -1 != self.audioPath.indexOf(".mp4") && self.useVideo_bl ? self.audioType_str = FWDMSP.VIDEO : self.isMobile_bl || FWDMSP.hasHTMLHLS || -1 == self.audioPath.indexOf(".m3u8") ? self.audioType_str = FWDMSP.AUDIO : self.audioType_str = FWDMSP.HLS, self.isMobile_bl ? self.largePlayButton_do && self.largePlayButton_do.hide() : self.largePlayButton_do && self.isFullScreen_bl && self.largePlayButton_do.show(), self.data.playlist_ar[self.id].atb && !self.isATBJsLoaded_bl) return (t = document.createElement("script")).src = self.data.mainFolderPath_str + "java/FWDMSPATB.js", document.head.appendChild(t), t.onerror = function() {
                                        self.main_do.addChild(self.info_do), self.info_do.showText('A to B plugin js file named <font color="#FF0000">FWDMSPATB.js</font> is not found. Please make sure that the content folder contains the java folder that contains the <font color="#FF0000">FWDMSPATB.js</font> file.'), self.preloader_do && self.preloader_do.hide()
                                    }, void(t.onload = function() {
                                        self.isATBJsLoaded_bl = !0, self.setupAtbWindow(), self.setSource(self.audioPath)
                                    });
                                    if (!(self.isMobile_bl || FWDMSP.hasHTMLHLS || -1 == self.audioPath.indexOf(".m3u8") || self.isHLSJsLoaded_bl || FWDMSP.isHLSJsLoaded_bl)) return -1 != location.protocol.indexOf("file:") ? (self.main_do.addChild(self.info_do), self.info_do.showText("This browser dosen't allow playing HLS / live streaming videos local, please test online."), void self.resizeHandler()) : ((t = document.createElement("script")).src = self.data.hlsPath_str, document.head.appendChild(t), t.onerror = function() {
                                        self.main_do.addChild(self.info_do), self.info_do.showText("Error loading HLS library <font color='#FF0000'>" + self.data.hlsPath_str + "</font>."), self.preloader_do && self.preloader_do.hide()
                                    }, void(t.onload = function() {
                                        self.isHLSJsLoaded_bl = !0, FWDMSP.isHLSJsLoaded_bl = !0, self.setupHLS(), self.setSource(self.audioPath)
                                    }));
                                    if (self.audioType_str == FWDMSP.YOUTUBE) {
                                        if (self.ytb_do.ytb && !self.ytb_do.ytb.cueVideoById) return;
                                        self.videoScreen_do && self.videoScreen_do.setX(-500), self.ytb_do.setX(0), self.isLoadingSoundcloudTrack_bl || (self.ytb_do.setSource(self.audioPath), (self.data.autoPlay_bl || self.isPlaylistItemClicked_bl) && self.play(), !FWDMSPUtils.getCookie("FWDMSPppPlay") || self.isMobile_bl || self.ppPplayedOnce || (self.play(), setTimeout(self.play, 1e3))), self.isMobile_bl ? self.largePlayButton_do && self.largePlayButton_do.hide() : self.largePlayButton_do && self.isFullScreen_bl && self.largePlayButton_do.show()
                                    } else self.audioType_str == FWDMSP.VIDEO || self.audioType_str == FWDMSP.HLS ? (self.ytb_do && self.ytb_do.setX(-500), self.isLoadingSoundcloudTrack_bl || (self.videoScreen_do.setSource(self.audioPath), self.videoScreen_do.initVideo(), self.audioType_str == FWDMSP.HLS ? (self.videoScreen_do.setX(-500), self.setupHLS(), self.hlsJS.loadSource(self.audioPath), self.hlsJS.attachMedia(self.videoScreen_do.video_el), self.isHLSManifestReady_bl = !0, (self.data.autoPlay_bl || self.isPlaylistItemClicked_bl) && self.play()) : (self.videoScreen_do.setX(0), (self.data.autoPlay_bl || self.isPlaylistItemClicked_bl) && self.play(), !Boolean("true" == FWDMSPUtils.getCookie("FWDMSPppPlay")) || self.isMobile_bl || self.ppPplayedOnce || self.play())), self.largePlayButton_do && self.isFullScreen_bl && self.largePlayButton_do.show()) : FWDMSP.hasHTML5Audio && (self.goNormalScreen(), self.ytb_do && self.ytb_do.setX(-500), self.videoScreen_do && self.videoScreen_do.setX(-500), self.audioScreen_do.setSource(self.audioPath), (self.data.autoPlay_bl || self.isPlaylistItemClicked_bl) && self.play(), !Boolean("true" == FWDMSPUtils.getCookie("FWDMSPppPlay")) || self.isMobile_bl || self.ppPplayedOnce || self.play());
                                    self.controller_do.stopEqulizer(), self.controller_do.setTitle(self.data.playlist_ar[self.id].title), null == self.data.playlist_ar[self.id].duration ? self.controller_do.updateTime("00:00", "00:00") : self.controller_do.updateTime("00:00", FWDMSP.formatTotalTime(self.data.playlist_ar[self.id].duration)), self.controller_do.loadThumb(self.data.playlist_ar[self.id].thumbPath), self.playlist_do ? self.playlist_do.activateItems(self.id, self.itemClicked) : self.loadID3IfPlaylistDisabled(), self.setPlaybackRate(self.data.defaultPlaybackRate)
                                }
                            }, this.destroyHLS = function() {
                                self.hlsJS && (self.hlsJS.destroy(), self.hlsJS = null)
                            }, this.setupHLS = function() {
                                self.hlsJS || (self.isHLSJsLoaded_bl = !0, self.hlsJS = new Hls, self.hlsJS.on(Hls.Events.ERROR, function(e, t) {
                                    switch (self.HLSError_str, t.details) {
                                        case Hls.ErrorDetails.MANIFEST_LOAD_ERROR:
                                            try {
                                                self.HLSError_str = 'cannot load <a href="' + t.context.url + '">' + url + "</a><br>HTTP response code:" + t.response.code + " <br>" + t.response.text, 0 === t.response.code && (self.HLSError_str += 'this might be a CORS issue, consider installing <a href="https://chrome.google.com/webstore/detail/allow-control-allow-origi/nlfbmbojpeacfghkpbjhddihlkkiljbi">Allow-Control-Allow-Origin</a> Chrome Extension')
                                            } catch (e) {
                                                self.HLSError_str = "cannot load " + self.audioPath
                                            }
                                            break;
                                        case Hls.ErrorDetails.MANIFEST_LOAD_TIMEOUT:
                                            self.HLSError_str = "timeout while loading manifest";
                                            break;
                                        case Hls.ErrorDetails.MANIFEST_PARSING_ERROR:
                                            self.HLSError_str = "error while parsing manifest:" + t.reason;
                                            break;
                                        case Hls.ErrorDetails.LEVEL_LOAD_ERROR:
                                            self.HLSError_str = "error while loading level playlist";
                                            break;
                                        case Hls.ErrorDetails.LEVEL_LOAD_TIMEOUT:
                                            self.HLSError_str = "timeout while loading level playlist";
                                            break;
                                        case Hls.ErrorDetails.LEVEL_SWITCH_ERROR:
                                            self.HLSError_str = "error while trying to switch to level " + t.level;
                                            break;
                                        case Hls.ErrorDetails.FRAG_LOAD_ERROR:
                                            self.HLSError_str = "error while loading fragment " + t.frag.url;
                                            break;
                                        case Hls.ErrorDetails.FRAG_LOAD_TIMEOUT:
                                            self.HLSError_str = "timeout while loading fragment " + t.frag.url;
                                            break;
                                        case Hls.ErrorDetails.FRAG_LOOP_LOADING_ERROR:
                                            self.HLSError_str = "Frag Loop Loading Error";
                                            break;
                                        case Hls.ErrorDetails.FRAG_DECRYPT_ERROR:
                                            self.HLSError_str = "Decrypting Error:" + t.reason;
                                            break;
                                        case Hls.ErrorDetails.FRAG_PARSING_ERROR:
                                            self.HLSError_str = "Parsing Error:" + t.reason;
                                            break;
                                        case Hls.ErrorDetails.KEY_LOAD_ERROR:
                                            self.HLSError_str = "error while loading key " + t.frag.decryptdata.uri;
                                            break;
                                        case Hls.ErrorDetails.KEY_LOAD_TIMEOUT:
                                            self.HLSError_str = "timeout while loading key " + t.frag.decryptdata.uri;
                                            break;
                                        case Hls.ErrorDetails.BUFFER_APPEND_ERROR:
                                            self.HLSError_str = "Buffer Append Error";
                                            break;
                                        case Hls.ErrorDetails.BUFFER_ADD_CODEC_ERROR:
                                            self.HLSError_str = "Buffer Add Codec Error for " + t.mimeType + ":" + t.err.message;
                                            break;
                                        case Hls.ErrorDetails.BUFFER_APPENDING_ERROR:
                                            self.HLSError_str = "Buffer Appending Error"
                                    }
                                    self.HLSError_str && (console && console.log(self.HLSError_str), self.main_do.addChild(self.info_do), self.info_do.showText(self.HLSError_str), self.resizeHandler())
                                }))
                            }, this.setupClickScreen = function() {
                                self.dumyClick_do = new FWDMSPDisplayObject("div"), self.dumyClick_do.getStyle().width = "100%", self.dumyClick_do.getStyle().height = "100%", FWDMSPUtils.isIE && (self.dumyClick_do.setBkColor("#00FF00"), self.dumyClick_do.setAlpha(1e-5)), self.dumyClick_do.screen.addEventListener ? self.dumyClick_do.screen.addEventListener("click", self.playPauseClickHandler) : self.dumyClick_do.screen.attachEvent && self.dumyClick_do.screen.attachEvent("onclick", self.playPauseClickHandler)
                            }, this.playPauseClickHandler = function(e) {
                                2 != e.button && (self.disableClick_bl || (self.firstTapPlaying_bl = self.isPlaying_bl, (FWDMSP.keyboardCurInstance = self).audioType_str == FWDMSP.YOUTUBE ? self.ytb_do.togglePlayPause() : self.audioType_str == FWDMSP.VIDEO && self.videoScreen_do && self.videoScreen_do.togglePlayPause()))
                            }, this.addDoubleClickSupport = function() {
                                !self.isMobile_bl && self.dumyClick_do.screen.addEventListener ? (self.dumyClick_do.screen.addEventListener("mousedown", self.onFirstDown), FWDMSPUtils.isIEWebKit && self.dumyClick_do.screen.addEventListener("dblclick", self.onSecondDown)) : self.isMobile_bl ? self.dumyClick_do.screen.addEventListener("touchstart", self.onFirstDown) : self.dumyClick_do.screen.addEventListener && self.dumyClick_do.screen.addEventListener("mousedown", self.onFirstDown)
                            }, this.onFirstDown = function(e) {
                                if (2 != e.button) {
                                    self.isFullscreen_bl && e.preventDefault && e.preventDefault();
                                    var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                                    self.firstTapX = t.screenX, self.firstTapY = t.screenY, self.firstTapPlaying_bl = self.isPlaying_bl, FWDMSPUtils.isIEWebKit || (self.isMobile_bl ? (self.dumyClick_do.screen.addEventListener("touchstart", self.onSecondDown), self.dumyClick_do.screen.removeEventListener("touchstart", self.onFirstDown)) : self.dumyClick_do.screen.addEventListener && (self.dumyClick_do.screen.addEventListener("mousedown", self.onSecondDown), self.dumyClick_do.screen.removeEventListener("mousedown", self.onFirstDown)), clearTimeout(self.secondTapId_to), self.secondTapId_to = setTimeout(self.doubleTapExpired, 250))
                                }
                            }, this.doubleTapExpired = function() {
                                clearTimeout(self.secondTapId_to), self.isMobile_bl ? (self.dumyClick_do.screen.removeEventListener("touchstart", self.onSecondDown), self.dumyClick_do.screen.addEventListener("touchstart", self.onFirstDown)) : self.dumyClick_do.screen.addEventListener && (self.dumyClick_do.screen.removeEventListener("mousedown", self.onSecondDown), self.dumyClick_do.screen.addEventListener("mousedown", self.onFirstDown))
                            }, this.onSecondDown = function(e) {
                                e.preventDefault && e.preventDefault();
                                var t, o, s = FWDMSPUtils.getViewportMouseCoordinates(e);
                                FWDMSPUtils.isIEWebKit && (self.firstTapPlaying_bl = self.isPlaying_bl), e.touches && 1 != e.touches.length || (t = Math.abs(s.screenX - self.firstTapX), o = Math.abs(s.screenY - self.firstTapY), self.isMobile_bl && (10 < t || 10 < o) || !self.isMobile_bl && (2 < t || 2 < o) || (self.switchFullScreenOnDoubleClick(), FWDMSPUtils.isIEWebKit || (self.firstTapPlaying_bl ? self.play() : self.pause())))
                            }, this.switchFullScreenOnDoubleClick = function() {
                                self.disableClick(), self.isFullScreen_bl ? self.goNormalScreen() : self.goFullScreen()
                            }, this.setupHider = function() {
                                FWDMSPHider.setPrototype(), self.hider = new FWDMSPHider(self.main_do, self.controller_do.videoControllerHolder_do, 2e3), self.hider.addListener(FWDMSPHider.SHOW, self.hiderShowHandler), self.hider.addListener(FWDMSPHider.HIDE, self.hiderHideHandler), self.hider.addListener(FWDMSPHider.HIDE_COMPLETE, self.hiderHideCompleteHandler)
                            }, this.hiderShowHandler = function() {
                                self.controller_do && self.controller_do.showVideoContoller(!0), self.showCursor()
                            }, this.hiderHideHandler = function() {
                                FWDMSPUtils.isIphone || ((self.audioType_str != FWDMSP.VIDEO || !self.videoScreen_do || self.videoScreen_do.isPlaying_bl) && (self.audioType_str != FWDMSP.YOUTUBE || !self.ytb_do || self.ytb_do.isPlaying_bl) ? FWDMSPUtils.hitTest(self.controller_do.videoControllerHolder_do.screen, self.hider.globalX, self.hider.globalY) ? self.hider.reset() : (self.hideCursor(), self.controller_do.hideVideoContoller(!0)) : self.hider.reset())
                            }, this.hiderHideCompleteHandler = function() {}, this.setupVideosHolder = function() {
                                this.videosHolder_do = new FWDMSPDisplayObject("div"), self.videosHolder_do.getStyle().background = "url('" + self.data.thumbnailBkPath_str + "')", this.videosHolder_do.setWidth(self.data.controllerHeight), this.videosHolder_do.setHeight(self.data.controllerHeight), this.controller_do.mainHolder_do.addChild(this.videosHolder_do), self.data.showVideoFullScreenButton_bl && (this.setupClickScreen(), this.setupDisableClick(), this.addDoubleClickSupport(), this.fullScreenButtonOverlay_do = new FWDMSPDisplayObject("div"), self.fullScreenButtonOverlay_do.getStyle().background = "url('" + self.data.thumbnailBkPath_str + "')", this.fullScreenButtonOverlay_do.setWidth(self.data.controllerHeight), this.fullScreenButtonOverlay_do.setHeight(self.data.controllerHeight), FWDMSPSimpleButton.setPrototype(), -1 != this.skinPath_str.indexOf("hex_white") ? self.largePlayButton_do = new FWDMSPSimpleButton(self.data.largePlayN_img, self.data.largePlayS_str, void 0, !0, self.data.useHEXColorsForSkin_bl, self.data.normalButtonsColor_str, "#FFFFFF") : self.largePlayButton_do = new FWDMSPSimpleButton(self.data.largePlayN_img, self.data.largePlayS_str, void 0, !0, self.data.useHEXColorsForSkin_bl, self.data.normalButtonsColor_str, self.data.selectedButtonsColor_str), self.largePlayButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, self.largePlayButtonUpHandler), self.largePlayButton_do.hide(), FWDMSPComplexButton.setPrototype(), self.fullScreenButton_do = new FWDMSPComplexButton(self.data.fullScreenN_img, self.data.fullScreenS_str, self.data.normalScreenN_img, self.data.normalScreenS_str, !0, self.data.useHEXColorsForSkin_bl, self.data.normalButtonsColor_str, self.data.selectedButtonsColor_str), self.fullScreenButton_do.addListener(FWDMSPComplexButton.MOUSE_UP, self.toggleFullScreen), self.checkShowFullScreenButtonHitTest(), setTimeout(function() {
                                    self.videosHolder_do.addChild(self.dumyClick_do), self.disableClick_do && self.main_do.addChild(self.disableClick_do), self.videosHolder_do.addChild(self.fullScreenButtonOverlay_do), self.controller_do.mainHolder_do.contains(self.fullScreenButton_do) || self.videosHolder_do.addChild(self.fullScreenButton_do), self.videosHolder_do.addChild(self.largePlayButton_do), self.hideFullScreenButtonAndOverlay(!1, !0)
                                }, 50))
                            }, this.largePlayButtonUpHandler = function() {
                                self.disableClick(), self.largePlayButton_do.hide(), self.play()
                            }, this.toggleFullScreen = function() {
                                self.isMobile_bl && self.fullScreenButton_do && self.fullScreenButton_do.alpha < .5 ? self.showFullScreenButtonAndOverlay(!0) : 1 == self.fullScreenButton_do.currentState ? self.goFullScreen() : self.goNormalScreen()
                            }, this.positionVideoHolder = function() {
                                if (self.isFullScreen_bl) {
                                    var e = FWDMSPUtils.getViewportSize();
                                    self.videosHolder_do.setWidth(e.w), self.videosHolder_do.setHeight(e.h), self.largePlayButton_do.setX(parseInt((e.w - self.largePlayButton_do.w) / 2)), self.largePlayButton_do.setY(parseInt((e.h - self.largePlayButton_do.h) / 2))
                                } else self.videosHolder_do && (self.videosHolder_do.setWidth(self.data.controllerHeight), self.videosHolder_do.setHeight(self.data.controllerHeight))
                            }, this.checkShowFullScreenButtonHitTest = function() {
                                self.fullScreenButtonOverlay_do && self.fullScreenButtonOverlay_do.screen.addEventListener && (self.fullScreenButtonOverlay_do.screen.addEventListener("mousemove", self.checkShowFullScreenButtonHitTestHandler), window.removeEventListener("mousemove", self.checkFullScreenAndOverlayHit))
                            }, this.checkShowFullScreenButtonHitTestHandler = function() {
                                self.isFullScreen_bl || (self.fullScreenButtonOverlay_do.screen.addEventListener && (self.fullScreenButtonOverlay_do.screen.removeEventListener("mousemove", self.checkShowFullScreenButtonHitTestHandler), window.addEventListener("mousemove", self.checkFullScreenAndOverlayHit)), self.showFullScreenButtonAndOverlay(!0))
                            }, this.checkFullScreenAndOverlayHit = function(e) {
                                if (!self.isFullScreen_bl) {
                                    self.fullScreenButtonOverlay_do.screen.EventListener && self.fullScreenButtonOverlay_do.screen.removeEventListener("mousemove", self.showFullScreenButtonAndOverlay);
                                    var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                                    FWDMSPUtils.hitTest(self.fullScreenButtonOverlay_do.screen, t.screenX, t.screenY) || (self.checkShowFullScreenButtonHitTest(), self.hideFullScreenButtonAndOverlay(!0))
                                }
                            }, this.showFullScreenButtonAndOverlay = function(e) {
                                self.isFullScreenButtonAndOverlayShowed_bl || (this.isFullScreenButtonAndOverlayShowed_bl = !0, FWDAnimation.killTweensOf(self.fullScreenButton_do), FWDAnimation.killTweensOf(self.fullScreenButtonOverlay_do), e ? (FWDAnimation.to(self.fullScreenButton_do, .8, {
                                    alpha: 1,
                                    ease: Expo.easeOut
                                }), FWDAnimation.to(self.fullScreenButtonOverlay_do, .8, {
                                    alpha: .6,
                                    ease: Expo.easeOut
                                })) : (self.fullScreenButton_do.setAlpha(1), self.fullScreenButtonOverlay_do.setAlpha(.6)), self.positionVideoHolder())
                            }, this.hideFullScreenButtonAndOverlay = function(e, t) {
                                (self.isFullScreenButtonAndOverlayShowed_bl || t) && (self.isFullScreenButtonAndOverlayShowed_bl = !1, self.fullScreenButton_do && (FWDAnimation.killTweensOf(self.fullScreenButton_do), FWDAnimation.killTweensOf(self.fullScreenButtonOverlay_do), e ? (0 == self.videosHolder_do.x && FWDAnimation.to(self.fullScreenButton_do, .8, {
                                    alpha: 0,
                                    ease: Expo.easeOut
                                }), FWDAnimation.to(self.fullScreenButtonOverlay_do, .8, {
                                    alpha: 0,
                                    ease: Expo.easeOut
                                })) : (0 == self.videosHolder_do.x && self.fullScreenButton_do.setAlpha(0), self.fullScreenButtonOverlay_do.setAlpha(0))))
                            }, this.setupDisableClick = function() {
                                self.disableClick_do = new FWDMSPDisplayObject("div")
                            }, this.disableClick = function() {
                                self.disableClick_bl = !0, clearTimeout(self.disableClickId_to), self.disableClick_do && (self.disableClick_do.getStyle().width = "5000px", self.disableClick_do.getStyle().height = "5000px"), self.disableClickId_to = setTimeout(function() {
                                    self.disableClick_do && (self.disableClick_do.setWidth(0), self.disableClick_do.setHeight(0)), self.disableClick_bl = !1
                                }, 500)
                            }, this.goFullScreen = function() {
                                if (self.isAPIReady_bl && (self.audioType_str == FWDMSP.YOUTUBE || self.audioType_str == FWDMSP.VIDEO)) {
                                    document.addEventListener && (document.addEventListener("fullscreenchange", self.onFullScreenChange), document.addEventListener("mozfullscreenchange", self.onFullScreenChange), document.addEventListener("webkitfullscreenchange", self.onFullScreenChange), document.addEventListener("MSFullscreenChange", self.onFullScreenChange)), document.documentElement.requestFullScreen ? document.documentElement.requestFullScreen() : document.documentElement.mozRequestFullScreen ? document.documentElement.mozRequestFullScreen() : document.documentElement.webkitRequestFullScreen ? document.documentElement.webkitRequestFullScreen() : document.documentElement.msRequestFullscreen && document.documentElement.msRequestFullscreen(), self.disableClick(), self.main_do.getStyle().position = "fixed", self.main_do.getStyle().overflow = "visible", self.controller_do.setOverflow("visible"), self.controller_do.mainHolder_do.setOverflow("visible"), document.documentElement.style.overflow = "hidden", self.opener_do && self.opener_do.setVisible(!1), self.main_do.getStyle().zIndex = 9999999999998, self.playlist_do && self.playlist_do.setVisible(!1), self.controller_do.goFullScreen(), self.controller_do.setY(0), self.controller_do.videoControllerHolder_do.addChild(self.fullScreenButton_do), self.videosHolder_do.setX(0), self.fullScreenButtonOverlay_do.setVisible(!1), FWDMSP.setInstancesInvisible(this), self.isFullScreen_bl = !0, self.fullScreenButton_do.setButtonState(0);
                                    var e = FWDMSPUtils.getScrollOffsets();
                                    self.lastX = e.x, self.lastY = e.y, self.hider && self.audioType_str == FWDMSP.VIDEO && self.videoScreen_do && self.videoScreen_do.isPlaying_bl ? self.hider.start() : self.hider && self.audioType_str == FWDMSP.YOUTUBE && self.ytb_do && self.ytb_do.isPlaying_bl && self.hider.start(), self.playlist_do && self.playlist_do.ascDscButton_do && self.playlist_do.ascDscButton_do.setAlpha(0), self.audioType_str == FWDMSP.VIDEO && self.videoScreen_do && !self.videoScreen_do.isPlaying_bl ? self.largePlayButton_do.show() : self.audioType_str != FWDMSP.YOUTUBE || !self.ytb_do || self.ytb_do.isPlaying_bl || self.isMobile_bl || self.largePlayButton_do.show(), window.scrollTo(0, 0), self.isMobile_bl && window.addEventListener("touchmove", self.disableFullScreenOnMobileHandler), self.resizeHandler(!0)
                                }
                            }, this.disableFullScreenOnMobileHandler = function(e) {
                                e.preventDefault && e.preventDefault()
                            }, this.goNormalScreen = function() {
                                self.isAPIReady_bl && (document.cancelFullScreen ? document.cancelFullScreen() : document.mozCancelFullScreen ? document.mozCancelFullScreen() : document.webkitCancelFullScreen ? document.webkitCancelFullScreen() : document.msExitFullscreen && document.msExitFullscreen(), self.disableClick(), self.addMainDoToTheOriginalParent(), self.showCursor(), self.fullScreenButton_do && self.fullScreenButton_do.setButtonState(1), self.playlist_do && self.playlist_do.ascDscButton_do && self.playlist_do.ascDscButton_do.setAlpha(1))
                            }, this.addMainDoToTheOriginalParent = function() {
                                self.isFullScreen_bl && (document.removeEventListener && (document.removeEventListener("fullscreenchange", self.onFullScreenChange), document.removeEventListener("mozfullscreenchange", self.onFullScreenChange), document.removeEventListener("webkitfullscreenchange", self.onFullScreenChange), document.removeEventListener("MSFullscreenChange", self.onFullScreenChange)), self.isFullScreen_bl = !1, self.isEmbedded_bl || (FWDMSPUtils.isIEAndLessThen9 ? document.documentElement.style.overflow = "auto" : document.documentElement.style.overflow = "visible", self.main_do.getStyle().position = "relative"), self.controller_do.setOverflow("hidden"), self.controller_do.mainHolder_do.setOverflow("hidden"), self.opener_do && self.opener_do.setVisible(!0), self.controller_do.goNormalScreen(), self.videosHolder_do.addChild(self.fullScreenButton_do), document.documentElement.style.overflow = "visible", self.main_do.getStyle().zIndex = 0, self.playlist_do && (self.playlist_do.setVisible(!0), self.playlist_do.ascDscButton_do && self.playlist_do.ascDscButton_do.setAlpha(1)), self.hideFullScreenButtonAndOverlay(!1), self.fullScreenButtonOverlay_do.setVisible(!0), self.checkShowFullScreenButtonHitTest(), self.largePlayButton_do && self.largePlayButton_do.hide(), self.hider && (self.hider.reset(), self.hider.stop()), FWDMSP.setInstancesInvisible(this, !0), self.resizeHandler(!0), window.scrollTo(self.lastX, self.lastY), FWDMSPUtils.isIE || setTimeout(function() {
                                    window.scrollTo(self.lastX, self.lastY)
                                }, 150), self.isMobile_bl && window.removeEventListener("touchmove", self.disableFullScreenOnMobileHandler))
                            }, this.onFullScreenChange = function(e) {
                                document.fullScreen || document.msFullscreenElement || document.mozFullScreen || document.webkitIsFullScreen || document.msieFullScreen || (self.fullScreenButton_do.setButtonState(1), self.addMainDoToTheOriginalParent(), self.isFullScreen_bl = !1, self.resizeHandler(!0))
                            }, this.hideCursor = function() {
                                document.documentElement.style.cursor = "none", self.dumyClick_do && (self.dumyClick_do.getStyle().cursor = "none"), document.getElementsByTagName("body")[0].style.cursor = "none"
                            }, this.showCursor = function() {
                                document.documentElement.style.cursor = "auto", document.getElementsByTagName("body")[0].style.cursor = "auto", self.dumyClick_do && (self.dumyClick_do.getStyle().cursor = "auto")
                            }, this.showPlayer = function() {
                                self.isAPIReady_bl && (self.controller_do.isShowed_bl = !0, self.opener_do.showCloseButton(), self.setStageContainerFinalHeightAndPosition(self.animate_bl), self.playlist_do && (clearTimeout(self.disablePlaylistForAWhileId_to), self.disablePlaylistForAWhileId_to = setTimeout(function() {
                                    self.playlist_do.hideDisable()
                                }, 500), self.playlist_do.showDisable()))
                            }, this.hidePlayer = function() {
                                self.isAPIReady_bl && (self.controller_do.isShowed_bl = !1, self.opener_do.showOpenButton(), self.setStageContainerFinalHeightAndPosition(self.animate_bl))
                            }, this.loadPlaylist = function(e) {
                                self.isAPIReady_bl && self.data.prevId != e && (self.catId = e, self.categories_do && (self.categories_do.id = self.catId), self.id = 0, self.catId < 0 ? self.catId = 0 : self.catId > self.data.totalCategories - 1 && (self.catId = self.data.totalCategories - 1), self.useDeepLinking_bl ? FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id) : self.loadInternalPlaylist(), self.data.playlist_ar && (self.videoNameGa = self.data.playlist_ar[self.id].titleText, self.videoCat = self.data.cats_ar[self.catId].playlistsName))
                            }, this.playNext = function() {
                                self.isAPIReady_bl && self.isPlaylistLoaded_bl && (self.data.showPlayListButtonAndPlaylist_bl ? self.playlist_do.items_ar[self.playlist_do.curItem_do.sortId + 1] ? self.id = self.playlist_do.items_ar[self.playlist_do.curItem_do.sortId + 1].id : self.id = self.playlist_do.items_ar[0].id : (self.id++, self.id < 0 ? self.id = self.totalAudio - 1 : self.id > self.totalAudio - 1 && (self.id = 0)), self.useDeepLinking_bl ? FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id) : (self.setSource(), self.changeHLS_bl = !0, self.audioType_str != FWDMSP.HLS && self.play()), self.prevId = self.id, self.data.playlist_ar && (self.videoNameGa = self.data.playlist_ar[self.id].titleText, self.videoCat = self.data.cats_ar[self.catId]))
                            }, this.playPrev = function() {
                                self.isAPIReady_bl && self.isPlaylistLoaded_bl && (self.data.showPlayListButtonAndPlaylist_bl ? self.playlist_do.items_ar[self.playlist_do.curItem_do.sortId - 1] ? self.id = self.playlist_do.items_ar[self.playlist_do.curItem_do.sortId - 1].id : self.id = self.playlist_do.items_ar[self.totalAudio - 1].id : (self.id--, self.id < 0 ? self.id = self.totalAudio - 1 : self.id > self.totalAudio - 1 && (self.id = 0)), self.useDeepLinking_bl ? FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id) : (self.setSource(), self.changeHLS_bl = !0, self.audioType_str != FWDMSP.HLS && self.play()), self.prevId = self.id, self.data.playlist_ar && (self.videoNameGa = self.data.playlist_ar[self.id].titleText, self.videoCat = self.data.cats_ar[self.catId].playlistsName))
                            }, this.playShuffle = function() {
                                if (self.isAPIReady_bl && self.isPlaylistLoaded_bl) {
                                    self.isPlaylistItemClicked_bl = !0;
                                    for (var e = parseInt(Math.random() * self.data.playlist_ar.length); e == self.id;) e = parseInt(Math.random() * self.data.playlist_ar.length);
                                    self.id = e, self.id < 0 ? self.id = self.totalAudio - 1 : self.id > self.totalAudio - 1 && (self.id = 0), self.useDeepLinking_bl ? FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id) : (self.setSource(), self.changeHLS_bl = !0, self.audioType_str != FWDMSP.HLS && self.play()), self.prevId = self.id, self.data.playlist_ar && (self.videoNameGa = self.data.playlist_ar[self.id].titleText, self.videoCat = self.data.cats_ar[self.catId])
                                }
                            }, this.playSpecificTrack = function(e, t) {
                                self.isAPIReady_bl && self.isPlaylistLoaded_bl && (self.isPlaylistItemClicked_bl = !0, self.catId = e, self.id = t, self.catId < 0 ? self.catId = 0 : self.catId > self.data.totalCategories - 1 && (self.catId = self.data.totalCategories - 1), self.id < 0 && (self.id = 0), self.useDeepLinking_bl ? FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id) : (self.setSource(), self.play()), self.prevId = self.id, self.data.playlist_ar && (self.videoNameGa = self.data.playlist_ar[self.id].titleText, self.videoCat = self.data.cats_ar[self.catId]))
                            }, this.play = function() {
                                if (self.isAPIReady_bl && self.isPlaylistLoaded_bl && !self.isLoadingSoundcloudTrack_bl) {
                                    if (self.isPlaylistItemClicked_bl = !0, self.audioType_str == FWDMSP.HLS && 0 <= location.protocol.indexOf("file:")) return self.main_do.addChild(self.info_do), self.info_do.showText("HLS m3u8 videos can't be played local on this browser, please test it online!."), void self.info_do.positionAndResize();
                                    if (self.data.playlist_ar[self.id].isPrivate && !self.hasPassedPassowrd_bl && self.passWindow_do) return self.resizeHandler(), void self.passWindow_do.show();
                                    self.hasPassedPassowrd_bl = !0, self.largePlayButton_do && self.largePlayButton_do.hide(), FWDMSP.pauseAllAudio(self), self.audioType_str == FWDMSP.YOUTUBE && self.ytb_do ? self.ytb_do.play() : self.audioType_str != FWDMSP.VIDEO && self.audioType_str != FWDMSP.HLS || !self.videoScreen_do ? self.audioScreen_do && self.audioScreen_do.play() : self.audioType_str != FWDMSP.HLS_JS || self.isHLSManifestReady_bl ? self.videoScreen_do && self.videoScreen_do.play() : (self.videoScreen_do.initVideo(), self.setupHLS(), self.hlsJS.loadSource(self.audioPath), self.hlsJS.attachMedia(self.videoScreen_do.video_el), self.hlsJS.on(Hls.Events.MANIFEST_PARSED, function(e) {
                                        self.isHLSManifestReady_bl = !0, self.audioType_str == FWDMSP.HLS_JS && self.play()
                                    }))
                                }
                            }, this.resume = function() {
                                self.isAPIReady_bl && FWDMSP.hasHTML5Audio && self.audioType_str == FWDMSP.HLS && self.flashObject.playerResume()
                            }, this.pause = function() {
                                self.isAPIReady_bl && self.isPlaylistLoaded_bl && (self.isPlaylistItemClicked_bl = !0, self.largePlayButton_do && self.isFullScreen_bl && self.largePlayButton_do.show(), self.audioType_str == FWDMSP.YOUTUBE ? self.ytb_do.pause() : self.audioType_str != FWDMSP.VIDEO && self.audioType_str != FWDMSP.HLS || !self.videoScreen_do ? FWDMSP.hasHTML5Audio && self.audioScreen_do && self.audioScreen_do.pause() : self.videoScreen_do.pause())
                            }, this.stop = function(e) {
                                self.isAPIReady_bl && (e || (self.isIcecastLoaded_bl = !1, self.isShoutcastLoaded_bl = !1), self.isRadioLoaded_bl = !1, self.hasStartedToPlay_bl = !1, self.hasPassedPassowrd_bl = !1, self.isShoutcast_bl = !1, self.isIcecast_bl = !1, self.destroyHLS(), self.atb_do && self.atb_do.hide(!0), self.opener_do && self.opener_do.showPlayButton(), self.largePlayButton_do && self.largePlayButton_do.hide(), self.playlist_do && (self.playlist_do.setCurItemPlayState(), self.playlist_do.updateCurItemProgress(0)), self.controller_do && self.controller_do.ttm && self.controller_do.ttm.hide(), self.showCursor(), self.audioType_str == FWDMSP.YOUTUBE ? self.ytb_do.stop() : self.audioType_str != FWDMSP.VIDEO && self.audioType_str != FWDMSP.HLS || !self.videoScreen_do ? FWDMSP.hasHTML5Audio && self.audioScreen_do.stop() : self.videoScreen_do.stop(), self.controller_do && self.controller_do.disableAtbButton(), self.setPlaybackRate(self.data.defaultPlaybackRate), self.hasHlsPlayedOnce_bl = !1, self.isSafeToScrub_bl = !1, self.hlsState = void 0, self.changeHLS_bl = !1)
                            }, this.startToScrub = function() {
                                self.isAPIReady_bl && self.isPlaylistLoaded_bl && (self.audioType_str == FWDMSP.YOUTUBE ? self.ytb_do.startToScrub() : self.audioType_str == FWDMSP.VIDEO ? self.videoScreen_do.startToScrub() : FWDMSP.hasHTML5Audio ? self.audioScreen_do.startToScrub() : self.isFlashScreenReady_bl && self.flashObject.startToScrub())
                            }, this.stopToScrub = function() {
                                self.isAPIReady_bl && self.isPlaylistLoaded_bl && (self.audioType_str == FWDMSP.YOUTUBE ? self.ytb_do.stopToScrub() : self.audioType_str == FWDMSP.VIDEO ? self.videoScreen_do.stopToScrub() : FWDMSP.hasHTML5Audio ? self.audioScreen_do.stopToScrub() : self.isFlashScreenReady_bl && self.flashObject.stopToScrub())
                            }, this.scrub = function(e) {
                                self.isAPIReady_bl && self.isPlaylistLoaded_bl && (isNaN(e) || (e < 0 ? e = 0 : 1 < e && (e = 1), self.audioType_str == FWDMSP.YOUTUBE ? self.ytb_do.scrub(e) : self.audioType_str == FWDMSP.VIDEO ? self.videoScreen_do.scrub(e) : FWDMSP.hasHTML5Audio ? self.audioType_str == FWDMSP.HLS ? self.flashObject.playerSeek(e * self.HLSDuration) : self.audioScreen_do && self.audioScreen_do.scrub(e) : self.isFlashScreenReady_bl && self.flashObject.scrub(e)))
                            }, this.setPlaybackRate = function(e) {
                                self.isAPIReady_bl && (self.data.defaultPlaybackRate = e, self.audioType_str == FWDMSP.VIDEO && self.videoScreen_do ? self.videoScreen_do.setPlaybackRate(e) : self.audioType_str == FWDMSP.AUDIO && self.audioScreen_do ? self.audioScreen_do.setPlaybackRate(e) : self.audioType_str == FWDMSP.YOUTUBE && self.ytb_do.setPlaybackRate(e))
                            }, this.setVolume = function(e) {
                                self.isAPIReady_bl && (self.volume = e, self.controller_do && self.controller_do.updateVolume(e, !0), self.audioType_str == FWDMSP.YOUTUBE && self.ytb_do ? self.ytb_do.setVolume(e) : self.audioType_str != FWDMSP.VIDEO && self.audioType_str != FWDMSP.HLS || !self.videoScreen_do ? FWDMSP.hasHTML5Audio && self.audioScreen_do && self.audioScreen_do.setVolume(e) : self.videoScreen_do.setVolume(e))
                            }, this.showCategories = function() {
                                self.isAPIReady_bl && self.categories_do && (self.categories_do.show(self.catId), self.customContextMenu_do && self.customContextMenu_do.updateParent(self.categories_do), self.controller_do.setCategoriesButtonState("selected"))
                            }, this.hideCategories = function() {
                                self.isAPIReady_bl && self.categories_do && (self.categories_do.hide(), self.controller_do.setCategoriesButtonState("unselected"))
                            }, this.showPlaylist = function() {
                                self.isAPIReady_bl && (self.playlist_do && (self.isPlaylistShowed_bl = !0, self.playlist_do.show(!0), self.controller_do.setPlaylistButtonState("selected"), clearTimeout(self.disablePlaylistForAWhileId_to), self.disablePlaylistForAWhileId_to = setTimeout(function() {
                                    self.playlist_do.hideDisable()
                                }, 150), self.playlist_do.showDisable()), self.setStageContainerFinalHeightAndPosition(self.animate_bl))
                            }, this.hidePlaylist = function() {
                                self.isAPIReady_bl && (self.playlist_do && (self.isPlaylistShowed_bl = !1, self.playlist_do.hide(), self.controller_do.setPlaylistButtonState("unselected"), self.setStageContainerFinalHeightAndPosition(self.animate_bl)), self.shareWindow_do && self.shareWindow_do.hide(!0))
                            }, this.getIsAPIReady = function() {
                                return self.isAPIReady_bl
                            }, this.getCatId = function() {
                                return self.catId
                            }, this.getTrackId = function() {
                                return self.id
                            }, this.getTrackTitle = function() {
                                if (self.isAPIReady_bl) return self.data.playlist_ar[self.id].title
                            }, this.getThumbnailPath = function() {
                                return self.data.playlist_ar[self.id].thumbPath
                            }, this.getCurrentTime = function() {
                                if (self.isAPIReady_bl) return self.audioType_str == FWDMSP.YOUTUBE ? self.ytb_do.getCurrentTime() : self.audioType_str == FWDMSP.AUDIO ? self.audioScreen_do.getCurrentTime() : self.audioType_str != FWDMSP.VIDEO && self.audioType_str != FWDMSP.HLS || !self.videoScreen_do ? void 0 : self.videoScreen_do.getCurrentTime()
                            }, this.getDuration = function() {
                                if (self.isAPIReady_bl) return self.audioType_str == FWDMSP.YOUTUBE ? self.ytb_do.getDuration() : self.audioType_str == FWDMSP.AUDIO ? self.audioScreen_do.getDuration() : self.audioType_str != FWDMSP.VIDEO && self.audioType_str != FWDMSP.HLS || !self.videoScreen_do ? void 0 : self.videoScreen_do.getDuration()
                            }, this.share = function() {
                                self.isAPIReady_bl && self.shareWindow_do && self.shareWindow_do.show()
                            }, this.scrubbAtTime = function(e) {
                                self.isAPIReady_bl && e && (-1 != String(e).indexOf(":") && (e = FWDMSPUtils.getSecondsFromString(e)), self.audioType_str == FWDMSP.YOUTUBE && self.ytb_do && self.ytb_do.isSafeToBeControlled_bl ? self.ytb_do.scrubbAtTime(e) : self.audioType_str == FWDMSP.AUDIO ? self.audioScreen_do && self.audioScreen_do.scrubbAtTime(e) : self.audioType_str != FWDMSP.VIDEO && self.audioType_str != FWDMSP.HLS || !self.videoScreen_do || self.videoScreen_do && self.videoScreen_do.scrubbAtTime(e))
                            }, this.downloadMP3 = function(e) {
                                if ("file:" == document.location.protocol) {
                                    return self.main_do.addChild(self.info_do), void self.info_do.showText("Downloading mp3 files local is not allowed or possible!. To function properly please test online.")
                                }
                                if (self.videoNameGa || (self.videoNameGa = self.data.playlist_ar[self.id].titleText, self.videoCat = self.data.cats_ar[self.catId].playlistsName), window.ga) {
                                    var t = "trackName:" + self.videoNameGa;
                                    ga("send", {
                                        hitType: "event",
                                        eventCategory: self.videoCat,
                                        eventAction: "downloaded",
                                        eventLabel: t,
                                        nonInteraction: !0
                                    })
                                }
                                null == e && (e = self.id);
                                var o = self.data.playlist_ar[e].downloadPath,
                                    s = self.data.playlist_ar[e].titleText;
                                self.data.downloadMp3(o, s)
                            }, this.buy = function(pId) {
                                if (self.isAPIReady_bl) {
                                    if ("file:" == document.location.protocol) {
                                        var error = "Buying mp3 files local is not allowed or possible!. To function properly please test online.";
                                        return self.main_do.addChild(self.info_do), void self.info_do.showText(error)
                                    }
                                    null == pId && (pId = self.id);
                                    var buy = self.data.playlist_ar[pId].buy; - 1 != buy.indexOf("http") && buy.indexOf("http") < 3 ? window.open(buy) : eval(buy)
                                }
                            }, this.playFirstTrack = function() {
                                self.playSpecificTrack(self.catId, 0)
                            }, this.playLastTrack = function() {
                                self.playSpecificTrack(self.catId, self.data.playlist_ar.length - 1)
                            }, this.addTrack = function(e, t, o, s, i, n, l) {
                                self.isReady_bl || (self.useDeepLinking_bl && (location.hash = self.instanceName_str + "?catid=" + self.catId + "&trackid=" + (self.id + 1)), self.playlist_do && self.playlist_do.addTrack(e, t, o, s, i, n, l), self.useDeepLinking_bl && (location.hash = self.instanceName_str + "?catid=" + self.catId + "&trackid=0"))
                            }, this.updateHEXColors = function(e, t) {
                                self.isAPIReady_bl && (self.controller_do.updateHEXColors(e, t), self.largePlayButton_do && self.largePlayButton_do.updateHEXColors(e, "#FFFFFF"), self.shareWindow_do && self.shareWindow_do.updateHEXColors(e, t), self.playlist_do && self.playlist_do.updateHEXColors(e, t), self.opener_do && self.opener_do.updateHEXColors(e, "#FFFFFF"), self.playbackRateWindow_do && self.playbackRateWindow_do.updateHEXColors(e, t))
                            }, this.addListener = function(e, t) {
                                if (this.listeners) {
                                    if (null == e) throw Error("type is required.");
                                    if ("object" == typeof e) throw Error("type must be of type String.");
                                    if ("function" != typeof t) throw Error("listener must be of type Function.");
                                    var o = {};
                                    o.type = e, o.listener = t, (o.target = this).listeners.events_ar.push(o)
                                }
                            }, this.dispatchEvent = function(e, t) {
                                if (null != this.listeners) {
                                    if (null == e) throw Error("type is required.");
                                    if ("object" == typeof e) throw Error("type must be of type String.");
                                    for (var o = 0, s = this.listeners.events_ar.length; o < s; o++)
                                        if (this.listeners.events_ar[o].target === this && this.listeners.events_ar[o].type === e) {
                                            if (t)
                                                for (var i in t) this.listeners.events_ar[o][i] = t[i];
                                            this.listeners.events_ar[o].listener.call(this, this.listeners.events_ar[o])
                                        }
                                }
                            }, this.removeListener = function(e, t) {
                                if (null == e) throw Error("type is required.");
                                if ("object" == typeof e) throw Error("type must be of type String.");
                                if ("function" != typeof t) throw Error("listener must be of type Function." + e);
                                for (var o = 0, s = this.listeners.events_ar.length; o < s; o++)
                                    if (this.listeners.events_ar[o].target === this && this.listeners.events_ar[o].type === e && this.listeners.events_ar[o].listener === t) {
                                        this.listeners.events_ar.splice(o, 1);
                                        break
                                    }
                            }, self.useYoutube_bl && (-1 != location.protocol.indexOf("file:") && FWDMSPUtils.isIE || -1 != location.protocol.indexOf("file:") && FWDMSPUtils.isOpera)) return self.stageContainer = FWDMSPUtils.getChildById(props.parentId), self.setupMainDo(), self.setupInfo(), self.main_do.addChild(self.info_do), self.info_do.allowToRemove_bl = !1, self.info_do.showText('This browser dosen\'t allow the Youtube API to run local, please test it online or in another browser like Firefox or Chrome! If you don\'t want to use Youtube set <font color="#FF000000">useYoutube:"no"</font>.'), void self.resizeHandler();
                        setTimeout(FWDMSP.checkIfHasYoutube, 100)
                    }
                } else alert("FWDMSP instance name is requires please make sure that the instanceName parameter exsists and it's value is uinique.");

                function handleMediaError() {
                    if (autoRecoverError) {
                        var e = performance.now();
                        !recoverDecodingErrorDate || 3e3 < e - recoverDecodingErrorDate ? (recoverDecodingErrorDate = performance.now(), self.HLSError_str = "try to recover media Error ...", self.hlsJS.recoverMediaError()) : !recoverSwapAudioCodecDate || 3e3 < e - recoverSwapAudioCodecDate ? (recoverSwapAudioCodecDate = performance.now(), self.HLSError_str = "try to swap Audio Codec and recover media Error ...", self.hlsJS.swapAudioCodec(), self.hlsJS.recoverMediaError()) : self.HLSError_str = "cannot recover, last media error recovery failed ..."
                    }
                    self.HLSError_str && (console && console.log(self.HLSError_str), self.main_do.addChild(self.info_do), self.info_do.showText(self.HLSError_str), self.resizeHandler())
                }
            },
            TZ, UZ, f$, g$;
        FWDMSP.checkIfHasYoutube = function() {
            if (!FWDMSP.checkIfHasYoutube_bl) {
                for (var e = !(FWDMSP.checkIfHasYoutube_bl = !0), t = FWDMSP.instaces_ar.length, o = 0; o < t; o++) FWDMSP.instaces_ar[o].useYoutube_bl && (e = !0);
                e ? setTimeout(FWDMSP.setupYoutubeAPI, 500) : setTimeout(FWDMSP.setupAllInstances, 500)
            }
        }, FWDMSP.setupYoutubeAPI = function() {
            if (!FWDMSP.isYoutubeAPICreated_bl)
                if (FWDMSP.isYoutubeAPICreated_bl = !0, "undefined" != typeof YT) FWDMSP.setupAllInstances();
                else {
                    var e = document.createElement("script");
                    e.src = "https://www.youtube.com/iframe_api";
                    var t = document.getElementsByTagName("script")[0];
                    t.parentNode.insertBefore(e, t), window.onYouTubeIframeAPIReady ? window.onYouTubeIframeAPIReady = function() {
                        FWDMSP.setupAllInstances()
                    } : setTimeout(FWDMSP.setupAllInstances, 1e3)
                }
        }, FWDMSP.setupAllInstances = function() {
            if (!FWDMSP.areInstancesCreated_bl) {
                var e = FWDMSPUtils.getUrlArgs(window.location.search).MSPInstanceName;
                "pause" != FWDMSP.audioStartBehaviour && "stop" != FWDMSP.audioStartBehaviour && "none" != FWDMSP.audioStartBehaviour && (FWDMSP.audioStartBehaviour = "pause"), FWDMSPUtils.isMobile_bl && (FWDMSP.audioStartBehaviour = "stop"), FWDMSP.areInstancesCreated_bl = !0;
                var t, o = FWDMSP.instaces_ar.length,
                    s = !1;
                if (e)
                    for (var i = 0; i < o; i++)
                        if ((t = FWDMSP.instaces_ar[i]).props.instanceName == e) return void(FWDMSP.isEmbedded_bl = !0);
                for (i = 0; i < o; i++) t = FWDMSP.instaces_ar[i], FWDMSP.instaces_ar[i - 1], t.init(), s && (t.data.autoPlay_bl = !1), 1 == t.data.autoPlay_bl && (s = !0)
            }
        }, FWDMSP.setInstancesInvisible = function(e, t) {
            for (var o = 0; o < FWDMSP.instaces_ar.length; o++) inst = FWDMSP.instaces_ar[o], e == inst || t ? (inst.stageContainer.style.overflow = "visible", inst.stageContainer.style.width = "100%") : (inst.stageContainer.style.overflow = "hidden", inst.stageContainer.style.width = "0px")
        }, FWDMSP.setPrototype = function() {
            FWDMSP.prototype = new FWDMSPEventDispatcher
        }, FWDMSP.pauseAllAudio = function(e) {
            for (var t, o = FWDMSP.instaces_ar.length, s = 0; s < o; s++)(t = FWDMSP.instaces_ar[s]) != e && t.stop()
        }, FWDMSP.stopAllAudio = function(e) {
            for (var t, o = FWDMSP.instaces_ar.length, s = 0; s < o; s++)(t = FWDMSP.instaces_ar[s]) != e && t.stop()
        }, FWDMSP.hasHTML5Audio = (TZ = document.createElement("audio"), UZ = !1, TZ.canPlayType && (UZ = Boolean("probably" == TZ.canPlayType("audio/mpeg") || "maybe" == TZ.canPlayType("audio/mpeg"))), !!self.isMobile_bl || UZ), FWDMSP.getAudioFormats = function() {
            var e = document.createElement("audio");
            if (e.canPlayType) {
                var t = "",
                    o = [];
                return "probably" != e.canPlayType("audio/mpeg") && "maybe" != e.canPlayType("audio/mpeg") || (t += ".mp3"), "probably" != e.canPlayType("audio/ogg") && "maybe" != e.canPlayType("audio/ogg") || (t += ".ogg"), "probably" != e.canPlayType("audio/mp4") && "maybe" != e.canPlayType("audio/mp4") || (t += ".webm"), (o = t.split(".")).shift(), e = null, o
            }
        }(), FWDMSP.hasCanvas = Boolean(document.createElement("canvas")), FWDMSP.formatTotalTime = function(e) {
            if ("string" == typeof e && -1 != e.indexOf(":")) return e;
            e /= 1e3;
            var t = Math.floor(e / 3600),
                o = e % 3600,
                s = Math.floor(o / 60),
                i = o % 60,
                n = Math.ceil(i);
            return s = 10 <= s ? s : "0" + s, n = 10 <= n ? n : "0" + n, isNaN(n) ? "00:00/00:00" : 0 < t ? t + ":" + s + ":" + n : s + ":" + n
        }, FWDMSP.getAudioFormats = function() {
            var e = document.createElement("audio");
            if (e.canPlayType) {
                var t = "",
                    o = [];
                return "probably" != e.canPlayType("audio/mpeg") && "maybe" != e.canPlayType("audio/mpeg") || (t += ".mp3"), "probably" != e.canPlayType("audio/ogg") && "maybe" != e.canPlayType("audio/ogg") || (t += ".ogg"), "probably" != e.canPlayType("audio/mp4") && "maybe" != e.canPlayType("audio/mp4") || (t += ".webm"), (o = t.split(".")).shift(), e = null, o
            }
        }(), FWDMSP.hasHTMLHLS = (f$ = document.createElement("video"), g$ = !1, f$.canPlayType && (g$ = Boolean("probably" === f$.canPlayType("application/vnd.apple.mpegurl") || "maybe" === f$.canPlayType("application/vnd.apple.mpegurl"))), g$), FWDMSP.instaces_ar = [], FWDMSP.CENTER = "center", FWDMSP.LEFT = "left", FWDMSP.RIGHT = "right", FWDMSP.YOUTUBE = "youtube", FWDMSP.VIDEO = "video", FWDMSP.AUDIO = "audio", FWDMSP.POPUP = "popup", FWDMSP.POSITION_TOP = "positionTop", FWDMSP.POSITION_BOTTOM = "positionBottom", FWDMSP.READY = "ready", FWDMSP.START = "start", FWDMSP.START_TO_LOAD_PLAYLIST = "startToLoadPlaylist", FWDMSP.LOAD_PLAYLIST_COMPLETE = "loadPlaylistComplete", FWDMSP.STOP = "stop", FWDMSP.PLAY = "play", FWDMSP.PAUSE = "pause", FWDMSP.UPDATE = "update", FWDMSP.UPDATE_TIME = "updateTime", FWDMSP.ERROR = "error", FWDMSP.PLAY_COMPLETE = "playComplete", FWDMSP.PLAYLIST_LOAD_COMPLETE = "onPlayListLoadComplete", FWDMSP.HLS = "hls_flash", window.FWDMSP = FWDMSP
    }(window),
    function(window) {
        var FWDMSPAudioData = function(props, playListElement, parent) {
            var self = this,
                prototype = FWDMSPAudioData.prototype;
            this.xhr = null, this.emailXHR = null, this.playlist_ar = null, this.dlIframe = null, this.mainPreloader_img = null, this.bk_img = null, this.thumbnail_img = null, this.separator1_img = null, this.separator2_img = null, this.prevN_img = null, this.playN_img = null, this.pauseN_img = null, this.nextN_img = null, this.popupN_img = null, this.downloaderN_img = null, this.toopTipBk_str = null, this.toopTipPointer_str = null, this.toopTipPointerUp_str = null, this.mainScrubberBkLeft_img = null, this.mainScrubberBkRight_img = null, this.mainScrubberDragLeft_img = null, this.mainScrubberLine_img = null, this.mainScrubberLeftProgress_img = null, this.volumeScrubberBkLeft_img = null, this.volumeScrubberBkRight_img = null, this.volumeScrubberDragLeft_img = null, this.volumeScrubberLine_img = null, this.volumeD_img = null, this.progressLeft_img = null, this.titleBarLeft_img = null, this.titleBarRigth_img = null, this.openerAnimation_img = null, this.openTopN_img = null, this.openTopS_img = null, this.openBottomN_img = null, this.openBottomS_img = null, this.closeN_img = null, this.closeS_img = null, this.openerPauseN_img = null, this.openerPauseS_img = null, this.openerPlayN_img = null, this.openerPlayS_img = null, this.categoriesN_img = null, this.replayN_img = null, this.playlistN_img = null, this.shuffleN_img = null, this.facebookN_img = null, this.titlebarAnimBkPath_img = null, this.titlebarLeftPath_img = null, this.titlebarRightPath_img = null, this.soundAnimationPath_img = null, this.controllerBk_img = null, this.playlistItemBk1_img = null, this.playlistItemBk2_img = null, this.playlistSeparator_img = null, this.playlistScrBkTop_img = null, this.playlistScrBkMiddle_img = null, this.playlistScrBkBottom_img = null, this.playlistScrDragTop_img = null, this.playlistScrDragMiddle_img = null, this.playlistScrDragBottom_img = null, this.playlistScrLines_img = null, this.playlistScrLinesOver_img = null, this.playlistPlayButtonN_img = null, this.playlistItemGrad1_img = null, this.playlistItemGrad2_img = null, this.playlistItemProgress1_img = null, this.playlistItemProgress2_img = null, this.playlistDownloadButtonN_img = null, this.playlistDownloadButtonS_img = null, this.catThumbBk_img = null, this.catThumbTextBk_img = null, this.catNextN_img = null, this.catNextS_img = null, this.catNextD_img = null, this.catPrevN_img = null, this.catPrevS_img = null, this.catPrevD_img = null, this.catCloseN_img = null, this.catCloseS_img = null, this.categories_el = null, this.scs_el = null, this.props_obj = props, this.skinPaths_ar = [], this.images_ar = [], this.cats_ar = [], this.scClientId_str = props.soundCloudAPIKey || "0aff03b3b79c2ac02fd2283b300735bd", this.flashPath_str = null, this.mp3DownloaderPath_str = null, this.proxyPath_str = null, this.proxyFolderPath_str = null, this.mailPath_str = null, this.skinPath_str = null, this.controllerBkPath_str = null, this.thumbnailBkPath_str = null, this.playlistIdOrPath_str = null, this.mainScrubberBkMiddlePath_str = null, this.volumeScrubberBkMiddlePath_str = null, this.mainScrubberDragMiddlePath_str = null, this.volumeScrubberDragMiddlePath_str = null, this.timeColor_str = null, this.titleColor_str = null, this.progressMiddlePath_str = null, this.sourceURL_str = null, this.titlebarBkMiddlePattern_str = null, this.playlistPlayButtonN_str = null, this.playlistPlayButtonS_str = null, this.playlistPauseButtonN_str = null, this.playlistPauseButtonS_str = null, this.trackTitleNormalColor_str = null, this.trackTitleSelected_str = null, this.trackDurationColor_str = null, this.categoriesId_str = null, this.thumbnailSelectedType_str = null, this.facebookAppId_str = null, this.openerAlignment_str = null, this.prevId = -1, this.totalCats = 0, this.countLoadedSkinImages = 0, this.volume = 1, this.startSpaceBetweenButtons = 0, this.spaceBetweenButtons = 0, this.mainScrubberOffsetTop = 0, this.spaceBetweenMainScrubberAndTime = 0, this.startTimeSpace = 0, this.scrubbersOffsetWidth = 0, this.scrubbersOffestTotalWidth = 0, this.volumeButtonAndScrubberOffsetTop = 0, this.maxPlaylistItems = 0, this.separatorOffsetOutSpace = 0, this.separatorOffsetInSpace = 0, this.lastButtonsOffsetTop = 0, this.allButtonsOffsetTopAndBottom = 0, this.controllerHeight = 0, this.titleBarOffsetTop = 0, this.scrubberOffsetBottom = 0, this.equlizerOffsetLeft = 0, this.nrOfVisiblePlaylistItems = 0, this.trackTitleOffsetLeft = 0, this.playPauseButtonOffsetLeftAndRight = 0, this.durationOffsetRight = 0, this.downloadButtonOffsetRight = 0, this.scrollbarOffestWidth = 0, this.resetLoadIndex = -1, this.startAtPlaylist = 0, this.startAtTrack = 0, this.totalCategories = 0, this.thumbnailMaxWidth = 0, this.buttonsMargins = 0, this.thumbnailMaxHeight = 0, this.horizontalSpaceBetweenThumbnails = 0, this.verticalSpaceBetweenThumbnails = 0, this.openerEqulizerOffsetLeft = 0, this.openerEqulizerOffsetTop = 0, this.countID3 = 0, this.JSONPRequestTimeoutId_to, this.showLoadPlaylistErrorId_to, this.dispatchPlaylistLoadCompleteWidthDelayId_to, this.loadImageId_to, this.loadPreloaderId_to, this.isPlaylistDispatchingError_bl = !1, this.allowToChangeVolume_bl = !0, this.showContextMenu_bl = !1, this.autoPlay_bl = !1, this.loop_bl = !1, this.shuffle_bl = !1, this.showLoopButton_bl = !1, this.showShuffleButton_bl = !1, this.showDownloadMp3Button_bl = !1, this.showPlaylistsButtonAndPlaylists_bl = !1, this.showPlaylistsByDefault_bl = !1, this.showPlayListButtonAndPlaylist_bl = !1, this.showFacebookButton_bl = !1, this.showPopupButton_bl = !1, this.animate_bl = !1, this.showControllerByDefault_bl = !1, this.showPlayListByDefault_bl = !1, this.isDataLoaded_bl = !1, this.useDeepLinking_bl = !1, this.showSoundCloudUserNameInTitle_bl = !1, this.showThumbnail_bl = !1, this.showSoundAnimation_bl = !1, this.expandControllerBackground_bl = !1, this.showPlaylistItemPlayButton_bl = !1, this.showPlaylistItemDownloadButton_bl = !1, this.forceDisableDownloadButtonForPodcast_bl = !1, this.forceDisableDownloadButtonForOfficialFM_bl = !1, this.forceDisableDownloadButtonForFolder_bl = !1, this.loadFromFolder_bl = !1, this.isMobile_bl = FWDMSPUtils.isMobile, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, self.init = function() {
                self.parseProperties()
            }, self.parseProperties = function() {
                if (this.useYoutube_bl = self.props_obj.useYoutube || "no", this.useYoutube_bl = "yes" == self.useYoutube_bl, this.addKeyboardSupport_bl = self.props_obj.addKeyboardSupport || "no", this.addKeyboardSupport_bl = "yes" == self.addKeyboardSupport_bl, this.useVideo_bl = self.props_obj.useVideo || "no", this.useVideo_bl = "yes" == self.useVideo_bl, self.useHEXColorsForSkin_bl = self.props_obj.useHEXColorsForSkin, self.useHEXColorsForSkin_bl = "yes" == self.useHEXColorsForSkin_bl, -1 != location.protocol.indexOf("file:") && (self.useHEXColorsForSkin_bl = !1), self.categoriesId_str = self.props_obj.playlistsId, self.categoriesId_str)
                    if (self.mainFolderPath_str = self.props_obj.mainFolderPath, self.mainFolderPath_str)
                        if (self.mainFolderPath_str.lastIndexOf("/") + 1 != self.mainFolderPath_str.length && (self.mainFolderPath_str += "/"), self.skinPath_str = self.props_obj.skinPath, self.skinPath_str)
                            if (self.skinPath_str.lastIndexOf("/") + 1 != self.skinPath_str.length && (self.skinPath_str += "/"), self.skinPath_str = self.mainFolderPath_str + self.skinPath_str, self.flashPath_str = self.mainFolderPath_str + "flashlsChromeless.swf", self.proxyPath_str = self.mainFolderPath_str + "proxy.php", self.proxyFolderPath_str = self.mainFolderPath_str + "proxyFolder.php", self.mailPath_str = self.mainFolderPath_str + "sendMail.php", self.mp3DownloaderPath_str = self.mainFolderPath_str + "downloader.php", self.hlsPath_str = self.mainFolderPath_str + "hls.js", self.categories_el = document.getElementById(self.categoriesId_str), self.categories_el) {
                                var e = FWDMSPUtils.getChildren(self.categories_el);
                                if (self.totalCats = e.length, self.categories_el = document.getElementById(self.categoriesId_str), 0 != self.totalCats) {
                                    for (var t = 0; t < self.totalCats; t++) {
                                        var o = {};
                                        if (child = e[t], !FWDMSPUtils.hasAttribute(child, "data-source")) return void setTimeout(function() {
                                            null != self && self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                                                text: "Attribute <font color='#FF0000'>data-source</font> is required in the categories html element at position <font color='#FF0000'>" + (t + 1)
                                            })
                                        }, 50);
                                        if (!FWDMSPUtils.hasAttribute(child, "data-thumbnail-path")) return void setTimeout(function() {
                                            null != self && self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                                                text: "Attribute <font color='#FF0000'>data-thumbnail-path</font> is required in the categories html element at position <font color='#FF0000'>" + (t + 1)
                                            })
                                        }, 50);
                                        o.playlistsName = FWDMSPUtils.getAttributeValue(child, "data-playlist-name"), o.source = FWDMSPUtils.getAttributeValue(child, "data-source"), o.thumbnailPath = FWDMSPUtils.getAttributeValue(child, "data-thumbnail-path"), o.htmlContent = child.innerHTML, o.htmlText_str = child.innerText, self.cats_ar[t] = o
                                    }
                                    self.playlistBackgroundColor_str = self.props_obj.playlistBackgroundColor || "transparent", self.searchInputColor_str = self.props_obj.searchInputColor || "#FF0000", self.facebookAppId_str = self.props_obj.facebookAppId || void 0, self.openerAlignment_str = self.props_obj.openerAlignment || "right", "right" != self.openerAlignment_str && "left" != self.openerAlignment_str && (self.openerAlignment_str = "right"), self.totalCategories = self.cats_ar.length, self.playlistIdOrPath_str = self.props_obj.playlistIdOrPath || void 0, self.timeColor_str = self.props_obj.timeColor || "#FF0000", self.playbackRateWindowTextColor_str = self.props_obj.playbackRateWindowTextColor || "#FF0000", self.showPlaylistsSearchInput_bl = self.props_obj.showPlaylistsSearchInput, self.showPlaylistsSearchInput_bl = "yes" == self.showPlaylistsSearchInput_bl, self.trackTitleNormalColor_str = self.props_obj.trackTitleNormalColor || "#FF0000", self.trackTitleSelected_str = self.props_obj.trackTitleSelectedColor || "#FF0000", self.trackDurationColor_str = self.props_obj.trackDurationColor || "#FF0000", self.titleColor_str = self.props_obj.titleColor || "#FF0000", self.thumbnailSelectedType_str = self.props_obj.thumbnailSelectedType || "opacity", "blackAndWhite" != self.thumbnailSelectedType_str && "threshold" != self.thumbnailSelectedType_str && "opacity" != self.thumbnailSelectedType_str && (self.thumbnailSelectedType_str = "opacity"), (self.isMobile_bl || FWDMSPUtils.isIEAndLessThen9) && (self.thumbnailSelectedType_str = "opacity"), "file:" == document.location.protocol && (self.thumbnailSelectedType_str = "opacity"), self.searchInputColor_str = self.props_obj.searchInputColor || "#FF0000", self.playlistBackgroundColor_str = self.props_obj.playlistBackgroundColor || "transparent", self.startAtPlaylist = self.props_obj.startAtPlaylist || 0, isNaN(self.startAtPlaylist) && (self.startAtPlaylist = 0), self.startAtPlaylist < 0 ? self.startAtPlaylist = 0 : self.startAtPlaylist > self.totalCats - 1 && (self.startAtPlaylist = self.totalCats - 1), self.startAtRandomTrack_bl = self.props_obj.startAtRandomTrack, self.startAtRandomTrack_bl = "no" != self.startAtRandomTrack_bl, self.startAtTrack = self.props_obj.startAtTrack || 0, self.volume = self.props_obj.volume, self.volume || (self.volume = 1), isNaN(self.volume) && (volume = 1), 1 < self.volume ? self.volume = 1 : self.volume < 0 && (self.volume = 0), self.searchBarHeight = self.props_obj.searchBarHeight || 50, self.buttonsMargins = self.props_obj.buttonsMargins || 0, self.thumbnailMaxWidth = self.props_obj.thumbnailMaxWidth || 330, self.thumbnailMaxHeight = self.props_obj.thumbnailMaxHeight || 330, self.horizontalSpaceBetweenThumbnails = self.props_obj.horizontalSpaceBetweenThumbnails, null == self.horizontalSpaceBetweenThumbnails && (self.horizontalSpaceBetweenThumbnails = 40), self.verticalSpaceBetweenThumbnails = parseInt(self.props_obj.verticalSpaceBetweenThumbnails), null == self.verticalSpaceBetweenThumbnails && (self.verticalSpaceBetweenThumbnails = 40), self.openerEqulizerOffsetLeft = self.props_obj.openerEqulizerOffsetLeft || 0, self.openerEqulizerOffsetTop = self.props_obj.openerEqulizerOffsetTop || 0, self.inputSearchTextOffsetTop = self.props_obj.inputSearchTextOffsetTop, self.inputSearchOffsetLeft = self.props_obj.inputSearchOffsetLeft, self.startSpaceBetweenButtons = self.props_obj.startSpaceBetweenButtons || 0, self.spaceBetweenButtons = self.props_obj.spaceBetweenButtons || 0, self.mainScrubberOffsetTop = self.props_obj.mainScrubberOffsetTop || 100, self.spaceBetweenMainScrubberAndTime = self.props_obj.spaceBetweenMainScrubberAndTime, self.startTimeSpace = self.props_obj.startTimeSpace, self.scrubbersOffsetWidth = self.props_obj.scrubbersOffsetWidth || 0, self.scrubbersOffestTotalWidth = self.props_obj.scrubbersOffestTotalWidth || 0, self.volumeButtonAndScrubberOffsetTop = self.props_obj.volumeButtonAndScrubberOffsetTop || 0, self.spaceBetweenVolumeButtonAndScrubber = self.props_obj.spaceBetweenVolumeButtonAndScrubber || 0, self.volumeScrubberOffestWidth = self.props_obj.volumeScrubberOffestWidth || 0, self.scrubberOffsetBottom = self.props_obj.scrubberOffsetBottom || 0, self.equlizerOffsetLeft = self.props_obj.equlizerOffsetLeft || 0, self.nrOfVisiblePlaylistItems = self.props_obj.nrOfVisiblePlaylistItems || 0, self.trackTitleOffsetLeft = self.props_obj.trackTitleOffsetLeft || 0, self.playPauseButtonOffsetLeftAndRight = self.props_obj.playPauseButtonOffsetLeftAndRight || 0, self.durationOffsetRight = self.props_obj.durationOffsetRight || 0, self.downloadButtonOffsetRight = self.props_obj.downloadButtonOffsetRight || 0, self.scrollbarOffestWidth = self.props_obj.scrollbarOffestWidth || 0, self.maxPlaylistItems = self.props_obj.maxPlaylistItems || 200, self.controllerHeight = self.props_obj.controllerHeight || 200, self.titleBarOffsetTop = self.props_obj.titleBarOffsetTop || 0, self.separatorOffsetInSpace = self.props_obj.separatorOffsetInSpace || 0, self.lastButtonsOffsetTop = self.props_obj.lastButtonsOffsetTop || 0, self.allButtonsOffsetTopAndBottom = self.props_obj.allButtonsOffsetTopAndBottom || 0, self.separatorOffsetOutSpace = self.props_obj.separatorOffsetOutSpace || 0, self.volumeScrubberWidth = self.props_obj.volumeScrubberWidth || 10, 200 < self.volumeScrubberWidth && (self.volumeScrubberWidth = 200), self.privateVideoPassword_str = self.props_obj.privatePassword, self.secondaryLabelsColor_str = self.props_obj.secondaryLabelsColor || "#FF0000", self.mainLabelsColor_str = self.props_obj.mainLabelsColor || "#FF0000", self.borderColor_str = self.props_obj.borderColor || "#FF0000", self.textColor_str = self.props_obj.textColor_str || "#FF0000", self.inputBackgroundColor_str = self.props_obj.inputBackgroundColor || "#FF0000", self.inputColor_str = self.props_obj.inputColor || "#FF0000", self.showContextMenu_bl = self.props_obj.showContextMenu, self.showContextMenu_bl = "no" != self.showContextMenu_bl, self.autoPlay_bl = self.props_obj.autoPlay, self.autoPlay_bl = "yes" == self.autoPlay_bl, self.loop_bl = self.props_obj.loop, self.loop_bl = "yes" == self.loop_bl, self.shuffle_bl = self.props_obj.shuffle, self.shuffle_bl = "yes" == self.shuffle_bl, self.useContinuousPlayback_bl = self.props_obj.useContinuousPlayback, self.useContinuousPlayback_bl = "yes" == self.useContinuousPlayback_bl, self.playVideoOnlyWhenLoggedIn_bl = self.props_obj.playTrackOnlyWhenLoggedIn, self.playVideoOnlyWhenLoggedIn_bl = "yes" == self.playVideoOnlyWhenLoggedIn_bl, self.isLoggedIn_bl = self.props_obj.isLoggedIn, self.isLoggedIn_bl = "yes" == self.isLoggedIn_bl, self.loggedInMessage_str = self.props_obj.loggedInMessage || "Only loggedin users can view this video", self.useDeepLinking_bl = self.props_obj.useDeepLinking, self.useDeepLinking_bl = "yes" == self.useDeepLinking_bl, self.showSoundCloudUserNameInTitle_bl = self.props_obj.showSoundCloudUserNameInTitle, self.showSoundCloudUserNameInTitle_bl = "yes" == self.showSoundCloudUserNameInTitle_bl, self.showThumbnail_bl = self.props_obj.showThumbnail, self.showThumbnail_bl = "yes" == self.showThumbnail_bl, self.showNextAndPrevButtons_bl = self.props_obj.showNextAndPrevButtons, self.showNextAndPrevButtons_bl = "yes" == self.showNextAndPrevButtons_bl, self.showLoopButton_bl = self.props_obj.showLoopButton, self.showLoopButton_bl = "no" != self.props_obj.showLoopButton, self.showPlayListButtonAndPlaylist_bl = self.props_obj.showPlayListButtonAndPlaylist, self.showPlayListButtonAndPlaylist_bl = "no" != self.showPlayListButtonAndPlaylist_bl, FWDMSPUtils.isAndroid && self.showPlayListButtonAndPlaylist_bl && "no" == self.props_obj.showPlayListOnAndroid && (self.showPlayListButtonAndPlaylist_bl = !1), self.rightClickContextMenu_str = self.props_obj.rightClickContextMenu || "developer", test = "developer" == self.rightClickContextMenu_str || "disabled" == self.rightClickContextMenu_str || "default" == self.rightClickContextMenu_str, test || (self.rightClickContextMenu_str = "developer"), self.showPlaylistsButtonAndPlaylists_bl = self.props_obj.showPlaylistsButtonAndPlaylists, self.showPlaylistsButtonAndPlaylists_bl = "no" != self.showPlaylistsButtonAndPlaylists_bl, self.showPlaylistsByDefault_bl = self.props_obj.showPlaylistsByDefault, self.showPlaylistsByDefault_bl = "yes" == self.showPlaylistsByDefault_bl, self.showShuffleButton_bl = self.props_obj.showShuffleButton, self.showShuffleButton_bl = "no" != self.showShuffleButton_bl, self.showShareWindowButton_bl = self.props_obj.showShareWindowButton, self.showShareWindowButton_bl = "no" != self.showShareWindowButton_bl, self.showDownloadMp3Button_bl = self.props_obj.showDownloadMp3Button, self.showDownloadMp3Button_bl = "no" != self.showDownloadMp3Button_bl, self.randomizePlaylist_bl = self.props_obj.randomizePlaylist, self.randomizePlaylist_bl = "yes" == self.randomizePlaylist_bl, self.showBuyButton_bl = self.props_obj.showBuyButton, self.showBuyButton_bl = "no" != self.showBuyButton_bl, self.showFacebookButton_bl = self.props_obj.showShareButton, self.showFacebookButton_bl = "no" != self.showFacebookButton_bl, self.showPopupButton_bl = self.props_obj.showPopupButton, self.showPopupButton_bl = "no" != self.showPopupButton_bl, self.showOpenerPlayPauseButton_bl = self.props_obj.showOpenerPlayPauseButton, self.showOpenerPlayPauseButton_bl = "no" != self.showOpenerPlayPauseButton_bl, self.showPlaylistItemBuyButton_bl = self.props_obj.showPlaylistItemBuyButton, self.showPlaylistItemBuyButton_bl = "no" != self.showPlaylistItemBuyButton_bl, self.normalButtonsColor_str = self.props_obj.normalHEXButtonsColor || "#FF0000", self.selectedButtonsColor_str = self.props_obj.selectedHEXButtonsColor || "#00FF00", self.showOpener_bl = self.props_obj.showOpener, self.showOpener_bl = "no" != self.showOpener_bl, self.showTracksNumbers_bl = self.props_obj.showTracksNumbers, self.showTracksNumbers_bl = "yes" == self.showTracksNumbers_bl, self.disableScrubber_bl = self.props_obj.disableScrubber, self.disableScrubber_bl = "yes" == self.disableScrubber_bl, self.showVideoFullScreenButton_bl = self.props_obj.showFullScreenButton, self.showVideoFullScreenButton_bl = "yes" == self.showVideoFullScreenButton_bl, self.showPlaybackRateButton_bl = self.props_obj.showPlaybackRateButton, self.showPlaybackRateButton_bl = "yes" == self.showPlaybackRateButton_bl, self.playTrackAfterPlaylistLoad_bl = self.props_obj.playTrackAfterPlaylistLoad, self.playTrackAfterPlaylistLoad_bl = "yes" == self.playTrackAfterPlaylistLoad_bl, self.atbTimeBackgroundColor = self.props_obj.atbTimeBackgroundColor || "transparent", self.atbTimeTextColorNormal = self.props_obj.atbTimeTextColorNormal || "#888888", self.atbTimeTextColorSelected = self.props_obj.atbTimeTextColorSelected || "#FFFFFF", self.atbButtonTextNormalColor = self.props_obj.atbButtonTextNormalColor || "#888888", self.atbButtonTextSelectedColor = self.props_obj.atbButtonTextSelectedColor || "#FFFFFF", self.atbButtonBackgroundNormalColor = self.props_obj.atbButtonBackgroundNormalColor || "#FFFFFF", self.atbButtonBackgroundSelectedColor = self.props_obj.atbButtonBackgroundSelectedColor || "#000000", self.defaultPlaybackRate = parseFloat(self.props_obj.defaultPlaybackRate.toFixed(1)) || 1, isNaN(self.defaultPlaybackRate) && (self.defaultPlaybackRate = 1), self.defaultPlaybackRate < .5 ? self.defaultPlaybackRate = .5 : 2 < self.defaultPlaybackRate && (self.defaultPlaybackRate = 2), self.animate_bl = self.props_obj.animate, self.animate_bl = "yes" == self.animate_bl, self.showControllerByDefault_bl = self.props_obj.showControllerByDefault, self.showControllerByDefault_bl = "no" != self.showControllerByDefault_bl, self.showPlayListByDefault_bl = self.props_obj.showPlayListByDefault, self.showPlayListByDefault_bl = "no" != self.showPlayListByDefault_bl, self.showSoundAnimation_bl = self.props_obj.showSoundAnimation, self.showSoundAnimation_bl = "yes" == self.showSoundAnimation_bl, self.showShareButton_bl = self.props_obj.showShareButton, self.showShareButton_bl = "yes" == self.showShareButton_bl, self.expandControllerBackground_bl = self.props_obj.expandBackground, self.expandControllerBackground_bl = "yes" == self.expandControllerBackground_bl, self.showPlaylistItemPlayButton_bl = self.props_obj.showPlaylistItemPlayButton, self.showPlaylistItemPlayButton_bl = "no" != self.showPlaylistItemPlayButton_bl, self.showPlaylistItemDownloadButton_bl = self.props_obj.showPlaylistItemDownloadButton, self.showPlaylistItemDownloadButton_bl = "no" != self.showPlaylistItemDownloadButton_bl, self.forceDisableDownloadButtonForPodcast_bl = self.props_obj.forceDisableDownloadButtonForPodcast, self.forceDisableDownloadButtonForPodcast_bl = "yes" == self.forceDisableDownloadButtonForPodcast_bl, self.forceDisableDownloadButtonForOfficialFM_bl = self.props_obj.forceDisableDownloadButtonForOfficialFM, self.forceDisableDownloadButtonForOfficialFM_bl = "yes" == self.forceDisableDownloadButtonForOfficialFM_bl, self.forceDisableDownloadButtonForFolder_bl = self.props_obj.forceDisableDownloadButtonForFolder, self.forceDisableDownloadButtonForFolder_bl = "yes" == self.forceDisableDownloadButtonForFolder_bl, self.addScrollBarMouseWheelSupport_bl = self.props_obj.addScrollBarMouseWheelSupport, self.addScrollBarMouseWheelSupport_bl = "no" != self.addScrollBarMouseWheelSupport_bl, self.usePlaylistsSelectBox_bl = self.props_obj.usePlaylistsSelectBox, self.usePlaylistsSelectBox_bl = "yes" == self.usePlaylistsSelectBox_bl, self.showPlaylistsSelectBoxNumbers_bl = self.props_obj.showPlaylistsSelectBoxNumbers, self.showPlaylistsSelectBoxNumbers_bl = "yes" == self.showPlaylistsSelectBoxNumbers_bl, self.mainSelectorBackgroundSelectedColor = self.props_obj.mainSelectorBackgroundSelectedColor || "#FFFFFF", self.mainSelectorTextNormalColor = self.props_obj.mainSelectorTextNormalColor || "#FFFFFF", self.mainSelectorTextSelectedColor = self.props_obj.mainSelectorTextSelectedColor || "#000000", self.mainButtonBackgroundNormalColor = self.props_obj.mainButtonBackgroundNormalColor || "#212021", self.mainButtonBackgroundSelectedColor = self.props_obj.mainButtonBackgroundSelectedColor || "#FFFFFF", self.mainButtonTextNormalColor = self.props_obj.mainButtonTextNormalColor || "#FFFFFF", self.mainButtonTextSelectedColor = self.props_obj.mainButtonTextSelectedColor || "#000000", self.showSearchBar_bl = self.props_obj.showSearchBar, self.showSearchBar_bl = "no" != self.showSearchBar_bl, self.showSortButtons_bl = self.props_obj.showSortButtons, self.showSortButtons_bl = "no" != self.showSortButtons_bl, self.preloaderPath_str = self.skinPath_str + "preloader.png", self.animationPath_str = self.skinPath_str + "equalizer.png", self.arrowN_str = self.skinPath_str + "combobox-arrow-normal.png", self.arrowS_str = self.skinPath_str + "combobox-arrow-selected.png", self.comboboxBk1_str = self.skinPath_str + "combobox-item-background1.png", self.comboboxBk2_str = self.skinPath_str + "combobox-item-background2.png", self.mainPreloader_img = new Image, self.mainPreloader_img.onerror = self.onSkinLoadErrorHandler, self.mainPreloader_img.onload = self.onPreloaderLoadHandler, self.mainPreloader_img.src = self.skinPath_str + "preloader.png", self.shareBkPath_str = self.skinPath_str + "categories-background.png", self.skinPaths_ar = [{
                                        img: self.controllerBk_img = new Image,
                                        src: self.skinPath_str + "controller-background.png"
                                    }, {
                                        img: self.separator1_img = new Image,
                                        src: self.skinPath_str + "separator.png"
                                    }, {
                                        img: self.separator2_img = new Image,
                                        src: self.skinPath_str + "separator.png"
                                    }, {
                                        img: self.prevN_img = new Image,
                                        src: self.skinPath_str + "prev-button.png"
                                    }, {
                                        img: self.playN_img = new Image,
                                        src: self.skinPath_str + "play-button.png"
                                    }, {
                                        img: self.pauseN_img = new Image,
                                        src: self.skinPath_str + "pause-button.png"
                                    }, {
                                        img: self.nextN_img = new Image,
                                        src: self.skinPath_str + "next-button.png"
                                    }, {
                                        img: self.popupN_img = new Image,
                                        src: self.skinPath_str + "popup-button.png"
                                    }, {
                                        img: self.downloaderN_img = new Image,
                                        src: self.skinPath_str + "download-button.png"
                                    }, {
                                        img: self.buyN_img = new Image,
                                        src: self.skinPath_str + "buy-button.png"
                                    }, {
                                        img: self.mainScrubberBkLeft_img = new Image,
                                        src: self.skinPath_str + "scrubber-left-background.png"
                                    }, {
                                        img: self.mainScrubberBkRight_img = new Image,
                                        src: self.skinPath_str + "scrubber-right-background.png"
                                    }, {
                                        img: self.mainScrubberDragLeft_img = new Image,
                                        src: self.skinPath_str + "scrubber-left-drag.png"
                                    }, {
                                        img: self.volumeScrubberDragLeft_img = new Image,
                                        src: self.skinPath_str + "scrubber-left-drag.png"
                                    }, {
                                        img: self.mainScrubberLine_img = new Image,
                                        src: self.skinPath_str + "scrubber-line.png"
                                    }, {
                                        img: self.mainScrubberLeftProgress_img = new Image,
                                        src: self.skinPath_str + "progress-left.png"
                                    }, {
                                        img: self.volumeN_img = new Image,
                                        src: self.skinPath_str + "volume-icon.png"
                                    }, {
                                        img: self.categoriesN_img = new Image,
                                        src: self.skinPath_str + "categories-button.png"
                                    }, {
                                        img: self.openTopN_img = new Image,
                                        src: self.skinPath_str + "open-button-normal-top.png"
                                    }, {
                                        img: self.openBottomN_img = new Image,
                                        src: self.skinPath_str + "open-button-normal-bottom.png"
                                    }, {
                                        img: self.closeN_img = new Image,
                                        src: self.skinPath_str + "close-button-normal.png"
                                    }, {
                                        img: self.openerPauseN_img = new Image,
                                        src: self.skinPath_str + "open-pause-button-normal.png"
                                    }, {
                                        img: self.openerPlayN_img = new Image,
                                        src: self.skinPath_str + "open-play-button-normal.png"
                                    }, {
                                        img: self.replayN_img = new Image,
                                        src: self.skinPath_str + "replay-button.png"
                                    }, {
                                        img: self.playlistN_img = new Image,
                                        src: self.skinPath_str + "playlist-button.png"
                                    }, {
                                        img: self.shuffleN_img = new Image,
                                        src: self.skinPath_str + "shuffle-button.png"
                                    }, {
                                        img: self.shareN_img = new Image,
                                        src: self.skinPath_str + "share.png"
                                    }, {
                                        img: self.titlebarAnimBkPath_img = new Image,
                                        src: self.skinPath_str + "titlebar-equlizer-background.png"
                                    }, {
                                        img: self.titlebarLeftPath_img = new Image,
                                        src: self.skinPath_str + "titlebar-grad-left.png"
                                    }, {
                                        img: self.playbackRateNormal_img = new Image,
                                        src: self.skinPath_str + "playback-rate-normal.png"
                                    }, {
                                        img: self.soundAnimationPath_img = new Image,
                                        src: self.skinPath_str + "equalizer.png"
                                    }, {
                                        img: self.passColoseN_img = new Image,
                                        src: self.skinPath_str + "embed-close-button.png"
                                    }, {
                                        img: self.titleBarLeft_img = new Image,
                                        src: self.skinPath_str + "titlebar-left-pattern.png"
                                    }, {
                                        img: self.titleBarRigth_img = new Image,
                                        src: self.skinPath_str + "titlebar-right-pattern.png"
                                    }, {
                                        img: self.atbNPath_img = new Image,
                                        src: self.skinPath_str + "a-to-b-button.png"
                                    }], self.skinPaths_ar.push({
                                        img: self.fullScreenN_img = new Image,
                                        src: self.skinPath_str + "full-screen.png"
                                    }, {
                                        img: self.normalScreenN_img = new Image,
                                        src: self.skinPath_str + "normal-screen.png"
                                    }, {
                                        img: self.largePlayN_img = new Image,
                                        src: self.skinPath_str + "large-play.png"
                                    }), self.largePlayS_str = self.skinPath_str + "large-play-over.png", self.fullScreenS_str = self.skinPath_str + "full-screen-over.png", self.normalScreenS_str = self.skinPath_str + "normal-screen-over.png", self.atbSPath_str = self.skinPath_str + "a-to-b-button-over.png", self.playbackRateSelectedPath_str = self.skinPath_str + "playback-rate-selected.png", self.prevSPath_str = self.skinPath_str + "prev-button-over.png", self.playSPath_str = self.skinPath_str + "play-button-over.png", self.pauseSPath_str = self.skinPath_str + "pause-button-over.png", self.nextSPath_str = self.skinPath_str + "next-button-over.png", self.popupSPath_str = self.skinPath_str + "popup-button-over.png", self.downloaderSPath_str = self.skinPath_str + "download-button-over.png", self.controllerBkPath_str = self.skinPath_str + "controller-background.png", self.thumbnailBkPath_str = self.skinPath_str + "thumbnail-background.png", self.mainScrubberBkMiddlePath_str = self.skinPath_str + "scrubber-middle-background.png", self.mainScrubberDragMiddlePath_str = self.skinPath_str + "scrubber-middle-drag.png", self.volumeScrubberBkMiddlePath_str = self.skinPath_str + "scrubber-middle-background.png", self.volumeScrubberDragMiddlePath_str = self.skinPath_str + "scrubber-middle-drag.png", self.volumeSPath_str = self.skinPath_str + "volume-icon-over.png", self.volumeDPath_str = self.skinPath_str + "volume-icon-disabled.png", self.openerAnimationPath_str = self.skinPath_str + "equalizer.png", self.openTopSPath_str = self.skinPath_str + "open-button-selected-top.png", self.openBottomSPath_str = self.skinPath_str + "open-button-selected-bottom.png", self.closeSPath_str = self.skinPath_str + "close-button-selected.png", self.openerPauseS_str = self.skinPath_str + "open-pause-button-selected.png", self.openerPlayS_str = self.skinPath_str + "open-play-button-selected.png", self.progressMiddlePath_str = self.skinPath_str + "progress-middle.png", self.buySPath_str = self.skinPath_str + "buy-button-over.png", self.showPlayListButtonAndPlaylist_bl && (self.skinPaths_ar.push({
                                        img: self.playlistItemBk1_img = new Image,
                                        src: self.skinPath_str + "playlist-item-background1.png"
                                    }, {
                                        img: self.playlistItemBk2_img = new Image,
                                        src: self.skinPath_str + "playlist-item-background2.png"
                                    }, {
                                        img: self.playlistSeparator_img = new Image,
                                        src: self.skinPath_str + "playlist-separator.png"
                                    }, {
                                        img: self.playlistScrBkTop_img = new Image,
                                        src: self.skinPath_str + "playlist-scrollbar-background-top.png"
                                    }, {
                                        img: self.playlistScrDragTop_img = new Image,
                                        src: self.skinPath_str + "playlist-scrollbar-drag-bottom.png"
                                    }, {
                                        img: self.playlistScrLines_img = new Image,
                                        src: self.skinPath_str + "playlist-scrollbar-lines.png"
                                    }, {
                                        img: self.playlistPlayButtonN_img = new Image,
                                        src: self.skinPath_str + "playlist-play-button.png"
                                    }, {
                                        img: self.playlistItemGrad1_img = new Image,
                                        src: self.skinPath_str + "playlist-item-grad1.png"
                                    }, {
                                        img: self.playlistItemGrad2_img = new Image,
                                        src: self.skinPath_str + "playlist-item-grad2.png"
                                    }, {
                                        img: self.playlistItemProgress1_img = new Image,
                                        src: self.skinPath_str + "playlist-item-progress1.png"
                                    }, {
                                        img: self.playlistItemProgress2_img = new Image,
                                        src: self.skinPath_str + "playlist-item-progress2.png"
                                    }, {
                                        img: self.playlistDownloadButtonN_img = new Image,
                                        src: self.skinPath_str + "playlist-download-button.png"
                                    }, {
                                        img: self.playlistBuyButtonN_img = new Image,
                                        src: self.skinPath_str + "playlist-buy-button.png"
                                    }), self.playlistDownloadButtonS_str = self.skinPath_str + "playlist-download-button-over.png", self.scrBkMiddlePath_str = self.skinPath_str + "playlist-scrollbar-background-middle.png", self.scrBkBottomPath_str = self.skinPath_str + "playlist-scrollbar-background-bottom.png", self.scrDragMiddlePath_str = self.skinPath_str + "playlist-scrollbar-drag-middle.png", self.scrDragBottomPath_str = self.skinPath_str + "playlist-scrollbar-drag-top.png", self.scrLinesSPath_str = self.skinPath_str + "playlist-scrollbar-lines-over.png", self.playlistBuyButtonS_str = self.skinPath_str + "playlist-buy-button-over.png", self.playlistPlayButtonN_str = self.skinPath_str + "playlist-play-button.png", self.playlistPlayButtonS_str = self.skinPath_str + "playlist-play-button-over.png", self.playlistPauseButtonN_str = self.skinPath_str + "playlist-pause-button.png", self.playlistPauseButtonS_str = self.skinPath_str + "playlist-pause-button-over.png"), self.showPlaylistsButtonAndPlaylists_bl && (self.skinPaths_ar.push({
                                        img: self.catNextN_img = new Image,
                                        src: self.skinPath_str + "categories-next-button.png"
                                    }, {
                                        img: self.catPrevN_img = new Image,
                                        src: self.skinPath_str + "categories-prev-button.png"
                                    }, {
                                        img: self.catCloseN_img = new Image,
                                        src: self.skinPath_str + "categories-close-button.png"
                                    }, {
                                        img: new Image,
                                        src: self.skinPath_str + "categories-background.png"
                                    }), self.catBkPath_str = self.skinPath_str + "categories-background.png", self.catThumbBkPath_str = self.skinPath_str + "categories-thumbnail-background.png", self.catThumbBkTextPath_str = self.skinPath_str + "categories-thumbnail-text-backgorund.png", self.catNextSPath_str = self.skinPath_str + "categories-next-button-over.png", self.catNextDPath_str = self.skinPath_str + "categories-next-button-disabled.png", self.catPrevSPath_str = self.skinPath_str + "categories-prev-button-over.png", self.catPrevDPath_str = self.skinPath_str + "categories-prev-button-disabled.png", self.catCloseSPath_str = self.skinPath_str + "categories-close-button-over.png"), self.showSearchBar_bl && (self.skinPaths_ar.push({
                                        img: self.sortAN_img = new Image,
                                        src: self.skinPath_str + "sort-alphabetical-button.png"
                                    }, {
                                        img: self.sortNN_img = new Image,
                                        src: self.skinPath_str + "sort-numerical-button.png"
                                    }, {
                                        img: self.ascendingN_img = new Image,
                                        src: self.skinPath_str + "ascending-button.png"
                                    }, {
                                        img: self.decendingN_img = new Image,
                                        src: self.skinPath_str + "descending-button.png"
                                    }), self.sortASPath_str = self.skinPath_str + "sort-alphabetical-button-over.png", self.sortNSPath_str = self.skinPath_str + "sort-numerical-button-over.png", self.ascendingSpath_str = self.skinPath_str + "ascending-button-over.png", self.decendingSpath_str = self.skinPath_str + "descending-button-over.png", self.inputArrowPath_str = self.skinPath_str + "input-arrow.png"), self.categoriesSPath_str = self.skinPath_str + "categories-button-over.png", self.replaySPath_str = self.skinPath_str + "replay-button-over.png";
                                    self.skinPath_str;
                                    self.playlistSPath_str = self.skinPath_str + "playlist-button-over.png", self.shuffleSPath_str = self.skinPath_str + "shuffle-button-over.png", self.shareSPath_str = self.skinPath_str + "share-over.png", self.animationPath_str = self.skinPath_str + "equalizer.png", self.titlebarBkMiddlePattern_str = self.skinPath_str + "titlebar-middle-pattern.png", self.passButtonNPath_str = self.skinPath_str + "pass-button.png", self.passButtonSPath_str = self.skinPath_str + "pass-button-over.png", self.showShareButton_bl && (self.skinPaths_ar.push({
                                        img: self.shareClooseN_img = new Image,
                                        src: self.skinPath_str + "embed-close-button.png"
                                    }, {
                                        img: self.facebookN_img = new Image,
                                        src: self.skinPath_str + "facebook-button.png"
                                    }, {
                                        img: self.googleN_img = new Image,
                                        src: self.skinPath_str + "google-plus.png"
                                    }, {
                                        img: self.twitterN_img = new Image,
                                        src: self.skinPath_str + "twitter.png"
                                    }, {
                                        img: self.likedInkN_img = new Image,
                                        src: self.skinPath_str + "likedin.png"
                                    }, {
                                        img: self.bufferkN_img = new Image,
                                        src: self.skinPath_str + "buffer.png"
                                    }, {
                                        img: self.diggN_img = new Image,
                                        src: self.skinPath_str + "digg.png"
                                    }, {
                                        img: self.redditN_img = new Image,
                                        src: self.skinPath_str + "reddit.png"
                                    }, {
                                        img: self.thumbrlN_img = new Image,
                                        src: self.skinPath_str + "thumbrl.png"
                                    }), self.facebookSPath_str = self.skinPath_str + "facebook-button-over.png", self.googleSPath_str = self.skinPath_str + "google-plus-over.png", self.twitterSPath_str = self.skinPath_str + "twitter-over.png", self.likedInSPath_str = self.skinPath_str + "likedin-over.png", self.bufferSPath_str = self.skinPath_str + "buffer-over.png", self.diggSPath_str = self.skinPath_str + "digg-over.png", self.redditSPath_str = self.skinPath_str + "reddit-over.png", self.thumbrlSPath_str = self.skinPath_str + "thumbrl-over.png"), self.embedWindowClosePathS_str = self.skinPath_str + "embed-close-button-over.png", self.showPlaybackRateButton_bl && (self.skinPaths_ar.push({
                                        img: self.playbackRateWindowClooseN_img = new Image,
                                        src: self.skinPath_str + "embed-close-button.png"
                                    }, {
                                        img: self.closeClooseN_img = new Image,
                                        src: self.skinPath_str + "embed-close-button.png"
                                    }), self.playbackRateClosePathS_str = self.skinPath_str + "embed-close-button-over.png"), self.totalGraphics = self.skinPaths_ar.length, self.loadSkin()
                                } else setTimeout(function() {
                                    null != self && (errorMessage_str = "At least one category is required!", self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                                        text: errorMessage_str
                                    }))
                                }, 50)
                            } else setTimeout(function() {
                                null != self && (errorMessage_str = "The html element with id <font color='#FF0000'>" + self.categoriesId_str + "</font> is not found in the DOM, this html element represents the player categories.!", self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                                    text: errorMessage_str
                                }))
                            }, 50);
                else setTimeout(function() {
                    null != self && (errorMessage_str = "The <font color='#FF0000'>skinPath</font> property is not defined in the constructor function!", self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: errorMessage_str
                    }))
                }, 50);
                else setTimeout(function() {
                    null != self && (errorMessage_str = "The <font color='#FF0000'>mainFolderPath</font> property is not defined in the constructor function!", self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: errorMessage_str
                    }))
                }, 50);
                else setTimeout(function() {
                    null != self && (errorMessage_str = "The <font color='#FF0000'>playlistsId</font> property is not defined in the constructor function!", self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: errorMessage_str
                    }))
                }, 50)
            }, this.onPreloaderLoadHandler = function() {
                setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.PRELOADER_LOAD_DONE)
                }, 50)
            }, self.loadSkin = function() {
                for (var e, t, o = 0; o < self.totalGraphics; o++) e = self.skinPaths_ar[o].img, t = self.skinPaths_ar[o].src, e.onload = self.onSkinLoadHandler, e.onerror = self.onSkinLoadErrorHandler, e.src = t
            }, this.onSkinLoadHandler = function(e) {
                self.countLoadedSkinImages++, self.countLoadedSkinImages == self.totalGraphics && setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.SKIN_LOAD_COMPLETE)
                }, 50)
            }, self.onSkinLoadErrorHandler = function(e) {
                message = FWDMSPUtils.isIEAndLessThen9 ? "Graphics image not found!" : "The skin icon with label <font color='#FF0000'>" + e.target.src + "</font> can't be loaded, check path!", window.console && console.log(e);
                var t = {
                    text: message
                };
                setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, t)
                }, 50)
            }, self.showPropertyError = function(e) {
                self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                    text: "The property called <font color='#FF0000'>" + e + "</font> is not defined."
                })
            }, this.downloadMp3 = function(e, t) {
                if ("file:" == document.location.protocol) return self.isPlaylistDispatchingError_bl = !0, void(showLoadPlaylistErrorId_to = setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: "Downloading mp3 files local is not allowed or possible!. To function properly please test online."
                    }), self.isPlaylistDispatchingError_bl = !1
                }, 50));
                var o = location.origin,
                    s = location.pathname;
                if (-1 != s.indexOf(".") && (s = s.substr(0, s.lastIndexOf("/") + 1)), -1 == e.indexOf("http:") && -1 == e.indexOf("https:") && (e = o + s + e), t) {
                    t = t.replace(/[^A-Z0-9\-\_\.]+/gi, "_"), /\.(mp3)$/i.test(t) || (t += ".mp3"), e = e;
                    var i = self.mp3DownloaderPath_str;
                    if (self.dlIframe || (self.dlIframe = document.createElement("IFRAME"), self.dlIframe.style.display = "none", document.documentElement.appendChild(self.dlIframe)), self.isMobile_bl && FWDMSPUtils.isIOS) {
                        var n = self.getValidEmail();
                        if (!n) return;
                        if (null != self.emailXHR) {
                            try {
                                self.emailXHR.abort()
                            } catch (e) {}
                            self.emailXHR.onreadystatechange = null, self.emailXHR.onerror = null, self.emailXHR = null
                        }
                        return self.emailXHR = new XMLHttpRequest, self.emailXHR.onreadystatechange = function(e) {
                            4 == self.emailXHR.readyState && (200 == self.emailXHR.status ? "sent" == self.emailXHR.responseText ? alert("Email sent.") : alert("Error sending email, this is a server side error, the php file can't send the email!") : alert("Error sending email: " + self.emailXHR.status + ": " + self.emailXHR.statusText))
                        }, self.emailXHR.onerror = function(e) {
                            try {
                                window.console && console.log(e), window.console && console.log(e.message)
                            } catch (e) {}
                            alert("Error sending email: " + e.message)
                        }, self.emailXHR.open("get", self.mailPath_str + "?mail=" + n + "&name=" + t + "&path=" + e, !0), void self.emailXHR.send()
                    } - 1 != e.indexOf("soundcloud.com") ? self.dlIframe.src = e : self.dlIframe.src = i + "?path=" + e + "&name=" + t
                }
            }, this.getValidEmail = function() {
                for (var e = prompt("Please enter your email address where the mp3 download link will be sent:"), t = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/; !t.test(e) || "" == e;) {
                    if (null === e) return;
                    e = prompt("Please enter a valid email address:")
                }
                return e
            }, this.loadPlaylist = function(e) {
                if (!self.isPlaylistDispatchingError_bl) {
                    clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to);
                    var t = self.cats_ar[e].source;
                    if (!t) return self.isPlaylistDispatchingError_bl = !0, void(showLoadPlaylistErrorId_to = setTimeout(function() {
                        self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                            text: "<font color='#FF0000'>loadPlaylist()</font> - Please specify an html elementid, podcast link, soudcloud link or xml path"
                        }), self.isPlaylistDispatchingError_bl = !1
                    }, 50));
                    if (!isNaN(t)) return self.isPlaylistDispatchingError_bl = !0, void(showLoadPlaylistErrorId_to = setTimeout(function() {
                        self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                            text: "<font color='#FF0000'>loadPlaylist()</font> - The parameter must be of type string!"
                        }), self.isPlaylistDispatchingError_bl = !1
                    }, 50));
                    self.closeData(), self.resetYoutubePlaylistLoader(), self.isYoutbe_bl = !1, -1 != t.indexOf("soundcloud.com") ? self.loadSoundCloudList(t) : -1 != t.indexOf("list=") && self.useYoutube_bl ? (self.isYoutbe_bl = !0, self.loadYoutubePlaylist(t)) : -1 != t.indexOf("official.fm") ? self.loadOfficialFmList(t) : -1 != t.indexOf("folder:") ? self.loadFolderPlaylist(t) : -1 != t.indexOf(".xml") || -1 != t.indexOf("http:") || -1 != t.indexOf("https:") || -1 != t.indexOf("www.") || -1 != t.indexOf(".pls") ? self.loadXMLPlaylist(t) : self.parseDOMPlaylist(t), self.prevId = e
                }
            }, this.loadYoutubePlaylist = function(e) {
                if (!self.isPlaylistDispatchingError_bl || self.isYoutbe_bl) {
                    self.youtubeUrl_str || (e = e.substr(e.indexOf("=") + 1), self.youtubeUrl_str = e), self.loadFromFolder_bl = !0, self.nextPageToken_str ? self.sourceURL_str = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken=" + self.nextPageToken_str + "&playlistId=" + self.youtubeUrl_str + "&key=AIzaSyAlyhJ-C5POyo4hofPh3b7ECAxWy6t6lyg&maxResults=50&callback=" + parent.instanceName_str + ".data.parseYoutubePlaylist" : self.sourceURL_str = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=" + self.youtubeUrl_str + "&key=AIzaSyAlyhJ-C5POyo4hofPh3b7ECAxWy6t6lyg&maxResults=50&callback=" + parent.instanceName_str + ".data.parseYoutubePlaylist";
                    try {
                        self.scs_el = document.createElement("script"), self.scs_el.src = self.sourceURL_str, document.documentElement.appendChild(self.scs_el)
                    } catch (e) {}
                }
            }, this.JSONPYotuubeRequestTimeoutError = function() {
                self.closeData(), self.isPlaylistDispatchingError_bl = !0, showLoadPlaylistErrorId_to = setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: "Error loading youtube playlist!<font color='#ff0000'>" + self.youtubeUrl_str + "</font>"
                    }), self.isPlaylistDispatchingError_bl = !1
                }, 50)
            }, this.resetYoutubePlaylistLoader = function() {
                self.isYoutbe_bl = !1, self.youtubeObject_ar = null, self.nextPageToken_str = null, self.youtubeUrl_str = null
            }, this.parseYoutubePlaylist = function(e) {
                if (!self.isPlaylistDispatchingError_bl && self.isYoutbe_bl) {
                    if (e.error) return self.JSONPRequestTimeoutError(), void(console && console.dir(e));
                    var t, o;
                    self.playlist_ar = [], self.youtubeObject_ar || (self.youtubeObject_ar = []);
                    for (var s = 0; s < e.items.length; s++) self.youtubeObject_ar.push(e.items[s]);
                    if (t = self.youtubeObject_ar.length, self.closeData(), e.nextPageToken && t < self.maxPlaylistItems) return self.nextPageToken_str = e.nextPageToken, void self.loadYoutubePlaylist();
                    for (s = 0; s < t && !(s > self.maxPlaylistItems - 1); s++) {
                        var i = {};
                        o = self.youtubeObject_ar[s], i.source = o.snippet.resourceId.videoId, i.buy = void 0;
                        var n = "";
                        self.showTracksNumbers_bl ? (s < 9 && (n = "0"), n = n + (s + 1) + ". ", i.title = n + "<span style='font-weight:bold;'>" + o.snippet.title + "</span>") : i.title = "<span style='font-weight:bold;'>" + o.snippet.title + "</span>", i.titleText = o.snippet.title, i.downloadable = !1;
                        try {
                            i.thumbPath = o.snippet.thumbnails.default.url
                        } catch (e) {}
                        i.posterSource = "none", -1 == o.snippet.title.indexOf("eleted video") && -1 == o.snippet.title.indexOf("his video is unavailable") && self.playlist_ar.push(i)
                    }
                    clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to), self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                        self.dispatchEvent(FWDMSPAudioData.PLAYLIST_LOAD_COMPLETE)
                    }, 50), self.isDataLoaded_bl = !0
                }
            }, this.loadSoundCloudList = function(e) {
                if (!self.isPlaylistDispatchingError_bl) {
                    self.closeXHR(), self.sourceURL_str = e, -1 != self.sourceURL_str.indexOf("likes") && (self.sourceURL_str = self.sourceURL_str.replace(/\/likes$/, "/favorites")), e = -1 == self.sourceURL_str.indexOf("api.soundcloud.") ? "https://api.soundcloud.com/resolve?format=json&url=" + self.sourceURL_str + "&limit=100&client_id=" + self.scClientId_str : self.sourceURL_str + "?format=json&client_id=" + self.scClientId_str + "&limit=100", self.loadFromFolder_bl = !1, self.sourceURL_str = e, self.xhr = new XMLHttpRequest, self.xhr.onreadystatechange = self.ajaxOnLoadHandler, self.xhr.onerror = self.ajaxOnErrorHandler;
                    try {
                        self.xhr.open("GET", self.sourceURL_str, !0), self.xhr.send()
                    } catch (e) {
                        var t = e;
                        e && e.message && (t = e.message), self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                            text: "Soundclud playlist can't be loaded! <font color='#FF0000'>" + self.sourceURL_str + "</font>. " + t
                        })
                    }
                }
            }, this.JSONPSoundcloudRequestTimeoutError = function() {
                self.isPlaylistDispatchingError_bl = !0, showLoadPlaylistErrorId_to = setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: "Error loading soundcloud url!<font color='#FF0000'>" + self.sourceURL_str + "</font>"
                    }), self.isPlaylistDispatchingError_bl = !1
                }, 50)
            }, this.getSoundcloudUrl = function(e) {
                if (!self.isPlaylistDispatchingError_bl) {
                    try {
                        self.closeJsonPLoader()
                    } catch (e) {}
                    self.sourceURL_str = e, -1 != self.sourceURL_str.indexOf("likes") && (self.sourceURL_str = self.sourceURL_str.replace(/\/likes$/, "/favorites")), e = "https://api.soundcloud.com/resolve?format=json&url=" + self.sourceURL_str + "&limit=100&client_id=" + self.scClientId_str, self.isSCTrack = !0, self.loadFromFolder_bl = !1, self.sourceURL_str = e, self.xhr = new XMLHttpRequest, self.xhr.onreadystatechange = self.ajaxOnLoadHandler, self.xhr.onerror = self.ajaxOnErrorHandler;
                    try {
                        self.xhr.open("GET", self.sourceURL_str, !0), self.xhr.send()
                    } catch (e) {
                        var t = e;
                        e && e.message && (t = e.message), self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                            text: "Soundclud track can't be loaded! <font color='#FF0000'>" + self.sourceURL_str + "</font>. " + t
                        })
                    }
                }
            }, this.parseSoundCloudURL = function(e) {
                var t;
                self.closeJsonPLoader(), e.stream_url ? (t = e.stream_url + "?consumer_key=" + self.scClientId_str, self.dispatchEvent(FWDMSPAudioData.SOUNDCLOUD_TRACK_READY, {
                    source: t
                })) : self.loadSoundcloudTrackError()
            }, this.loadSoundcloudTrackError = function() {
                self.closeJsonPLoader(), self.isPlaylistDispatchingError_bl = !0, showLoadPlaylistErrorId_to = setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: "Error loading soundcloud track url!<font color='#FF0000'>" + self.sourceURL_str + "</font>"
                    }), self.isPlaylistDispatchingError_bl = !1
                }, 50)
            }, this.loadOfficialFmList = function(e) {
                if (!self.isPlaylistDispatchingError_bl) {
                    self.closeXHR();
                    e = "http://api.official.fm/playlists/" + (self.sourceURL_str = e).substr(e.indexOf("/") + 1) + "/tracks?format=jsonp&fields=streaming&api_version=2&callback=" + parent.instanceName_str + ".data.parseOfficialFM";
                    if (null == self.scs_el) try {
                        self.scs_el = document.createElement("script"), self.scs_el.src = e, self.scs_el.id = parent.instanceName_str + ".data.parseOfficialFM", document.documentElement.appendChild(self.scs_el)
                    } catch (e) {}
                    self.JSONPRequestTimeoutId_to = setTimeout(self.JSONPRequestTimeoutError, 8e3)
                }
            }, this.JSONPRequestTimeoutError = function() {
                self.isPlaylistDispatchingError_bl = !0, showLoadPlaylistErrorId_to = setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: "Error loading official.fm url!<font color='#FF0000'>" + self.sourceURL_str + "</font>"
                    }), self.isPlaylistDispatchingError_bl = !1
                }, 50)
            }, this.closeJsonPLoader = function() {
                self.isSCTrack = !1, self.isLoadingShoutcast_bl = !1, self.isLoadingIcecast_bl = !1, clearTimeout(self.JSONPRequestTimeoutId_to), clearTimeout(self.updateRadioTitleId_to);
                try {
                    self.icecastxmlHttp.abort()
                } catch (e) {}
                self.icecastxmlHttp = null;
                try {
                    self.shoutcastxmlHttp.abort()
                } catch (e) {}
                self.shoutcastxmlHttp = null;
                try {
                    document.documentElement.removeChild(self.scs_el)
                } catch (e) {}
                try {
                    document.documentElement.removeChild(self.scs2_el)
                } catch (e) {}
                try {
                    document.documentElement.removeChild(self.scs3_el)
                } catch (e) {}
            }, this.startToUpdateIcecastName = function() {
                self.closeJsonPLoader(), self.getIcecastRadioNameAndStream(self.sourceURL_str, !0)
            }, this.getIcecastRadioNameAndStream = function(e, t) {
                self.isPlaylistDispatchingError_bl || (self.sourceURL_str = e, "/" == self.sourceURL_str.substr(self.sourceURL_str.length - 1) && (self.sourceURL_str = self.sourceURL_str.substr(0, self.sourceURL_str.length - 1)), "/" != self.sourceURL_str.substr(self.sourceURL_str.length - 1) && (self.sourceURL_str += "/"), e = "https://cors-anywhere.herokuapp.com/" + self.sourceURL_str + "status-json.xsl", self.originalSourceURL_str = self.sourceURL_str, self.icecastxmlHttp = new XMLHttpRequest, self.icecastxmlHttp.onreadystatechange = function() {
                    4 == self.icecastxmlHttp.readyState && 200 == self.icecastxmlHttp.status && self.parseIcecastRadioURL(self.icecastxmlHttp.responseText)
                }, self.icecastxmlHttp.open("GET", e, !0), self.icecastxmlHttp.send(null), t || (self.JSONPRequestTimeoutId_to = setTimeout(self.parseRadioErrorURL, 5e3)))
            }, this.parseIcecastRadioURL = function(e) {
                if ("/" == self.sourceURL_str.substr(self.sourceURL_str.length - 1) && (self.sourceURL_str = self.sourceURL_str.substr(0, self.sourceURL_str.length - 1)), e = JSON.parse(e), self.closeJsonPLoader(), e.icestats.source[0]) var t = e.icestats.source[0].listenurl,
                    o = e.icestats.source[0].title;
                else t = e.icestats.source.listenurl, o = e.icestats.source.title;
                if (o = o || "title not defined", e.icestats.source[0]) self.stationLabelClassName, self.stationClassName, e.icestats.source[0].server_name, self.genreLabelClassName, self.genreClassName, e.icestats.source[0].genre, self.currentListenersLabelClassName, self.currentListenersClassName, e.icestats.source[0].listeners, self.bitrateLabelClassName, self.bitrateClassName, e.icestats.source[0].bitrate;
                else self.stationLabelClassName, self.stationClassName, e.icestats.source.server_name, self.genreLabelClassName, self.genreClassName, e.icestats.source.genre, self.currentListenersLabelClassName, self.currentListenersClassName, e.icestats.source.listeners, self.bitrateLabelClassName, self.bitrateClassName, e.icestats.source.bitrate;
                self.dispatchEvent(FWDMSPAudioData.RADIO_TRACK_READY, {
                    source: t,
                    songTitle: o
                }), self.updateRadioTitleId_to = setTimeout(function() {
                    parent.isIcecast_bl && self.startToUpdateIcecastName()
                }, 5e3);
                var s = o,
                    i = s.substr(0, s.indexOf("-") - 1),
                    n = s.substr(s.indexOf("-") + 2);
                self.getImage(i, n)
            }, this.startToUpdateShoutcast = function() {
                self.closeJsonPLoader(), self.getShoutcastRadioNameAndStream(self.sourceURL_str, !0)
            }, this.getShoutcastRadioNameAndStream = function(e, t) {
                if (!self.isPlaylistDispatchingError_bl) {
                    if (self.sourceURL_str = e, self.originalSourceURL_str = e, "/" == self.sourceURL_str.substr(self.sourceURL_str.length - 1) && (self.sourceURL_str = self.sourceURL_str.substr(0, self.sourceURL_str.length - 1)), 1 == self.shoutcastVersion) e = "https://cors-anywhere.herokuapp.com/" + self.sourceURL_str + "/7.html", self.originalSourceURL_str = e, self.shoutcastxmlHttp = new XMLHttpRequest, self.shoutcastxmlHttp.onreadystatechange = function() {
                        if (4 == self.shoutcastxmlHttp.readyState && 200 == self.shoutcastxmlHttp.status) {
                            var e = self.shoutcastxmlHttp.responseText.match(/<body>.*?<\/body>/im)[0];
                            e = (e = (e = (e = e.replace("<body>", "")).replace("<body> ", "")).replace(" </body>", "")).replace("</body> ", "");
                            var t = {
                                streampath: "/;type=mp3",
                                servertitle: "Shoutcast v1",
                                servergenre: "Shoutcast v1"
                            };
                            t.songtitle = e.split(",")[6], t.currentlisteners = e.split(",")[0], t.bitrate = e.split(",")[5], self.parseShoutcastRadioURL(t)
                        }
                    }, self.shoutcastxmlHttp.open("GET", e, !0), self.shoutcastxmlHttp.send(null);
                    else {
                        e = self.sourceURL_str + "/stats?sid=1&json=1&callback=" + parent.instanceName_str + ".data.parseShoutcastRadioURL";
                        try {
                            document.documentElement.removeChild(self.scs_el)
                        } catch (e) {}
                        try {
                            document.documentElement.removeChild(self.scs_el)
                        } catch (e) {}
                        try {
                            self.scs_el = document.createElement("script"), self.scs_el.src = e, self.scs_el.id = parent.instanceName_str + ".data.parseRadioErrorURL", document.documentElement.appendChild(self.scs_el)
                        } catch (e) {}
                    }
                    t || (self.JSONPRequestTimeoutId_to = setTimeout(self.parseRadioErrorURL, 5e3))
                }
            }, this.parseShoutcastRadioURL = function(e) {
                var t;
                if (parent.isShoutcast_bl || parent.isIcecast_bl)
                    if (self.closeJsonPLoader(), e.streampath) {
                        t = self.sourceURL_str + e.streampath, "/" == e.streampath && (t += ";.mp3"), songTitle = e.songtitle, self.prevSongTitle != songTitle && self.getSoutcastHistory();
                        self.stationLabelClassName, self.stationClassName, e.servertitle, self.genreLabelClassName, self.genreClassName, e.servergenre, self.currentListenersLabelClassName, self.currentListenersClassName, e.currentlisteners, self.bitrateLabelClassName, self.bitrateClassName, e.bitrate;
                        var o = songTitle.substr(0, songTitle.indexOf("-") - 1),
                            s = songTitle.substr(songTitle.indexOf("-") + 2);
                        self.getImage(o, s), self.dispatchEvent(FWDMSPAudioData.RADIO_TRACK_READY, {
                            source: t,
                            songTitle: songTitle
                        }), self.updateRadioTitleId_to = setTimeout(function() {
                            parent.isShoutcast_bl && self.startToUpdateShoutcast()
                        }, 5e3)
                    } else self.parseRadioErrorURL()
            }, this.parseRadioErrorURL = function() {
                (parent.isShoutcast_bl || parent.isIcecast_bl) && (self.closeJsonPLoader(), self.isPlaylistDispatchingError_bl = !0, showLoadPlaylistErrorId_to = setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: "Error loading radio track url!<font color='#FF0000'>" + self.sourceURL_str + "</font>"
                    }), self.isPlaylistDispatchingError_bl = !1
                }, 50), parent.isShoutcast_bl && self.startToUpdateShoutcast())
            }, this.getSoutcastHistory = function() {
                if (parent.isShoutcast_bl || parent.isIcecast_bl) {
                    "/" != self.sourceURL_str.substr(self.sourceURL_str.length - 1) && (self.sourceURL_str = self.sourceURL_str + "/"), url = self.sourceURL_str + "played?sid=1&type=json&callback=" + parent.instanceName_str + ".data.parseShoutcastRadioHisotry";
                    try {
                        document.documentElement.removeChild(self.scs2_el)
                    } catch (e) {}
                    try {
                        self.scs2_el = document.createElement("script"), self.scs2_el.src = url, document.documentElement.appendChild(self.scs2_el)
                    } catch (e) {}
                }
            }, this.parseShoutcastRadioHisotry = function(e) {
                if (self.prevObj != e[0].title) {
                    var t;
                    self.history_ar = [];
                    for (var o = 0; o < e.length; o++) {
                        t = e[o];
                        var s = new Date(1e3 * t.playedat),
                            i = String(s.getHours());
                        1 == i.length && parseInt(i) <= 9 ? i = "0" + i : 1 == i.length && 9 < parseInt(i) && (i += "0");
                        var n = String(s.getMinutes());
                        1 == n.length && parseInt(n) <= 9 ? n = "0" + n : 1 == n.length && 9 < parseInt(n) && (n += "0");
                        var l = String(s.getSeconds());
                        1 == l.length && parseInt(l) <= 9 ? l = "0" + l : 1 == l.length && 9 < parseInt(l) && (l += "0"), s = i + ":" + n + ":" + l;
                        var r = t.title;
                        if (0 == o) var a = "<span class='" + self.titleClassNameSelected + "'>" + r + "</span><span class='" + self.lineClassNameSelected + "'> - </span><span class='" + self.playedAtClassNameSelected + "'>played at:</span> <span class='" + self.timeClassNameSelected + "'>" + s + "</span>";
                        else a = "<span class='" + self.titleClassName + "'>" + r + "</span><span class='" + self.lineClassName + "'> - </span><span class='" + self.playedAtClassName + "'>played at</span> <span class='" + self.timeClassName + "'>" + s + "</span>";
                        self.history_ar[o] = a, self.prevObj = e[0].title
                    }
                }
            }, this.getImage = function(e, t) {
                if (parent.isShoutcast_bl || parent.isIcecast_bl) {
                    var o = "http://itunes.apple.com/search?type=jsonp&term==" + (e = encodeURI(e)) + "-" + (t = encodeURI(t)) + "&media=music&limit=1&callback=" + parent.instanceName_str + ".data.parseImage";
                    try {
                        document.documentElement.removeChild(self.scs3_el)
                    } catch (e) {}
                    try {
                        self.scs3_el = document.createElement("script"), self.scs3_el.src = o, document.documentElement.appendChild(self.scs3_el)
                    } catch (e) {}
                }
            }, this.parseImage = function(e) {
                e.results && e.results[0] && self.dispatchEvent(FWDMSPAudioData.UPDATE_IMAGE, {
                    image: e.results[0].artworkUrl100
                })
            }, this.loadXMLPlaylist = function(e) {
                if (!self.isPlaylistDispatchingError_bl) {
                    if ("file:" == document.location.protocol && -1 == e.indexOf("official.fm")) return self.isPlaylistDispatchingError_bl = !0, void(showLoadPlaylistErrorId_to = setTimeout(function() {
                        -1 != e.indexOf(".xml") ? self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                            text: "Loading XML files local is not allowed or possible!. To function properly please test online."
                        }) : self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                            text: "Loading PLS files local is not allowed or possible!. To function properly please test online."
                        }), self.isPlaylistDispatchingError_bl = !1
                    }, 50));
                    if (self.closeXHR(), self.loadFromFolder_bl = !1, self.sourceURL_str = e, self.xhr = new XMLHttpRequest, self.xhr.onreadystatechange = self.ajaxOnLoadHandler, self.xhr.onerror = self.ajaxOnErrorHandler, -1 != self.sourceURL_str.indexOf(".pls")) try {
                        self.xhr.open("GET", self.sourceURL_str, !0), self.xhr.send()
                    } catch (e) {
                        var t = e;
                        e && e.message && (t = e.message), self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                            text: "PLS  file can't be loaded! <font color='#FF0000'>" + self.sourceURL_str + "</font>. " + t
                        })
                    } else try {
                        self.xhr.open("GET", self.proxyPath_str + "?url=" + self.sourceURL_str + "&rand=" + parseInt(99999999 * Math.random()), !0), self.xhr.send()
                    } catch (e) {
                        t = e;
                        e && e.message && (t = e.message), self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                            text: "XML file can't be loaded! <font color='#FF0000'>" + self.sourceURL_str + "</font>. " + t
                        })
                    }
                }
            }, this.loadFolderPlaylist = function(e) {
                if (!self.isPlaylistDispatchingError_bl) {
                    if ("file:" == document.location.protocol && -1 == e.indexOf("official.fm")) return self.isPlaylistDispatchingError_bl = !0, void(showLoadPlaylistErrorId_to = setTimeout(function() {
                        self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                            text: "Creating a mp3 playlist from a folder is not allowed or possible local! To function properly please test online."
                        }), self.isPlaylistDispatchingError_bl = !1
                    }, 50));
                    self.closeXHR(), self.loadFromFolder_bl = !0, self.countID3 = 0, self.sourceURL_str = e.substr(e.indexOf(":") + 1), self.xhr = new XMLHttpRequest, self.xhr.onreadystatechange = self.ajaxOnLoadHandler, self.xhr.onerror = self.ajaxOnErrorHandler;
                    try {
                        self.xhr.open("get", self.proxyFolderPath_str + "?dir=" + encodeURIComponent(self.sourceURL_str) + "&rand=" + parseInt(9999999 * Math.random()), !0), self.xhr.send()
                    } catch (e) {
                        e && e.message && e.message, self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                            text: "Folder proxy file path is not found: <font color='#FF0000'>" + self.proxyFolderPath_str + "</font>"
                        })
                    }
                }
            }, this.ajaxOnLoadHandler = function(e) {
                var response, isXML = !1;
                if (4 == self.xhr.readyState)
                    if (404 == self.xhr.status) self.loadFromFolder_bl ? self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: "Folder proxy file path is not found: <font color='#FF0000'>" + self.proxyFolderPath_str + "</font>"
                    }) : -1 != self.sourceURL_str.indexOf(".pls") ? self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: "Error loading file <font color='#FF0000'>" + self.sourceURL_str + "</font>. Probably the file path is incorect."
                    }) : self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: "Proxy file path is not found: <font color='#FF0000'>" + self.proxyPath_str + "</font>"
                    });
                    else if (408 == self.xhr.status) self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                    text: "Proxy file request load timeout!"
                });
                else if (200 == self.xhr.status) {
                    if (-1 != self.xhr.responseText.indexOf("<b>Warning</b>:")) return void self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: "Error loading folder: <font color='#FF0000'>" + self.sourceURL_str + "</font>. Make sure that the folder path is correct!"
                    });
                    response = -1 != self.xhr.responseText.indexOf("NumberOfEntries") ? PLS.parse(this.response) : window.JSON ? JSON.parse(self.xhr.responseText) : eval("(" + self.xhr.responseText + ")"), -1 != self.xhr.responseText.indexOf("api.soundcloud.com") ? (self.isSCTrack ? self.parseSoundCloudURL(response) : self.parseSoundCloud(response), self.isSCTrack = !1) : response.channel ? self.parsePodcast(response) : response.folder ? self.parseFolderJSON(response) : response.li ? self.parseXML(response) : -1 != self.xhr.responseText.indexOf("NumberOfEntries") ? self.parsePLS(response) : response.error && self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                        text: "Error loading file: <font color='#FF0000'>" + self.sourceURL_str + "</font>. Make sure the file path (xml or podcast) is correct and well formatted!"
                    })
                }
            }, this.ajaxOnErrorHandler = function(e) {
                try {
                    window.console && console.log(e), window.console && console.log(e.message)
                } catch (e) {}
                self.loadFromFolder_bl ? self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                    text: "Error loading file : <font color='#FF0000'>" + self.proxyFolderPath_str + "</font>. Make sure the path is correct"
                }) : self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                    text: "Error loading file : <font color='#FF0000'>" + self.proxyPath_str + "</font>. Make sure the path is correct"
                })
            }, this.parseSoundCloud = function(e) {
                var t;
                if (self.closeJsonPLoader(), self.playlist_ar = [], e && e.uri) return "track" == e.kind ? void self.createSoundcloudPlaylist(e) : (t = -1 == e.uri.indexOf("/tracks") ? e.uri + "/tracks" : e.uri + "/favorites", void self.loadSoundCloudList(t));
                e.length || "track" == e.kind ? self.createSoundcloudPlaylist(e) : self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                    text: "Please provide a playlist or track URL : <font color='#FF0000'>" + self.sourceURL_str + "</font>."
                })
            }, this.createSoundcloudPlaylist = function(e) {
                if (e.length)
                    for (var t = 0; t < e.length; t++) {
                        if (track = e[t], obj = {}, obj.source = track.stream_url + "?consumer_key=" + self.scClientId_str, obj.downloadPath = 1 == track.downloadable ? track.download_url + "?consumer_key=" + self.scClientId_str : void 0, obj.downloadable = track.downloadable, obj.buy = void 0, obj.thumbPath = track.artwork_url, self.showSoundCloudUserNameInTitle_bl) {
                            var o = "";
                            self.showTracksNumbers_bl ? (t < 9 && (o = "0"), o = o + (t + 1) + ". ", obj.title = o + "<span style='font-weight:bold;'>" + track.user.username + "</span> - " + track.title) : obj.title = "<span style='font-weight:bold;'>" + track.user.username + "</span> - " + track.title, obj.titleText = track.user.username + " - " + track.title
                        } else {
                            o = "";
                            self.showTracksNumbers_bl ? (t < 9 && (o = "0"), o = o + (t + 1) + ". ", obj.title = o + track.title) : obj.title = track.title, obj.titleText = track.title
                        }
                        if (obj.duration = track.duration, track.streamable && self.playlist_ar.push(obj), t > self.maxPlaylistItems - 1) break
                    } else track = e, obj = {}, obj.source = track.stream_url + "?consumer_key=" + self.scClientId_str, obj.downloadPath = 1 == track.downloadable ? track.download_url + "?consumer_key=" + self.scClientId_str : void 0, obj.downloadable = track.downloadable, obj.buy = void 0, obj.thumbPath = track.artwork_url, self.showSoundCloudUserNameInTitle_bl ? (obj.title = "<span style='font-weight:bold;'>" + track.user.username + "</span> - " + track.title, obj.titleText = track.user.username + " - " + track.title) : (obj.title = track.title, obj.titleText = track.title), obj.duration = track.duration, track.streamable && self.playlist_ar.push(obj);
                clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to), self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.PLAYLIST_LOAD_COMPLETE)
                }, 50), self.isDataLoaded_bl = !0
            }, this.parseOfficialFM = function(e) {
                var t, o;
                self.closeJsonPLoader(), self.playlist_ar = [];
                for (var s = e.tracks, i = 0; i < s.length; i++) {
                    o = e.tracks[i].track, (t = {}).id = i, t.source = encodeURI(o.streaming.http), t.downloadPath = t.source, t.downloadable = self.showDownloadMp3Button_bl, t.buy = void 0, self.forceDisableDownloadButtonForOfficialFM_bl && (t.downloadable = !1), t.thumbPath = void 0;
                    var n = "";
                    if (self.showTracksNumbers_bl ? (i < 9 && (n = "0"), n = n + (i + 1) + ". ", t.title = n + "<span style='font-weight:bold;'>" + o.artist + "</span> - " + o.title) : t.title = "<span style='font-weight:bold;'>" + o.artist + "</span> - " + o.title, t.titleText = o.artist + " - " + o.title, t.duration = 1e3 * o.duration, self.playlist_ar[i] = t, i > self.maxPlaylistItems - 1) break
                }
                clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to), self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.PLAYLIST_LOAD_COMPLETE)
                }, 50), self.isDataLoaded_bl = !0
            }, this.parsePodcast = function(e) {
                var t;
                self.playlist_ar = [];
                var o = e.channel.item,
                    s = void 0;
                try {
                    s = e.channel.image.url
                } catch (e) {}
                for (var i = 0; i < o.length; i++) {
                    t = {}, o[i].enclosure ? t.source = encodeURI(o[i].enclosure["@attributes"].url) : t.source = encodeURI(o[i].link), t.downloadPath = t.source, t.downloadable = self.showDownloadMp3Button_bl, t.buy = void 0, self.forceDisableDownloadButtonForPodcast_bl && (t.downloadable = !1), t.thumbPath = s;
                    var n = "";
                    if (self.showTracksNumbers_bl ? (i < 9 && (n = "0"), n = n + (i + 1) + ". ", t.title = n + o[i].title) : t.title = o[i].title, t.titleText = o[i].title, t.duration = void 0, self.playlist_ar[i] = t, i > self.maxPlaylistItems - 1) break
                }
                clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to), self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.PLAYLIST_LOAD_COMPLETE)
                }, 50), self.isDataLoaded_bl = !0
            }, this.parseXML = function(e) {
                var t;
                self.playlist_ar = [];
                var o = e.li;
                o.length || (o = [o]);
                for (var s = 0; s < o.length; s++) {
                    (t = {}).source = o[s]["@attributes"]["data-path"], -1 != t.source.indexOf("encrypt:") && (t.source = atob(t.source.substr(8)));
                    var i = encodeURI(t.source.substr(0, t.source.lastIndexOf("/") + 1)),
                        n = t.source.substr(t.source.lastIndexOf("/") + 1);
                    if (-1 != t.source.indexOf("youtube.")) {
                        var l = t.source.match(/^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/);
                        t.source = l[2]
                    } else n = -1 != n.indexOf(";.mp3") || FWDMSPUtils.isURLEncoded(n) ? t.source.substr(t.source.lastIndexOf("/") + 1) : encodeURIComponent(t.source.substr(t.source.lastIndexOf("/") + 1)), t.source = i + n;
                    t.downloadPath = t.source, t.downloadable = "yes" == o[s]["@attributes"]["data-downloadable"], t.buy = o[s]["@attributes"]["data-buy-url"], null == t.buy && (t.buy = ""), t.thumbPath = o[s]["@attributes"]["data-thumbpath"];
                    var r = "";
                    if (self.showTracksNumbers_bl ? (s < 9 && (r = "0"), r = r + (s + 1) + ". ", t.title = r + o[s]["@attributes"]["data-title"]) : t.title = o[s]["@attributes"]["data-title"], t.titleText = o[s]["@attributes"]["data-title"], t.duration = o[s]["@attributes"]["data-duration"], t.atb = o[s]["@attributes"]["data-use-a-to-b"], t.isPrivate = o[s]["@attributes"]["data-is-private"], "yes" == t.isPrivate ? t.isPrivate = !0 : t.isPrivate = !1, t.privateVideoPassword_str = o[s]["@attributes"]["data-private-video-password"], t.startAtTime = o[s]["@attributes"]["data-start-at-time"], "00:00:00" != t.startAtTime && FWDMSPUtils.checkTime(t.startAtTime) || (t.startAtTime = void 0), t.stopAtTime = o[s]["@attributes"]["data-stop-at-time"], "00:00:00" != t.stopAtTime && FWDMSPUtils.checkTime(t.stopAtTime) || (t.stopAtTime = void 0), t.isShoutcast_bl = o[s]["@attributes"]["data-type"], t.isShoutcast_bl && (-1 != t.isShoutcast_bl.toLowerCase().indexOf("shoutcastv1") ? (t.shoutcastVersion = 1, t.isShoutcast_bl = !0) : -1 != t.isShoutcast_bl.toLowerCase().indexOf("shoutcastv2") ? (t.shoutcastVersion = 2, t.isShoutcast_bl = !0) : t.isShoutcast_bl = !1), t.isIcecast_bl = o[s]["@attributes"]["data-type"], t.isIcecast_bl && (-1 != t.isIcecast_bl.toLowerCase().indexOf("icecast") ? t.isIcecast_bl = !0 : t.isIcecast_bl = !1), self.playlist_ar[s] = t, s > self.maxPlaylistItems - 1) break
                }
                clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to), self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.PLAYLIST_LOAD_COMPLETE)
                }, 50), self.isDataLoaded_bl = !0
            }, this.parsePLS = function(e) {
                var t;
                self.playlist_ar = [];
                for (var o = e, s = 0; s < o.length; s++) {
                    (t = {}).source = o[s].file + "/;.mp3", t.downloadable = !1, t.buy = void 0, t.thumbPath = void 0, t.title = o[s].title, t.titleText = o[s].title;
                    var i = "";
                    if (self.showTracksNumbers_bl ? (s < 9 && (i = "0"), i = i + (s + 1) + ". ", t.title = i + " " + t.title) : (s < 9 && (i = "0"), i += s + 1, t.title = " " + i), t.titleText = t.title, self.playlist_ar[s] = t, s > self.maxPlaylistItems - 1) break
                }
                clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to), self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.PLAYLIST_LOAD_COMPLETE)
                }, 50), self.isDataLoaded_bl = !0
            }, this.parseFolderJSON = function(e) {
                var t;
                self.playlist_ar = [];
                for (var o = e.folder, s = 0; s < o.length; s++) {
                    (t = {}).source = o[s]["@attributes"]["data-path"], -1 != t.source.indexOf("encrypt:") && (t.source = atob(t.source.substr(8)));
                    var i = encodeURI(t.source.substr(0, t.source.lastIndexOf("/") + 1)),
                        n = encodeURIComponent(t.source.substr(t.source.lastIndexOf("/") + 1));
                    if (t.source = i + n, t.downloadPath = t.source, t.downloadable = self.showDownloadMp3Button_bl, t.buy = void 0, self.forceDisableDownloadButtonForFolder_bl && (t.downloadable = !1), t.thumbPath = o[s]["@attributes"]["data-thumbpath"], t.title = "...", t.titleText = "...", FWDMSPUtils.isIEAndLessThen9) {
                        var l = "";
                        self.showTracksNumbers_bl ? (s < 9 && (l = "0"), l = l + (s + 1) + ". ", t.title = l + "track ", t.titleText = "track") : (s < 9 && (l = "0"), l += s + 1, t.title = "track " + l, t.titleText = "track " + l)
                    }
                    if (self.playlist_ar[s] = t, s > self.maxPlaylistItems - 1) break
                }
                clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to), self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                    self.dispatchEvent(FWDMSPAudioData.PLAYLIST_LOAD_COMPLETE)
                }, 50), self.isDataLoaded_bl = !0
            }, this.parseDOMPlaylist = function(e) {
                if (!self.isPlaylistDispatchingError_bl) {
                    var t;
                    if (self.closeXHR(), !(t = document.getElementById(e))) return self.isPlaylistDispatchingError_bl = !0, void(showLoadPlaylistErrorId_to = setTimeout(function() {
                        self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                            text: "The playlist with id <font color='#FF0000'>" + e + "</font> is not found in the DOM."
                        }), self.isPlaylistDispatchingError_bl = !1
                    }, 50));
                    var o, s = FWDMSPUtils.getChildren(t),
                        i = s.length;
                    if (self.playlist_ar = [], 0 == i) return self.isPlaylistDispatchingError_bl = !0, void(showLoadPlaylistErrorId_to = setTimeout(function() {
                        self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                            text: "The playlist whit the id  <font color='#FF0000'>" + e + "</font> must contain at least one track."
                        }), self.isPlaylistDispatchingError_bl = !1
                    }, 50));
                    for (var n = 0; n < i; n++) {
                        var l = {};
                        if (o = s[n], !FWDMSPUtils.hasAttribute(o, "data-path")) return self.isPlaylistDispatchingError_bl = !0, void(showLoadPlaylistErrorId_to = setTimeout(function() {
                            self.dispatchEvent(FWDMSPAudioData.LOAD_ERROR, {
                                text: "Attribute <font color='#FF0000'>data-path</font> is required in the playlist at position <font color='#FF0000'>" + (n + 1)
                            })
                        }, 50));
                        if (n > self.maxPlaylistItems - 1) break;

                        if (l.isShoutcast_bl = FWDMSPUtils.getAttributeValue(o, "data-type"), l.isShoutcast_bl && (-1 != l.isShoutcast_bl.toLowerCase().indexOf("shoutcastv1") ? (l.shoutcastVersion = 1, l.isShoutcast_bl = !0) : -1 != l.isShoutcast_bl.toLowerCase().indexOf("shoutcastv2") ? (l.shoutcastVersion = 2, l.isShoutcast_bl = !0) : l.isShoutcast_bl = !1), l.isIcecast_bl = FWDMSPUtils.getAttributeValue(o, "data-type"), l.isIcecast_bl && (-1 != l.isIcecast_bl.toLowerCase().indexOf("icecast") ? l.isIcecast_bl = !0 : l.isIcecast_bl = !1), l.source = FWDMSPUtils.getAttributeValue(o, "data-path"), -1 != l.source.indexOf("encrypt:") && (l.source = atob(l.source.substr(8))), -1 != l.source.indexOf("youtube.")) {
                            var r = l.source.match(/^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/);
                            l.source = r[2]
                        } else if (-1 == l.source.lastIndexOf("google.") && !l.isShoutcast_bl && !l.isIcecast_bl) {
                            var a = encodeURI(l.source.substr(0, l.source.lastIndexOf("/") + 1)),
                                d = l.source.substr(l.source.lastIndexOf("/") + 1);
                            d = -1 != d.indexOf(";.mp3") || FWDMSPUtils.isURLEncoded(d) ? l.source.substr(l.source.lastIndexOf("/") + 1) : encodeURIComponent(l.source.substr(l.source.lastIndexOf("/") + 1)), l.source = a + d
                        }
                        if (l.source.indexOf(".soundcloud.") != -1){
                          l.source = l.source + '/stream?client_id=' + 'dce5652caa1b66331903493735ddd64d'
                        };
                        l.downloadPath = l.source, (l.isShoutcast_bl || l.isIcecast_bl) && "/" != l.source.substr(l.source.length - 1) && (l.source += "/"), FWDMSPUtils.hasAttribute(o, "data-thumbpath") ? l.thumbPath = FWDMSPUtils.getAttributeValue(o, "data-thumbpath") : l.thumbPath = void 0, FWDMSPUtils.hasAttribute(o, "data-downloadable") ? l.downloadable = "yes" == FWDMSPUtils.getAttributeValue(o, "data-downloadable") : l.downloadable = void 0, FWDMSPUtils.hasAttribute(o, "data-buy-url") ? l.buy = FWDMSPUtils.getAttributeValue(o, "data-buy-url") : l.buy = void 0, l.title = "not defined!";
                        try {
                            var u = "";
                            self.showTracksNumbers_bl ? (n < 9 && (u = "0"), u = u + (n + 1) + ". ", l.title = u + FWDMSPUtils.getChildren(o)[0].innerHTML) : l.title = FWDMSPUtils.getChildren(o)[0].innerHTML
                        } catch (e) {}
                        try {
                            l.titleText = FWDMSPUtils.getChildren(o)[0].textContent || FWDMSPUtils.getChildren(o)[0].innerText
                        } catch (e) {}
                        FWDMSPUtils.hasAttribute(o, "data-duration") && (l.duration = FWDMSPUtils.getAttributeValue(o, "data-duration")), FWDMSPUtils.hasAttribute(o, "data-use-a-to-b") && (l.atb = FWDMSPUtils.getAttributeValue(o, "data-use-a-to-b")), l.isPrivate = FWDMSPUtils.getAttributeValue(o, "data-is-private"), "yes" == l.isPrivate ? l.isPrivate = !0 : l.isPrivate = !1, l.privateVideoPassword_str = FWDMSPUtils.getAttributeValue(o, "data-private-video-password"), l.startAtTime = FWDMSPUtils.getAttributeValue(o, "data-start-at-time"), "00:00:00" != l.startAtTime && FWDMSPUtils.checkTime(l.startAtTime) || (l.startAtTime = void 0), l.stopAtTime = FWDMSPUtils.getAttributeValue(o, "data-stop-at-time"), "00:00:00" != l.stopAtTime && FWDMSPUtils.checkTime(l.stopAtTime) || (l.stopAtTime = void 0), self.playlist_ar[n] = l
                    }
                    clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to), self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                        self.dispatchEvent(FWDMSPAudioData.PLAYLIST_LOAD_COMPLETE)
                    }, 50), self.isDataLoaded_bl = !0
                }
            }, this.closeXHR = function() {
                self.closeJsonPLoader();
                try {
                    document.documentElement.removeChild(self.scs_el), self.scs_el = null
                } catch (e) {}
                if (null != self.xhr) {
                    try {
                        self.xhr.abort()
                    } catch (e) {}
                    self.xhr.onreadystatechange = null, self.xhr.onerror = null, self.xhr = null
                }
                self.countID3 = 2e3
            }, this.closeData = function() {
                self.closeXHR(), self.closeJsonPLoader(), clearTimeout(self.loadImageId_to), clearTimeout(self.showLoadPlaylistErrorId_to), clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to), clearTimeout(self.loadImageId_to), clearTimeout(self.loadPreloaderId_to), self.image_img && (self.image_img.onload = null, self.image_img.onerror = null)
            }, self.init()
        };
        FWDMSPAudioData.setPrototype = function() {
            FWDMSPAudioData.prototype = new FWDMSPEventDispatcher
        }, FWDMSPAudioData.prototype = null, FWDMSPAudioData.RADIO_TRACK_UPDATE = "shoutcastTitleUpdate", FWDMSPAudioData.RADIO_TRACK_READY = "radioTrackReady", FWDMSPAudioData.UPDATE_IMAGE = "updateImage", FWDMSPAudioData.SOUNDCLOUD_TRACK_READY = "soundcloudTrackReady", FWDMSPAudioData.PRELOADER_LOAD_DONE = "onPreloaderLoadDone", FWDMSPAudioData.LOAD_DONE = "onLoadDone", FWDMSPAudioData.LOAD_ERROR = "onLoadError", FWDMSPAudioData.IMAGE_LOADED = "onImageLoaded", FWDMSPAudioData.SKIN_LOAD_COMPLETE = "onSkinLoadComplete", FWDMSPAudioData.SKIN_PROGRESS = "onSkinProgress", FWDMSPAudioData.IMAGES_PROGRESS = "onImagesPogress", FWDMSPAudioData.PLAYLIST_LOAD_COMPLETE = "onPlaylistLoadComplete", window.FWDMSPAudioData = FWDMSPAudioData
    }(window),
    function(o) {
        var i = function(e) {
            var l = this;
            i.prototype;
            this.audio_el = null, this.sourcePath_str = null, this.lastPercentPlayed = 0, this.volume = e, this.curDuration = 0, this.countNormalMp3Errors = 0, this.countShoutCastErrors = 0, this.maxShoutCastCountErrors = 5, this.maxNormalCountErrors = 1, this.testShoutCastId_to, this.preload_bl = !1, this.allowScrubing_bl = !1, this.hasError_bl = !0, this.isPlaying_bl = !1, this.isStopped_bl = !0, this.hasPlayedOnce_bl = !1, this.isStartEventDispatched_bl = !1, this.isSafeToBeControlled_bl = !1, this.isShoutcast_bl = !1, this.isNormalMp3_bl = !1, this.init = function() {
                l.setupAudio(), l.setHeight(0)
            }, this.setupAudio = function() {
                null == l.audio_el && (l.audio_el = document.createElement("audio"), l.screen.appendChild(l.audio_el), l.audio_el.controls = !1, l.audio_el.preload = "auto", l.audio_el.volume = l.volume), l.audio_el.addEventListener("error", l.errorHandler), l.audio_el.addEventListener("canplay", l.safeToBeControlled), l.audio_el.addEventListener("canplaythrough", l.safeToBeControlled), l.audio_el.addEventListener("progress", l.updateProgress), l.audio_el.addEventListener("timeupdate", l.updateAudio), l.audio_el.addEventListener("pause", l.pauseHandler), l.audio_el.addEventListener("play", l.playHandler), l.audio_el.addEventListener("ended", l.endedHandler)
            }, this.destroyAudio = function() {
                l.audio_el && (l.audio_el.removeEventListener("error", l.errorHandler), l.audio_el.removeEventListener("canplay", l.safeToBeControlled), l.audio_el.removeEventListener("canplaythrough", l.safeToBeControlled), l.audio_el.removeEventListener("progress", l.updateProgress), l.audio_el.removeEventListener("timeupdate", l.updateAudio), l.audio_el.removeEventListener("pause", l.pauseHandler), l.audio_el.removeEventListener("play", l.playHandler), l.audio_el.removeEventListener("ended", l.endedHandler), l.audio_el.src = "", l.audio_el.load())
            }, this.errorHandler = function(e) {
                if (null != l.sourcePath_str && null != l.sourcePath_str) {
                    if (l.isNormalMp3_bl && l.countNormalMp3Errors <= l.maxNormalCountErrors) return l.stop(), l.testShoutCastId_to = setTimeout(l.play, 200), void l.countNormalMp3Errors++;
                    if (l.isShoutcast_bl && l.countShoutCastErrors <= l.maxShoutCastCountErrors && 0 == l.audio_el.networkState) return l.testShoutCastId_to = setTimeout(l.play, 200), void l.countShoutCastErrors++;
                    var t;
                    l.hasError_bl = !0, l.stop(), t = 0 == l.audio_el.networkState ? "error 'self.audio_el.networkState = 1'" : 1 == l.audio_el.networkState ? "error 'self.audio_el.networkState = 1'" : 2 == l.audio_el.networkState ? "'self.audio_el.networkState = 2'" : 3 == l.audio_el.networkState ? "source not found <font color='#FF0000'>" + l.sourcePath_str + "</font>" : e, o.console && o.console.log(l.audio_el.networkState), l.dispatchEvent(i.ERROR, {
                        text: t
                    })
                }
            }, this.setSource = function(e) {
                l.sourcePath_str = e, clearTimeout(l.testShoutCastId_to), -1 != l.sourcePath_str.indexOf(";") ? (l.isShoutcast_bl = !0, l.countShoutCastErrors = 0) : l.isShoutcast_bl = !1, -1 == l.sourcePath_str.indexOf(";") ? (l.isNormalMp3_bl = !0, l.countNormalMp3Errors = 0) : l.isNormalMp3_bl = !1, l.lastPercentPlayed = 0, l.audio_el && l.stop(!0)
            }, this.play = function(e) {
                if (l.isStopped_bl) l.isPlaying_bl = !1, l.hasError_bl = !1, l.allowScrubing_bl = !1, l.isStopped_bl = !1, l.setupAudio(), l.audio_el.src = l.sourcePath_str, l.play();
                else if (!l.audio_el.ended || e) try {
                    l.isPlaying_bl = !0, l.hasPlayedOnce_bl = !0, l.audio_el.play(), FWDMSPUtils.isIE && l.dispatchEvent(i.PLAY)
                } catch (e) {}
            }, this.pause = function() {
                if (null != l && null != l.audio_el && !l.audio_el.ended) try {
                    l.audio_el.pause(), l.isPlaying_bl = !1, FWDMSPUtils.isIE && l.dispatchEvent(i.PAUSE)
                } catch (e) {}
            }, this.pauseHandler = function() {
                l.allowScrubing_bl || l.dispatchEvent(i.PAUSE)
            }, this.playHandler = function() {
                l.allowScrubing_bl || (l.isStartEventDispatched_bl || (l.dispatchEvent(i.START), l.isStartEventDispatched_bl = !0), l.dispatchEvent(i.PLAY))
            }, this.endedHandler = function() {
                l.dispatchEvent(i.PLAY_COMPLETE)
            }, this.getDuration = function() {
                return l.formatTime(l.audio_el.duration)
            }, this.getCurrentTime = function() {
                return l.formatTime(l.audio_el.currentTime)
            }, this.stop = function(e) {
                l.dispatchEvent(i.UPDATE_TIME, {
                    curTime: "00:00",
                    totalTime: "00:00",
                    seconds: 0
                }), (null != l && null != l.audio_el && !l.isStopped_bl || e) && (l.isPlaying_bl = !1, l.isStopped_bl = !0, l.hasPlayedOnce_bl = !0, l.isSafeToBeControlled_bl = !1, l.isStartEventDispatched_bl = !1, clearTimeout(l.testShoutCastId_to), l.audio_el.pause(), l.destroyAudio(), l.dispatchEvent(i.STOP), l.dispatchEvent(i.LOAD_PROGRESS, {
                    percent: 0
                }))
            }, this.togglePlayPause = function() {
                null != l && l.isSafeToBeControlled_bl && (l.isPlaying_bl ? l.pause() : l.play())
            }, this.safeToBeControlled = function() {
                l.isSafeToBeControlled_bl || (l.hasHours_bl = 0 < Math.floor(l.audio_el.duration / 3600), l.isPlaying_bl = !0, l.isSafeToBeControlled_bl = !0, l.dispatchEvent(i.SAFE_TO_SCRUBB), l.dispatchEvent(i.SAFE_TO_UPDATE_VOLUME))
            }, this.updateProgress = function() {
                var e = 0;
                0 < l.audio_el.buffered.length && (e = l.audio_el.buffered.end(l.audio_el.buffered.length - 1).toFixed(1) / l.audio_el.duration.toFixed(1), !isNaN(e) && e || (e = 0)), 1 == e && l.audio_el.removeEventListener("progress", l.updateProgress), l.dispatchEvent(i.LOAD_PROGRESS, {
                    percent: e
                })
            }, this.updateAudio = function() {
                var e;
                l.allowScrubing_bl || (e = l.audio_el.currentTime / l.audio_el.duration, l.dispatchEvent(i.UPDATE, {
                    percent: e
                }));
                var t = l.formatTime(l.audio_el.duration),
                    o = l.formatTime(l.audio_el.currentTime);
                isNaN(l.audio_el.duration) ? l.dispatchEvent(i.UPDATE_TIME, {
                    curTime: "00:00",
                    totalTime: "00:00",
                    seconds: 0,
                    totalTimeInSeconds: 0
                }) : l.dispatchEvent(i.UPDATE_TIME, {
                    curTime: o,
                    totalTime: t,
                    seconds: Math.round(l.audio_el.currentTime),
                    totalTimeInSeconds: l.audio_el.duration
                }), l.lastPercentPlayed = e, l.curDuration = o
            }, this.startToScrub = function() {
                l.allowScrubing_bl = !0
            }, this.stopToScrub = function() {
                l.allowScrubing_bl = !1
            }, this.scrubbAtTime = function(e) {
                l.audio_el.currentTime = e;
                var t = FWDMSPUtils.formatTime(l.audio_el.duration),
                    o = FWDMSPUtils.formatTime(l.audio_el.currentTime);
                l.dispatchEvent(i.UPDATE_TIME, {
                    curTime: o,
                    totalTime: t,
                    seconds: e
                })
            }, this.scrub = function(e, t) {
                if (null != l.audio_el && l.audio_el.duration) {
                    t && l.startToScrub();
                    try {
                        l.audio_el.currentTime = l.audio_el.duration * e;
                        var o = l.formatTime(l.audio_el.duration),
                            s = l.formatTime(l.audio_el.currentTime);
                        l.dispatchEvent(i.UPDATE_TIME, {
                            curTime: s,
                            totalTime: o
                        })
                    } catch (t) {}
                }
            }, this.replay = function() {
                l.scrub(0), l.play()
            }, this.setVolume = function(e) {
                null != e && (l.volume = e), l.audio_el && (l.audio_el.volume = l.volume)
            }, this.formatTime = function(e) {
                var t = Math.floor(e / 3600),
                    o = e % 3600,
                    s = Math.floor(o / 60),
                    i = o % 60,
                    n = Math.ceil(i);
                return s = 10 <= s ? s : "0" + s, n = 10 <= n ? n : "0" + n, isNaN(n) ? "00:00" : l.hasHours_bl ? t + ":" + s + ":" + n : s + ":" + n
            }, this.setPlaybackRate = function(e) {
                l.audio_el && (l.audio_el.defaultPlaybackRate = e, l.audio_el.playbackRate = e)
            }, this.init()
        };
        i.setPrototype = function() {
            i.prototype = new FWDMSPDisplayObject("div")
        }, i.ERROR = "error", i.UPDATE = "update", i.UPDATE = "update", i.UPDATE_TIME = "updateTime", i.SAFE_TO_SCRUBB = "safeToControll", i.SAFE_TO_UPDATE_VOLUME = "safeToUpdateVolume", i.LOAD_PROGRESS = "loadProgress", i.START = "start", i.PLAY = "play", i.PAUSE = "pause", i.STOP = "stop", i.PLAY_COMPLETE = "playComplete", o.FWDMSPAudioScreen = i
    }(window),
    function() {
        var t = function(o, e) {
            var p = this;
            t.prototype;
            this.image_img, this.catThumbBk_img = o.catThumbBk_img, this.catNextN_img = o.catNextN_img, this.catPrevN_img = o.catPrevN_img, this.catCloseN_img = o.catCloseN_img, this.mainHolder_do = null, this.closeButton_do = null, this.nextButton_do = null, this.prevButton_do = null, this.thumbs_ar = [], this.categories_ar = o.cats_ar, this.catBkPath_str = o.catBkPath_str, this.id = 0, this.mouseX = 0, this.mouseY = 0, this.dif = 0, this.tempId = p.id, this.stageWidth = 0, this.stageHeight = 0, this.thumbW = 0, this.thumbH = 0, this.buttonsMargins = o.buttonsMargins, this.thumbnailMaxWidth = o.thumbnailMaxWidth, this.thumbnailMaxHeight = o.thumbnailMaxHeight, this.spacerH = o.horizontalSpaceBetweenThumbnails, this.spacerV = o.verticalSpaceBetweenThumbnails, this.dl, this.howManyThumbsToDisplayH = 0, this.howManyThumbsToDisplayV = 0, this.categoriesOffsetTotalWidth = 2 * p.catNextN_img.width + 30, this.categoriesOffsetTotalHeight = p.catNextN_img.height + 30, this.totalThumbnails = p.categories_ar.length, this.delayRate = .06, this.countLoadedThumbs = 0, this.hideCompleteId_to, this.showCompleteId_to, this.loadThumbnailsId_to, this.preventMouseWheelNavigId_to, this.showSearchInput_bl = o.showPlaylistsSearchInput_bl, this.inputBackgroundColor_str = o.inputBackgroundColor_str, this.inputColor_str = o.searchInputColor_str, this.preventMouseWheelNavig_bl = !1, this.areThumbnailsCreated_bl = !1, this.areThumbnailsLoaded_bl = !1, this.isShowed_bl = !1, this.isOnDOM_bl = !1, this.isMobile_bl = FWDMSPUtils.isMobile, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, p.init = function() {
                -1 != o.skinPath_str.indexOf("hex_white") ? p.selectedButtonsColor_str = "#FFFFFF" : p.selectedButtonsColor_str = o.selectedButtonsColor_str, p.getStyle().zIndex = 16777271, p.getStyle().msTouchAction = "none", p.getStyle().webkitTapHighlightColor = "rgba(0, 0, 0, 0)", p.getStyle().width = "100%", p.mainHolder_do = new FWDMSPDisplayObject("div"), p.mainHolder_do.getStyle().background = "url('" + p.catBkPath_str + "')", p.mainHolder_do.setY(-3e3), p.addChild(p.mainHolder_do), p.setupButtons(), p.setupDisable(), p.isMobile_bl && (p.setupMobileMove(), FWDMSPUtils.isChrome && (FWDMSPUtils.isIEAndLessThen9 ? document.getElementsByTagName("body")[0].appendChild(p.screen) : document.documentElement.appendChild(p.screen))), (!p.isMobile_bl || p.isMobile_bl && p.hasPointerEvent_bl) && p.setSelectable(!1), window.addEventListener ? (p.screen.addEventListener("mousewheel", p.mouseWheelDumyHandler), p.screen.addEventListener("DOMMouseScroll", p.mouseWheelDumyHandler)) : document.attachEvent && p.screen.attachEvent("onmousewheel", p.mouseWheelDumyHandler), p.showSearchInput_bl && p.setupInput()
            }, this.mouseWheelDumyHandler = function(e) {
                var t;
                if (FWDAnimation.isTweening(p.mainHolder_do)) return e.preventDefault && e.preventDefault(), !1;
                for (var o = 0; o < p.totalThumbnails; o++)
                    if (t = p.thumbs_ar[o], FWDAnimation.isTweening(t)) return e.preventDefault && e.preventDefault(), !1;
                var s = e.detail || e.wheelDelta;
                if (e.wheelDelta && (s *= -1), FWDMSPUtils.isOpera && (s *= -1), 0 < s) p.nextButtonOnMouseUpHandler();
                else if (s < 0) {
                    if (p.leftId <= 0) return;
                    p.prevButtonOnMouseUpHandler()
                }
                if (!e.preventDefault) return !1;
                e.preventDefault()
            }, p.resizeAndPosition = function(e) {
                if (p.isShowed_bl || e) {
                    var t = FWDMSPUtils.getScrollOffsets(),
                        o = FWDMSPUtils.getViewportSize();
                    p.stageWidth = o.w, p.stageHeight = o.h, FWDAnimation.killTweensOf(p.mainHolder_do), p.mainHolder_do.setX(0), p.mainHolder_do.setWidth(p.stageWidth), p.mainHolder_do.setHeight(p.stageHeight), p.setX(t.x), p.setY(t.y), p.setHeight(p.stageHeight), p.isMobile_bl && p.setWidth(p.stageWidth), p.positionButtons(), p.tempId = p.id, p.resizeAndPositionThumbnails(), p.disableEnableNextAndPrevButtons(), p.input_do && (p.input_do.setX(p.stageWidth - p.input_do.getWidth() - p.buttonsMargins), p.input_do.setY(p.stageHeight - p.input_do.getHeight() - p.buttonsMargins), p.inputArrow_do.setX(p.input_do.x + p.input_do.getWidth() - 20), p.inputArrow_do.setY(p.input_do.y + p.input_do.getHeight() / 2 - p.inputArrow_do.getHeight() / 2 - 1))
                }
            }, p.onScrollHandler = function() {
                var e = FWDMSPUtils.getScrollOffsets();
                p.setX(e.x), p.setY(e.y)
            }, this.setupInput = function() {
                p.input_do = new FWDMSPDisplayObject("input"), p.input_do.screen.maxLength = 20, p.input_do.getStyle().textAlign = "left", p.input_do.getStyle().outline = "none", p.input_do.getStyle().boxShadow = "none", p.input_do.getStyle().fontSmoothing = "antialiased", p.input_do.getStyle().webkitFontSmoothing = "antialiased", p.input_do.getStyle().textRendering = "optimizeLegibility", p.input_do.getStyle().fontFamily = "Arial", p.input_do.getStyle().fontSize = "12px", p.input_do.getStyle().padding = "6px", FWDMSPUtils.isIEAndLessThen9 || (p.input_do.getStyle().paddingRight = "-6px"), p.input_do.getStyle().paddingTop = "2px", p.input_do.getStyle().paddingBottom = "3px", p.input_do.getStyle().backgroundColor = p.inputBackgroundColor_str, p.input_do.getStyle().color = p.inputColor_str, p.input_do.getStyle().borderRadius = "6px", p.input_do.screen.value = "search", p.input_do.setHeight(20), p.input_do.setX(18), p.noSearchFound_do = new FWDMSPDisplayObject("div"), p.noSearchFound_do.setX(0), p.noSearchFound_do.getStyle().textAlign = "center", p.noSearchFound_do.getStyle().width = "100%", p.noSearchFound_do.getStyle().fontSmoothing = "antialiased", p.noSearchFound_do.getStyle().webkitFontSmoothing = "antialiased", p.noSearchFound_do.getStyle().textRendering = "optimizeLegibility", p.noSearchFound_do.getStyle().fontFamily = "Arial", p.noSearchFound_do.getStyle().fontSize = "12px", p.noSearchFound_do.getStyle().color = p.inputColor_str, p.noSearchFound_do.setInnerHTML("NOTHING FOUND!"), p.noSearchFound_do.setVisible(!1), p.addChild(p.noSearchFound_do);
                var e = new Image;
                e.src = o.inputArrowPath_str, p.inputArrow_do = new FWDMSPDisplayObject("img"), p.inputArrow_do.setScreen(e), p.inputArrow_do.setWidth(14), p.inputArrow_do.setHeight(12), p.hasPointerEvent_bl ? p.input_do.screen.addEventListener("pointerdown", p.inputFocusInHandler) : p.input_do.screen.addEventListener && (p.input_do.screen.addEventListener("mousedown", p.inputFocusInHandler), p.input_do.screen.addEventListener("touchstart", p.inputFocusInHandler)), p.input_do.screen.addEventListener("keyup", p.keyUpHandler), p.mainHolder_do.addChild(p.input_do), p.mainHolder_do.addChild(p.inputArrow_do)
            }, this.inputFocusInHandler = function() {
                p.hasInputFocus_bl || (p.hasInputFocus_bl = !0, "search" == p.input_do.screen.value && (p.input_do.screen.value = ""), p.input_do.screen.focus(), setTimeout(function() {
                    p.hasPointerEvent_bl ? window.addEventListener("pointerdown", p.inputFocusOutHandler) : window.addEventListener && (window.addEventListener("mousedown", p.inputFocusOutHandler), window.addEventListener("touchstart", p.inputFocusOutHandler))
                }, 50))
            }, this.inputFocusOutHandler = function(e) {
                if (p.hasInputFocus_bl) {
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                    return FWDMSPUtils.hitTest(p.input_do.screen, t.screenX, t.screenY) ? void 0 : (p.hasInputFocus_bl = !1, void("" == p.input_do.screen.value && (p.input_do.screen.value = "search", p.hasPointerEvent_bl ? window.removeEventListener("pointerdown", p.inputFocusOutHandler) : window.removeEventListener && (window.removeEventListener("mousedown", p.inputFocusOutHandler), window.removeEventListener("touchstart", p.inputFocusOutHandler)))))
                }
            }, this.keyUpHandler = function(e) {
                e.stopPropagation && e.stopPropagation(), p.prevInputValue_str != p.input_do.screen.value && (clearTimeout(p.keyPressedId_to), p.keyPressed_bl = !0, clearTimeout(p.rsId_to), p.rsId_to = setTimeout(function() {
                    p.resizeAndPositionThumbnails(!0), p.disableEnableNextAndPrevButtons()
                }, 400)), p.prevInputValue_str = p.input_do.screen.value, p.keyPressedId_to = setTimeout(function() {
                    p.keyPressed_bl = !1
                }, 450)
            }, this.showNothingFound = function() {
                p.isShowNothingFound_bl || (p.isShowNothingFound_bl = !0, p.noSearchFound_do.setVisible(!0), p.noSearchFound_do.setY(parseInt((p.stageHeight - p.noSearchFound_do.getHeight()) / 2)), p.noSearchFound_do.setAlpha(0), FWDAnimation.to(p.noSearchFound_do, .1, {
                    alpha: 1,
                    yoyo: !0,
                    repeat: 4
                }))
            }, this.hideNothingFound = function() {
                p.isShowNothingFound_bl && (p.isShowNothingFound_bl = !1, FWDAnimation.killTweensOf(p.noSearchFound_do), p.noSearchFound_do.setVisible(!1))
            }, this.setupDisable = function() {
                p.disable_do = new FWDMSPDisplayObject("div"), FWDMSPUtils.isIE && (p.disable_do.setBkColor("#FFFFFF"), p.disable_do.setAlpha(.01)), p.addChild(p.disable_do)
            }, this.showDisable = function() {
                p.disable_do.w != p.stageWidth && (p.disable_do.setWidth(p.stageWidth), p.disable_do.setHeight(p.stageHeight))
            }, this.hideDisable = function() {
                0 != p.disable_do.w && (p.disable_do.setWidth(0), p.disable_do.setHeight(0))
            }, this.setupButtons = function() {
                FWDMSPSimpleButton.setPrototype(), p.closeButton_do = new FWDMSPSimpleButton(p.catCloseN_img, o.catCloseSPath_str, void 0, !0, o.useHEXColorsForSkin_bl, o.normalButtonsColor_str, p.selectedButtonsColor_str), p.closeButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.closeButtonOnMouseUpHandler), FWDMSPSimpleButton.setPrototype(), p.nextButton_do = new FWDMSPSimpleButton(p.catNextN_img, o.catNextSPath_str, void 0, !0, o.useHEXColorsForSkin_bl, o.normalButtonsColor_str, p.selectedButtonsColor_str), p.nextButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.nextButtonOnMouseUpHandler), FWDMSPSimpleButton.setPrototype(), p.prevButton_do = new FWDMSPSimpleButton(p.catPrevN_img, o.catPrevSPath_str, void 0, !0, o.useHEXColorsForSkin_bl, o.normalButtonsColor_str, p.selectedButtonsColor_str), p.prevButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.prevButtonOnMouseUpHandler)
            }, this.closeButtonOnMouseUpHandler = function() {
                p.hide()
            }, this.nextButtonOnMouseUpHandler = function() {
                var e = p.howManyThumbsToDisplayH * p.howManyThumbsToDisplayV;
                p.tempId += e, p.tempId > p.totalThumbnails - 1 && (p.tempId = p.totalThumbnails - 1);
                var t = Math.floor(p.tempId / e);
                p.tempId = t * e, p.resizeAndPositionThumbnails(!0, "next"), p.disableEnableNextAndPrevButtons(!1, !0)
            }, this.prevButtonOnMouseUpHandler = function() {
                var e = p.howManyThumbsToDisplayH * p.howManyThumbsToDisplayV;
                p.tempId -= e, p.tempId < 0 && (p.tempId = 0);
                var t = Math.floor(p.tempId / e);
                p.tempId = t * e, p.resizeAndPositionThumbnails(!0, "prev"), p.disableEnableNextAndPrevButtons(!0, !1)
            }, this.positionButtons = function() {
                p.closeButton_do.setX(p.stageWidth - p.closeButton_do.w - p.buttonsMargins), p.closeButton_do.setY(p.buttonsMargins), p.nextButton_do.setX(p.stageWidth - p.nextButton_do.w - p.buttonsMargins), p.nextButton_do.setY(parseInt((p.stageHeight - p.nextButton_do.h) / 2)), p.prevButton_do.setX(p.buttonsMargins), p.prevButton_do.setY(parseInt((p.stageHeight - p.prevButton_do.h) / 2))
            }, this.disableEnableNextAndPrevButtons = function(e, t) {
                var o = p.howManyThumbsToDisplayH * p.howManyThumbsToDisplayV,
                    s = Math.floor(p.tempId / o),
                    i = Math.ceil(p.totalThumbnails / o) - 1;
                p.howManyThumbsToDisplayH, p.howManyThumbsToDisplayH;
                o >= p.totalThumbnails ? (p.nextButton_do.disable(), p.prevButton_do.disable(), p.nextButton_do.setDisabledState(), p.prevButton_do.setDisabledState()) : 0 == s ? (p.nextButton_do.enable(), p.prevButton_do.disable(), p.nextButton_do.setEnabledState(), p.prevButton_do.setDisabledState()) : (s == i ? (p.nextButton_do.disable(), p.prevButton_do.enable(), p.nextButton_do.setDisabledState()) : (p.nextButton_do.enable(), p.prevButton_do.enable(), p.nextButton_do.setEnabledState()), p.prevButton_do.setEnabledState()), e || p.prevButton_do.setNormalState(), t || p.nextButton_do.setNormalState()
            }, this.setupMobileMove = function() {
                p.hasPointerEvent_bl ? p.screen.addEventListener("pointerdown", p.mobileDownHandler) : p.screen.addEventListener("touchstart", p.mobileDownHandler)
            }, this.mobileDownHandler = function(e) {
                if (!e.touches || 1 == e.touches.length) {
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                    p.mouseX = t.screenX, p.mouseY = t.screenY, p.hasPointerEvent_bl ? (window.addEventListener("pointerup", p.mobileUpHandler), window.addEventListener("pointermove", p.mobileMoveHandler)) : (window.addEventListener("touchend", p.mobileUpHandler), window.addEventListener("touchmove", p.mobileMoveHandler))
                }
            }, this.mobileMoveHandler = function(e) {
                if (e.preventDefault && e.preventDefault(), !e.touches || 1 == e.touches.length) {
                    p.showDisable();
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                    p.dif = p.mouseX - t.screenX, p.mouseX = t.screenX, p.mouseY = t.screenY
                }
            }, this.mobileUpHandler = function(e) {
                p.hideDisable(), 10 < p.dif ? p.nextButtonOnMouseUpHandler() : p.dif < -10 && p.prevButtonOnMouseUpHandler(), p.dif = 0, p.hasPointerEvent_bl ? (window.removeEventListener("pointerup", p.mobileUpHandler), window.removeEventListener("pointermove", p.mobileMoveHandler)) : (window.removeEventListener("touchend", p.mobileUpHandler), window.removeEventListener("touchmove", p.mobileMoveHandler))
            }, this.setupThumbnails = function() {
                if (!p.areThumbnailsCreated_bl) {
                    var e;
                    p.areThumbnailsCreated_bl = !0;
                    for (var t = 0; t < p.totalThumbnails; t++) FWDMSPCategoriesThumb.setPrototype(), (e = new FWDMSPCategoriesThumb(p, t, o.catThumbBkPath_str, o.catThumbBkTextPath_str, o.thumbnailSelectedType_str, p.categories_ar[t].htmlContent, p.categories_ar[t].htmlText_str)).addListener(FWDMSPCategoriesThumb.MOUSE_UP, p.thumbnailOnMouseUpHandler), p.thumbs_ar[t] = e, p.mainHolder_do.addChild(e);
                    p.mainHolder_do.addChild(p.closeButton_do), p.mainHolder_do.addChild(p.nextButton_do), p.mainHolder_do.addChild(p.prevButton_do)
                }
            }, this.thumbnailOnMouseUpHandler = function(e) {
                p.id = e.id, p.disableOrEnableThumbnails(), p.hide()
            }, this.resizeAndPositionThumbnails = function(e, t) {
                if (p.areThumbnailsCreated_bl) {
                    var o, s, i, n, l, r, a, d, u, c = [].concat(p.thumbs_ar);
                    if (p.isSearched_bl = !1, p.input_do && (inputValue = p.input_do.screen.value.toLowerCase(), "search" != inputValue))
                        for (var h = 0; h < c.length; h++) - 1 == (o = c[h]).htmlText_str.toLowerCase().indexOf(inputValue.toLowerCase()) && (FWDAnimation.killTweensOf(o), o.hide(), c.splice(h, 1), h--);
                    p.totalThumbnails = c.length, p.totalThumbnails != p.thumbs_ar.length && (p.isSearched_bl = !0), 0 == p.totalThumbnails ? p.showNothingFound() : p.hideNothingFound(), this.remainWidthSpace = this.stageWidth - n;
                    var _ = p.stageWidth - p.categoriesOffsetTotalWidth,
                        f = p.stageHeight - p.categoriesOffsetTotalHeight;
                    p.howManyThumbsToDisplayH = Math.ceil((_ - p.spacerH) / (p.thumbnailMaxWidth + p.spacerH)), p.thumbW = Math.floor((_ - p.spacerH * (p.howManyThumbsToDisplayH - 1)) / p.howManyThumbsToDisplayH), p.thumbW > p.thumbnailMaxWidth && (p.howManyThumbsToDisplayH += 1, p.thumbW = Math.floor((_ - p.spacerH * (p.howManyThumbsToDisplayH - 1)) / p.howManyThumbsToDisplayH)), p.thumbH = Math.floor(p.thumbW / p.thumbnailMaxWidth * p.thumbnailMaxHeight), p.howManyThumbsToDisplayV = Math.floor(f / (p.thumbH + p.spacerV)), p.howManyThumbsToDisplayV < 1 && (p.howManyThumbsToDisplayV = 1), n = Math.min(p.howManyThumbsToDisplayH, p.totalThumbnails) * (p.thumbW + p.spacerH) - p.spacerH, l = Math.min(Math.ceil(p.totalThumbnails / p.howManyThumbsToDisplayH), p.howManyThumbsToDisplayV) * (p.thumbH + p.spacerV) - p.spacerV, r = p.howManyThumbsToDisplayH > p.totalThumbnails ? 0 : _ - n, p.howManyThumbsToDisplayH > p.totalThumbnails && (p.howManyThumbsToDisplayH = p.totalThumbnails), u = p.howManyThumbsToDisplayH * p.howManyThumbsToDisplayV, s = Math.floor(p.tempId / u), p.isSearched_bl && (s = 0), d = p.howManyThumbsToDisplayH * s, firstId = s * u, (a = firstId + u) > p.totalThumbnails && (a = p.totalThumbnails);
                    for (h = 0; h < p.totalThumbnails; h++)(o = c[h]).finalW = p.thumbW, h % p.howManyThumbsToDisplayH == p.howManyThumbsToDisplayH - 1 && (o.finalW += r), o.finalH = p.thumbH, o.finalX = h % p.howManyThumbsToDisplayH * (p.thumbW + p.spacerH), o.finalX += Math.floor(h / u) * p.howManyThumbsToDisplayH * (p.thumbW + p.spacerH), o.finalX += (p.stageWidth - n) / 2, o.finalX = Math.floor(o.finalX - d * (p.thumbW + p.spacerH)), o.finalY = h % u, o.finalY = Math.floor(o.finalY / p.howManyThumbsToDisplayH) * (p.thumbH + p.spacerV), o.finalY += (f - l) / 2, o.finalY += p.categoriesOffsetTotalHeight / 2, o.finalY = Math.floor(o.finalY), s < (i = Math.floor(h / u)) ? o.finalX += 150 : i < s && (o.finalX -= 150), e ? h >= firstId && h < a ? (dl = "next" == t ? h % u * p.delayRate + .1 : (u - h % u) * p.delayRate + .1, p.keyPressed_bl && (dl = 0), o.resizeAndPosition(!0, dl)) : o.resizeAndPosition(!0, 0) : o.resizeAndPosition(), o.show();
                    p.howManyThumbsToDisplayH * p.howManyThumbsToDisplayV >= p.totalThumbnails ? (p.nextButton_do.setVisible(!1), p.prevButton_do.setVisible(!1)) : (p.nextButton_do.setVisible(!0), p.prevButton_do.setVisible(!0))
                }
            }, this.loadImages = function() {
                p.countLoadedThumbs > p.totalThumbnails - 1 || (p.image_img && (p.image_img.onload = null, p.image_img.onerror = null), p.image_img = new Image, p.image_img.onerror = p.onImageLoadError, p.image_img.onload = p.onImageLoadComplete, p.image_img.src = p.categories_ar[p.countLoadedThumbs].thumbnailPath)
            }, this.onImageLoadError = function(e) {}, this.onImageLoadComplete = function(e) {
                p.thumbs_ar[p.countLoadedThumbs].setImage(p.image_img), p.countLoadedThumbs++, p.loadWithDelayId_to = setTimeout(p.loadImages, 40)
            }, this.disableOrEnableThumbnails = function() {
                for (var e, t = 0; t < p.totalThumbnails; t++) e = p.thumbs_ar[t], t == p.id ? e.disable() : e.enable()
            }, this.show = function(e) {
                p.isShowed_bl || (p.isShowed_bl = !0, p.isOnDOM_bl = !0, p.id = e, FWDMSPUtils.isChrome && p.isMobile_bl ? p.setVisible(!0) : FWDMSPUtils.isIEAndLessThen9 ? document.getElementsByTagName("body")[0].appendChild(p.screen) : document.documentElement.appendChild(p.screen), window.addEventListener ? window.addEventListener("scroll", p.onScrollHandler) : window.attachEvent && window.attachEvent("onscroll", p.onScrollHandler), p.setupThumbnails(), p.resizeAndPosition(!0), p.showDisable(), p.disableOrEnableThumbnails(), clearTimeout(p.hideCompleteId_to), clearTimeout(p.showCompleteId_to), p.mainHolder_do.setY(-p.stageHeight), p.isMobile_bl ? (p.showCompleteId_to = setTimeout(p.showCompleteHandler, 1200), FWDAnimation.to(p.mainHolder_do, .8, {
                    y: 0,
                    delay: .4,
                    ease: Expo.easeInOut
                })) : (p.showCompleteId_to = setTimeout(p.showCompleteHandler, 800), FWDAnimation.to(p.mainHolder_do, .8, {
                    y: 0,
                    ease: Expo.easeInOut
                })))
            }, this.showCompleteHandler = function() {
                p.mainHolder_do.setY(0), p.hideDisable(), FWDMSPUtils.isIphone && (e.videoScreen_do && e.videoScreen_do.setY(-5e3), e.ytb_do && e.ytb_do.setY(-5e3)), p.resizeAndPosition(!0), p.areThumbnailsLoaded_bl || (p.loadImages(), p.areThumbnailsLoaded_bl = !0)
            }, this.hide = function() {
                p.isShowed_bl && (p.isShowed_bl = !1, FWDMSPUtils.isIphone && (e.videoScreen_do && e.videoScreen_do.setY(0), e.ytb_do && e.ytb_do.setY(0)), clearTimeout(p.hideCompleteId_to), clearTimeout(p.showCompleteId_to), p.showDisable(), p.hideCompleteId_to = setTimeout(p.hideCompleteHandler, 800), FWDAnimation.killTweensOf(p.mainHolder_do), FWDAnimation.to(p.mainHolder_do, .8, {
                    y: -p.stageHeight,
                    ease: Expo.easeInOut
                }), window.addEventListener ? window.removeEventListener("scroll", p.onScrollHandler) : window.detachEvent && window.detachEvent("onscroll", p.onScrollHandler), p.resizeAndPosition())
            }, this.hideCompleteHandler = function() {
                FWDMSPUtils.isChrome && p.isMobile_bl ? p.setVisible(!1) : FWDMSPUtils.isIEAndLessThen9 ? document.getElementsByTagName("body")[0].removeChild(p.screen) : document.documentElement.removeChild(p.screen), p.isOnDOM_bl = !1, p.dispatchEvent(t.HIDE_COMPLETE)
            }, this.updateHEXColors = function(e, t) {
                -1 != o.skinPath_str.indexOf("hex_white") ? p.selectedColor_str = "#FFFFFF" : p.selectedColor_str = t, p.closeButton_do.updateHEXColors(e, p.selectedColor_str), p.nextButton_do.updateHEXColors(e, p.selectedColor_str), p.prevButton_do.updateHEXColors(e, p.selectedColor_str)
            }, this.init()
        };
        t.setPrototype = function() {
            t.prototype = new FWDMSPDisplayObject("div")
        }, t.HIDE_COMPLETE = "hideComplete", t.prototype = null, window.FWDMSPCategories = t
    }(),
    function(e) {
        var a = function(t, e, o, s, i, n, l) {
            var r = this;
            a.prototype;
            this.backgroundImagePath_str = o, this.catThumbTextBkPath_str = s, this.canvas_el = null, this.htmlContent = n, this.simpleText_do = null, this.effectImage_do = null, this.imageHolder_do = null, this.normalImage_do = null, this.effectImage_do = null, this.dumy_do = null, this.htmlText_str = l, this.thumbnailSelectedType_str = i, this.id = e, this.imageOriginalW, this.imageOriginalH, this.finalX, this.finalY, this.finalW, this.finalH, this.imageFinalX, this.imageFinalY, this.imageFinalW, this.imageFinalH, this.dispatchShowWithDelayId_to, this.isShowed_bl = !1, this.hasImage_bl = !1, this.isSelected_bl = !1, this.isDisabled_bl = !1, this.hasCanvas_bl = FWDMSP.hasCanvas, this.isMobile_bl = FWDMSPUtils.isMobile, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, this.init = function() {
                r.getStyle().background = "url('" + r.backgroundImagePath_str + "')", r.setupMainContainers(), r.setupDescription(), r.setupDumy()
            }, this.setupMainContainers = function() {
                r.imageHolder_do = new FWDMSPDisplayObject("div"), r.addChild(r.imageHolder_do)
            }, this.setupDumy = function() {
                r.dumy_do = new FWDMSPDisplayObject("div"), FWDMSPUtils.isIE && (r.dumy_do.setBkColor("#FFFFFF"), r.dumy_do.setAlpha(0)), r.addChild(r.dumy_do)
            }, this.setupDescription = function() {
                r.simpleText_do = new FWDMSPDisplayObject("div"), r.simpleText_do.getStyle().background = "url('" + r.catThumbTextBkPath_str + "')", FWDMSPUtils.isFirefox && (r.simpleText_do.hasTransform3d_bl = !1, r.simpleText_do.hasTransform2d_bl = !1), r.simpleText_do.setBackfaceVisibility(), r.simpleText_do.getStyle().width = "100%", r.simpleText_do.getStyle().fontFamily = "Arial", r.simpleText_do.getStyle().fontSize = "12px", r.simpleText_do.getStyle().textAlign = "left", r.simpleText_do.getStyle().color = "#FFFFFF", r.simpleText_do.getStyle().fontSmoothing = "antialiased", r.simpleText_do.getStyle().webkitFontSmoothing = "antialiased", r.simpleText_do.getStyle().textRendering = "optimizeLegibility", r.simpleText_do.setInnerHTML(r.htmlContent), r.addChild(r.simpleText_do)
            }, this.positionDescription = function() {
                r.simpleText_do.setY(parseInt(r.finalH - r.simpleText_do.getHeight()))
            }, this.setupBlackAndWhiteImage = function(e) {
                if (r.hasCanvas_bl && "opacity" != r.thumbnailSelectedType_str) {
                    var t = document.createElement("canvas"),
                        o = t.getContext("2d");
                    t.width = r.imageOriginalW, t.height = r.imageOriginalH, o.drawImage(e, 0, 0);
                    var s = o.getImageData(0, 0, t.width, t.height),
                        i = s.data;
                    if ("threshold" == r.thumbnailSelectedType_str)
                        for (var n = 0; n < i.length; n += 4) {
                            var l = 150 <= .2126 * i[n] + .7152 * i[n + 1] + .0722 * i[n + 2] ? 255 : 0;
                            i[n] = i[n + 1] = i[n + 2] = l
                        } else if ("blackAndWhite" == r.thumbnailSelectedType_str)
                            for (n = 0; n < i.length; n += 4) {
                                l = .2126 * i[n] + .7152 * i[n + 1] + .0722 * i[n + 2];
                                i[n] = i[n + 1] = i[n + 2] = l
                            }
                    o.putImageData(s, 0, 0, 0, 0, s.width, s.height), r.effectImage_do = new FWDMSPDisplayObject("canvas"), r.effectImage_do.screen = t, r.effectImage_do.setAlpha(.9), r.effectImage_do.setMainProperties()
                }
            }, this.setImage = function(e) {
                r.normalImage_do = new FWDMSPDisplayObject("img"), r.normalImage_do.setScreen(e), r.imageOriginalW = r.normalImage_do.w, r.imageOriginalH = r.normalImage_do.h, r.setButtonMode(!0), r.setupBlackAndWhiteImage(e), r.resizeImage(), r.imageHolder_do.setX(parseInt(r.finalW / 2)), r.imageHolder_do.setY(parseInt(r.finalH / 2)), r.imageHolder_do.setWidth(0), r.imageHolder_do.setHeight(0), r.normalImage_do.setX(-parseInt(r.normalImage_do.w / 2)), r.normalImage_do.setY(-parseInt(r.normalImage_do.h / 2)), r.normalImage_do.setAlpha(0), r.effectImage_do && (r.effectImage_do.setX(-parseInt(r.normalImage_do.w / 2)), r.effectImage_do.setY(-parseInt(r.normalImage_do.h / 2)), r.effectImage_do.setAlpha(.01)), FWDAnimation.to(r.imageHolder_do, .8, {
                    x: 0,
                    y: 0,
                    w: r.finalW,
                    h: r.finalH,
                    ease: Expo.easeInOut
                }), FWDAnimation.to(r.normalImage_do, .8, {
                    alpha: 1,
                    x: r.imageFinalX,
                    y: r.imageFinalY,
                    ease: Expo.easeInOut
                }), r.effectImage_do && FWDAnimation.to(r.effectImage_do, .8, {
                    x: r.imageFinalX,
                    y: r.imageFinalY,
                    ease: Expo.easeInOut
                }), r.isMobile_bl ? r.hasPointerEvent_bl ? (r.screen.addEventListener("pointerup", r.onMouseUp), r.screen.addEventListener("pointerover", r.onMouseOver), r.screen.addEventListener("pointerout", r.onMouseOut)) : r.screen.addEventListener("mouseup", r.onMouseUp) : r.screen.addEventListener ? (r.screen.addEventListener("mouseover", r.onMouseOver), r.screen.addEventListener("mouseout", r.onMouseOut), r.screen.addEventListener("mouseup", r.onMouseUp)) : r.screen.attachEvent && (r.screen.attachEvent("onmouseover", r.onMouseOver), r.screen.attachEvent("onmouseout", r.onMouseOut), r.screen.attachEvent("onmouseup", r.onMouseUp)), this.imageHolder_do.addChild(r.normalImage_do), r.effectImage_do && r.imageHolder_do.addChild(r.effectImage_do), this.hasImage_bl = !0, r.id == t.id && r.disable()
            }, r.onMouseOver = function(e, t) {
                r.isDisabled_bl || e.pointerType && e.pointerType != e.MSPOINTER_TYPE_MOUSE || r.setSelectedState(!0)
            }, r.onMouseOut = function(e) {
                r.isDisabled_bl || e.pointerType && e.pointerType != e.MSPOINTER_TYPE_MOUSE || r.setNormalState(!0)
            }, r.onMouseUp = function(e) {
                r.isDisabled_bl || 2 == e.button || (e.preventDefault && e.preventDefault(), r.dispatchEvent(a.MOUSE_UP, {
                    id: r.id
                }))
            }, this.resizeAndPosition = function(e, t) {
                FWDAnimation.killTweensOf(r), FWDAnimation.killTweensOf(r.imageHolder_do), e ? FWDAnimation.to(r, .8, {
                    x: r.finalX,
                    y: r.finalY,
                    delay: t,
                    ease: Expo.easeInOut
                }) : (r.setX(r.finalX), r.setY(r.finalY)), r.setWidth(r.finalW), r.setHeight(r.finalH), r.imageHolder_do.setX(0), r.imageHolder_do.setY(0), r.imageHolder_do.setWidth(r.finalW), r.imageHolder_do.setHeight(r.finalH), r.dumy_do.setWidth(r.finalW), r.dumy_do.setHeight(r.finalH), r.resizeImage(), r.positionDescription()
            }, this.resizeImage = function(e) {
                if (r.normalImage_do) {
                    FWDAnimation.killTweensOf(r.normalImage_do);
                    var t, o = r.finalW / r.imageOriginalW,
                        s = r.finalH / r.imageOriginalH;
                    t = s <= o ? o : s, r.imageFinalW = Math.ceil(t * r.imageOriginalW), r.imageFinalH = Math.ceil(t * r.imageOriginalH), r.imageFinalX = Math.round((r.finalW - r.imageFinalW) / 2), r.imageFinalY = Math.round((r.finalH - r.imageFinalH) / 2), r.effectImage_do && (FWDAnimation.killTweensOf(r.effectImage_do), r.effectImage_do.setX(r.imageFinalX), r.effectImage_do.setY(r.imageFinalY), r.effectImage_do.setWidth(r.imageFinalW), r.effectImage_do.setHeight(r.imageFinalH), r.isDisabled_bl && r.setSelectedState(!1, !0)), r.normalImage_do.setX(r.imageFinalX), r.normalImage_do.setY(r.imageFinalY), r.normalImage_do.setWidth(r.imageFinalW), r.normalImage_do.setHeight(r.imageFinalH), r.isDisabled_bl ? r.normalImage_do.setAlpha(.3) : r.normalImage_do.setAlpha(1)
                }
            }, this.setNormalState = function(e) {
                r.isSelected_bl && (r.isSelected_bl = !1, "threshold" == r.thumbnailSelectedType_str || "blackAndWhite" == r.thumbnailSelectedType_str ? e ? FWDAnimation.to(r.effectImage_do, 1, {
                    alpha: .01,
                    ease: Quart.easeOut
                }) : r.effectImage_do.setAlpha(.01) : "opacity" == r.thumbnailSelectedType_str && (e ? FWDAnimation.to(r.normalImage_do, 1, {
                    alpha: 1,
                    ease: Quart.easeOut
                }) : r.normalImage_do.setAlpha(1)))
            }, this.setSelectedState = function(e, t) {
                r.isSelected_bl && !t || (r.isSelected_bl = !0, "threshold" == r.thumbnailSelectedType_str || "blackAndWhite" == r.thumbnailSelectedType_str ? e ? FWDAnimation.to(r.effectImage_do, 1, {
                    alpha: 1,
                    ease: Expo.easeOut
                }) : r.effectImage_do.setAlpha(1) : "opacity" == r.thumbnailSelectedType_str && (e ? FWDAnimation.to(r.normalImage_do, 1, {
                    alpha: .3,
                    ease: Expo.easeOut
                }) : r.normalImage_do.setAlpha(.3)))
            }, this.show = function() {
                FWDAnimation.to(r, .8, {
                    scale: 1,
                    ease: Expo.easeInOut
                })
            }, this.hide = function() {
                FWDAnimation.to(r, .8, {
                    scale: 0,
                    ease: Expo.easeInOut
                })
            }, this.enable = function() {
                r.hasImage_bl && (r.isDisabled_bl = !1, r.setButtonMode(!0), r.setNormalState(!0))
            }, this.disable = function() {
                r.hasImage_bl && (r.isDisabled_bl = !0, r.setButtonMode(!1), r.setSelectedState(!0))
            }, this.init()
        };
        a.setPrototype = function() {
            a.prototype = new FWDMSPTransformDisplayObject("div")
        }, a.MOUSE_UP = "onMouseUp", a.prototype = null, e.FWDMSPCategoriesThumb = a
    }(window),
    function(r) {
        var t = function(i, n) {
            var l = this,
                e = t.prototype;
            this.categories_ar = n.categories_ar, this.buttons_ar = [], this.mainHolder_do = null, this.selector_do = null, this.mainButtonsHolder_do = null, this.buttonsHolder_do = null, this.arrowW = n.arrowW, this.arrowH = n.arrowH, l.useHEXColorsForSkin_bl = i.data.useHEXColorsForSkin_bl, l.normalButtonsColor_str = i.data.normalButtonsColor_str, l.selectedButtonsColor_str = i.data.selectedButtonsColor_str, this.arrowN_str = n.arrowN_str, this.arrowS_str = n.arrowS_str, this.bk1_str = n.bk1_str, this.bk2_str = n.bk2_str, this.selectorLabel_str = n.selectorLabel, this.selectorBkColorN_str = n.selectorBackgroundNormalColor, this.selectorBkColorS_str = n.selectorBackgroundSelectedColor, this.selectorTextColorN_str = n.selectorTextNormalColor, this.selectorTextColorS_str = n.selectorTextSelectedColor, this.itemBkColorN_str = n.buttonBackgroundNormalColor, this.itemBkColorS_str = n.buttonBackgroundSelectedColor, this.itemTextColorN_str = n.buttonTextNormalColor, this.itemTextColorS_str = n.buttonTextSelectedColor, this.scrollBarHandlerFinalY = 0, this.finalX, this.finalY, this.totalButtons = l.categories_ar.length, this.curId = n.startAtPlaylist, this.buttonsHolderWidth = 0, this.buttonsHolderHeight = 0, this.totalWidth = i.stageWidth, this.buttonHeight = n.buttonHeight, this.totalButtonsHeight = 0, this.sapaceBetweenButtons = 0, this.thumbnailsFinalY = 0, this.vy = 0, this.vy2 = 0, this.friction = .9, this.hideMenuTimeOutId_to, this.getMaxWidthResizeAndPositionId_to, this.isShowed_bl = !1, this.addMouseWheelSupport_bl = i.data.addScrollBarMouseWheelSupport_bl, this.scollbarSpeedSensitivity = .5, this.isOpened_bl = !1, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, this.isMobile_bl = FWDMSPUtils.isMobile, this.init = function() {
                l.setOverflow("visible"), l.setupMainContainers(), l.setupScrollLogic(), l.getMaxWidthResizeAndPosition(), l.setupSeparator(), l.mainButtonsHolder_do.setVisible(!1), l.bk_do.setVisible(!1)
            }, this.setupSeparator = function() {
                l.separator_do = new FWDMSPDisplayObject("div"), l.separator_do.setBackfaceVisibility(), l.separator_do.hasTransform3d_bl = !1, l.separator_do.hasTransform2d_bl = !1, l.separator_do.getStyle().background = "url('" + i.playlistSeparator_img.src + "')", l.separator_do.setHeight(i.playlistSeparator_img.height), l.separator_do.setY(l.buttonHeight), l.addChild(l.separator_do)
            }, this.setupMainContainers = function() {
                var e;
                if (l.mainHolder_do = new FWDMSPDisplayObject("div"), l.mainHolder_do.setOverflow("visible"), l.addChild(l.mainHolder_do), l.bk_do = new FWDMSPDisplayObject("div"), l.bk_do.setY(l.buttonHeight), l.bk_do.setBkColor(i.playlistBackgroundColor_str), l.bk_do.setAlpha(0), l.mainHolder_do.addChild(l.bk_do), l.mainButtonsHolder_do = new FWDMSPDisplayObject("div"), l.mainButtonsHolder_do.setY(l.buttonHeight), l.mainHolder_do.addChild(l.mainButtonsHolder_do), i.expandPlaylistBackground_bl) {
                    l.dummyBk_do = new FWDMSPDisplayObject("img");
                    var t = new Image;
                    t.src = i.controllerBkPath_str, l.dummyBk_do.setScreen(t), l.dummyBk_do.getStyle().backgroundColor = "#000000"
                } else l.dummyBk_do = new FWDMSPDisplayObject("div"), l.dummyBk_do.getStyle().background = "url('" + i.controllerBkPath_str + "')";
                l.dummyBk_do.setHeight(l.buttonHeight), l.mainHolder_do.addChild(l.dummyBk_do), l.buttonsHolder_do = new FWDMSPDisplayObject("div"), l.mainButtonsHolder_do.addChild(l.buttonsHolder_do);
                var o = l.selectorLabel_str;
                "default" == l.selectorLabel_str && (o = l.categories_ar[l.curId]), FWDMSPComboBoxSelector.setPrototype(), l.selector_do = new FWDMSPComboBoxSelector(11, 6, n.arrowN_str, n.arrowS_str, o, l.selectorBkColorN_str, l.selectorBkColorS_str, l.selectorTextColorN_str, l.selectorTextColorS_str, l.buttonHeight, l.useHEXColorsForSkin_bl, l.normalButtonsColor_str, l.selectedButtonsColor_str), l.mainHolder_do.addChild(l.selector_do), l.selector_do.setNormalState(!1), l.selector_do.addListener(FWDMSPComboBoxSelector.MOUSE_DOWN, l.openMenuHandler);
                for (var s = 0; s < l.totalButtons; s++) FWDMSPComboBoxButton.setPrototype(), e = new FWDMSPComboBoxButton(l, l.categories_ar[s], l.bk1_str, l.bk2_str, l.itemBkColorN_str, l.itemBkColorS_str, l.itemTextColorN_str, l.itemTextColorS_str, s, l.buttonHeight), (l.buttons_ar[s] = e).addListener(FWDMSPComboBoxButton.MOUSE_DOWN, l.buttonOnMouseDownHandler), l.buttonsHolder_do.addChild(e)
            }, this.buttonOnMouseDownHandler = function(e) {
                l.curId = e.target.id, clearTimeout(l.hideMenuTimeOutId_to), l.hide(!1), l.selector_do.enable(), l.isMobile_bl ? l.hasPointerEvent_bl ? r.removeEventListener("MSPointerDown", l.checkOpenedMenu) : r.removeEventListener("touchstart", l.checkOpenedMenu) : r.addEventListener ? (r.removeEventListener("mousedown", l.checkOpenedMenu), r.removeEventListener("mousemove", l.checkOpenedMenu)) : document.attachEvent && document.detachEvent("onmousemove", l.checkOpenedMenu), i.data.showPlaylistsSelectBoxNumbers_bl ? l.selector_do.setText(l.buttons_ar[l.curId].label1_str.substr(4)) : l.selector_do.setText(l.buttons_ar[l.curId].label1_str), l.isButtonCliecked_bl = !0, l.dispatchEvent(t.BUTTON_PRESSED, {
                    id: l.curId
                })
            }, this.openMenuHandler = function(e) {
                FWDAnimation.isTweening(l.mainButtonsHolder_do) || (l.isShowed_bl ? l.checkOpenedMenu(e.e, !0) : (l.selector_do.disable(), l.show(!0), l.startToCheckOpenedMenu(), l.dispatchEvent(t.OPEN)))
            }, this.setButtonsStateBasedOnId = function(e) {
                l.curId = e;
                for (var t = 0; t < l.totalButtons; t++) button_do = l.buttons_ar[t], t == l.curId ? button_do.disable() : button_do.enable();
                i.data.showPlaylistsSelectBoxNumbers_bl ? l.selector_do.setText(l.buttons_ar[l.curId].label1_str.substr(4)) : l.selector_do.setText(l.buttons_ar[l.curId].label1_str), l.scrHandler_do ? (l.updateScrollBarSizeActiveAndDeactivate(), l.updateScrollBarHandlerAndContent(!1, !0)) : l.thumbnailsFinalY = 0
            }, this.setValue = function(e) {
                l.curId = e, l.setButtonsStateBasedOnId()
            }, this.startToCheckOpenedMenu = function(e) {
                l.isMobile_bl ? l.hasPointerEvent_bl ? r.addEventListener("MSPointerDown", l.checkOpenedMenu) : r.addEventListener("touchstart", l.checkOpenedMenu) : r.addEventListener ? r.addEventListener("mousedown", l.checkOpenedMenu) : document.attachEvent && document.attachEvent("onmousemove", l.checkOpenedMenu)
            }, this.checkOpenedMenu = function(e, t) {
                e.preventDefault && e.preventDefault();
                var o = FWDMSPUtils.getViewportMouseCoordinates(e),
                    s = 1e3;
                "mousedown" == e.type && (s = 0), !FWDMSPUtils.hitTest(l.screen, o.screenX, o.screenY) && !FWDMSPUtils.hitTest(l.mainButtonsHolder_do.screen, o.screenX, o.screenY) || t ? (l.isMobile_bl ? (l.hide(!0), l.selector_do.enable()) : (clearTimeout(l.hideMenuTimeOutId_to), l.hideMenuTimeOutId_to = setTimeout(function() {
                    l.hide(!0), l.selector_do.enable()
                }, s)), l.isMobile_bl ? l.hasPointerEvent_bl ? r.removeEventListener("MSPointerDown", l.checkOpenedMenu) : r.removeEventListener("touchstart", l.checkOpenedMenu) : r.addEventListener ? (r.removeEventListener("mousemove", l.checkOpenedMenu), r.removeEventListener("mousedown", l.checkOpenedMenu)) : document.attachEvent && document.detachEvent("onmousemove", l.checkOpenedMenu)) : clearTimeout(l.hideMenuTimeOutId_to)
            }, l.getMaxWidthResizeAndPosition = function() {
                for (var e, t = l.totalButtonsHeight = 0; t < l.totalButtons; t++)(e = l.buttons_ar[t]).setY(1 + t * (e.totalHeight + l.sapaceBetweenButtons)), l.allowToScrollAndScrollBarIsActive_bl && !l.isMobile_bl ? l.totalWidth = i.stageWidth - 6 : l.totalWidth = i.stageWidth, e.totalWidth = l.totalWidth, e.setWidth(l.totalWidth), e.centerText();
                l.totalButtonsHeight = e.getY() + e.totalHeight - l.sapaceBetweenButtons, l.dummyBk_do.setWidth(l.totalWidth + 6), l.setWidth(l.totalWidth), l.setHeight(l.buttonHeight), l.selector_do.totalWidth = l.totalWidth + 6, l.selector_do.setWidth(l.totalWidth + 6), l.selector_do.centerText(), l.buttonsHolder_do.setWidth(l.totalWidth), l.buttonsHolder_do.setHeight(l.totalButtonsHeight)
            }, this.position = function() {
                FWDMSPUtils.isAndroid ? (l.setX(Math.floor(l.finalX)), l.setY(Math.floor(l.finalY - 1)), setTimeout(l.poscombo - box, 100)) : (l.poscombo, box())
            }, this.resizeAndPosition = function() {
                l.stageWidth = i.stageWidth, l.stageHeight = i.stageHeight, l.bk_do.setWidth(l.stageWidth), l.bk_do.setHeight(l.stageHeight), l.mainButtonsHolder_do.setWidth(l.stageWidth), l.mainButtonsHolder_do.setHeight(l.stageHeight), l.totalButtonsHeight > l.mainButtonsHolder_do.h ? l.allowToScrollAndScrollBarIsActive_bl = !0 : l.allowToScrollAndScrollBarIsActive_bl = !1, !l.allowToScrollAndScrollBarIsActive_bl && l.scrMainHolder_do ? l.scrMainHolder_do.setVisible(!1) : l.allowToScrollAndScrollBarIsActive_bl && l.scrMainHolder_do && l.isShowed_bl && l.scrMainHolder_do.setVisible(!0), l.separator_do.setWidth(l.stageWidth), l.scrHandler_do && l.updateScrollBarSizeActiveAndDeactivate(), this.getMaxWidthResizeAndPosition(), l.updateScrollBarHandlerAndContent()
            }, this.hide = function(e, t) {
                (l.isShowed_bl || t) && (FWDAnimation.killTweensOf(this), l.isShowed_bl = !1, FWDAnimation.killTweensOf(l.mainButtonsHolder_do), FWDAnimation.killTweensOf(l.bk_do), e ? (FWDAnimation.to(l.mainButtonsHolder_do, .8, {
                    y: -l.totalButtonsHeight,
                    ease: Expo.easeInOut,
                    onComplete: l.hideComplete
                }), FWDAnimation.to(l.bk_do, .8, {
                    alpha: 0
                })) : (l.bk_do.setVisible(!1), l.mainButtonsHolder_do.setY(l.buttonHeight - l.totalButtonsHeight), l.bk_do.setAlpha(0), l.setHeight(l.buttonHeight), l.hideComplete()))
            }, this.hideComplete = function() {
                l.mainButtonsHolder_do.setVisible(!1), l.bk_do.setVisible(!1)
            }, this.show = function(e, t) {
                l.isShowed_bl && !t || (FWDAnimation.killTweensOf(this), l.mainButtonsHolder_do.setY(-l.totalButtonsHeight), l.isShowed_bl = !0, l.mainButtonsHolder_do.setVisible(!0), l.bk_do.setVisible(!0), l.resizeAndPosition(), FWDAnimation.killTweensOf(l.mainButtonsHolder_do), FWDAnimation.killTweensOf(l.bk_do), l.scrMainHolder_do && l.allowToScrollAndScrollBarIsActive_bl && l.scrMainHolder_do.setVisible(!0), e ? (FWDAnimation.to(l.bk_do, .8, {
                    alpha: 1
                }), FWDAnimation.to(l.mainButtonsHolder_do, .8, {
                    y: l.buttonHeight,
                    ease: Expo.easeInOut
                })) : (l.bk_do.setAlpha(1), l.mainButtonsHolder_do.setY(l.buttonHeight)))
            }, this.setupScrollLogic = function() {
                l.isMobile_bl ? l.setupMobileScrollbar() : (l.setupScrollbar(), l.addMouseWheelSupport_bl && l.addMouseWheelSupport())
            }, this.setupMobileScrollbar = function() {
                l.hasPointerEvent_bl ? l.mainButtonsHolder_do.screen.addEventListener("pointerdown", l.scrollBarTouchStartHandler) : l.mainButtonsHolder_do.screen.addEventListener("touchstart", l.scrollBarTouchStartHandler), l.mainButtonsHolder_do.screen.addEventListener("mousedown", l.scrollBarTouchStartHandler), l.updateMobileScrollBarId_int = setInterval(l.updateMobileScrollBar, 16)
            }, this.scrollBarTouchStartHandler = function(e) {
                e.preventDefault && e.preventDefault(), l.isScrollingOnMove_bl = !1, FWDAnimation.killTweensOf(l.buttonsHolder_do);
                var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                l.isDragging_bl = !0, l.lastPresedY = t.screenY, l.checkLastPresedY = t.screenY, l.hasPointerEvent_bl ? (r.addEventListener("pointerup", l.scrollBarTouchEndHandler), r.addEventListener("pointermove", l.scrollBarTouchMoveHandler)) : (r.addEventListener("touchend", l.scrollBarTouchEndHandler), r.addEventListener("touchmove", l.scrollBarTouchMoveHandler)), r.addEventListener("mouseup", l.scrollBarTouchEndHandler), r.addEventListener("mousemove", l.scrollBarTouchMoveHandler), clearInterval(l.updateMoveMobileScrollbarId_int), l.updateMoveMobileScrollbarId_int = setInterval(l.updateMoveMobileScrollbar, 20)
            }, this.scrollBarTouchMoveHandler = function(e) {
                if (e.preventDefault && e.preventDefault(), e.stopImmediatePropagation(), !(l.totalButtonsHeight < l.mainButtonsHolder_do.h)) {
                    i.showDisable();
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                    (t.screenY >= l.checkLastPresedY + 6 || t.screenY <= l.checkLastPresedY - 6) && (l.isScrollingOnMove_bl = !0);
                    var o = t.screenY - l.lastPresedY;
                    l.thumbnailsFinalY += o, l.thumbnailsFinalY = Math.round(l.thumbnailsFinalY), l.lastPresedY = t.screenY, l.vy = 2 * o
                }
            }, this.scrollBarTouchEndHandler = function(e) {
                l.isDragging_bl = !1, clearInterval(l.updateMoveMobileScrollbarId_int), clearTimeout(l.disableOnMoveId_to), l.disableOnMoveId_to = setTimeout(function() {
                    i.hideDisable()
                }, 100), l.hasPointerEvent_bl ? (r.removeEventListener("pointerup", l.scrollBarTouchEndHandler), r.removeEventListener("pointermove", l.scrollBarTouchMoveHandler)) : (r.removeEventListener("touchend", l.scrollBarTouchEndHandler), r.removeEventListener("touchmove", l.scrollBarTouchMoveHandler)), r.removeEventListener("mousemove", l.scrollBarTouchMoveHandler)
            }, this.updateMoveMobileScrollbar = function() {
                l.buttonsHolder_do.setY(l.thumbnailsFinalY)
            }, this.updateMobileScrollBar = function(e) {
                l.isDragging_bl || (l.totalButtonsHeight < l.mainButtonsHolder_do.h && (l.thumbnailsFinalY = .01), l.vy *= l.friction, l.thumbnailsFinalY += l.vy, 0 < l.thumbnailsFinalY ? (l.vy2 = .3 * (0 - l.thumbnailsFinalY), l.vy *= l.friction, l.thumbnailsFinalY += l.vy2) : l.thumbnailsFinalY < l.mainButtonsHolder_do.h - l.totalButtonsHeight && (l.vy2 = .3 * (l.mainButtonsHolder_do.h - l.totalButtonsHeight - l.thumbnailsFinalY), l.vy *= l.friction, l.thumbnailsFinalY += l.vy2), l.buttonsHolder_do.setY(Math.round(l.thumbnailsFinalY)))
            }, this.setupScrollbar = function() {
                l.scrMainHolder_do = new FWDMSPDisplayObject("div"), l.scrMainHolder_do.setVisible(!1), l.scrMainHolder_do.setWidth(i.scrWidth), l.scrTrack_do = new FWDMSPDisplayObject("div"), l.scrTrack_do.setWidth(i.scrWidth);
                var e = new Image;
                e.src = i.playlistScrBkTop_img.src, l.scrTrackTop_do = new FWDMSPDisplayObject("img"), l.scrTrackTop_do.setWidth(i.scrTrackTop_do.w), l.scrTrackTop_do.setHeight(i.scrTrackTop_do.h), l.scrTrackTop_do.setScreen(e), l.scrTrackMiddle_do = new FWDMSPDisplayObject("div"), l.scrTrackMiddle_do.getStyle().background = "url('" + i.data.scrBkMiddlePath_str + "')", l.scrTrackMiddle_do.setWidth(i.scrWidth), l.scrTrackMiddle_do.setY(l.scrTrackTop_do.h);
                var t = new Image;
                t.src = i.data.scrBkBottomPath_str, l.scrTrackBottom_do = new FWDMSPDisplayObject("img"), l.scrTrackBottom_do.setScreen(t), l.scrTrackBottom_do.setWidth(l.scrTrackTop_do.w), l.scrTrackBottom_do.setHeight(l.scrTrackTop_do.h), l.scrHandler_do = new FWDMSPDisplayObject("div"), l.scrHandler_do.setWidth(i.scrWidth), l.playlistScrDragTop_img = new Image, l.playlistScrDragTop_img.src = i.data.scrDragBottomPath_str, l.playlistScrDragTop_img.width = i.playlistScrDragTop_img.width, l.playlistScrDragTop_img.height = i.playlistScrDragTop_img.height, l.scrHandlerTop_do = new FWDMSPDisplayObject("img"), l.useHEXColorsForSkin_bl ? (l.scrHandlerTop_do = new FWDMSPDisplayObject("div"), l.scrHandlerTop_do.setWidth(l.playlistScrDragTop_img.width), l.scrHandlerTop_do.setHeight(l.playlistScrDragTop_img.height), l.mainScrubberDragTop_canvas = FWDMSPUtils.getCanvasWithModifiedColor(l.playlistScrDragTop_img, l.normalButtonsColor_str).canvas, l.scrHandlerTop_do.screen.appendChild(l.mainScrubberDragTop_canvas)) : (l.scrHandlerTop_do = new FWDMSPDisplayObject("img"), l.scrHandlerTop_do.setScreen(l.playlistScrDragTop_img)), l.scrHandlerMiddle_do = new FWDMSPDisplayObject("div"), l.middleImage = new Image, l.middleImage.src = i.data.scrDragMiddlePath_str, l.useHEXColorsForSkin_bl ? l.middleImage.onload = function() {
                    l.scrubberDragMiddle_canvas = FWDMSPUtils.getCanvasWithModifiedColor(l.middleImage, l.normalButtonsColor_str, !0), l.scrubberDragImage_img = l.scrubberDragMiddle_canvas.image, l.scrHandlerMiddle_do.getStyle().background = "url('" + l.scrubberDragImage_img.src + "') repeat-y"
                } : l.scrHandlerMiddle_do.getStyle().background = "url('" + i.data.scrDragMiddlePath_str + "')", l.scrHandlerMiddle_do.setWidth(i.scrWidth), l.scrHandlerMiddle_do.setY(l.scrHandlerTop_do.h), l.scrHandlerBottom_do = new FWDMSPDisplayObject("div"), l.bottomImage = new Image, l.bottomImage.src = i.data.scrDragMiddlePath_str, l.useHEXColorsForSkin_bl ? l.bottomImage.onload = function() {
                    l.scrubberDragBottom_canvas = FWDMSPUtils.getCanvasWithModifiedColor(l.bottomImage, l.normalButtonsColor_str, !0), l.scrubberDragBottomImage_img = l.scrubberDragBottom_canvas.image, l.scrHandlerBottom_do.getStyle().background = "url('" + l.scrubberDragBottomImage_img.src + "') repeat-y"
                } : l.scrHandlerBottom_do.getStyle().background = "url('" + i.playlistScrDragTop_img.src + "')", l.scrHandlerBottom_do.setWidth(i.scrWidth), l.scrHandlerBottom_do.setY(l.scrHandlerTop_do.h), console.log(), console.log(), l.scrHandlerBottom_do.setWidth(l.scrHandlerTop_do.w), l.scrHandlerBottom_do.setHeight(l.scrHandlerTop_do.h), l.scrHandler_do.setButtonMode(!0), l.playlistScrLines_img = new Image, l.playlistScrLines_img.src = i.playlistScrLines_img.src, l.playlistScrLines_img.width = i.playlistScrLines_img.width, l.playlistScrLines_img.height = i.playlistScrLines_img.height, l.useHEXColorsForSkin_bl ? (l.scrHandlerLinesN_do = new FWDMSPDisplayObject("div"), l.scrHandlerLinesN_do.setWidth(l.playlistScrLines_img.width), l.scrHandlerLinesN_do.setHeight(l.playlistScrLines_img.height), l.mainhandlerN_canvas = FWDMSPUtils.getCanvasWithModifiedColor(l.playlistScrLines_img, l.normalButtonsColor_str).canvas, l.scrHandlerLinesN_do.screen.appendChild(l.mainhandlerN_canvas)) : (l.scrHandlerLinesN_do = new FWDMSPDisplayObject("img"), l.scrHandlerLinesN_do.setScreen(l.playlistScrLines_img)), l.scrHandlerLinesS_img = new Image, l.scrHandlerLinesS_img.src = i.data.scrLinesSPath_str, l.useHEXColorsForSkin_bl ? (l.scrHandlerLinesS_do = new FWDMSPDisplayObject("div"), l.scrHandlerLinesS_img.onload = function() {
                    l.scrHandlerLinesS_do.setWidth(l.scrHandlerLinesN_do.w), l.scrHandlerLinesS_do.setHeight(l.scrHandlerLinesN_do.h), l.scrubberLines_s_canvas = FWDMSPUtils.getCanvasWithModifiedColor(l.scrHandlerLinesS_img, l.selectedButtonsColor_str, !0), l.scrubbelinesSImage_img = l.scrubberLines_s_canvas.image, l.scrHandlerLinesS_do.getStyle().background = "url('" + l.scrubbelinesSImage_img.src + "') repeat-y"
                }) : (l.scrHandlerLinesS_do = new FWDMSPDisplayObject("img"), l.scrHandlerLinesS_do.setScreen(l.scrHandlerLinesS_img), l.scrHandlerLinesS_do.setWidth(l.scrHandlerLinesN_do.w), l.scrHandlerLinesS_do.setHeight(l.scrHandlerLinesN_do.h)), l.scrHandlerLinesS_do.setAlpha(0), l.scrHandlerLines_do = new FWDMSPDisplayObject("div"), l.scrHandlerLines_do.setWidth(l.scrHandlerLinesN_do.w), l.scrHandlerLines_do.setHeight(l.scrHandlerLinesN_do.h), l.scrHandlerLines_do.setButtonMode(!0), l.scrTrack_do.addChild(l.scrTrackTop_do), l.scrTrack_do.addChild(l.scrTrackMiddle_do), l.scrTrack_do.addChild(l.scrTrackBottom_do), l.scrHandler_do.addChild(l.scrHandlerTop_do), l.scrHandler_do.addChild(l.scrHandlerMiddle_do), l.scrHandler_do.addChild(l.scrHandlerBottom_do), l.scrHandlerLines_do.addChild(l.scrHandlerLinesN_do), l.scrHandlerLines_do.addChild(l.scrHandlerLinesS_do), l.scrMainHolder_do.addChild(l.scrTrack_do), l.scrMainHolder_do.addChild(l.scrHandler_do), l.scrMainHolder_do.addChild(l.scrHandlerLines_do), l.mainButtonsHolder_do.addChild(l.scrMainHolder_do), l.scrHandler_do.screen.addEventListener ? (l.scrHandler_do.screen.addEventListener("mouseover", l.scrollBarHandlerOnMouseOver), l.scrHandler_do.screen.addEventListener("mouseout", l.scrollBarHandlerOnMouseOut), l.scrHandler_do.screen.addEventListener("mousedown", l.scrollBarHandlerOnMouseDown), l.scrHandlerLines_do.screen.addEventListener("mouseover", l.scrollBarHandlerOnMouseOver), l.scrHandlerLines_do.screen.addEventListener("mouseout", l.scrollBarHandlerOnMouseOut), l.scrHandlerLines_do.screen.addEventListener("mousedown", l.scrollBarHandlerOnMouseDown)) : l.scrHandler_do.screen.attachEvent && (l.scrHandler_do.screen.attachEvent("onmouseover", l.scrollBarHandlerOnMouseOver), l.scrHandler_do.screen.attachEvent("onmouseout", l.scrollBarHandlerOnMouseOut), l.scrHandler_do.screen.attachEvent("onmousedown", l.scrollBarHandlerOnMouseDown), l.scrHandlerLines_do.screen.attachEvent("onmouseover", l.scrollBarHandlerOnMouseOver), l.scrHandlerLines_do.screen.attachEvent("onmouseout", l.scrollBarHandlerOnMouseOut), l.scrHandlerLines_do.screen.attachEvent("onmousedown", l.scrollBarHandlerOnMouseDown))
            }, this.scrollBarHandlerOnMouseOver = function(e) {
                l.allowToScrollAndScrollBarIsActive_bl && (FWDAnimation.killTweensOf(l.scrHandlerLinesN_do), FWDAnimation.killTweensOf(l.scrHandlerLinesS_do), FWDAnimation.to(l.scrHandlerLinesN_do, .8, {
                    alpha: 0,
                    ease: Expo.easeOut
                }), FWDAnimation.to(l.scrHandlerLinesS_do, .8, {
                    alpha: 1,
                    ease: Expo.easeOut
                }))
            }, this.scrollBarHandlerOnMouseOut = function(e) {
                !l.isDragging_bl && l.allowToScrollAndScrollBarIsActive_bl && (FWDAnimation.killTweensOf(l.scrHandlerLinesN_do), FWDAnimation.killTweensOf(l.scrHandlerLinesS_do), FWDAnimation.to(l.scrHandlerLinesN_do, .8, {
                    alpha: 1,
                    ease: Expo.easeOut
                }), FWDAnimation.to(l.scrHandlerLinesS_do, .8, {
                    alpha: 0,
                    ease: Expo.easeOut
                }))
            }, this.scrollBarHandlerOnMouseDown = function(e) {
                if (l.allowToScrollAndScrollBarIsActive_bl) {
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                    l.isDragging_bl = !0, l.yPositionOnPress = l.scrHandler_do.y, l.lastPresedY = t.screenY, FWDAnimation.killTweensOf(l.scrHandler_do), i.showDisable(), r.addEventListener ? (r.addEventListener("mousemove", l.scrollBarHandlerMoveHandler), r.addEventListener("mouseup", l.scrollBarHandlerEndHandler)) : document.attachEvent && (document.attachEvent("onmousemove", l.scrollBarHandlerMoveHandler), document.attachEvent("onmouseup", l.scrollBarHandlerEndHandler))
                }
            }, this.scrollBarHandlerMoveHandler = function(e) {
                e.preventDefault && e.preventDefault();
                var t = FWDMSPUtils.getViewportMouseCoordinates(e),
                    o = l.scrollBarHandlerFinalY + parseInt((l.scrHandler_do.h - l.scrHandlerLines_do.h) / 2);
                l.scrollBarHandlerFinalY = Math.round(l.yPositionOnPress + t.screenY - l.lastPresedY), l.scrollBarHandlerFinalY >= l.scrTrack_do.h - l.scrHandler_do.h ? l.scrollBarHandlerFinalY = l.scrTrack_do.h - l.scrHandler_do.h : l.scrollBarHandlerFinalY <= 0 && (l.scrollBarHandlerFinalY = 0), l.scrHandler_do.setY(l.scrollBarHandlerFinalY), FWDAnimation.killTweensOf(l.scrHandler_do), FWDAnimation.to(l.scrHandlerLines_do, .8, {
                    y: o,
                    ease: Quart.easeOut
                }), l.updateScrollBarHandlerAndContent(!0)
            }, l.scrollBarHandlerEndHandler = function(e) {
                var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                l.isDragging_bl = !1, FWDMSPUtils.hitTest(l.scrHandler_do.screen, t.screenX, t.screenY) || (FWDAnimation.killTweensOf(l.scrHandlerLinesN_do), FWDAnimation.killTweensOf(l.scrHandlerLinesS_do), FWDAnimation.to(l.scrHandlerLinesN_do, .8, {
                    alpha: 1,
                    ease: Expo.easeOut
                }), FWDAnimation.to(l.scrHandlerLinesS_do, .8, {
                    alpha: 0,
                    ease: Expo.easeOut
                })), i.hideDisable(), FWDAnimation.killTweensOf(l.scrHandler_do), FWDAnimation.to(l.scrHandler_do, .4, {
                    y: l.scrollBarHandlerFinalY,
                    ease: Quart.easeOut
                }), r.removeEventListener ? (r.removeEventListener("mousemove", l.scrollBarHandlerMoveHandler), r.removeEventListener("mouseup", l.scrollBarHandlerEndHandler)) : document.detachEvent && (document.detachEvent("onmousemove", l.scrollBarHandlerMoveHandler), document.detachEvent("onmouseup", l.scrollBarHandlerEndHandler))
            }, this.updateScrollBarSizeActiveAndDeactivate = function() {
                l.disableForAWhileAfterThumbClick_bl || (l.allowToScrollAndScrollBarIsActive_bl ? (l.allowToScrollAndScrollBarIsActive_bl = !0, l.scrMainHolder_do.setX(l.stageWidth - l.scrMainHolder_do.w), l.scrMainHolder_do.setHeight(l.mainButtonsHolder_do.h), l.scrTrack_do.setHeight(l.scrMainHolder_do.h), l.scrTrackMiddle_do.setHeight(l.scrTrack_do.h - 2 * l.scrTrackTop_do.h), l.scrTrackBottom_do.setY(l.scrTrackMiddle_do.y + l.scrTrackMiddle_do.h), l.scrMainHolder_do.setAlpha(1), l.scrHandler_do.setButtonMode(!0), l.scrHandlerLines_do.setButtonMode(!0)) : (l.allowToScrollAndScrollBarIsActive_bl = !1, l.scrMainHolder_do.setX(l.stageWidth - l.scrMainHolder_do.w), l.scrMainHolder_do.setHeight(l.mainButtonsHolder_do.h), l.scrTrack_do.setHeight(l.scrMainHolder_do.h), l.scrTrackMiddle_do.setHeight(l.scrTrack_do.h - 2 * l.scrTrackTop_do.h), l.scrTrackBottom_do.setY(l.scrTrackMiddle_do.y + l.scrTrackMiddle_do.h), l.scrMainHolder_do.setAlpha(.5), l.scrHandler_do.setY(0), l.scrHandler_do.setButtonMode(!1), l.scrHandlerLines_do.setButtonMode(!1)), l.scrHandler_do.setHeight(Math.max(120, Math.round(Math.min(1, l.scrMainHolder_do.h / l.totalButtonsHeight) * l.scrMainHolder_do.h))), l.scrHandlerMiddle_do.setHeight(l.scrHandler_do.h - 2 * l.scrHandlerTop_do.h), FWDAnimation.killTweensOf(l.scrHandlerLines_do), l.scrHandlerLines_do.setY(l.scrollBarHandlerFinalY + parseInt((l.scrHandler_do.h - l.scrHandlerLines_do.h) / 2)), l.scrHandlerBottom_do.setY(l.scrHandler_do.h - l.scrHandlerBottom_do.h - 1))
            }, this.addMouseWheelSupport = function() {
                l.screen.addEventListener ? (l.screen.addEventListener("DOMMouseScroll", l.mouseWheelHandler), l.screen.addEventListener("mousewheel", l.mouseWheelHandler)) : l.screen.attachEvent && l.screen.attachEvent("onmousewheel", l.mouseWheelHandler)
            }, l.mouseWheelHandler = function(e) {
                if (e.preventDefault && e.preventDefault(), l.disableMouseWheel_bl || l.isDragging_bl) return !1;
                var t = e.detail || e.wheelDelta;
                e.wheelDelta && (t *= -1), 0 < t ? l.scrollBarHandlerFinalY += Math.round(160 * l.scollbarSpeedSensitivity * (l.mainButtonsHolder_do.h / l.totalButtonsHeight)) : t < 0 && (l.scrollBarHandlerFinalY -= Math.round(160 * l.scollbarSpeedSensitivity * (l.mainButtonsHolder_do.h / l.totalButtonsHeight))), l.scrollBarHandlerFinalY >= l.scrTrack_do.h - l.scrHandler_do.h ? l.scrollBarHandlerFinalY = l.scrTrack_do.h - l.scrHandler_do.h : l.scrollBarHandlerFinalY <= 0 && (l.scrollBarHandlerFinalY = 0);
                var o = l.scrollBarHandlerFinalY + parseInt((l.scrHandler_do.h - l.scrHandlerLines_do.h) / 2);
                if (FWDAnimation.killTweensOf(l.scrHandler_do), FWDAnimation.killTweensOf(l.scrHandlerLines_do), FWDAnimation.to(l.scrHandlerLines_do, .8, {
                        y: o,
                        ease: Quart.easeOut
                    }), FWDAnimation.to(l.scrHandler_do, .5, {
                        y: l.scrollBarHandlerFinalY,
                        ease: Quart.easeOut
                    }), l.isDragging_bl = !0, l.updateScrollBarHandlerAndContent(!0), l.isDragging_bl = !1, !e.preventDefault) return !1;
                e.preventDefault()
            }, this.updateScrollBarHandlerAndContent = function(e, t) {
                if (!l.disableForAWhileAfterThumbClick_bl && (l.allowToScrollAndScrollBarIsActive_bl || t)) {
                    var o = 0;
                    l.isDragging_bl && !l.isMobile_bl ? ("Infinity" == (o = l.scrollBarHandlerFinalY / (l.scrMainHolder_do.h - l.scrHandler_do.h)) ? o = 0 : 1 <= o && (scrollPercent = 1), l.thumbnailsFinalY = -1 * Math.round(o * (l.totalButtonsHeight - l.mainButtonsHolder_do.h))) : (o = l.curId / (l.totalButtons - 1), l.thumbnailsFinalY = Math.min(0, -1 * Math.round(o * (l.totalButtonsHeight - l.mainButtonsHolder_do.h))), l.scrMainHolder_do && (l.scrollBarHandlerFinalY = Math.round((l.scrMainHolder_do.h - l.scrHandler_do.h) * o), l.scrollBarHandlerFinalY < 0 ? l.scrollBarHandlerFinalY = 0 : l.scrollBarHandlerFinalY > l.scrMainHolder_do.h - l.scrHandler_do.h - 1 && (l.scrollBarHandlerFinalY = l.scrMainHolder_do.h - l.scrHandler_do.h - 1), FWDAnimation.killTweensOf(l.scrHandler_do), FWDAnimation.killTweensOf(l.scrHandlerLines_do), e ? (FWDAnimation.to(l.scrHandler_do, .4, {
                        y: l.scrollBarHandlerFinalY,
                        ease: Quart.easeOut
                    }), FWDAnimation.to(l.scrHandlerLines_do, .8, {
                        y: l.scrollBarHandlerFinalY + parseInt((l.scrHandler_do.h - l.scrHandlerLinesN_do.h) / 2),
                        ease: Quart.easeOut
                    })) : (l.scrHandler_do.setY(l.scrollBarHandlerFinalY), l.scrHandlerLines_do.setY(l.scrollBarHandlerFinalY + parseInt((l.scrHandler_do.h - l.scrHandlerLinesN_do.h) / 2))))), l.lastThumbnailFinalY != l.thumbnailsFinalY && (FWDAnimation.killTweensOf(l.buttonsHolder_do), e ? FWDAnimation.to(l.buttonsHolder_do, .5, {
                        y: l.thumbnailsFinalY,
                        ease: Quart.easeOut
                    }) : l.buttonsHolder_do.setY(l.thumbnailsFinalY)), l.lastThumbnailFinalY = l.thumbnailsFinalY
                }
            }, this.init(), this.destroy = function() {
                l.isMobile_bl ? (r.removeEventListener("MSPointerDown", l.checkOpenedMenu), r.removeEventListener("touchstart", l.checkOpenedMenu)) : r.removeEventListener ? r.removeEventListener("mousemove", l.checkOpenedMenu) : document.detachEvent && document.detachEvent("onmousemove", l.checkOpenedMenu), clearTimeout(l.hideMenuTimeOutId_to), clearTimeout(l.getMaxWidthResizeAndPositionId_to), FWDAnimation.killTweensOf(l), FWDAnimation.killTweensOf(l.mainHolder_do), FWDAnimation.killTweensOf(l.buttonsHolder_do), FWDAnimation.killTweensOf(l.mainButtonsHolder_do), l.mainHolder_do.destroy(), l.selector_do.destroy(), l.mainButtonsHolder_do.destroy(), l.buttonsHolder_do.destroy(), l.categories_ar = null, l.buttons_ar = null, l.mainHolder_do = null, l.selector_do = null, l.mainButtonsHolder_do = null, l.buttonsHolder_do = null, l.upArrowN_img = null, l.upArrowS_img = null, n = i = null, l.setInnerHTML(""), e.destroy(), e = l = null, t.prototype = null
            }
        };
        t.setPrototype = function() {
            t.prototype = new FWDMSPDisplayObject("div")
        }, t.OPEN = "open", t.HIDE_COMPLETE = "infoWindowHideComplete", t.BUTTON_PRESSED = "buttonPressed", t.prototype = null, r.FWDMSPComboBox = t
    }(window),
    function() {
        var h = function(t, e, o, s, i, n, l, r, a, d) {
            var u = this,
                c = h.prototype;
            this.bk_sdo = null, this.text_sdo = null, this.dumy_sdo = null, this.label1_str = e, this.backgroundNormalColor_str = i, this.backgroundSelectedColor_str = n, this.textNormalColor_str = l, this.textSelectedColor_str = r, this.bk1_str = o, this.bk2_str = s, this.totalWidth = 400, this.totalHeight = d, this.id = a, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, this.isMobile_bl = FWDMSPUtils.isMobile, this.isDisabled_bl = !1, u.init = function() {
                u.setBackfaceVisibility(), u.setButtonMode(!0), u.setupMainContainers(), u.setWidth(u.totalWidth), u.setHeight(u.totalHeight), u.setNormalState()
            }, u.setupMainContainers = function() {
                u.bk_sdo = new FWDMSPDisplayObject("div"), u.bk_sdo.setBkColor(u.backgroundNormalColor_str), u.id % 2 == 0 ? u.bk_sdo.getStyle().background = "url('" + u.bk1_str + "')" : (u.bk_sdo.getStyle().background = "url('" + u.bk2_str + "')", u.type = 2), u.addChild(u.bk_sdo), u.text_sdo = new FWDMSPDisplayObject("div"), u.text_sdo.getStyle().whiteSpace = "nowrap", u.text_sdo.setBackfaceVisibility(), u.text_sdo.setOverflow("visible"), u.text_sdo.setDisplay("inline-block"), u.text_sdo.getStyle().fontFamily = "Arial", u.text_sdo.getStyle().fontSize = "13px", u.text_sdo.getStyle().padding = "6px", u.text_sdo.getStyle().fontWeight = "100", u.text_sdo.getStyle().color = u.normalColor_str, u.text_sdo.getStyle().fontSmoothing = "antialiased", u.text_sdo.getStyle().webkitFontSmoothing = "antialiased", u.text_sdo.getStyle().textRendering = "optimizeLegibility", FWDMSPUtils.isIEAndLessThen9 ? u.text_sdo.screen.innerText = u.label1_str : u.text_sdo.setInnerHTML(u.label1_str), u.addChild(u.text_sdo), u.dumy_sdo = new FWDMSPDisplayObject("div"), FWDMSPUtils.isIE && (u.dumy_sdo.setBkColor("#FF0000"), u.dumy_sdo.setAlpha(0)), u.addChild(u.dumy_sdo), u.isMobile_bl ? u.hasPointerEvent_bl ? (u.screen.addEventListener("MSPointerOver", u.onMouseOver), u.screen.addEventListener("MSPointerOut", u.onMouseOut), u.screen.addEventListener("MSPointerDown", u.onMouseDown), u.screen.addEventListener("MSPointerUp", u.onClick)) : u.screen.addEventListener("touchend", u.onMouseDown) : u.screen.addEventListener ? (u.screen.addEventListener("mouseover", u.onMouseOver), u.screen.addEventListener("mouseout", u.onMouseOut), u.screen.addEventListener("click", u.onMouseDown), u.screen.addEventListener("click", u.onClick)) : u.screen.attachEvent && (u.screen.attachEvent("onmouseover", u.onMouseOver), u.screen.attachEvent("onmouseout", u.onMouseOut), u.screen.attachEvent("onmousedown", u.onMouseDown), u.screen.attachEvent("onclick", u.onClick))
            }, u.onMouseOver = function(e) {
                u.isDisabled_bl || e.pointerType && e.pointerType != e.MSPOINTER_TYPE_MOUSE || (FWDAnimation.killTweensOf(u.text_sdo), u.setSelectedState(!0), u.dispatchEvent(h.MOUSE_OVER))
            }, u.onMouseOut = function(e) {
                u.isDisabled_bl || e.pointerType && e.pointerType != e.MSPOINTER_TYPE_MOUSE || (FWDAnimation.killTweensOf(u.text_sdo), u.setNormalState(!0), u.dispatchEvent(h.MOUSE_OUT))
            }, u.onClick = function(e) {
                u.isDisabled_bl || (e.preventDefault && e.preventDefault(), u.dispatchEvent(h.CLICK))
            }, u.onMouseDown = function(e) {
                u.isDisabled_bl || t.isScrollingOnMove_bl || (e.preventDefault && e.preventDefault(), u.dispatchEvent(h.MOUSE_DOWN, {
                    e: e
                }))
            }, this.setSelectedState = function(e) {
                e ? FWDAnimation.to(u.text_sdo.screen, .6, {
                    css: {
                        color: u.textSelectedColor_str
                    },
                    ease: Quart.easeOut
                }) : u.text_sdo.getStyle().color = u.textSelectedColor_str
            }, this.setNormalState = function(e) {
                e ? FWDAnimation.to(u.text_sdo.screen, .6, {
                    css: {
                        color: u.textNormalColor_str
                    },
                    ease: Quart.easeOut
                }) : u.text_sdo.getStyle().color = u.textNormalColor_str
            }, u.centerText = function() {
                u.dumy_sdo.setWidth(u.totalWidth), u.dumy_sdo.setHeight(u.totalHeight), u.bk_sdo.setWidth(u.totalWidth), u.bk_sdo.setHeight(u.totalHeight), u.text_sdo.setX(4), u.text_sdo.setY(Math.round((u.totalHeight - u.text_sdo.getHeight()) / 2))
            }, u.getMaxTextWidth = function() {
                return u.text_sdo.getWidth()
            }, this.disable = function() {
                u.isDisabled_bl = !0, u.setButtonMode(!1), u.setSelectedState(!0)
            }, this.enable = function() {
                u.isDisabled_bl = !1, u.setNormalState(!0), u.setButtonMode(!0)
            }, u.destroy = function() {
                u.isMobile_bl ? u.hasPointerEvent_bl ? (u.screen.removeEventListener("MSPointerOver", u.onMouseOver), u.screen.removeEventListener("MSPointerOut", u.onMouseOut), u.screen.removeEventListener("MSPointerDown", u.onMouseDown), u.screen.removeEventListener("MSPointerUp", u.onClick)) : u.screen.removeEventListener("touchstart", u.onMouseDown) : u.screen.removeEventListener ? (u.screen.removeEventListener("mouseover", u.onMouseOver), u.screen.removeEventListener("mouseout", u.onMouseOut), u.screen.removeEventListener("mousedown", u.onMouseDown), u.screen.removeEventListener("click", u.onClick)) : u.screen.detachEvent && (u.screen.detachEvent("onmouseover", u.onMouseOver), u.screen.detachEvent("onmouseout", u.onMouseOut), u.screen.detachEvent("onmousedown", u.onMouseDown), u.screen.detachEvent("onclick", u.onClick)), FWDAnimation.killTweensOf(u.text_sdo.screen), FWDAnimation.killTweensOf(u.bk_sdo.screen), u.text_sdo.destroy(), u.bk_sdo.destroy(), u.dumy_sdo.destroy(), u.bk_sdo = null, u.text_sdo = null, u.dumy_sdo = null, u.label1_str = null, u.normalColor_str = null, u.textSelectedColor_str = null, u.disabledColor_str = null, u.setInnerHTML(""), c.destroy(), c = u = null, h.prototype = null
            }, u.init()
        };
        h.setPrototype = function() {
            h.prototype = new FWDMSPDisplayObject("div")
        }, h.FIRST_BUTTON_CLICK = "onFirstClick", h.SECOND_BUTTON_CLICK = "secondButtonOnClick", h.MOUSE_OVER = "onMouseOver", h.MOUSE_OUT = "onMouseOut", h.MOUSE_DOWN = "onMouseDown", h.CLICK = "onClick", h.prototype = null, window.FWDMSPComboBoxButton = h
    }(window),
    function() {
        var p = function(e, t, o, s, i, n, l, r, a, d, u, c, h) {
            var _ = this,
                f = p.prototype;
            this.arrow_do = null, this.arrowN_sdo = null, this.arrowS_sdo = null, this.arrowN_str = o, this.arrowS_str = s, this.label1_str = i, this.backgroundNormalColor_str = n, this.backgroundSelectedColor_str = l, this.textNormalColor_str = r, this.textSelectedColor_str = a, _.useHEXColorsForSkin_bl = u, _.normalButtonsColor_str = c, _.selectedButtonsColor_str = h, this.totalWidth = 400, this.totalHeight = d, this.arrowWidth = e, this.arrowHeight = t, this.bk_sdo = null, this.text_sdo = null, this.dumy_sdo = null, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, this.isMobile_bl = FWDMSPUtils.isMobile, this.isDisabled_bl = !1, _.init = function() {
                _.setBackfaceVisibility(), _.setButtonMode(!0), _.setupMainContainers(), _.setWidth(_.totalWidth), _.setHeight(_.totalHeight)
            }, _.setupMainContainers = function() {
                _.bk_sdo = new FWDMSPDisplayObject("div"), _.bk_sdo.getStyle().backgroundColor = _.backgroundNormalColor_str, _.addChild(_.bk_sdo), _.text_sdo = new FWDMSPDisplayObject("div"), _.text_sdo.getStyle().whiteSpace = "nowrap", _.text_sdo.setBackfaceVisibility(), _.text_sdo.setOverflow("visible"), _.text_sdo.setDisplay("inline-block"), _.text_sdo.getStyle().fontFamily = "Arial", _.text_sdo.getStyle().fontSize = "13px", _.text_sdo.getStyle().fontWeight = "100", _.text_sdo.getStyle().padding = "6px", _.text_sdo.getStyle().color = _.normalColor_str, _.text_sdo.getStyle().fontSmoothing = "antialiased", _.text_sdo.getStyle().webkitFontSmoothing = "antialiased", _.text_sdo.getStyle().textRendering = "optimizeLegibility", FWDMSPUtils.isIEAndLessThen9 ? _.text_sdo.screen.innerText = _.label1_str : _.text_sdo.setInnerHTML(_.label1_str), _.addChild(_.text_sdo), _.arrow_do = new FWDMSPDisplayObject("div"), _.arrow_do.setOverflow("visible"), _.useHEXColorsForSkin_bl ? (_.arrowN_img = new Image, _.arrowN_img.src = _.arrowN_str, _.arrowS_img = new Image, _.arrowS_img.src = _.arrowS_str, _.arrowN_sdo = new FWDMSPDisplayObject("div"), _.arrowS_sdo = new FWDMSPDisplayObject("div"), _.arrowN_img.onload = function() {
                    _.arrowN_sdo.setWidth(_.arrowN_img.width), _.arrowN_sdo.setHeight(_.arrowN_img.height), _.scrubberLines_n_canvas = FWDMSPUtils.getCanvasWithModifiedColor(_.arrowN_img, _.normalButtonsColor_str, !0), _.scrubbelinesNImage_img = _.scrubberLines_n_canvas.image, _.arrowN_sdo.getStyle().background = "url('" + _.scrubbelinesNImage_img.src + "') repeat-y", _.arrowS_sdo.setWidth(_.arrowS_img.width), _.arrowS_sdo.setHeight(_.arrowS_img.height), _.scrubberLines_s_canvas = FWDMSPUtils.getCanvasWithModifiedColor(_.arrowS_img, _.selectedButtonsColor_str, !0), _.scrubbelinesSImage_img = _.scrubberLines_s_canvas.image, _.arrowS_sdo.getStyle().background = "url('" + _.scrubbelinesSImage_img.src + "') repeat-y"
                }) : (_.arrowN_sdo = new FWDMSPDisplayObject("div"), _.arrowN_sdo.screen.style.backgroundImage = "url(" + _.arrowN_str + ")", _.arrowS_sdo = new FWDMSPDisplayObject("div"), _.arrowS_sdo.screen.style.backgroundImage = "url(" + _.arrowS_str + ")"), _.arrowS_sdo.setAlpha(0), _.arrow_do.addChild(_.arrowN_sdo), _.arrow_do.addChild(_.arrowS_sdo), _.addChild(_.arrow_do), _.arrowN_sdo.setWidth(_.arrowWidth), _.arrowN_sdo.setHeight(_.arrowHeight), _.arrowS_sdo.setWidth(_.arrowWidth), _.arrowS_sdo.setHeight(_.arrowHeight), _.dumy_sdo = new FWDMSPDisplayObject("div"), FWDMSPUtils.isIE && (_.dumy_sdo.setBkColor("#FF0000"), _.dumy_sdo.setAlpha(0)), _.addChild(_.dumy_sdo), _.isMobile_bl ? _.hasPointerEvent_bl ? (_.screen.addEventListener("MSPointerOver", _.onMouseOver), _.screen.addEventListener("MSPointerOut", _.onMouseOut), _.screen.addEventListener("MSPointerDown", _.onMouseDown), _.screen.addEventListener("MSPointerUp", _.onClick)) : _.screen.addEventListener("touchend", _.onMouseDown) : _.screen.addEventListener ? (_.screen.addEventListener("mouseover", _.onMouseOver), _.screen.addEventListener("mouseout", _.onMouseOut), _.screen.addEventListener("mousedown", _.onMouseDown), _.screen.addEventListener("click", _.onClick)) : _.screen.attachEvent && (_.screen.attachEvent("onmouseover", _.onMouseOver), _.screen.attachEvent("onmouseout", _.onMouseOut), _.screen.attachEvent("onmousedown", _.onMouseDown), _.screen.attachEvent("onclick", _.onClick))
            }, _.onMouseOver = function(e) {
                _.isDisabled_bl || e.pointerType && e.pointerType != e.MSPOINTER_TYPE_MOUSE || (FWDAnimation.killTweensOf(_.text_sdo), _.setSelectedState(!0, 0), _.dispatchEvent(p.MOUSE_OVER))
            }, _.onMouseOut = function(e) {
                _.isDisabled_bl || e.pointerType && e.pointerType != e.MSPOINTER_TYPE_MOUSE || (FWDAnimation.killTweensOf(_.text_sdo), _.setNormalState(!0, !0), _.dispatchEvent(p.MOUSE_OUT))
            }, _.onClick = function(e) {
                _.isDeveleper_bl ? window.open("http://www.webdesign-flash.ro", "_blank") : _.isDisabled_bl || (e.preventDefault && e.preventDefault(), _.dispatchEvent(p.CLICK))
            }, _.onMouseDown = function(e) {
                e.preventDefault && e.preventDefault(), _.dispatchEvent(p.MOUSE_DOWN, {
                    e: e
                })
            }, this.setSelectedState = function(e, t) {
                FWDAnimation.killTweensOf(_.bk_sdo), FWDAnimation.killTweensOf(_.text_sdo), FWDAnimation.killTweensOf(_.arrowS_sdo), e ? (FWDAnimation.to(_.bk_sdo, .6, {
                    alpha: 1,
                    ease: Expo.easeOut
                }), FWDAnimation.to(_.text_sdo.screen, .6, {
                    css: {
                        color: _.textSelectedColor_str
                    },
                    ease: Expo.easeOut
                }), FWDAnimation.to(_.arrowS_sdo, .6, {
                    alpha: 1,
                    ease: Expo.easeOut
                })) : (_.bk_sdo.setAlpha(1), _.text_sdo.getStyle().color = _.textSelectedColor_str, _.arrowS_sdo.alpha = 1)
            }, this.setNormalState = function(e, t) {
                var o = .6;
                t && (o = 0), o = 0, FWDAnimation.killTweensOf(_.bk_sdo), FWDAnimation.killTweensOf(_.text_sdo), FWDAnimation.killTweensOf(_.arrowS_sdo), e ? (FWDAnimation.to(_.bk_sdo, .6, {
                    alpha: 0,
                    delay: o,
                    ease: Expo.easeOut
                }), FWDAnimation.to(_.text_sdo.screen, .6, {
                    css: {
                        color: _.textNormalColor_str
                    },
                    delay: o,
                    ease: Expo.easeOut
                }), FWDAnimation.to(_.arrowS_sdo, .6, {
                    alpha: 0,
                    delay: o,
                    ease: Expo.easeOut
                })) : (_.bk_sdo.setAlpha(0), _.text_sdo.getStyle().color = _.textNormalColor_str, _.arrowS_sdo.alpha = 0)
            }, _.centerText = function() {
                _.dumy_sdo.setWidth(_.totalWidth), _.dumy_sdo.setHeight(_.totalHeight), _.bk_sdo.setWidth(_.totalWidth), _.bk_sdo.setHeight(_.totalHeight), _.text_sdo.setX(6), _.text_sdo.setY(Math.round((_.totalHeight - _.text_sdo.getHeight()) / 2) + 1), _.arrow_do.setX(_.totalWidth - _.arrowWidth - 10), _.arrow_do.setY(Math.round((_.totalHeight - _.arrowHeight) / 2))
            }, _.getMaxTextWidth = function() {
                return _.text_sdo.getWidth()
            }, this.disable = function() {
                _.isDisabled_bl = !0, _.setSelectedState(!0), FWDMSPUtils.hasTransform2d && (FWDAnimation.to(_.arrowN_sdo.screen, .8, {
                    css: {
                        rotation: 180
                    },
                    ease: Quart.easeOut
                }), FWDAnimation.to(_.arrowS_sdo.screen, .8, {
                    css: {
                        rotation: 180
                    },
                    ease: Quart.easeOut
                })), _.setButtonMode(!1)
            }, this.enable = function() {
                _.isDisabled_bl = !1, _.setNormalState(!0), FWDMSPUtils.hasTransform2d && (FWDAnimation.to(_.arrowN_sdo.screen, .8, {
                    css: {
                        rotation: 0
                    },
                    ease: Quart.easeOut
                }), FWDAnimation.to(_.arrowS_sdo.screen, .8, {
                    css: {
                        rotation: 0
                    },
                    ease: Quart.easeOut
                })), _.setButtonMode(!0)
            }, this.setText = function(e) {
                FWDMSPUtils.isIEAndLessThen9 ? _.text_sdo.screen.innerText = e : _.text_sdo.setInnerHTML(e)
            }, _.destroy = function() {
                _.isMobile_bl ? _.screen.removeEventListener("touchstart", _.onMouseDown) : _.screen.removeEventListener ? (_.screen.removeEventListener("mouseover", _.onMouseOver), _.screen.removeEventListener("mouseout", _.onMouseOut), _.screen.removeEventListener("mousedown", _.onMouseDown), _.screen.removeEventListener("click", _.onClick)) : _.screen.detachEvent && (_.screen.detachEvent("onmouseover", _.onMouseOver), _.screen.detachEvent("onmouseout", _.onMouseOut), _.screen.detachEvent("onmousedown", _.onMouseDown), _.screen.detachEvent("onclick", _.onClick)), FWDAnimation.killTweensOf(_.text_sdo), FWDAnimation.killTweensOf(_.colorObj), _.text_sdo.destroy(), _.dumy_sdo.destroy(), _.text_sdo = null, _.dumy_sdo = null, _.label1_str = null, _.normalColor_str = null, _.textSelectedColor_str = null, _.disabledColor_str = null, normalColor = i = null, selectedColor = null, disabledColor = null, _.setInnerHTML(""), f.destroy(), f = _ = null, p.prototype = null
            }, _.init()
        };
        p.setPrototype = function() {
            p.prototype = new FWDMSPDisplayObject("div")
        }, p.FIRST_BUTTON_CLICK = "onFirstClick", p.SECOND_BUTTON_CLICK = "secondButtonOnClick", p.MOUSE_OVER = "onMouseOver", p.MOUSE_OUT = "onMouseOut", p.MOUSE_DOWN = "onMouseDown", p.CLICK = "onClick", p.prototype = null, window.FWDMSPComboBoxSelector = p
    }(window),
    function() {
        var d = function(e, t, o, s, i, n, l, r) {
            var a = this;
            d.prototype;
            this.n1Img = e, this.s1Path_str = t, this.n2Img = o, this.s2Path_str = s, this.firstButton_do, this.n1_do, this.s1_do, this.secondButton_do, this.n2_do, this.s2_do, this.buttonWidth = a.n1Img.width, this.buttonHeight = a.n1Img.height, this.useHEXColorsForSkin_bl = n, this.normalButtonsColor_str = l, this.selectedButtonsColor_str = r, this.isSelectedState_bl = !1, this.currentState = 1, this.isDisabled_bl = !1, this.isMaximized_bl = !1, this.disptachMainEvent_bl = i, this.isDisabled_bl = !1, this.isMobile_bl = FWDMSPUtils.isMobile, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, this.allowToCreateSecondButton_bl = !a.isMobile_bl || a.hasPointerEvent_bl, a.init = function() {
                a.hasTransform2d_bl = !1, a.setButtonMode(!0), a.setWidth(a.buttonWidth), a.setHeight(a.buttonHeight), a.setupMainContainers(), a.secondButton_do.setVisible(!1)
            }, a.setupMainContainers = function() {
                a.firstButton_do = new FWDMSPDisplayObject("div"), a.firstButton_do.setWidth(a.buttonWidth), a.firstButton_do.setHeight(a.buttonHeight), a.useHEXColorsForSkin_bl ? (a.n1_do = new FWDMSPDisplayObject("div"), a.n1_do.setWidth(a.buttonWidth), a.n1_do.setHeight(a.buttonHeight), a.n1_sdo_canvas = FWDMSPUtils.getCanvasWithModifiedColor(a.n1Img, a.normalButtonsColor_str).canvas, a.n1_do.screen.appendChild(a.n1_sdo_canvas)) : (a.n1_do = new FWDMSPDisplayObject("img"), a.n1_do.setScreen(a.n1Img)), a.firstButton_do.addChild(a.n1_do), a.allowToCreateSecondButton_bl && (a.s1_img = new Image, a.s1_img.src = a.s1Path_str, a.useHEXColorsForSkin_bl ? (a.s1_do = new FWDMSPTransformDisplayObject("div"), a.s1_do.setWidth(a.buttonWidth), a.s1_do.setHeight(a.buttonHeight), a.s1_img.onload = function() {
                    a.s1_do_canvas = FWDMSPUtils.getCanvasWithModifiedColor(a.s1_img, a.selectedButtonsColor_str).canvas, a.s1_do.screen.appendChild(a.s1_do_canvas)
                }) : (a.s1_do = new FWDMSPDisplayObject("img"), a.s1_do.setScreen(a.s1_img), a.s1_do.setWidth(a.buttonWidth), a.s1_do.setHeight(a.buttonHeight)), a.s1_do.setAlpha(0), a.firstButton_do.addChild(a.s1_do)), a.secondButton_do = new FWDMSPDisplayObject("div"), a.secondButton_do.setWidth(a.buttonWidth), a.secondButton_do.setHeight(a.buttonHeight), a.useHEXColorsForSkin_bl ? (a.n2_do = new FWDMSPDisplayObject("div"), a.n2_do.setWidth(a.buttonWidth), a.n2_do.setHeight(a.buttonHeight), a.n2_sdo_canvas = FWDMSPUtils.getCanvasWithModifiedColor(a.n2Img, a.normalButtonsColor_str).canvas, a.n2_do.screen.appendChild(a.n2_sdo_canvas)) : (a.n2_do = new FWDMSPDisplayObject("img"), a.n2_do.setScreen(a.n2Img)), a.secondButton_do.addChild(a.n2_do), a.allowToCreateSecondButton_bl && (a.s2_img = new Image, a.s2_img.src = a.s2Path_str, a.useHEXColorsForSkin_bl ? (a.s2_do = new FWDMSPTransformDisplayObject("div"), a.s2_do.setWidth(a.buttonWidth), a.s2_do.setHeight(a.buttonHeight), a.s2_img.onload = function() {
                    a.s2_do_canvas = FWDMSPUtils.getCanvasWithModifiedColor(a.s2_img, a.selectedButtonsColor_str).canvas, a.s2_do.screen.appendChild(a.s2_do_canvas)
                }) : (a.s2_do = new FWDMSPDisplayObject("img"), a.s2_do.setScreen(a.s2_img), a.s2_do.setWidth(a.buttonWidth), a.s2_do.setHeight(a.buttonHeight)), a.s2_do.setAlpha(0), a.secondButton_do.addChild(a.s2_do)), a.addChild(a.secondButton_do), a.addChild(a.firstButton_do), a.isMobile_bl ? a.hasPointerEvent_bl ? (a.screen.addEventListener("pointerdown", a.onMouseUp), a.screen.addEventListener("pointerover", a.onMouseOver), a.screen.addEventListener("pointerout", a.onMouseOut)) : (a.screen.addEventListener("toustart", a.onDown), a.screen.addEventListener("touchend", a.onMouseUp)) : a.screen.addEventListener ? (a.screen.addEventListener("mouseover", a.onMouseOver), a.screen.addEventListener("mouseout", a.onMouseOut), a.screen.addEventListener("mouseup", a.onMouseUp)) : a.screen.attachEvent && (a.screen.attachEvent("onmouseover", a.onMouseOver), a.screen.attachEvent("onmouseout", a.onMouseOut), a.screen.attachEvent("onmousedown", a.onMouseUp))
            }, a.onMouseOver = function(e, t) {
                a.isDisabled_bl || a.isSelectedState_bl || e.pointerType && e.pointerType != e.MSPOINTER_TYPE_MOUSE && "mouse" != e.pointerType || (a.dispatchEvent(d.MOUSE_OVER, {
                    e: e
                }), a.setSelectedState(!0))
            }, a.onMouseOut = function(e) {
                !a.isDisabled_bl && a.isSelectedState_bl && (e.pointerType && e.pointerType != e.MSPOINTER_TYPE_MOUSE && "mouse" != e.pointerType || (a.setNormalState(), a.dispatchEvent(d.MOUSE_OUT)))
            }, a.onDown = function(e) {
                e.preventDefault && e.preventDefault()
            }, a.onMouseUp = function(e) {
                a.isDisabled_bl || 2 == e.button || (e.preventDefault && e.preventDefault(), a.isMobile_bl || a.onMouseOver(e, !1), a.disptachMainEvent_bl && a.dispatchEvent(d.MOUSE_UP, {
                    e: e
                }))
            }, a.toggleButton = function() {
                1 == a.currentState ? (a.firstButton_do.setVisible(!1), a.secondButton_do.setVisible(!0), a.currentState = 0, a.dispatchEvent(d.FIRST_BUTTON_CLICK)) : (a.firstButton_do.setVisible(!0), a.secondButton_do.setVisible(!1), a.currentState = 1, a.dispatchEvent(d.SECOND_BUTTON_CLICK))
            }, a.setButtonState = function(e) {
                1 == e ? (a.firstButton_do.setVisible(!0), a.secondButton_do.setVisible(!1), a.currentState = 1) : (a.firstButton_do.setVisible(!1), a.secondButton_do.setVisible(!0), a.currentState = 0)
            }, this.setNormalState = function() {
                a.isMobile_bl && !a.hasPointerEvent_bl || (a.isSelectedState_bl = !1, FWDAnimation.killTweensOf(a.s1_do), FWDAnimation.killTweensOf(a.s2_do), FWDAnimation.to(a.s1_do, .5, {
                    alpha: 0,
                    ease: Expo.easeOut
                }), FWDAnimation.to(a.s2_do, .5, {
                    alpha: 0,
                    ease: Expo.easeOut
                }))
            }, this.setSelectedState = function(e) {
                a.isSelectedState_bl = !0, FWDAnimation.killTweensOf(a.s1_do), FWDAnimation.killTweensOf(a.s2_do), FWDAnimation.to(a.s1_do, .5, {
                    alpha: 1,
                    delay: .1,
                    ease: Expo.easeOut
                }), FWDAnimation.to(a.s2_do, .5, {
                    alpha: 1,
                    delay: .1,
                    ease: Expo.easeOut
                })
            }, this.disable = function() {
                a.isDisabled_bl || (a.isDisabled_bl = !0, a.setButtonMode(!1), FWDAnimation.to(a, .6, {
                    alpha: .4
                }), a.setNormalState())
            }, this.enable = function() {
                a.isDisabled_bl && (a.isDisabled_bl = !1, a.setButtonMode(!0), FWDAnimation.to(a, .6, {
                    alpha: 1
                }))
            }, this.updateHEXColors = function(e, t) {
                FWDMSPUtils.changeCanvasHEXColor(a.n1Img, a.n1_sdo_canvas, e), FWDMSPUtils.changeCanvasHEXColor(a.s1_img, a.s1_do_canvas, t), FWDMSPUtils.changeCanvasHEXColor(a.n2Img, a.n2_sdo_canvas, e), FWDMSPUtils.changeCanvasHEXColor(a.s2_img, a.s2_do_canvas, t)
            }, a.init()
        };
        d.setPrototype = function() {
            d.prototype = new FWDMSPDisplayObject("div")
        }, d.FIRST_BUTTON_CLICK = "onFirstClick", d.SECOND_BUTTON_CLICK = "secondButtonOnClick", d.MOUSE_OVER = "onMouseOver", d.MOUSE_OUT = "onMouseOut", d.MOUSE_UP = "onMouseUp", d.CLICK = "onClick", d.prototype = null, window.FWDMSPComplexButton = d
    }(window),
    function() {
        function e(e, t) {
            var l = this;
            this.parent = e, this.url = "", this.menu_do = null, this.normalMenu_do = null, this.selectedMenu_do = null, this.over_do = null, this.isDisabled_bl = !1, this.init = function() {
                l.updateParent(l.parent)
            }, this.updateParent = function(e) {
                l.parent && (l.parent.screen.addEventListener ? l.parent.screen.removeEventListener("contextmenu", this.contextMenuHandler) : l.parent.screen.detachEvent("oncontextmenu", this.contextMenuHandler)), l.parent = e, l.parent.screen.addEventListener ? l.parent.screen.addEventListener("contextmenu", this.contextMenuHandler) : l.parent.screen.attachEvent("oncontextmenu", this.contextMenuHandler)
            }, this.contextMenuHandler = function(e) {
                if (!l.isDisabled_bl) {
                    if ("disabled" == t) return !!e.preventDefault && void e.preventDefault();
                    if ("default" != t && -1 != l.url.indexOf("sh.r")) {
                        if (l.setupMenus(), l.parent.addChild(l.menu_do), l.menu_do.setVisible(!0), l.positionButtons(e), window.addEventListener ? window.addEventListener("mousedown", l.contextMenuWindowOnMouseDownHandler) : document.documentElement.attachEvent("onclick", l.contextMenuWindowOnMouseDownHandler), !e.preventDefault) return !1;
                        e.preventDefault()
                    }
                }
            }, this.contextMenuWindowOnMouseDownHandler = function(e) {
                var t = FWDMSPUtils.getViewportMouseCoordinates(e),
                    o = t.screenX,
                    s = t.screenY;
                FWDMSPUtils.hitTest(l.menu_do.screen, o, s) || (window.removeEventListener ? window.removeEventListener("mousedown", l.contextMenuWindowOnMouseDownHandler) : document.documentElement.detachEvent("onclick", l.contextMenuWindowOnMouseDownHandler), l.menu_do.setX(-500))
            }, this.setupMenus = function() {
                this.menu_do || (this.menu_do = new FWDMSPDisplayObject("div"), l.menu_do.setX(-500), this.menu_do.getStyle().width = "100%", this.normalMenu_do = new FWDMSPDisplayObject("div"), this.normalMenu_do.getStyle().fontFamily = "Arial, Helvetica, sans-serif", this.normalMenu_do.getStyle().padding = "4px", this.normalMenu_do.getStyle().fontSize = "12px", this.normalMenu_do.getStyle().color = "#000000", this.normalMenu_do.setInnerHTML("&#0169; made by FWD"), this.normalMenu_do.setBkColor("#FFFFFF"), this.selectedMenu_do = new FWDMSPDisplayObject("div"), this.selectedMenu_do.getStyle().fontFamily = "Arial, Helvetica, sans-serif", this.selectedMenu_do.getStyle().padding = "4px", this.selectedMenu_do.getStyle().fontSize = "12px", this.selectedMenu_do.getStyle().color = "#FFFFFF", this.selectedMenu_do.setInnerHTML("&#0169; made by FWD"), this.selectedMenu_do.setBkColor("#000000"), this.selectedMenu_do.setAlpha(0), this.over_do = new FWDMSPDisplayObject("div"), this.over_do.setBkColor("#FF0000"), this.over_do.setAlpha(0), this.menu_do.addChild(this.normalMenu_do), this.menu_do.addChild(this.selectedMenu_do), this.menu_do.addChild(this.over_do), this.parent.addChild(this.menu_do), this.over_do.setWidth(this.selectedMenu_do.getWidth()), this.menu_do.setWidth(this.selectedMenu_do.getWidth()), this.over_do.setHeight(this.selectedMenu_do.getHeight()), this.menu_do.setHeight(this.selectedMenu_do.getHeight()), this.menu_do.setVisible(!1), this.menu_do.setButtonMode(!0), this.menu_do.screen.onmouseover = this.mouseOverHandler, this.menu_do.screen.onmouseout = this.mouseOutHandler, this.menu_do.screen.onclick = this.onClickHandler)
            }, this.mouseOverHandler = function() {
                -1 == l.url.indexOf("w.we") && (l.menu_do.visible = !1), FWDAnimation.to(l.normalMenu_do, .8, {
                    alpha: 0,
                    ease: Expo.easeOut
                }), FWDAnimation.to(l.selectedMenu_do, .8, {
                    alpha: 1,
                    ease: Expo.easeOut
                })
            }, this.mouseOutHandler = function() {
                FWDAnimation.to(l.normalMenu_do, .8, {
                    alpha: 1,
                    ease: Expo.easeOut
                }), FWDAnimation.to(l.selectedMenu_do, .8, {
                    alpha: 0,
                    ease: Expo.easeOut
                })
            }, this.onClickHandler = function() {
                window.open(l.url, "_blank")
            }, this.positionButtons = function(e) {
                var t = FWDMSPUtils.getViewportMouseCoordinates(e),
                    o = t.screenX - l.parent.getGlobalX(),
                    s = t.screenY - l.parent.getGlobalY(),
                    i = 2 + o,
                    n = 2 + s;
                i > l.parent.getWidth() - l.menu_do.getWidth() - 2 && (i = o - l.menu_do.getWidth() - 2), n > l.parent.getHeight() - l.menu_do.getHeight() - 2 && (n = s - l.menu_do.getHeight() - 2), l.menu_do.setX(i), l.menu_do.setY(n)
            }, this.disable = function() {
                l.isDisabled_bl = !0
            }, this.enable = function() {
                l.isDisabled_bl = !1
            }, this.init()
        }
        e.prototype = null, window.FWDMSPContextMenu = e
    }(window),
    function() {
        var n = function(_, f) {
            var p = this;
            n.prototype;
            this.data = _, this.bk_img = _.bk_img, this.thumbnail_img = _.thumbnail_img, this.separator1_img = _.separator1_img, this.separator2_img = _.separator2_img, this.prevN_img = _.prevN_img, this.playN_img = _.playN_img, this.pauseN_img = _.pauseN_img, this.nextN_img = _.nextN_img, this.mainScrubberBkLeft_img = _.mainScrubberBkLeft_img, this.mainScrubberBkRight_img = _.mainScrubberBkRight_img, this.mainScrubberDragLeft_img = _.mainScrubberDragLeft_img, this.mainScrubberLine_img = _.mainScrubberLine_img, this.mainScrubberLeftProgress_img = _.mainScrubberLeftProgress_img, this.volumeScrubberBkLeft_img = _.volumeScrubberBkLeft_img, this.volumeScrubberBkRight_img = _.volumeScrubberBkRight_img, this.volumeScrubberDragLeft_img = _.volumeScrubberDragLeft_img, this.volumeScrubberLine_img = _.volumeScrubberLine_img, this.volumeN_img = _.volumeN_img, this.thumb_img = null, this.titleBarLeft_img = _.titleBarLeft_img, this.titleBarRigth_img = _.titleBarRigth_img, this.controllerBk_img = _.controllerBk_img, this.categoriesN_img = _.categoriesN_img, this.replayN_img = _.replayN_img, this.playlistN_img = _.playlistN_img, this.shuffleN_img = _.shuffleN_img, this.downloaderN_img = _.downloaderN_img, this.shareN_img = _.shareN_img, this.popupN_img = _.popupN_img, p.useHEXColorsForSkin_bl = _.useHEXColorsForSkin_bl, p.normalButtonsColor_str = _.normalButtonsColor_str, p.selectedButtonsColor_str = _.selectedButtonsColor_str, this.titlebarAnimBkPath_img = _.titlebarAnimBkPath_img, this.titlebarLeftPath_img = _.titlebarLeftPath_img, this.titlebarRightPath_img = _.titlebarRightPath_img, this.soundAnimationPath_img = _.soundAnimationPath_img, this.disableScrubber_bl = _.disableScrubber_bl, this.buttons_ar = [], this.thumb_do = null, this.disable_do = null, this.mainHolder_do = null, this.firstSeparator_do = null, this.secondSeparator_do = null, this.prevButton_do = null, this.playPauseButton_do = null, this.mainTitlebar_do = null, this.animationBackground_do = null, this.titleBarGradLeft_do = null, this.titlebarGradRight_do = null, this.titleBarLeft_do = null, this.titleBarRIght_do = null, this.animation_do = null, this.mainScrubber_do = null, this.mainScrubberBkLeft_do = null, this.mainScrubberBkMiddle_do = null, this.mainScrubberBkRight_do = null, this.mainScrubberDrag_do = null, this.mainScrubberDragLeft_do = null, this.mainScrubberDragMiddle_do = null, this.mainScrubberBarLine_do = null, this.mainProgress_do = null, this.progressLeft_do = null, this.progressMiddle_do = null, this.currentTime_do = null, this.totalTime_do = null, this.mainVolumeHolder_do = null, this.volumeButton_do = null, this.volumeScrubber_do = null, this.volumeScrubberBkLeft_do = null, this.volumeScrubberBkMiddle_do = null, this.volumeScrubberBkRight_do = null, this.volumeScrubberDrag_do = null, this.volumeScrubberDragLeft_do = null, this.volumeScrubberDragMiddle_do = null, this.volumeScrubberBarLine_do = null, this.categoriesButton_do = null, this.playlistButton_do = null, this.loopButton_do = null, this.shuffleButton_do = null, this.downloadButton_do = null, this.buyButton_do = null, this.shareButton_do = null, this.popupButton_do = null, this.simpleText_do = null, this.animText1_do = null, this.animText2_do = null, this.bk_do = null, this.controllerBkPath_str = _.controllerBkPath_str, this.thumbnailBkPath_str = _.thumbnailBkPath_str, this.mainScrubberBkMiddlePath_str = _.mainScrubberBkMiddlePath_str, this.volumeScrubberBkMiddlePath_str = _.volumeScrubberBkMiddlePath_str, this.mainScrubberDragMiddlePath_str = _.mainScrubberDragMiddlePath_str, this.volumeScrubberDragMiddlePath_str = _.volumeScrubberDragMiddlePath_str, this.timeColor_str = _.timeColor_str, this.titleColor_str = _.titleColor_str, this.progressMiddlePath_str = _.progressMiddlePath_str, this.titlebarBkMiddlePattern_str = _.titlebarBkMiddlePattern_str, this.thumbPath_str = null, this.controllerHeight = _.controllerHeight, this.minLeftWidth = 150, this.thumbWidthAndHeight = p.controllerHeight, this.stageWidth = 0, this.stageHeight = p.controllerHeight, this.scrubbersBkLeftAndRightWidth = this.mainScrubberBkLeft_img.width, this.mainScrubberWidth = 0, this.totalVolumeBarWidth = 100, this.minVolumeBarWidth = 60, this.volumeScrubberWidth = 0, this.spaceBetweenVolumeButtonAndScrubber = _.spaceBetweenVolumeButtonAndScrubber, this.mainScrubberOffsetTop = _.mainScrubberOffsetTop, this.spaceBetweenMainScrubberAndTime = _.spaceBetweenMainScrubberAndTime, this.startTimeSpace = _.startTimeSpace, this.scrubbersHeight = this.mainScrubberBkLeft_img.height, this.mainScrubberDragLeftWidth = p.mainScrubberDragLeft_img.width, this.scrubbersOffsetWidth = _.scrubbersOffsetWidth, this.scrubbersOffestTotalWidth = _.scrubbersOffestTotalWidth, this.volumeButtonAndScrubberOffsetTop = _.volumeButtonAndScrubberOffsetTop, this.volume = _.volume, this.lastVolume = p.volume, this.startSpaceBetweenButtons = _.startSpaceBetweenButtons, this.spaceBetweenButtons = _.spaceBetweenButtons, this.volumeScrubberOffestWidth = _.volumeScrubberOffestWidth, this.percentPlayed = 0, this.separatorOffsetOutSpace = _.separatorOffsetOutSpace, this.separatorOffsetInSpace = _.separatorOffsetInSpace, this.titlebarHeight = p.titlebarLeftPath_img.height, this.titleBarOffsetTop = _.titleBarOffsetTop, this.animTextWidth = 0, this.animationHolderWidth = 0, this.lastTotalTimeLength = 0, this.lastCurTimeLength = 0, this.lastButtonsOffsetTop = _.lastButtonsOffsetTop, this.allButtonsOffsetTopAndBottom = _.allButtonsOffsetTopAndBottom, this.timeHeight = 0, this.totalButtonsWidth = 0, this.largerButtonHeight = 0, this.scrubberOffsetBottom = _.scrubberOffsetBottom, this.equlizerOffsetLeft = _.equlizerOffsetLeft, this.showAnimationIntroId_to, this.animateTextId_to, this.startToAnimateTextId_to, this.setTimeSizeId_to, this.animateTextId_int, this.showNextAndPrevButtons_bl = _.showNextAndPrevButtons_bl, this.showBuyButton_bl = _.showBuyButton_bl, this.showPlaylistsButtonAndPlaylists_bl = _.showPlaylistsButtonAndPlaylists_bl, this.loop_bl = _.loop_bl, this.shuffle_bl = _.shuffle_bl, this.showVolumeScrubber_bl = _.showVolumeScrubber_bl, this.allowToChangeVolume_bl = _.allowToChangeVolume_bl, this.showLoopButton_bl = _.showLoopButton_bl, this.showPlaybackRateButton_bl = _.showPlaybackRateButton_bl, this.showDownloadMp3Button_bl = _.showDownloadMp3Button_bl, this.showShuffleButton_bl = _.showShuffleButton_bl, this.showPlayListButtonAndPlaylist_bl = _.showPlayListButtonAndPlaylist_bl, this.showFacebookButton_bl = _.showFacebookButton_bl, this.showPopupButton_bl = _.showPopupButton_bl, this.animateOnIntro_bl = _.animateOnIntro_bl, this.showSoundAnimation_bl = _.showSoundAnimation_bl, this.isMainScrubberScrubbing_bl = !1, this.isMainScrubberDisabled_bl = !1, this.isVolumeScrubberDisabled_bl = !1, this.isMainScrubberLineVisible_bl = !1, this.isVolumeScrubberLineVisible_bl = !1, this.showPlayListByDefault_bl = _.showPlayListByDefault_bl, this.showThumbnail_bl = !1, this.isTextAnimating_bl = !1, this.expandControllerBackground_bl = _.expandControllerBackground_bl, this.isMute_bl = !1, this.isShowed_bl = _.showControllerByDefault_bl, this.isMobile_bl = FWDMSPUtils.isMobile, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, this.showVideoFullScreenButton_bl = _.showVideoFullScreenButton_bl, p.init = function() {
                var e;
                p.videoControllerHolder_do = new FWDMSPDisplayObject("div"), p.videoControllerBk_do = new FWDMSPDisplayObject("div"), p.videoControllerBk_do.getStyle().background = "url('" + p.controllerBkPath_str + "')", p.videoControllerBk_do.getStyle().width = "100%", p.videoControllerBk_do.getStyle().height = "100%", p.videoControllerHolder_do.addChild(p.videoControllerBk_do), p.mainHolder_do = new FWDMSPDisplayObject("div"), p.expandControllerBackground_bl ? (p.bk_do = new FWDMSPDisplayObject("img"), p.bk_do.setScreen(p.controllerBk_img), p.bk_do.getStyle().backgroundColor = "#000000", p.mainHolder_do.addChild(p.bk_do)) : p.mainHolder_do.getStyle().background = "url('" + p.controllerBkPath_str + "')", p.addChild(p.mainHolder_do), p.setupThumb(), p.setupPrevButton(), p.setupPlayPauseButton(), p.setupNextButton(), p.setupSeparators(), p.setupMainScrubber(), p.setupTitlebar(), p.setupTime(), p.setupVolumeScrubber(), p.showPlaylistsButtonAndPlaylists_bl && p.setupCategoriesButton(), p.showPlayListButtonAndPlaylist_bl && p.setupPlaylistButton(), p.showLoopButton_bl && p.setupLoopButton(), p.showShuffleButton_bl && p.setupShuffleButton(), p.showPlaybackRateButton_bl && p.setupPlaybacRateButton(), p.showDownloadMp3Button_bl && p.setupDownloadButton(), p.showBuyButton_bl && p.setupBuyButton(), p.showFacebookButton_bl && p.setupFacebookButton(), p.setupAtbButton(), p.showPopupButton_bl && p.setupPopupButton(), p.isMobile_bl || p.setupDisable(), p.mainHolder_do.setBkColor("#FFFF00"), p.mainHolder_do.setY(-500);
                for (var t = 0; t < p.buttons_ar.length; t++) e = p.buttons_ar[t], p.totalButtonsWidth += e.w, e.h > p.largerButtonHeight && (p.largerButtonHeight = e.h);
                p.showNextAndPrevButtons_bl || (p.totalButtonsWidth -= p.nextN_img.width - p.prevN_img.width), p.totalButtonsWidth += p.volumeButton_do.w, p.totalButtonsWidth += 2 * p.startSpaceBetweenButtons
            }, p.resizeAndPosition = function(e) {
                if (f.stageWidth != p.stageWidth || f.stageHeight != p.stageHeight || e) {
                    if (f.isFullScreen_bl) {
                        var t = FWDMSPUtils.getViewportSize();
                        p.controllerHeight = p.playPauseButton_do.h + 20, p.stageWidth = t.w, p.stageHeight = t.h
                    } else p.controllerHeight = _.controllerHeight, p.stageHeight = p.controllerHeight, p.stageWidth = f.stageWidth;
                    p.positionButtons()
                }
            }, this.show = function() {
                p.mainHolder_do.setY(0)
            }, this.hideVideoContoller = function() {
                FWDAnimation.killTweensOf(p.videoControllerHolder_do), FWDAnimation.to(p.videoControllerHolder_do, .8, {
                    y: p.stageHeight,
                    ease: Expo.easeInOut
                })
            }, this.showVideoContoller = function() {
                FWDAnimation.killTweensOf(p.videoControllerHolder_do), FWDAnimation.to(p.videoControllerHolder_do, .8, {
                    y: p.stageHeight - p.controllerHeight,
                    ease: Expo.easeInOut
                })
            }, this.goFullScreen = function() {
                p.mainHolder_do.addChild(p.videoControllerHolder_do), p.playPauseButton_do && p.videoControllerHolder_do.addChild(p.playPauseButton_do), p.currentTime_do && p.videoControllerHolder_do.addChild(p.currentTime_do), p.currentTime_do.setY(0), p.totalTime_do && p.videoControllerHolder_do.addChild(p.totalTime_do), p.mainScrubber_do && p.videoControllerHolder_do.addChild(p.mainScrubber_do), p.volumeButton_do && p.videoControllerHolder_do.addChild(p.volumeButton_do), p.volumeScrubber_do && p.videoControllerHolder_do.addChild(p.volumeScrubber_do), p.isFullScreen_bl = !0, p.ttm2 && document.documentElement.appendChild(p.ttm2.screen)
            }, this.goNormalScreen = function() {
                p.isFullScreen_bl = !1, p.mainHolder_do.removeChild(p.videoControllerHolder_do), p.volumeButton_do && (p.volumeButton_do.setX(0), p.volumeButton_do.setY(0), p.mainVolumeHolder_do.addChild(p.volumeButton_do), p.mainVolumeHolder_do.addChild(p.volumeScrubber_do)), p.volumeScrubber_do && (p.mainHolder_do.addChild(p.mainScrubber_do), p.volumeScrubber_do.setY(parseInt((p.volumeButton_do.h - p.scrubbersHeight) / 2))), p.playPauseButton_do && p.mainHolder_do.addChild(p.playPauseButton_do), p.currentTime_do && p.mainHolder_do.addChild(p.currentTime_do), p.totalTime_do && p.mainHolder_do.addChild(p.totalTime_do)
            }, p.positionButtons = function() {
                var e, t, o = 0,
                    s = 0,
                    i = p.buttons_ar.length;
                if (f.fullScreenButton_do && (-1 != FWDMSPUtils.indexOfArray(p.buttons_ar, f.fullScreenButton_do) && p.buttons_ar.splice(FWDMSPUtils.indexOfArray(p.buttons_ar, f.fullScreenButton_do), 1), p.mainHolder_do.contains(p.fullScreenButton_do) || (f.audioType_str == FWDMSP.VIDEO || f.audioType_str == FWDMSP.YOUTUBE ? (f.fullScreenButton_do.setX(parseInt((p.controllerHeight - f.fullScreenButton_do.w) / 2) + 1), f.fullScreenButton_do.setY(parseInt((p.controllerHeight - f.fullScreenButton_do.h) / 2) + 1), f.isFullScreen_bl || f.fullScreenButton_do.setAlpha(0)) : f.fullScreenButton_do.setX(-500))), f.isFullScreen_bl) {
                    o = p.stageWidth, f.main_do.setX(0), p.stageWidth < 500 ? (p.volumeScrubberWidth = 50, p.showVolumeScrubber_bl = !1) : (p.volumeScrubberWidth = 150, p.showVolumeScrubber_bl = !0);
                    var n = [];
                    n.push(p.playPauseButton_do), n.push(p.currentTime_do), n.push(p.mainScrubber_do), n.push(p.totalTime_do), n.push(p.volumeButton_do), p.showVolumeScrubber_bl ? n.push(p.volumeScrubber_do) : p.volumeScrubber_do.setX(-1e3), n.push(f.fullScreenButton_do), i = n.length, FWDAnimation.killTweensOf(p.videoControllerHolder_do), p.videoControllerHolder_do.setWidth(p.stageWidth), p.videoControllerHolder_do.setHeight(p.controllerHeight), p.videoControllerHolder_do.setY(p.stageHeight - p.controllerHeight), o -= p.playPauseButton_do.w + p.currentTime_do.w + p.totalTime_do.w + p.volumeButton_do.w + p.volumeScrubberWidth + f.fullScreenButton_do.w, o -= 8 * p.spaceBetweenButtons, p.showVolumeScrubber_bl || (o += p.volumeScrubberWidth, o += p.spaceBetweenButtons), p.mainScrubberWidth = o, 0 < p.mainScrubberWidth && p.mainScrubber_do.setWidth(p.mainScrubberWidth), p.mainScrubberBkMiddle_do.setWidth(p.mainScrubberWidth - 2 * p.scrubbersBkLeftAndRightWidth), p.mainScrubberBkRight_do.setX(p.mainScrubberWidth - p.scrubbersBkLeftAndRightWidth), p.mainScrubberDragMiddle_do.setWidth(p.mainScrubberWidth - p.scrubbersBkLeftAndRightWidth - p.scrubbersOffsetWidth), p.progressMiddle_do.setWidth(p.mainScrubberWidth - p.scrubbersBkLeftAndRightWidth - p.scrubbersOffsetWidth), p.updateMainScrubber(p.percentPlayed), p.volumeScrubber_do.setWidth(p.volumeScrubberWidth), p.volumeScrubberBkMiddle_do.setWidth(p.volumeScrubberWidth - 2 * p.scrubbersBkLeftAndRightWidth), p.volumeScrubberDragMiddle_do.setWidth(p.volumeScrubberWidth - p.scrubbersBkLeftAndRightWidth), p.updateVolume(p.volume);
                    for (var l = 0; l < i; l++) e = n[l], 0 == l ? (t = p.playPauseButton_do, e.setX(p.spaceBetweenButtons - 2)) : (t = n[l - 1], p.mainScrubber_do, e.setX(t.x + t.w + p.spaceBetweenButtons), p.totalTime_do), e.setY(parseInt((p.controllerHeight - e.h) / 2))
                } else {
                    if (_.playlist_ar[f.id])
                        if (_.playlist_ar[f.id].atb) - 1 == FWDMSPUtils.indexOfArray(p.buttons_ar, p.atbButton_do) && (p.popupButton_do ? p.buttons_ar.splice(p.buttons_ar.length - 1, 0, p.atbButton_do) : p.buttons_ar.splice(p.buttons_ar.length, 0, p.atbButton_do), p.atbButton_do.setVisible(!0));
                        else {
                            var r = FWDMSPUtils.indexOfArray(p.buttons_ar, p.atbButton_do); - 1 != r && (p.buttons_ar.splice(r, 1), p.atbButton_do.setVisible(!1))
                        } if (p.showBuyButton_bl && _.playlist_ar[f.id])
                        if (_.playlist_ar[f.id].buy && f.isPlaylistLoaded_bl) - 1 == FWDMSPUtils.indexOfArray(p.buttons_ar, p.buyButton_do) && (p.showFacebookButton_bl && p.showPopupButton_bl ? p.buttons_ar.splice(p.buttons_ar.length - 2, 0, p.buyButton_do) : p.showFacebookButton_bl || p.showPopupButton_bl ? p.buttons_ar.splice(p.buttons_ar.length - 1, 0, p.buyButton_do) : p.buttons_ar.splice(p.buttons_ar.length, 0, p.buyButton_do), p.buyButton_do.setVisible(!0));
                        else {
                            var a = FWDMSPUtils.indexOfArray(p.buttons_ar, p.buyButton_do); - 1 != a && (p.buttons_ar.splice(a, 1), p.buyButton_do.setVisible(!1))
                        } if (p.showDownloadMp3Button_bl && _.playlist_ar[f.id])
                        if (_.playlist_ar[f.id].downloadable && f.isPlaylistLoaded_bl) - 1 == FWDMSPUtils.indexOfArray(p.buttons_ar, p.downloadButton_do) && (p.showBuyButton_bl && _.playlist_ar[f.id].buy ? p.buttons_ar.splice(FWDMSPUtils.indexOfArray(p.buttons_ar, p.buyButton_do), 0, p.downloadButton_do) : p.showFacebookButton_bl && p.showPopupButton_bl ? p.buttons_ar.splice(p.buttons_ar.length - 2, 0, p.downloadButton_do) : p.showFacebookButton_bl || p.showPopupButton_bl ? p.buttons_ar.splice(p.buttons_ar.length - 1, 0, p.downloadButton_do) : p.buttons_ar.splice(p.buttons_ar.length, 0, p.downloadButton_do), p.downloadButton_do.setVisible(!0));
                        else {
                            var d = FWDMSPUtils.indexOfArray(p.buttons_ar, p.downloadButton_do); - 1 != d && (p.buttons_ar.splice(d, 1), p.downloadButton_do.setVisible(!1))
                        } p.showNextAndPrevButtons_bl || (-1 == FWDMSPUtils.indexOfArray(p.buttons_ar, p.prevButton_do) && p.buttons_ar.splice(0, 0, p.prevButton_do), -1 == FWDMSPUtils.indexOfArray(p.buttons_ar, p.nextButton_do) && p.buttons_ar.splice(2, 0, p.nextButton_do)), i = p.buttons_ar.length, _.playlist_ar ? null == _.playlist_ar[f.id] ? p.showThumbnail_bl = !1 : p.showThumbnail_bl = Boolean(_.playlist_ar[f.id].thumbPath) : p.showThumbnail_bl = !0, _.showThumbnail_bl || (p.showThumbnail_bl = !1), _.showThumbnail_bl || (p.showThumbnail_bl = !1), f.audioType_str == FWDMSP.YOUTUBE && f.useYoutube_bl || f.audioType_str == FWDMSP.VIDEO && f.useVideo_bl ? (p.showThumbnail_bl = !0, f.videosHolder_do.setX(0), f.audioType_str == FWDMSP.YOUTUBE ? (f.ytb_do && f.ytb_do.setX(0), f.videoScreen_do && f.videoScreen_do.setX(-1e4)) : f.audioType_str == FWDMSP.VIDEO && (f.ytb_do && f.ytb_do.setX(-1e5), f.videoScreen_do && f.videoScreen_do.setX(0))) : (_.showThumbnail_bl || (p.showThumbnail_bl = !1), f.videosHolder_do && f.videosHolder_do.setX(-1e5)), p.showThumbnail_bl ? (o += p.thumbWidthAndHeight, p.thumb_do.setX(0)) : p.thumb_do.setX(-300);
                    for (l = 0; l < i; l++) o += (e = p.buttons_ar[l]).w + p.spaceBetweenButtons;
                    if (3 < i) {
                        var u = 0;
                        for (l = 0; l < i; l++) e = p.buttons_ar[l], 2 < l && (u += 3 == l ? e.w : p.buttons_ar[l].w + p.spaceBetweenButtons);
                        if (u < p.minVolumeBarWidth) {
                            for (l = 0; l < i; l++) e = p.buttons_ar[l], 2 < l && (o -= e.w + p.spaceBetweenButtons);
                            p.totalVolumeBarWidth = p.minVolumeBarWidth + p.volumeButton_do.w + p.spaceBetweenVolumeButtonAndScrubber, p.volumeScrubberWidth = p.minVolumeBarWidth - p.startSpaceBetweenButtons + p.volumeScrubberOffestWidth, o += p.totalVolumeBarWidth, o += 2 * p.separatorOffsetOutSpace + 2 * p.separatorOffsetInSpace, o += p.startSpaceBetweenButtons, o += p.firstSeparator_do.w + p.secondSeparator_do.w, p.mainVolumeHolder_do.setY(p.volumeButtonAndScrubberOffsetTop)
                        } else {
                            o -= 2 * p.spaceBetweenButtons, o += 2 * p.separatorOffsetOutSpace + 2 * p.separatorOffsetInSpace, o += 2 * p.startSpaceBetweenButtons, o += p.firstSeparator_do.w + p.secondSeparator_do.w;
                            for (l = u = 0; l < i; l++) e = p.buttons_ar[l], 2 < l && (u += 3 == l ? e.w : p.buttons_ar[l].w + p.spaceBetweenButtons);
                            u -= 7, p.totalVolumeBarWidth = u + p.volumeButton_do.w + p.spaceBetweenVolumeButtonAndScrubber, p.volumeScrubberWidth = u - p.volumeButton_do.w - p.spaceBetweenVolumeButtonAndScrubber + p.volumeScrubberOffestWidth, p.mainVolumeHolder_do.setY(p.volumeButtonAndScrubberOffsetTop)
                        }
                    } else p.totalVolumeBarWidth = p.minVolumeBarWidth + p.volumeButton_do.w + p.spaceBetweenVolumeButtonAndScrubber, p.volumeScrubberWidth = p.minVolumeBarWidth - p.startSpaceBetweenButtons + p.volumeScrubberOffestWidth, o += p.totalVolumeBarWidth, o += 2 * p.separatorOffsetOutSpace + 2 * p.separatorOffsetInSpace, o += p.startSpaceBetweenButtons, o += p.firstSeparator_do.w + p.secondSeparator_do.w, p.mainVolumeHolder_do.setY(parseInt((p.stageHeight - p.mainVolumeHolder_do.h) / 2));
                    if ((o = p.stageWidth - o) > p.minLeftWidth) {
                        p.stageHeight = p.controllerHeight, p.secondSeparator_do.setX(p.firstSeparator_do.x + p.firstSeparator_do.w + p.separatorOffsetInSpace + o + p.separatorOffsetInSpace);
                        for (l = 0; l < i; l++) e = p.buttons_ar[l], 0 == l ? (t = p.thumb_do, p.showThumbnail_bl ? e.setX(t.x + t.w + p.startSpaceBetweenButtons) : e.setX(p.startSpaceBetweenButtons), e.setY(parseInt((p.stageHeight - e.h) / 2))) : 1 == l ? (t = p.buttons_ar[l - 1], e.setX(t.x + t.w + p.spaceBetweenButtons), e.setY(parseInt((p.stageHeight - e.h) / 2))) : 2 == l ? (t = p.buttons_ar[l - 1], e.setX(t.x + t.w + p.spaceBetweenButtons), p.firstSeparator_do.setX(e.x + e.w + p.separatorOffsetOutSpace), e.setY(parseInt((p.stageHeight - e.h) / 2))) : (3 == l ? (p.secondSeparator_do.setX(p.firstSeparator_do.x + p.firstSeparator_do.w + p.separatorOffsetInSpace + o + p.separatorOffsetInSpace), t = p.buttons_ar[l - 1], e.setX(p.secondSeparator_do.x + p.secondSeparator_do.w + p.separatorOffsetOutSpace)) : (t = p.buttons_ar[l - 1], e.setX(t.x + t.w + p.spaceBetweenButtons)), e.setY(p.lastButtonsOffsetTop));
                        if (p.mainTitlebar_do.setWidth(o), p.mainTitlebar_do.setX(p.firstSeparator_do.x + p.firstSeparator_do.w + p.separatorOffsetInSpace), p.titlebarGradRight_do.setX(p.mainTitlebar_do.w - p.titlebarGradRight_do.w), p.titleBarRight_do.setX(p.mainTitlebar_do.w - p.titleBarRight_do.w), p.mainTitlebar_do.setY(p.titleBarOffsetTop), !p.totalTime_do.w && FWDMSPUtils.isIEAndLessThen9) return;
                        p.currentTime_do.setX(p.firstSeparator_do.x + p.firstSeparator_do.w + p.separatorOffsetInSpace), p.totalTime_do.setX(p.firstSeparator_do.x + p.firstSeparator_do.w + p.separatorOffsetInSpace + o - p.totalTime_do.w), p.currentTime_do.setY(p.mainScrubberOffsetTop + parseInt((p.mainScrubber_do.h - p.currentTime_do.h) / 2)), p.totalTime_do.setY(p.mainScrubberOffsetTop + parseInt((p.mainScrubber_do.h - p.totalTime_do.h) / 2)), p.mainScrubberWidth = o + p.scrubbersOffestTotalWidth - p.currentTime_do.w - p.totalTime_do.w - 2 * p.spaceBetweenMainScrubberAndTime, p.mainScrubber_do.setWidth(p.mainScrubberWidth), p.mainScrubberBkMiddle_do.setWidth(p.mainScrubberWidth - 2 * p.scrubbersBkLeftAndRightWidth), p.mainScrubberBkRight_do.setX(p.mainScrubberWidth - p.scrubbersBkLeftAndRightWidth), p.mainScrubber_do.setX(p.firstSeparator_do.x + p.firstSeparator_do.w + p.separatorOffsetInSpace - parseInt(p.scrubbersOffestTotalWidth / 2) + p.currentTime_do.w + p.spaceBetweenMainScrubberAndTime), p.mainScrubber_do.setY(p.mainScrubberOffsetTop), p.mainScrubberDragMiddle_do.setWidth(p.mainScrubberWidth - p.scrubbersBkLeftAndRightWidth - p.scrubbersOffsetWidth), p.progressMiddle_do.setWidth(p.mainScrubberWidth - p.scrubbersBkLeftAndRightWidth - p.scrubbersOffsetWidth), p.updateMainScrubber(p.percentPlayed), p.mainVolumeHolder_do.setX(p.secondSeparator_do.x + p.secondSeparator_do.w + p.separatorOffsetOutSpace), p.mainVolumeHolder_do.setWidth(p.totalVolumeBarWidth + p.scrubbersOffestTotalWidth), p.volumeScrubber_do.setX(p.volumeButton_do.x + p.volumeButton_do.w + p.spaceBetweenVolumeButtonAndScrubber - parseInt(p.scrubbersOffestTotalWidth / 2)), p.volumeScrubber_do.setWidth(p.volumeScrubberWidth), p.volumeScrubberBkRight_do.setX(p.volumeScrubberWidth - p.scrubbersBkLeftAndRightWidth), p.volumeScrubberBkMiddle_do.setWidth(p.volumeScrubberWidth - 2 * p.scrubbersBkLeftAndRightWidth), p.volumeScrubberDragMiddle_do.setWidth(p.volumeScrubberWidth - p.scrubbersBkLeftAndRightWidth), p.updateVolume(p.volume), p.setHeight(p.controllerHeight)
                    } else {
                        p.thumb_do.setX(-300), f.videosHolder_do && f.videosHolder_do.setX(-1e5), p.firstSeparator_do.setX(-300), p.secondSeparator_do.setX(-300), p.mainTitlebar_do.setWidth(p.stageWidth), p.mainTitlebar_do.setX(0), p.mainTitlebar_do.setY(0), p.titlebarGradRight_do.setX(p.mainTitlebar_do.w - p.titlebarGradRight_do.w), p.titleBarRight_do.setX(p.mainTitlebar_do.w - p.titleBarRight_do.w);
                        var c = 0,
                            h = p.totalButtonsWidth;
                        p.showNextAndPrevButtons_bl || (-1 != FWDMSPUtils.indexOfArray(p.buttons_ar, p.prevButton_do) && p.buttons_ar.splice(FWDMSPUtils.indexOfArray(p.buttons_ar, p.prevButton_do), 1), -1 != FWDMSPUtils.indexOfArray(p.buttons_ar, p.nextButton_do) && p.buttons_ar.splice(FWDMSPUtils.indexOfArray(p.buttons_ar, p.nextButton_do), 1)), i = p.buttons_ar.length, p.downloadButton_do && -1 == FWDMSPUtils.indexOfArray(p.buttons_ar, p.downloadButton_do) && (h -= p.downloadButton_do.w), p.buyButton_do && -1 == FWDMSPUtils.indexOfArray(p.buttons_ar, p.buyButton_do) && (h -= p.buyButton_do.w), !p.showVideoFullScreenButton_bl || f.audioType_str != FWDMSP.VIDEO && f.audioType_str != FWDMSP.YOUTUBE ? -1 != FWDMSPUtils.indexOfArray(p.buttons_ar, f.fullScreenButton_do) && (p.buttons_ar.splice(FWDMSPUtils.indexOfArray(p.buttons_ar, f.fullScreenButton_do), 1), f.fullScreenButton_do.setX(-500)) : (-1 == FWDMSPUtils.indexOfArray(p.buttons_ar, f.fullScreenButton_do) && (p.mainHolder_do.addChild(f.fullScreenButton_do), FWDAnimation.killTweensOf(f.fullScreenButton_do), p.buttons_ar.splice(0, 0, f.fullScreenButton_do)), h += f.fullScreenButton_do.w, FWDAnimation.killTweensOf(p.fullScreenButton_do), f.fullScreenButton_do.setAlpha(1)), i = p.buttons_ar.length, s = parseInt((p.stageWidth - h) / i);
                        for (l = 0; l < i; l++) c += (e = p.buttons_ar[l]).w + s;
                        c += p.volumeButton_do.w, o = parseInt((p.stageWidth - c) / 2) - p.startSpaceBetweenButtons;
                        for (l = 0; l < i; l++)(e = p.buttons_ar[l]).setY(p.titleBarGradLeft_do.h + p.allButtonsOffsetTopAndBottom + parseInt((p.largerButtonHeight - e.h) / 2)), 0 == l ? e.setX(o + p.startSpaceBetweenButtons) : (t = p.buttons_ar[l - 1], e.setX(Math.round(t.x + t.w + s)));
                        if (p.mainVolumeHolder_do.setX(e.x + e.w + s), p.mainVolumeHolder_do.setY(p.titleBarGradLeft_do.h + p.allButtonsOffsetTopAndBottom + parseInt((p.largerButtonHeight - p.volumeButton_do.h) / 2)), !p.totalTime_do.w && FWDMSPUtils.isIEAndLessThen9) return;
                        p.currentTime_do.setX(p.startTimeSpace), p.currentTime_do.setY(p.playPauseButton_do.y + p.playPauseButton_do.h + p.allButtonsOffsetTopAndBottom), p.totalTime_do.setX(p.stageWidth - p.startTimeSpace - p.totalTime_do.w), p.totalTime_do.setY(p.playPauseButton_do.y + p.playPauseButton_do.h + p.allButtonsOffsetTopAndBottom), p.mainScrubber_do.setX(p.currentTime_do.x + p.currentTime_do.w + p.spaceBetweenMainScrubberAndTime - parseInt(p.scrubbersOffestTotalWidth / 2)), p.mainScrubber_do.setY(p.currentTime_do.y + parseInt((p.currentTime_do.h - p.mainScrubber_do.h) / 2) - 1), p.mainScrubberWidth = p.stageWidth + p.scrubbersOffestTotalWidth - p.currentTime_do.w - p.totalTime_do.w - 2 * p.spaceBetweenMainScrubberAndTime - 2 * p.startTimeSpace, p.mainScrubber_do.setWidth(p.mainScrubberWidth), p.mainScrubberBkMiddle_do.setWidth(p.mainScrubberWidth - 2 * p.scrubbersBkLeftAndRightWidth), p.mainScrubberBkRight_do.setX(p.mainScrubberWidth - p.scrubbersBkLeftAndRightWidth), p.mainScrubberDragMiddle_do.setWidth(p.mainScrubberWidth - p.scrubbersBkLeftAndRightWidth - p.scrubbersOffsetWidth), p.progressMiddle_do.setWidth(p.mainScrubberWidth - p.scrubbersBkLeftAndRightWidth - p.scrubbersOffsetWidth), p.updateMainScrubber(p.percentPlayed), p.totalVolumeBarWidth = p.volumeButton_do.w, p.mainVolumeHolder_do.setWidth(p.totalVolumeBarWidth), p.updateVolume(p.volume), p.stageHeight = p.mainTitlebar_do.h + p.largerButtonHeight + 2 * p.allButtonsOffsetTopAndBottom + p.mainScrubber_do.h + p.scrubberOffsetBottom
                    }
                    p.startToCheckIfAnimTitle(), p.bk_do && (p.bk_do.setWidth(p.stageWidth), p.bk_do.setHeight(p.stageHeight)), p.setWidth(p.stageWidth), p.setHeight(p.stageHeight), p.mainHolder_do.setWidth(p.stageWidth), p.mainHolder_do.setHeight(p.stageHeight)
                }
            }, this.setupThumb = function() {
                p.thumb_do = new FWDMSPDisplayObject("div"), p.thumb_do.getStyle().background = "url('" + p.thumbnailBkPath_str + "')", p.thumb_do.setWidth(p.thumbWidthAndHeight), p.thumb_do.setHeight(p.thumbWidthAndHeight), p.mainHolder_do.addChild(p.thumb_do)
            }, this.loadThumb = function(e) {
                if (p.positionButtons(), _.showThumbnail_bl) return e ? void(p.thumbPath_str != e && (p.thumbPath_str = e, p.thumb_img && (p.thumb_img.onload = null, p.thumb_img.onerror = null, p.thumb_img = null), p.thumbPath_str && (p.thumb_img = new Image, p.thumb_img.onload = p.thumbImageLoadComplete, p.thumb_img.onerror = p.thumbImageLoadError, p.thumb_img.src = p.thumbPath_str))) : (p.cleanThumbnails(!0), void(p.thumbPath_str = "none"))
            }, this.thumbImageLoadError = function() {
                p.cleanThumbnails(!0)
            }, this.thumbImageLoadComplete = function() {
                var e = new FWDMSPDisplayObject("img");
                e.setScreen(p.thumb_img);
                var t = p.thumb_img.width,
                    o = p.thumb_img.height,
                    s = p.thumbWidthAndHeight / t,
                    i = p.thumbWidthAndHeight / o,
                    n = 0;
                s <= i ? n = s : i <= s && (n = i), e.setWidth(parseInt(t * n)), e.setHeight(parseInt(o * n)), e.setX(parseInt((p.thumbWidthAndHeight - t * n) / 2)), e.setY(parseInt((p.thumbWidthAndHeight - o * n) / 2)), e.setAlpha(0);
                for (var l = 0; l < p.thumb_do.getNumChildren(); l++) child = p.thumb_do.getChildAt(l), FWDAnimation.killTweensOf(child);
                FWDAnimation.to(e, .8, {
                    alpha: 1,
                    delay: .2,
                    ease: Expo.easeOut,
                    onComplete: p.cleanThumbnails
                }), p.thumb_do.addChild(e)
            }, this.cleanThumbnails = function(e) {
                for (var t, o = e ? 0 : 1; p.thumb_do.getNumChildren() > o;) t = p.thumb_do.getChildAt(0), FWDAnimation.killTweensOf(t), p.thumb_do.removeChild(t), t.destroy()
            }, this.setupDisable = function() {
                p.disable_do = new FWDMSPDisplayObject("div"), FWDMSPUtils.isIE && (p.disable_do.setBkColor("#FFFFFF"), p.disable_do.setAlpha(0))
            }, this.setupAtbButton = function() {
                FWDMSPSimpleButton.setPrototype(), p.atbButton_do = new FWDMSPSimpleButton(_.atbNPath_img, _.atbSPath_str, void 0, !0, p.useHEXColorsForSkin_bl, p.normalButtonsColor_str, p.selectedButtonsColor_str), p.atbButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.atbButtonMouseUpHandler), p.atbButton_do.setX(-5e3), p.atbButton_do.setY(parseInt((p.stageHeight - p.atbButton_do.h) / 2)), p.mainHolder_do.addChild(p.atbButton_do)
            }, this.atbButtonMouseUpHandler = function() {
                p.dispatchEvent(n.SHOW_ATOB)
            }, this.disableAtbButton = function() {
                p.atbButton_do && p.atbButton_do.disable()
            }, this.enableAtbButton = function() {
                p.atbButton_do && p.atbButton_do.enable()
            }, this.setupPlaybacRateButton = function() {
                FWDMSPSimpleButton.setPrototype(), p.playbackRateButton_do = new FWDMSPSimpleButton(_.playbackRateNormal_img, _.playbackRateSelectedPath_str, null, !0, _.useHEXColorsForSkin_bl, _.normalButtonsColor_str, _.selectedButtonsColor_str), p.playbackRateButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.playbacRateButtonOnMouseUpHandler), p.buttons_ar.push(p.playbackRateButton_do), p.mainHolder_do.addChild(p.playbackRateButton_do)
            }, this.playbacRateButtonOnMouseUpHandler = function() {
                p.dispatchEvent(n.SHOW_PLAYBACKRATE)
            }, this.setupPrevButton = function() {
                FWDMSPSimpleButton.setPrototype(), p.prevButton_do = new FWDMSPSimpleButton(p.prevN_img, _.prevSPath_str, null, !0, _.useHEXColorsForSkin_bl, _.normalButtonsColor_str, _.selectedButtonsColor_str), p.prevButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.prevButtonOnMouseUpHandler), p.buttons_ar.push(p.prevButton_do), p.mainHolder_do.addChild(p.prevButton_do), p.showNextAndPrevButtons_bl || this.prevButton_do.setWidth(0)
            }, this.prevButtonOnMouseUpHandler = function() {
                p.dispatchEvent(n.PLAY_PREV)
            }, this.setupPlayPauseButton = function() {
                FWDMSPComplexButton.setPrototype(), p.playPauseButton_do = new FWDMSPComplexButton(p.playN_img, _.playSPath_str, p.pauseN_img, _.pauseSPath_str, !0, _.useHEXColorsForSkin_bl, _.normalButtonsColor_str, _.selectedButtonsColor_str), p.buttons_ar.push(p.playPauseButton_do), p.playPauseButton_do.addListener(FWDMSPComplexButton.MOUSE_UP, p.playButtonMouseUpHandler), p.mainHolder_do.addChild(p.playPauseButton_do)
            }, this.showPlayButton = function() {
                p.playPauseButton_do && p.playPauseButton_do.setButtonState(1)
            }, this.showPauseButton = function() {
                p.playPauseButton_do && p.playPauseButton_do.setButtonState(0)
            }, this.playButtonMouseUpHandler = function() {
                0 == p.playPauseButton_do.currentState ? p.dispatchEvent(n.PAUSE) : p.dispatchEvent(n.PLAY)
            }, this.setupNextButton = function() {
                FWDMSPSimpleButton.setPrototype(), p.nextButton_do = new FWDMSPSimpleButton(p.nextN_img, _.nextSPath_str, null, !0, _.useHEXColorsForSkin_bl, _.normalButtonsColor_str, _.selectedButtonsColor_str), p.nextButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.nextButtonOnMouseUpHandler), p.nextButton_do.setY(parseInt((p.stageHeight - p.nextButton_do.h) / 2)), p.buttons_ar.push(p.nextButton_do), p.mainHolder_do.addChild(p.nextButton_do), p.showNextAndPrevButtons_bl || this.nextButton_do.setWidth(0)
            }, this.nextButtonOnMouseUpHandler = function() {
                p.dispatchEvent(n.PLAY_NEXT)
            }, this.setupSeparators = function() {
                p.firstSeparator_do = new FWDMSPDisplayObject("img"), p.firstSeparator_do.setScreen(p.separator1_img), p.secondSeparator_do = new FWDMSPDisplayObject("img"), p.secondSeparator_do.setScreen(p.separator2_img), p.firstSeparator_do.setX(-10), p.secondSeparator_do.setX(-10), p.firstSeparator_do.setY(parseInt((p.stageHeight - p.firstSeparator_do.h) / 2)), p.secondSeparator_do.setY(parseInt((p.stageHeight - p.secondSeparator_do.h) / 2)), p.mainHolder_do.addChild(p.firstSeparator_do), p.mainHolder_do.addChild(p.secondSeparator_do)
            }, this.setupTitlebar = function() {
                p.mainTitlebar_do = new FWDMSPDisplayObject("div"), p.mainTitlebar_do.getStyle().background = "url('" + p.titlebarBkMiddlePattern_str + "')", p.mainTitlebar_do.setHeight(p.titlebarHeight), p.titleBarLeft_do = new FWDMSPDisplayObject("img"), p.titleBarLeft_do.setScreen(p.titleBarLeft_img), p.titleBarRight_do = new FWDMSPDisplayObject("img"), p.titleBarRight_do.setScreen(p.titleBarRigth_img), p.simpleText_do = new FWDMSPDisplayObject("div"), p.simpleText_do.setOverflow("visible"), p.simpleText_do.hasTransform3d_bl = !1, p.simpleText_do.hasTransform2d_bl = !1, p.simpleText_do.setBackfaceVisibility(), p.simpleText_do.getStyle().fontFamily = "Arial", p.simpleText_do.getStyle().fontSize = "12px", p.simpleText_do.getStyle().whiteSpace = "nowrap", p.simpleText_do.getStyle().textAlign = "left", p.simpleText_do.getStyle().color = p.titleColor_str, p.simpleText_do.getStyle().fontSmoothing = "antialiased", p.simpleText_do.getStyle().webkitFontSmoothing = "antialiased", p.simpleText_do.getStyle().textRendering = "optimizeLegibility", p.animText1_do = new FWDMSPDisplayObject("div"), p.animText1_do.setOverflow("visible"), p.animText1_do.hasTransform3d_bl = !1, p.animText1_do.hasTransform2d_bl = !1, p.animText1_do.setBackfaceVisibility(), p.animText1_do.getStyle().fontFamily = "Arial", p.animText1_do.getStyle().fontSize = "12px", p.animText1_do.getStyle().whiteSpace = "nowrap", p.animText1_do.getStyle().textAlign = "left", p.animText1_do.getStyle().color = p.titleColor_str, p.animText1_do.getStyle().fontSmoothing = "antialiased", p.animText1_do.getStyle().webkitFontSmoothing = "antialiased", p.animText1_do.getStyle().textRendering = "optimizeLegibility", p.animText2_do = new FWDMSPDisplayObject("div"), p.animText2_do.setOverflow("visible"), p.animText2_do.hasTransform3d_bl = !1, p.animText2_do.hasTransform2d_bl = !1, p.animText2_do.setBackfaceVisibility(), p.animText2_do.getStyle().fontFamily = "Arial", p.animText2_do.getStyle().fontSize = "12px", p.animText2_do.getStyle().whiteSpace = "nowrap", p.animText2_do.getStyle().textAlign = "left", p.animText2_do.getStyle().color = p.titleColor_str, p.animText2_do.getStyle().fontSmoothing = "antialiased", p.animText2_do.getStyle().webkitFontSmoothing = "antialiased", p.animText2_do.getStyle().textRendering = "optimizeLegibility", p.titleBarGradLeft_do = new FWDMSPDisplayObject("img"), p.titleBarGradLeft_do.setScreen(p.titlebarLeftPath_img), p.titleBarGradLeft_do.setX(-50), p.titlebarGradRight_do = new FWDMSPDisplayObject("img"), p.titlebarGradRight_do.setScreen(p.titlebarRightPath_img), p.showSoundAnimation_bl ? (p.animationBackground_do = new FWDMSPDisplayObject("img"), p.animationBackground_do.setScreen(p.titlebarAnimBkPath_img), p.animationHolderWidth = p.animationBackground_do.w, p.simpleText_do.setX(p.animationBackground_do.w + 5), FWDMSPPreloader.setPrototype(), p.animation_do = new FWDMSPPreloader(_.animationPath_str, 29, 22, 31, 80, !0), p.animation_do.setX(p.equlizerOffsetLeft), p.animation_do.setY(0), p.animation_do.show(!0), p.animation_do.stop()) : p.simpleText_do.setX(5), p.positionTitleId_to = setTimeout(function e() {
                    if (null == p) return;
                    clearTimeout(p.positionTitleId_to);
                    0 == p.simpleText_do.getHeight() ? p.positionTitleId_to = setTimeout(e, 200) : (p.simpleText_do.setY(parseInt((p.mainTitlebar_do.h - p.simpleText_do.getHeight()) / 2) + 1), p.animText1_do.setY(parseInt((p.mainTitlebar_do.h - p.simpleText_do.getHeight()) / 2) + 1), p.animText2_do.setY(parseInt((p.mainTitlebar_do.h - p.simpleText_do.getHeight()) / 2) + 1))
                }, 1e3), p.mainTitlebar_do.addChild(p.titleBarLeft_do), p.mainTitlebar_do.addChild(p.titleBarRight_do), p.mainTitlebar_do.addChild(p.simpleText_do), p.mainTitlebar_do.addChild(p.animText1_do), p.mainTitlebar_do.addChild(p.animText2_do), p.showSoundAnimation_bl && (p.mainTitlebar_do.addChild(p.animationBackground_do), p.mainTitlebar_do.addChild(p.animation_do)), p.mainTitlebar_do.addChild(p.titleBarGradLeft_do), p.mainTitlebar_do.addChild(p.titlebarGradRight_do), p.mainHolder_do.addChild(p.mainTitlebar_do)
            }, this.setTitle = function(e) {
                p.simpleText_do.setInnerHTML(e), p.animText1_do.setInnerHTML(e + "***"), p.animText2_do.setInnerHTML(e + "***"), p.animText1_do.setX(-1e3), p.animText2_do.setX(-1e3), p.startToCheckIfAnimTitle(!0)
            }, this.startToCheckIfAnimTitle = function(e) {
                e && p.stopToAnimateText(), clearTimeout(p.animateTextId_to), clearTimeout(p.startToAnimateTextId_to), p.animateTextId_to = setTimeout(p.checkIfAnimTitle, 10)
            }, this.checkIfAnimTitle = function() {
                var e = p.mainTitlebar_do.w - 5 - p.titlebarGradRight_do.w;
                if (e -= p.animationHolderWidth, p.simpleText_do.getWidth() > e) {
                    if (p.isTextAnimating_bl) return;
                    p.showSoundAnimation_bl ? p.titleBarGradLeft_do.setX(p.animationHolderWidth) : p.titleBarGradLeft_do.setX(0), p.titlebarGradRight_do.setY(0), clearTimeout(p.startToAnimateTextId_to), p.startToAnimateTextId_to = setTimeout(p.startToAnimateText, 300)
                } else p.titleBarGradLeft_do.setX(-50), p.titlebarGradRight_do.setY(-50), p.stopToAnimateText()
            }, this.startToAnimateText = function() {
                p.isTextAnimating_bl || (p.isTextAnimating_bl = !0, p.animTextWidth = p.animText1_do.getWidth(), p.simpleText_do.setX(-1e3), p.animText1_do.setX(p.animationHolderWidth + 5), p.animText2_do.setX(p.animationHolderWidth + p.animTextWidth + 10), clearInterval(p.animateTextId_int), p.animateTextId_int = setInterval(p.animateText, 40))
            }, this.stopToAnimateText = function() {
                p.isTextAnimating_bl && (p.isTextAnimating_bl = !1, p.simpleText_do.setX(p.animationHolderWidth + 5), p.animText1_do.setX(-1e3), p.animText2_do.setX(-1e3), clearInterval(p.animateTextId_int))
            }, this.animateText = function() {
                p.animText1_do.setX(p.animText1_do.x - 1), p.animText2_do.setX(p.animText2_do.x - 1), p.animText1_do.x < -(p.animTextWidth - p.animationHolderWidth) && p.animText1_do.setX(p.animText2_do.x + p.animTextWidth + 5), p.animText2_do.x < -(p.animTextWidth - p.animationHolderWidth) && p.animText2_do.setX(p.animText1_do.x + p.animTextWidth + 5)
            }, this.stopEqulizer = function() {
                p.animation_do && p.animation_do.stop()
            }, this.startEqulizer = function() {
                p.animation_do && p.animation_do.start()
            }, this.setupMainScrubber = function() {
                p.mainScrubber_do = new FWDMSPDisplayObject("div"), p.mainScrubber_do.setY(parseInt((p.stageHeight - p.scrubbersHeight) / 2)), p.mainScrubber_do.setHeight(p.scrubbersHeight), p.mainScrubberBkLeft_do = new FWDMSPDisplayObject("img"), p.mainScrubberBkLeft_do.setScreen(p.mainScrubberBkLeft_img), p.mainScrubberBkRight_do = new FWDMSPDisplayObject("img"), p.mainScrubberBkRight_do.setScreen(p.mainScrubberBkRight_img);
                var e = new Image;
                e.src = p.mainScrubberBkMiddlePath_str, p.mainScrubberBkMiddle_do = new FWDMSPDisplayObject("div"), p.mainScrubberBkMiddle_do.getStyle().background = "url('" + p.mainScrubberBkMiddlePath_str + "')", p.mainScrubberBkMiddle_do.setHeight(p.scrubbersHeight), p.mainScrubberBkMiddle_do.setX(p.scrubbersBkLeftAndRightWidth), p.mainProgress_do = new FWDMSPDisplayObject("div"), p.mainProgress_do.setHeight(p.scrubbersHeight), p.progressLeft_do = new FWDMSPDisplayObject("img"), p.progressLeft_do.setScreen(p.mainScrubberLeftProgress_img), (e = new Image).src = p.progressMiddlePath_str, p.progressMiddle_do = new FWDMSPDisplayObject("div"), p.progressMiddle_do.getStyle().background = "url('" + p.progressMiddlePath_str + "')", p.progressMiddle_do.setHeight(p.scrubbersHeight), p.progressMiddle_do.setX(p.mainScrubberDragLeftWidth), p.mainScrubberDrag_do = new FWDMSPDisplayObject("div"), p.mainScrubberDrag_do.setHeight(p.scrubbersHeight), p.useHEXColorsForSkin_bl ? (p.mainScrubberDragLeft_do = new FWDMSPDisplayObject("div"), p.mainScrubberDragLeft_do.setWidth(p.mainScrubberDragLeft_img.width), p.mainScrubberDragLeft_do.setHeight(p.mainScrubberDragLeft_img.height), p.mainScrubberDragLeft_canvas = FWDMSPUtils.getCanvasWithModifiedColor(p.mainScrubberDragLeft_img, p.normalButtonsColor_str).canvas, p.mainScrubberDragLeft_do.screen.appendChild(p.mainScrubberDragLeft_canvas)) : (p.mainScrubberDragLeft_do = new FWDMSPDisplayObject("img"), p.mainScrubberDragLeft_do.setScreen(p.mainScrubberDragLeft_img)), p.mainScrubberMiddleImage = new Image, p.mainScrubberMiddleImage.src = p.mainScrubberDragMiddlePath_str, p.volumeScrubberDragMiddle_do = new FWDMSPDisplayObject("div"), p.useHEXColorsForSkin_bl ? (p.mainScrubberDragMiddle_do = new FWDMSPDisplayObject("div"), p.mainScrubberMiddleImage.onload = function() {
                    var e = FWDMSPUtils.getCanvasWithModifiedColor(p.mainScrubberMiddleImage, p.normalButtonsColor_str, !0);
                    p.mainSCrubberMiddleCanvas = e.canvas, p.mainSCrubberDragMiddleImageBackground = e.image, p.mainScrubberDragMiddle_do.getStyle().background = "url('" + p.mainSCrubberDragMiddleImageBackground.src + "') repeat-x", setTimeout(function() {
                        p.volumeScrubberDragMiddle_do.getStyle().background = "url('" + p.mainSCrubberDragMiddleImageBackground.src + "') repeat-x"
                    }, 50)
                }) : (p.mainScrubberDragMiddle_do = new FWDMSPDisplayObject("div"), p.mainScrubberDragMiddle_do.getStyle().background = "url('" + p.mainScrubberDragMiddlePath_str + "') repeat-x"), p.mainScrubberDragMiddle_do.setHeight(p.scrubbersHeight), p.mainScrubberDragMiddle_do.setX(p.mainScrubberDragLeftWidth), p.mainScrubberBarLine_do = new FWDMSPDisplayObject("img"), p.mainScrubberBarLine_do.setScreen(p.mainScrubberLine_img), p.mainScrubberBarLine_do.setAlpha(0), p.mainScrubberBarLine_do.hasTransform3d_bl = !1, p.mainScrubberBarLine_do.hasTransform2d_bl = !1, p.mainScrubber_do.addChild(p.mainScrubberBkLeft_do), p.mainScrubber_do.addChild(p.mainScrubberBkMiddle_do), p.mainScrubber_do.addChild(p.mainScrubberBkRight_do), p.mainScrubberDrag_do.addChild(p.mainScrubberDragLeft_do), p.mainScrubberDrag_do.addChild(p.mainScrubberDragMiddle_do), p.mainProgress_do.addChild(p.progressLeft_do), p.mainProgress_do.addChild(p.progressMiddle_do), p.mainScrubber_do.addChild(p.mainProgress_do), p.mainScrubber_do.addChild(p.mainScrubberDrag_do), p.mainScrubber_do.addChild(p.mainScrubberBarLine_do), p.mainHolder_do.addChild(p.mainScrubber_do), p.disableScrubber_bl || (p.hasPointerEvent_bl ? (p.mainScrubber_do.screen.addEventListener("pointerover", p.mainScrubberOnOverHandler), p.mainScrubber_do.screen.addEventListener("pointerout", p.mainScrubberOnOutHandler), p.mainScrubber_do.screen.addEventListener("pointerdown", p.mainScrubberOnDownHandler)) : p.screen.addEventListener && (p.isMobile_bl || (p.mainScrubber_do.screen.addEventListener("mouseover", p.mainScrubberOnOverHandler), p.mainScrubber_do.screen.addEventListener("mouseout", p.mainScrubberOnOutHandler), p.mainScrubber_do.screen.addEventListener("mousedown", p.mainScrubberOnDownHandler)), p.mainScrubber_do.screen.addEventListener("touchstart", p.mainScrubberOnDownHandler))), p.disableMainScrubber()
            }, this.mainScrubberOnOverHandler = function(e) {
                if (!p.isMainScrubberDisabled_bl) {
                    0 != f.totalDuration && p.ttm.show(), !p.isMobile_bl && p.ttm && window.addEventListener("mousemove", p.mainScrubberWMouseMove);
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e).screenX - p.mainScrubber_do.getGlobalX();
                    t < 0 ? t = 0 : t > p.mainScrubberWidth - p.scrubbersOffsetWidth && (t = p.mainScrubberWidth - p.scrubbersOffsetWidth);
                    var o = t / p.mainScrubberWidth;
                }
            }, p.mainScrubberWMouseMove = function(e) {
                var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                p.vcX = t.screenX, p.vcY = t.screenY, FWDMSPUtils.hitTest(p.mainScrubber_do.screen, p.vcX, p.vcY) || p.isMainScrubberScrubbing_bl || (window.removeEventListener("mousemove", p.mainScrubberWMouseMove), p.ttm.hide());
                var o = FWDMSPUtils.getViewportMouseCoordinates(e).screenX - p.mainScrubber_do.getGlobalX();
                o < 0 ? o = 0 : o > p.mainScrubberWidth - p.scrubbersOffsetWidth && (o = p.mainScrubberWidth - p.scrubbersOffsetWidth);
                var s = o / p.mainScrubberWidth;
            }, this.mainScrubberOnOutHandler = function(e) {
                p.isMainScrubberDisabled_bl || p.isMainScrubberScrubbing_bl || p.ttm && p.ttm.hide()
            }, this.mainScrubberOnDownHandler = function(e) {
                if (!p.isMainScrubberDisabled_bl) {
                    e.preventDefault && e.preventDefault(), p.isMainScrubberScrubbing_bl = !0;
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e).screenX - p.mainScrubber_do.getGlobalX();
                    t < 0 ? t = 0 : t > p.mainScrubberWidth - p.scrubbersOffsetWidth && (t = p.mainScrubberWidth - p.scrubbersOffsetWidth);
                    var o = t / p.mainScrubberWidth;
                    !FWDMSP.hasHTML5Audio && t >= p.mainProgress_do.w && (t = p.mainProgress_do.w);
                    var s = t / p.mainScrubberWidth;
                    p.disable_do && p.addChild(p.disable_do), p.ttm.show(), p.updateMainScrubber(o), p.dispatchEvent(n.START_TO_SCRUB), p.dispatchEvent(n.SCRUB_PLAYLIST_ITEM, {
                        percent: s
                    }), p.dispatchEvent(n.SCRUB, {
                        percent: o
                    }), p.hasPointerEvent_bl ? (window.addEventListener("pointermove", p.mainScrubberMoveHandler), window.addEventListener("pointerup", p.mainScrubberEndHandler)) : (window.addEventListener("mousemove", p.mainScrubberMoveHandler), window.addEventListener("mouseup", p.mainScrubberEndHandler), window.addEventListener("touchmove", p.mainScrubberMoveHandler), window.addEventListener("touchend", p.mainScrubberEndHandler))
                }
            }, this.mainScrubberMoveHandler = function(e) {
                e.preventDefault && e.preventDefault();
                var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                p.vcX = t.screenX, p.vcY = t.screenY, FWDMSPUtils.hitTest(p.mainScrubber_do.screen, p.vcX, p.vcY) || p.isMainScrubberScrubbing_bl || (window.removeEventListener("mousemove", p.mainScrubberWMouseMove), p.ttm.hide());
                var o = FWDMSPUtils.getViewportMouseCoordinates(e).screenX - p.mainScrubber_do.getGlobalX();
                FWDMSPUtils.hitTest(p.mainScrubber_do.screen, p.vcX, p.vcY) || p.isMainScrubberScrubbing_bl || (window.removeEventListener("mousemove", p.mainScrubberWMouseMove), p.ttm.hide()), o < 0 ? o = 0 : o > p.mainScrubberWidth - p.scrubbersOffsetWidth && (o = p.mainScrubberWidth - p.scrubbersOffsetWidth);
                var s = o / p.mainScrubberWidth;
                !FWDMSP.hasHTML5Audio && o >= p.mainProgress_do.w && (o = p.mainProgress_do.w);
                var i = o / p.mainScrubberWidth;
                p.updateMainScrubber(s), p.dispatchEvent(n.SCRUB_PLAYLIST_ITEM, {
                    percent: i
                }), p.dispatchEvent(n.SCRUB, {
                    percent: s
                })
            }, this.mainScrubberEndHandler = function(e) {
                if (p.disable_do && p.contains(p.disable_do) && p.removeChild(p.disable_do), p.isMainScrubberScrubbing_bl = !1, e) {
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                    FWDMSPUtils.hitTest(p.mainScrubber_do.screen, t.screenX, t.screenY) || p.ttm && p.ttm.hide()
                }
                p.dispatchEvent(n.STOP_TO_SCRUB), p.hasPointerEvent_bl ? (window.removeEventListener("pointermove", p.mainScrubberMoveHandler), window.removeEventListener("pointerup", p.mainScrubberEndHandler)) : (window.removeEventListener("mousemove", p.mainScrubberMoveHandler), window.removeEventListener("mouseup", p.mainScrubberEndHandler), window.removeEventListener("touchmove", p.mainScrubberMoveHandler), window.removeEventListener("touchend", p.mainScrubberEndHandler))
            }, this.disableMainScrubber = function() {
                p.mainScrubber_do && (p.isMainScrubberDisabled_bl = !0, p.mainScrubber_do.setButtonMode(!1), p.updateMainScrubber(0), p.updatePreloaderBar(0), p.mainScrubberEndHandler(), p.disableAtbButton())
            }, this.enableMainScrubber = function() {
                p.mainScrubber_do && (p.isMainScrubberDisabled_bl = !1, p.disableScrubber_bl || p.mainScrubber_do.setButtonMode(!0), p.enableAtbButton())
            }, this.updateMainScrubber = function(e) {
                if (p.mainScrubber_do && !isNaN(e)) {
                    var t = parseInt(e * p.mainScrubberWidth);
                    p.percentPlayed = e, !FWDMSP.hasHTML5Audio && t >= p.mainProgress_do.w && (t = p.mainProgress_do.w), t < 1 && p.isMainScrubberLineVisible_bl ? (p.isMainScrubberLineVisible_bl = !1, FWDAnimation.to(p.mainScrubberBarLine_do, .5, {
                        alpha: 0
                    })) : 2 < t && !p.isMainScrubberLineVisible_bl && (p.isMainScrubberLineVisible_bl = !0, FWDAnimation.to(p.mainScrubberBarLine_do, .5, {
                        alpha: 1
                    })), p.mainScrubberDrag_do.setWidth(t), t > p.mainScrubberWidth - p.scrubbersOffsetWidth && (t = p.mainScrubberWidth - p.scrubbersOffsetWidth), FWDAnimation.to(p.mainScrubberBarLine_do, .8, {
                        x: t,
                        ease: Expo.easeOut
                    })
                }
            }, this.updatePreloaderBar = function(e) {
                if (p.mainProgress_do) {
                    var t = parseInt(e * p.mainScrubberWidth);
                    1 == e ? p.mainProgress_do.setY(-30) : 0 != p.mainProgress_do.y && 1 != e && p.mainProgress_do.setY(0), t > p.mainScrubberWidth - p.scrubbersOffsetWidth && (t = p.mainScrubberWidth - p.scrubbersOffsetWidth), t < 0 && (t = 0), p.mainProgress_do.setWidth(t)
                }
            }, this.setupTime = function() {
                p.currentTime_do = new FWDMSPDisplayObject("div"), p.currentTime_do.hasTransform3d_bl = !1, p.currentTime_do.hasTransform2d_bl = !1, p.currentTime_do.getStyle().fontFamily = "Arial", p.currentTime_do.getStyle().fontSize = "12px", p.currentTime_do.getStyle().whiteSpace = "nowrap", p.currentTime_do.getStyle().textAlign = "left", p.currentTime_do.getStyle().color = p.timeColor_str, p.currentTime_do.getStyle().fontSmoothing = "antialiased", p.currentTime_do.getStyle().webkitFontSmoothing = "antialiased", p.currentTime_do.getStyle().textRendering = "optimizeLegibility", p.currentTime_do.setInnerHTML("00"), p.mainHolder_do.addChild(p.currentTime_do), p.totalTime_do = new FWDMSPDisplayObject("div"), p.totalTime_do.hasTransform3d_bl = !1, p.totalTime_do.hasTransform2d_bl = !1, p.totalTime_do.getStyle().fontFamily = "Arial", p.totalTime_do.getStyle().fontSize = "12px", p.totalTime_do.getStyle().whiteSpace = "nowrap", p.totalTime_do.getStyle().textAlign = "right", p.totalTime_do.getStyle().color = p.timeColor_str, p.totalTime_do.getStyle().fontSmoothing = "antialiased", p.totalTime_do.getStyle().webkitFontSmoothing = "antialiased", p.totalTime_do.getStyle().textRendering = "optimizeLegibility", p.mainHolder_do.addChild(p.totalTime_do), p.updateTime(), setTimeout(function() {
                    null != p && (p.timeHeight = p.currentTime_do.getHeight(), p.currentTime_do.h = p.timeHeight, p.totalTime_do.h = p.timeHeight, p.stageWidth = f.stageWidth, p.positionButtons())
                }, 100)
            }, this.updateTime = function(e, t) {
                if (p.currentTime_do && t && ("00:00" == t && (t = e), p.currentTime_do.setInnerHTML(e), p.totalTime_do.setInnerHTML(t), e.length != p.lastTotalTimeLength || t.length != p.lastCurTimeLength)) {
                    var o = p.currentTime_do.offsetWidth,
                        s = p.totalTime_do.offsetWidth;
                    p.currentTime_do.w = o, p.totalTime_do.w = s, p.positionButtons(), setTimeout(function() {
                        p.currentTime_do.w = p.currentTime_do.getWidth(), p.totalTime_do.w = p.totalTime_do.getWidth(), p.positionButtons()
                    }, 50), p.lastCurTimeLength = e.length, p.lastTotalTimeLength = t.length
                }
            }, this.setupVolumeScrubber = function() {
                p.mainVolumeHolder_do = new FWDMSPDisplayObject("div"), p.mainVolumeHolder_do.setHeight(p.volumeN_img.height), p.mainHolder_do.addChild(p.mainVolumeHolder_do), FWDMSPSimpleButton.setPrototype(), p.volumeButton_do = new FWDMSPSimpleButton(p.volumeN_img, _.volumeSPath_str, _.volumeDPath_str, !0, _.useHEXColorsForSkin_bl, _.normalButtonsColor_str, _.selectedButtonsColor_str), p.volumeButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.volumeButtonOnMouseUpHandler), p.allowToChangeVolume_bl || p.volumeButton_do.disable(), p.volumeScrubber_do = new FWDMSPDisplayObject("div"), p.volumeScrubber_do.setHeight(p.scrubbersHeight), p.volumeScrubber_do.setX(p.volumeButton_do.w), p.volumeScrubber_do.setY(parseInt((p.volumeButton_do.h - p.scrubbersHeight) / 2)), p.volumeScrubberBkLeft_do = new FWDMSPDisplayObject("img");
                var e = new Image;
                e.src = p.mainScrubberBkLeft_do.screen.src, p.volumeScrubberBkLeft_do.setScreen(e), p.volumeScrubberBkLeft_do.setWidth(p.mainScrubberBkLeft_do.w), p.volumeScrubberBkLeft_do.setHeight(p.mainScrubberBkLeft_do.h), p.volumeScrubberBkRight_do = new FWDMSPDisplayObject("img");
                var t = new Image;
                t.src = p.mainScrubberBkRight_do.screen.src, p.volumeScrubberBkRight_do.setScreen(t), p.volumeScrubberBkRight_do.setWidth(p.mainScrubberBkRight_do.w), p.volumeScrubberBkRight_do.setHeight(p.mainScrubberBkRight_do.h), (new Image).src = p.volumeScrubberBkMiddlePath_str, p.volumeScrubberBkMiddle_do = new FWDMSPDisplayObject("div"), p.volumeScrubberBkMiddle_do.getStyle().background = "url('" + p.volumeScrubberBkMiddlePath_str + "')", p.volumeScrubberBkMiddle_do.setHeight(p.scrubbersHeight), p.volumeScrubberBkMiddle_do.setX(p.scrubbersBkLeftAndRightWidth), p.volumeScrubberDrag_do = new FWDMSPDisplayObject("div"), p.volumeScrubberDrag_do.setHeight(p.scrubbersHeight), p.useHEXColorsForSkin_bl ? (p.volumeScrubberDragLeft_do = new FWDMSPDisplayObject("div"), p.volumeScrubberDragLeft_do.setWidth(p.volumeScrubberDragLeft_img.width), p.volumeScrubberDragLeft_do.setHeight(p.volumeScrubberDragLeft_img.height), p.volumeScrubberDragLeft_canvas = FWDMSPUtils.getCanvasWithModifiedColor(p.volumeScrubberDragLeft_img, p.normalButtonsColor_str).canvas, p.volumeScrubberDragLeft_do.screen.appendChild(p.volumeScrubberDragLeft_canvas)) : (p.volumeScrubberDragLeft_do = new FWDMSPDisplayObject("img"), p.volumeScrubberDragLeft_do.setScreen(p.volumeScrubberDragLeft_img)), p.useHEXColorsForSkin_bl || (p.volumeScrubberDragMiddle_do = new FWDMSPDisplayObject("div"), p.volumeScrubberDragMiddle_do.getStyle().background = "url('" + p.volumeScrubberDragMiddlePath_str + "') repeat-x"), p.volumeScrubberDragMiddle_do.setHeight(p.scrubbersHeight), p.volumeScrubberDragMiddle_do.setX(p.mainScrubberDragLeftWidth), p.volumeScrubberBarLine_do = new FWDMSPDisplayObject("img");
                var o = new Image;
                o.src = p.mainScrubberBarLine_do.screen.src, p.volumeScrubberBarLine_do.setScreen(o), p.volumeScrubberBarLine_do.setWidth(p.mainScrubberBarLine_do.w), p.volumeScrubberBarLine_do.setHeight(p.mainScrubberBarLine_do.h), p.volumeScrubberBarLine_do.setAlpha(0), p.volumeScrubberBarLine_do.hasTransform3d_bl = !1, p.volumeScrubberBarLine_do.hasTransform2d_bl = !1, p.volumeScrubber_do.addChild(p.volumeScrubberBkLeft_do), p.volumeScrubber_do.addChild(p.volumeScrubberBkMiddle_do), p.volumeScrubber_do.addChild(p.volumeScrubberBkRight_do), p.volumeScrubber_do.addChild(p.volumeScrubberBarLine_do), p.volumeScrubberDrag_do.addChild(p.volumeScrubberDragLeft_do), p.volumeScrubberDrag_do.addChild(p.volumeScrubberDragMiddle_do), p.volumeScrubber_do.addChild(p.volumeScrubberDrag_do), p.volumeScrubber_do.addChild(p.volumeScrubberBarLine_do), p.mainVolumeHolder_do.addChild(p.volumeButton_do), p.mainVolumeHolder_do.addChild(p.volumeScrubber_do), p.allowToChangeVolume_bl && (p.hasPointerEvent_bl ? (p.volumeScrubber_do.screen.addEventListener("pointerover", p.volumeScrubberOnOverHandler), p.volumeScrubber_do.screen.addEventListener("pointerout", p.volumeScrubberOnOutHandler), p.volumeScrubber_do.screen.addEventListener("pointerdown", p.volumeScrubberOnDownHandler)) : (p.isMobile_bl || (p.volumeScrubber_do.screen.addEventListener("mouseover", p.volumeScrubberOnOverHandler), p.volumeScrubber_do.screen.addEventListener("mouseout", p.volumeScrubberOnOutHandler), p.volumeScrubber_do.screen.addEventListener("mousedown", p.volumeScrubberOnDownHandler), p.volumeScrubber_do.screen.addEventListener("touchstart", p.volumeScrubberOnDownHandler))), document.documentElement.appendChild(p.ttm2.screen)), p.enableVolumeScrubber(), p.updateVolumeScrubber(p.volume)
            }, this.volumeButtonOnMouseUpHandler = function() {
                var e = p.lastVolume;
                p.isMute_bl ? (e = p.lastVolume, p.isMute_bl = !1) : (e = 1e-6, p.isMute_bl = !0), p.updateVolume(e)
            }, this.volumeScrubberOnOverHandler = function(e) {
                p.isVolumeScrubberDisabled_bl || (p.ttm2.show())
            }, this.volumeScrubberOnOutHandler = function(e) {
                p.isVolumeScrubberDisabled_bl || p.isVolumeScrubberScrubbing_bl || p.ttm2 && p.ttm2.hide()
            }, this.volumeScrubberOnDownHandler = function(e) {
                if (!p.isVolumeScrubberDisabled_bl) {
                    e.preventDefault && e.preventDefault();
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e).screenX - p.volumeScrubber_do.getGlobalX();
                    t < 0 ? t = 0 : t > p.volumeScrubberWidth - p.scrubbersOffsetWidth && (t = p.volumeScrubberWidth - p.scrubbersOffsetWidth);
                    var o = t / p.volumeScrubberWidth;
                    p.disable_do && p.addChild(p.disable_do), p.lastVolume = o, p.isVolumeScrubberScrubbing_bl = !0, p.updateVolume(o), p.dispatchEvent(n.VOLUME_START_TO_SCRUB), p.isMobile_bl ? p.hasPointerEvent_bl ? (window.addEventListener("pointermove", p.volumeScrubberMoveHandler), window.addEventListener("pointerup", p.volumeScrubberEndHandler)) : (window.addEventListener("touchmove", p.volumeScrubberMoveHandler), window.addEventListener("touchend", p.volumeScrubberEndHandler)) : (window.addEventListener("mousemove", p.volumeScrubberMoveHandler), window.addEventListener("mouseup", p.volumeScrubberEndHandler))
                }
            }, this.volumeScrubberMoveHandler = function(e) {
                if (!p.isVolumeScrubberDisabled_bl) {
                    e.preventDefault && e.preventDefault();
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e).screenX - p.volumeScrubber_do.getGlobalX();
                    t < 0 ? t = 0 : t > p.volumeScrubberWidth - p.scrubbersOffsetWidth && (t = p.volumeScrubberWidth - p.scrubbersOffsetWidth);
                    var o = t / p.volumeScrubberWidth;
                    .98 <= o && (o = 1), p.lastVolume = o, p.updateVolume(o)
                }
            }, this.volumeScrubberEndHandler = function(e) {
                if (p.dispatchEvent(n.VOLUME_STOP_TO_SCRUB), p.isVolumeScrubberScrubbing_bl = !1, p.disable_do && p.contains(p.disable_do) && p.removeChild(p.disable_do), e) {
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                    FWDMSPUtils.hitTest(p.volumeScrubber_do.screen, t.screenX, t.screenY) || p.ttm2 && p.ttm2.hide()
                }
                p.isMobile_bl ? p.hasPointerEvent_bl ? (window.removeEventListener("pointermove", p.volumeScrubberMoveHandler), window.removeEventListener("pointerup", p.volumeScrubberEndHandler)) : (window.removeEventListener("touchmove", p.volumeScrubberMoveHandler), window.removeEventListener("touchend", p.volumeScrubberEndHandler)) : window.removeEventListener ? (window.removeEventListener("mousemove", p.volumeScrubberMoveHandler), window.removeEventListener("mouseup", p.volumeScrubberEndHandler)) : document.detachEvent && (document.detachEvent("onmousemove", p.volumeScrubberMoveHandler), document.detachEvent("onmouseup", p.volumeScrubberEndHandler))
            }, this.disableVolumeScrubber = function() {
                p.isVolumeScrubberDisabled_bl = !0, p.volumeScrubber_do.setButtonMode(!1), p.volumeScrubberEndHandler()
            }, this.enableVolumeScrubber = function() {
                p.isVolumeScrubberDisabled_bl = !1, p.volumeScrubber_do.setButtonMode(!0)
            }, this.updateVolumeScrubber = function(e) {
                var t = parseInt(e * p.volumeScrubberWidth);
                p.volume = e, p.volumeScrubberDrag_do.setWidth(t), t < 1 && p.isVolumeScrubberLineVisible_bl ? (p.isVolumeScrubberLineVisible_bl = !1, FWDAnimation.to(p.volumeScrubberBarLine_do, .5, {
                    alpha: 0
                })) : 1 < t && !p.isVolumeScrubberLineVisible_bl && (p.isVolumeScrubberLineVisible_bl = !0, FWDAnimation.to(p.volumeScrubberBarLine_do, .5, {
                    alpha: 1
                })), t > p.volumeScrubberWidth - p.scrubbersOffsetWidth && (t = p.volumeScrubberWidth - p.scrubbersOffsetWidth), FWDAnimation.to(p.volumeScrubberBarLine_do, .8, {
                    x: t,
                    ease: Expo.easeOut
                })
            }, this.updateVolume = function(e, t) {
                p.volume = e, p.volume <= 1e-6 ? (p.isMute_bl = !0, p.volume = 1e-6) : 1 <= p.volume ? (p.isMute_bl = !1, p.volume = 1) : p.isMute_bl = !1, 1e-6 == p.volume ? p.volumeButton_do && p.volumeButton_do.setDisabledState() : p.volumeButton_do && p.volumeButton_do.setEnabledState(), p.volumeScrubberBarLine_do && p.updateVolumeScrubber(p.volume), t || p.dispatchEvent(n.CHANGE_VOLUME, {
                    percent: p.volume
                })
            }, this.setupPlaylistButton = function() {
                FWDMSPSimpleButton.setPrototype(), p.playlistButton_do = new FWDMSPSimpleButton(p.playlistN_img, _.playlistSPath_str, null, !0, _.useHEXColorsForSkin_bl, _.normalButtonsColor_str, _.selectedButtonsColor_str), p.playlistButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.playlistButtonOnMouseUpHandler), p.playlistButton_do.setY(parseInt((p.stageHeight - p.playlistButton_do.h) / 2)), p.buttons_ar.push(p.playlistButton_do), p.mainHolder_do.addChild(p.playlistButton_do), p.showPlayListByDefault_bl && p.setPlaylistButtonState("selected")
            }, this.playlistButtonOnMouseUpHandler = function() {
                p.playlistButton_do.isSelectedFinal_bl ? p.dispatchEvent(n.HIDE_PLAYLIST) : p.dispatchEvent(n.SHOW_PLAYLIST)
            }, this.setPlaylistButtonState = function(e) {
                p.playlistButton_do && ("selected" == e ? p.playlistButton_do.setSelected() : "unselected" == e && p.playlistButton_do.setUnselected())
            }, this.setupCategoriesButton = function() {
                FWDMSPSimpleButton.setPrototype(), p.categoriesButton_do = new FWDMSPSimpleButton(p.categoriesN_img, _.categoriesSPath_str, null, !0, _.useHEXColorsForSkin_bl, _.normalButtonsColor_str, _.selectedButtonsColor_str), p.categoriesButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.categoriesButtonOnMouseUpHandler), p.categoriesButton_do.setY(parseInt((p.stageHeight - p.categoriesButton_do.h) / 2)), p.buttons_ar.push(p.categoriesButton_do), p.mainHolder_do.addChild(p.categoriesButton_do)
            }, this.categoriesButtonOnMouseUpHandler = function() {
                p.dispatchEvent(n.SHOW_CATEGORIES)
            }, this.setCategoriesButtonState = function(e) {
                p.categoriesButton_do && ("selected" == e ? p.categoriesButton_do.setSelected() : "unselected" == e && p.categoriesButton_do.setUnselected())
            }, this.setupLoopButton = function() {
                FWDMSPSimpleButton.setPrototype(), p.loopButton_do = new FWDMSPSimpleButton(p.replayN_img, _.replaySPath_str, null, !0, _.useHEXColorsForSkin_bl, _.normalButtonsColor_str, _.selectedButtonsColor_str), p.loopButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.loopButtonOnMouseUpHandler), p.loopButton_do.setY(parseInt((p.stageHeight - p.loopButton_do.h) / 2)), p.buttons_ar.push(p.loopButton_do), p.mainHolder_do.addChild(p.loopButton_do), p.loop_bl && p.setLoopStateButton("selected")
            }, this.loopButtonOnMouseUpHandler = function() {
                p.loopButton_do.isSelectedFinal_bl ? p.dispatchEvent(n.DISABLE_LOOP) : p.dispatchEvent(n.ENABLE_LOOP)
            }, this.setLoopStateButton = function(e) {
                p.loopButton_do && ("selected" == e ? p.loopButton_do.setSelected() : "unselected" == e && p.loopButton_do.setUnselected())
            }, this.setupDownloadButton = function() {
                FWDMSPSimpleButton.setPrototype(), p.downloadButton_do = new FWDMSPSimpleButton(p.downloaderN_img, _.downloaderSPath_str, null, !0, _.useHEXColorsForSkin_bl, _.normalButtonsColor_str, _.selectedButtonsColor_str), p.downloadButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.downloadButtonOnMouseUpHandler), p.downloadButton_do.setY(parseInt((p.stageHeight - p.downloadButton_do.h) / 2)), p.buttons_ar.push(p.downloadButton_do), p.mainHolder_do.addChild(p.downloadButton_do)
            }, this.downloadButtonOnMouseUpHandler = function() {
                p.dispatchEvent(n.DOWNLOAD_MP3)
            }, this.setupBuyButton = function() {
                FWDMSPSimpleButton.setPrototype(), p.buyButton_do = new FWDMSPSimpleButton(_.buyN_img, _.buySPath_str, null, !0, _.useHEXColorsForSkin_bl, _.normalButtonsColor_str, _.selectedButtonsColor_str), p.buyButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.buyButtonOnMouseUpHandler), p.buttons_ar.push(p.buyButton_do), p.mainHolder_do.addChild(p.buyButton_do)
            }, this.buyButtonOnMouseUpHandler = function() {
                p.dispatchEvent(n.BUY)
            }, this.setupShuffleButton = function() {
                FWDMSPSimpleButton.setPrototype(), p.shuffleButton_do = new FWDMSPSimpleButton(p.shuffleN_img, _.shuffleSPath_str, null, !0, _.useHEXColorsForSkin_bl, _.normalButtonsColor_str, _.selectedButtonsColor_str), p.shuffleButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.shuffleButtonOnMouseUpHandler), p.shuffleButton_do.setY(parseInt((p.stageHeight - p.shuffleButton_do.h) / 2)), p.buttons_ar.push(p.shuffleButton_do), p.mainHolder_do.addChild(p.shuffleButton_do), !p.loop_bl && p.shuffle_bl && p.setShuffleButtonState("selected")
            }, this.shuffleButtonOnMouseUpHandler = function() {
                p.shuffleButton_do.isSelectedFinal_bl ? p.dispatchEvent(n.DISABLE_SHUFFLE) : p.dispatchEvent(n.ENABLE_SHUFFLE)
            }, this.setShuffleButtonState = function(e) {
                p.shuffleButton_do && ("selected" == e ? p.shuffleButton_do.setSelected() : "unselected" == e && p.shuffleButton_do.setUnselected())
            }, this.setupFacebookButton = function() {
                FWDMSPSimpleButton.setPrototype(), p.shareButton_do = new FWDMSPSimpleButton(p.shareN_img, _.shareSPath_str, null, !0, _.useHEXColorsForSkin_bl, _.normalButtonsColor_str, _.selectedButtonsColor_str), p.shareButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.faceboolButtonOnMouseUpHandler), p.shareButton_do.setY(parseInt((p.stageHeight - p.shareButton_do.h) / 2)), p.buttons_ar.push(p.shareButton_do), p.mainHolder_do.addChild(p.shareButton_do)
            }, this.faceboolButtonOnMouseUpHandler = function() {
                p.dispatchEvent(n.FACEBOOK_SHARE)
            }, this.setupPopupButton = function() {
                FWDMSPSimpleButton.setPrototype(), p.popupButton_do = new FWDMSPSimpleButton(p.popupN_img, _.popupSPath_str, null, !0, _.useHEXColorsForSkin_bl, _.normalButtonsColor_str, _.selectedButtonsColor_str), p.popupButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, p.popupButtonOnMouseUpHandler), p.popupButton_do.setY(parseInt((p.stageHeight - p.popupButton_do.h) / 2)), p.buttons_ar.push(p.popupButton_do), p.mainHolder_do.addChild(p.popupButton_do)
            }, this.popupButtonOnMouseUpHandler = function() {
                p.dispatchEvent(n.POPUP)
            }, this.disableControllerWhileLoadingPlaylist = function() {
                p.prevButton_do.disable(), p.playPauseButton_do.disable(), p.nextButton_do.disable(), p.downloadButton_do && p.downloadButton_do.disable(), p.buyButton_do && p.buyButton_do.disable(), p.playlistButton_do && p.playlistButton_do.disable(!0), p.shareButton_do && p.shareButton_do.disable(), p.updateTime("...", "..."), p.setTitle("...")
            }, this.enableControllerWhileLoadingPlaylist = function() {
                p.prevButton_do.enable(), p.playPauseButton_do.enable(), p.nextButton_do.enable(), p.downloadButton_do && p.downloadButton_do.enable(), p.buyButton_do && p.buyButton_do.enable(), p.playlistButton_do && p.playlistButton_do.enable(), p.shareButton_do && p.shareButton_do.enable()
            }, p.updateHEXColors = function(e, t) {
                p.normalColor_str = e, p.selectedColor_str = t, FWDMSPUtils.changeCanvasHEXColor(p.mainScrubberDragLeft_img, p.mainScrubberDragLeft_canvas, e);
                try {
                    FWDMSPUtils.changeCanvasHEXColor(p.volumeScrubberDragBottom_img, p.volumeScrubberDragBottom_canvas, e)
                } catch (e) {}
                var o = FWDMSPUtils.changeCanvasHEXColor(p.mainScrubberMiddleImage, p.mainSCrubberMiddleCanvas, e, !0);
                p.mainScrubberDragMiddle_do.getStyle().background = "url('" + o.src + "') repeat-x";
                try {
                    FWDMSPUtils.changeCanvasHEXColor(p.volumeScrubberDragLeft_img, p.volumeScrubberDragLeft_canvas, e), p.volumeScrubberDragMiddle_do.getStyle().background = "url('" + o.src + "') repeat-x"
                } catch (e) {}
                if (p.playPauseButton_do.updateHEXColors(e, t), p.volumeButton_do && p.volumeButton_do.updateHEXColors(e, t), p.playlistButton_do && p.playlistButton_do.updateHEXColors(e, t), p.downloadButton_do && p.downloadButton_do.updateHEXColors(e, t), p.infoButton_do && p.infoButton_do.updateHEXColors(e, t), p.categoriesButton_do && p.categoriesButton_do.updateHEXColors(e, t), p.nextButton_do && p.nextButton_do.updateHEXColors(e, t), p.shareButton_do && p.shareButton_do.updateHEXColors(e, t), p.prevButton_do && p.prevButton_do.updateHEXColors(e, t), f.fullScreenButton_do && f.fullScreenButton_do.updateHEXColors(e, t), p.loopButton_do && p.loopButton_do.updateHEXColors(e, t), p.shuffleButton_do && p.shuffleButton_do.updateHEXColors(e, t), p.buyButton_do && p.buyButton_do.updateHEXColors(e, t), p.popupButton_do && p.popupButton_do.updateHEXColors(e, t), p.playbackRateButton_do && p.playbackRateButton_do.updateHEXColors(e, t), p.currentTime_do && (p.currentTime_do.getStyle().color = e), p.totalTime_do && (p.totalTime_do.getStyle().color = e), p.ytbButtons_ar)
                    for (var s = 0; s < p.totalYtbButtons; s++) {
                        var i = p.ytbButtons_ar[s];
                        i.normalColor_str = e, i.selectedColor_str = t, i.isSelected_bl ? i.isSelected_bl || i.setSelectedState() : i.setNormalState()
                    }
            }, this.init()
        };
        n.setPrototype = function() {
            n.prototype = new FWDMSPDisplayObject("div")
        }, n.SHOW_ATOB = "showAtob", n.FACEBOOK_SHARE = "facebookShare", n.SHOW_PLAYBACKRATE = "showPlaybackRate", n.PLAY_NEXT = "playNext", n.PLAY_PREV = "playPrev", n.PLAY = "play", n.PAUSE = "pause", n.POPUP = "popup", n.VOLUME_START_TO_SCRUB = "volumeStartToScrub", n.VOLUME_STOP_TO_SCRUB = "volumeStopToScrub", n.START_TO_SCRUB = "startToScrub", n.SCRUB = "scrub", n.SCRUB_PLAYLIST_ITEM = "scrubPlaylistItem", n.STOP_TO_SCRUB = "stopToScrub", n.CHANGE_VOLUME = "changeVolume", n.SHOW_CATEGORIES = "showCategories", n.SHOW_PLAYLIST = "showPlaylist", n.HIDE_PLAYLIST = "hidePlaylist", n.ENABLE_LOOP = "enableLoop", n.DISABLE_LOOP = "disableLoop", n.ENABLE_SHUFFLE = "enableShuffle", n.DISABLE_SHUFFLE = "disableShuffle", n.DOWNLOAD_MP3 = "downloadMp3", n.BUY = "buy", n.prototype = null, window.FWDMSPController = n
    }(), window.FWDMSPDisplayObject = function(e, t, o, s) {
        var i = this;
        i.listeners = {
            events_ar: []
        }, i.type = e, this.children_ar = [], this.style, this.screen, this.transform, this.position = t || "absolute", this.overflow = o || "hidden", this.display = s || "inline-block", this.visible = !0, this.buttonMode, this.x = 0, this.y = 0, this.w = 0, this.h = 0, this.rect, this.alpha = 1, this.innerHTML = "", this.opacityType = "", this.isHtml5_bl = !1, this.hasTransform3d_bl = FWDMSPUtils.hasTransform3d, this.hasTransform2d_bl = FWDMSPUtils.hasTransform2d, (FWDMSPUtils.isIE || FWDMSPUtils.isIE11 && !FWDMSPUtils.isMobile) && (i.hasTransform3d_bl = !1, i.hasTransform2d_bl = !1), this.hasBeenSetSelectable_bl = !1, i.init = function() {
            i.setScreen()
        }, i.getTransform = function() {
            for (var e, t = ["transform", "msTransform", "WebkitTransform", "MozTransform", "OTransform"]; e = t.shift();)
                if (void 0 !== i.screen.style[e]) return e;
            return !1
        }, i.getOpacityType = function() {
            return void 0 !== i.screen.style.opacity ? "opacity" : "filter"
        }, i.setScreen = function(e) {
            "img" == i.type && e ? i.screen = e : i.screen = document.createElement(i.type), i.setMainProperties()
        }, i.setMainProperties = function() {
            i.transform = i.getTransform(), i.setPosition(i.position), i.setOverflow(i.overflow), i.opacityType = i.getOpacityType(), "opacity" == i.opacityType && (i.isHtml5_bl = !0), "filter" == i.opacityType && (i.screen.style.filter = "inherit"), i.screen.style.left = "0px", i.screen.style.top = "0px", i.screen.style.margin = "0px", i.screen.style.padding = "0px", i.screen.style.maxWidth = "none", i.screen.style.maxHeight = "none", i.screen.style.border = "none", i.screen.style.lineHeight = "1", i.screen.style.backgroundColor = "transparent", i.screen.style.backfaceVisibility = "hidden", i.screen.style.webkitBackfaceVisibility = "hidden", i.screen.style.MozBackfaceVisibility = "hidden", i.screen.style.MozImageRendering = "optimizeSpeed", i.screen.style.WebkitImageRendering = "optimizeSpeed", "img" == e && (i.setWidth(i.screen.width), i.setHeight(i.screen.height))
        }, i.setBackfaceVisibility = function() {
            i.screen.style.backfaceVisibility = "visible", i.screen.style.webkitBackfaceVisibility = "visible", i.screen.style.MozBackfaceVisibility = "visible"
        }, i.setSelectable = function(e) {
            e || (i.screen.style.userSelect = "none", i.screen.style.MozUserSelect = "none", i.screen.style.webkitUserSelect = "none", i.screen.style.khtmlUserSelect = "none", i.screen.style.oUserSelect = "none", i.screen.style.msUserSelect = "none", i.screen.msUserSelect = "none", i.screen.ondragstart = function(e) {
                return !1
            }, i.screen.onselectstart = function() {
                return !1
            }, i.screen.ontouchstart = function() {
                return !1
            }, i.screen.style.webkitTouchCallout = "none", i.hasBeenSetSelectable_bl = !0)
        }, i.getScreen = function() {
            return i.screen
        }, i.setVisible = function(e) {
            i.visible = e, 1 == i.visible ? i.screen.style.visibility = "visible" : i.screen.style.visibility = "hidden"
        }, i.getVisible = function() {
            return i.visible
        }, i.setResizableSizeAfterParent = function() {
            i.screen.style.width = "100%", i.screen.style.height = "100%"
        }, i.getStyle = function() {
            return i.screen.style
        }, i.setOverflow = function(e) {
            i.overflow = e, i.screen.style.overflow = i.overflow
        }, i.setPosition = function(e) {
            i.position = e, i.screen.style.position = i.position
        }, i.setDisplay = function(e) {
            i.display = e, i.screen.style.display = i.display
        }, i.setButtonMode = function(e) {
            i.buttonMode = e, 1 == i.buttonMode ? i.screen.style.cursor = "pointer" : i.screen.style.cursor = "default"
        }, i.setBkColor = function(e) {
            i.screen.style.backgroundColor = e
        }, i.setInnerHTML = function(e) {
            i.innerHTML = e, i.screen.innerHTML = i.innerHTML
        }, i.getInnerHTML = function() {
            return i.innerHTML
        }, i.getRect = function() {
            return i.screen.getBoundingClientRect()
        }, i.setAlpha = function(e) {
            i.alpha = e, "opacity" == i.opacityType ? i.screen.style.opacity = i.alpha : "filter" == i.opacityType && (i.screen.style.filter = "alpha(opacity=" + 100 * i.alpha + ")", i.screen.style.filter = "progid:DXImageTransform.Microsoft.Alpha(Opacity=" + Math.round(100 * i.alpha) + ")")
        }, i.getAlpha = function() {
            return i.alpha
        }, i.getRect = function() {
            return i.screen.getBoundingClientRect()
        }, i.getGlobalX = function() {
            return i.getRect().left
        }, i.getGlobalY = function() {
            return i.getRect().top
        }, i.setX = function(e) {
            i.x = e, i.hasTransform3d_bl ? i.screen.style[i.transform] = "translate3d(" + i.x + "px," + i.y + "px,0)" : i.hasTransform2d_bl ? i.screen.style[i.transform] = "translate(" + i.x + "px," + i.y + "px)" : i.screen.style.left = i.x + "px"
        }, i.getX = function() {
            return i.x
        }, i.setY = function(e) {
            i.y = e, i.hasTransform3d_bl ? i.screen.style[i.transform] = "translate3d(" + i.x + "px," + i.y + "px,0)" : i.hasTransform2d_bl ? i.screen.style[i.transform] = "translate(" + i.x + "px," + i.y + "px)" : i.screen.style.top = i.y + "px"
        }, i.getY = function() {
            return i.y
        }, i.setWidth = function(e) {
            i.w = e, "img" == i.type && (i.screen.width = i.w), i.screen.style.width = i.w + "px"
        }, i.getWidth = function() {
            return "div" == i.type || "input" == i.type ? 0 != i.screen.offsetWidth ? i.screen.offsetWidth : i.w : "img" == i.type ? 0 != i.screen.offsetWidth ? i.screen.offsetWidth : 0 != i.screen.width ? i.screen.width : i._w : "canvas" == i.type ? 0 != i.screen.offsetWidth ? i.screen.offsetWidth : i.w : void 0
        }, i.setHeight = function(e) {
            i.h = e, "img" == i.type && (i.screen.height = i.h), i.screen.style.height = i.h + "px"
        }, i.getHeight = function() {
            return "div" == i.type || "input" == i.type ? 0 != i.screen.offsetHeight ? i.screen.offsetHeight : i.h : "img" == i.type ? 0 != i.screen.offsetHeight ? i.screen.offsetHeight : 0 != i.screen.height ? i.screen.height : i.h : "canvas" == i.type ? 0 != i.screen.offsetHeight ? i.screen.offsetHeight : i.h : void 0
        }, i.addChild = function(e) {
            i.contains(e) && i.children_ar.splice(FWDMSPUtils.indexOfArray(i.children_ar, e), 1), i.children_ar.push(e), i.screen.appendChild(e.screen)
        }, i.removeChild = function(e) {
            if (!i.contains(e)) throw Error("##removeChild()## Child dose't exist, it can't be removed!");
            i.children_ar.splice(FWDMSPUtils.indexOfArray(i.children_ar, e), 1), i.screen.removeChild(e.screen)
        }, i.contains = function(e) {
            return -1 != FWDMSPUtils.indexOfArray(i.children_ar, e)
        }, i.addChildAt = function(e, t) {
            if (0 == i.getNumChildren()) i.children_ar.push(e), i.screen.appendChild(e.screen);
            else if (1 == t) i.screen.insertBefore(e.screen, i.children_ar[0].screen), i.screen.insertBefore(i.children_ar[0].screen, e.screen), i.contains(e) ? i.children_ar.splice(FWDMSPUtils.indexOfArray(i.children_ar, e), 1, e) : i.children_ar.splice(FWDMSPUtils.indexOfArray(i.children_ar, e), 0, e);
            else {
                if (t < 0 || t > i.getNumChildren() - 1) throw Error("##getChildAt()## Index out of bounds!");
                i.screen.insertBefore(e.screen, i.children_ar[t].screen), i.contains(e) ? i.children_ar.splice(FWDMSPUtils.indexOfArray(i.children_ar, e), 1, e) : i.children_ar.splice(FWDMSPUtils.indexOfArray(i.children_ar, e), 0, e)
            }
        }, i.getChildAt = function(e) {
            if (e < 0 || e > i.getNumChildren() - 1) throw Error("##getChildAt()## Index out of bounds!");
            if (0 == i.getNumChildren()) throw Errror("##getChildAt## Child dose not exist!");
            return i.children_ar[e]
        }, i.removeChildAtZero = function() {
            i.screen.removeChild(i.children_ar[0].screen), i.children_ar.shift()
        }, i.getNumChildren = function() {
            return i.children_ar.length
        }, i.addListener = function(e, t) {
            if (null == e) throw Error("type is required.");
            if ("object" == typeof e) throw Error("type must be of type String.");
            if ("function" != typeof t) throw Error("listener must be of type Function.");
            var o = {};
            o.type = e, o.listener = t, (o.target = this).listeners.events_ar.push(o)
        }, i.dispatchEvent = function(e, t) {
            if (null != this.listeners) {
                if (null == e) throw Error("type is required.");
                if ("object" == typeof e) throw Error("type must be of type String.");
                for (var o = 0, s = this.listeners.events_ar.length; o < s; o++)
                    if (this.listeners.events_ar[o].target === this && this.listeners.events_ar[o].type === e) {
                        if (t)
                            for (var i in t) this.listeners.events_ar[o][i] = t[i];
                        this.listeners.events_ar[o].listener.call(this, this.listeners.events_ar[o])
                    }
            }
        }, i.removeListener = function(e, t) {
            if (null == e) throw Error("type is required.");
            if ("object" == typeof e) throw Error("type must be of type String.");
            if ("function" != typeof t) throw Error("listener must be of type Function." + e);
            for (var o = 0, s = this.listeners.events_ar.length; o < s; o++)
                if (this.listeners.events_ar[o].target === this && this.listeners.events_ar[o].type === e && this.listeners.events_ar[o].listener === t) {
                    this.listeners.events_ar.splice(o, 1);
                    break
                }
        }, i.disposeImage = function() {
            "img" == i.type && (i.screen.src = null)
        }, i.destroy = function() {
            i.hasBeenSetSelectable_bl && (i.screen.ondragstart = null, i.screen.onselectstart = null, i.screen.ontouchstart = null), i.screen.removeAttribute("style"), i.listeners = [], i.listeners = null, i.children_ar = [], i.children_ar = null, i.style = null, i.screen = null, i.transform = null, i.position = null, i.overflow = null, i.display = null, i.visible = null, i.buttonMode = null, i.x = null, i.y = null, i.w = null, i.h = null, i.rect = null, i.alpha = null, i.innerHTML = null, i.opacityType = null, i.isHtml5_bl = null, i.hasTransform3d_bl = null, i.hasTransform2d_bl = null, i = null
        }, i.init()
    }, window, window.FWDMSPEventDispatcher = function() {
        this.listeners = {
            events_ar: []
        }, this.addListener = function(e, t) {
            if (null == e) throw Error("type is required.");
            if ("object" == typeof e) throw Error("type must be of type String.");
            if ("function" != typeof t) throw Error("listener must be of type Function.");
            var o = {};
            o.type = e, o.listener = t, (o.target = this).listeners.events_ar.push(o)
        }, this.dispatchEvent = function(e, t) {
            if (null != this.listeners) {
                if (null == e) throw Error("type is required.");
                if ("object" == typeof e) throw Error("type must be of type String.");
                for (var o = 0, s = this.listeners.events_ar.length; o < s; o++)
                    if (this.listeners.events_ar[o].target === this && this.listeners.events_ar[o].type === e) {
                        if (t)
                            for (var i in t) this.listeners.events_ar[o][i] = t[i];
                        this.listeners.events_ar[o].listener.call(this, this.listeners.events_ar[o])
                    }
            }
        }, this.removeListener = function(e, t) {
            if (null == e) throw Error("type is required.");
            if ("object" == typeof e) throw Error("type must be of type String.");
            if ("function" != typeof t) throw Error("listener must be of type Function." + e);
            for (var o = 0, s = this.listeners.events_ar.length; o < s; o++)
                if (this.listeners.events_ar[o].target === this && this.listeners.events_ar[o].type === e && this.listeners.events_ar[o].listener === t) {
                    this.listeners.events_ar.splice(o, 1);
                    break
                }
        }, this.destroy = function() {
            this.listeners = null, this.addListener = null, this.dispatchEvent = null, this.removeListener = null
        }
    },
    function(n) {
        var l = function(e, t, o) {
            var s = this,
                i = l.prototype;
            this.screenToTest = e, this.screenToTest2 = t, this.hideDelay = o, this.globalX = 0, this.globalY = 0, this.currentTime, this.checkIntervalId_int, this.hideCompleteId_to, this.hasInitialTestEvents_bl = !1, this.addSecondTestEvents_bl = !1, this.dispatchOnceShow_bl = !0, this.dispatchOnceHide_bl = !1, this.isStopped_bl = !0, this.isMobile_bl = FWDMSPUtils.isMobile, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, s.init = function() {}, s.start = function() {
                s.currentTime = (new Date).getTime(), clearInterval(s.checkIntervalId_int), s.checkIntervalId_int = setInterval(s.update, 100), s.addMouseOrTouchCheck(), s.isStopped_bl = !1
            }, s.stop = function() {
                clearInterval(s.checkIntervalId_int), s.isStopped_bl = !0, s.removeMouseOrTouchCheck(), s.removeMouseOrTouchCheck2()
            }, s.addMouseOrTouchCheck = function() {
                s.hasInitialTestEvents_bl || (s.hasInitialTestEvents_bl = !0, s.isMobile_bl ? s.hasPointerEvent_bl ? (s.screenToTest.screen.addEventListener("pointerdown", s.onMouseOrTouchUpdate), s.screenToTest.screen.addEventListener("MSPointerMove", s.onMouseOrTouchUpdate)) : s.screenToTest.screen.addEventListener("touchstart", s.onMouseOrTouchUpdate) : n.addEventListener ? n.addEventListener("mousemove", s.onMouseOrTouchUpdate) : document.attachEvent && document.attachEvent("onmousemove", s.onMouseOrTouchUpdate))
            }, s.removeMouseOrTouchCheck = function() {
                s.hasInitialTestEvents_bl && (s.hasInitialTestEvents_bl = !1, s.isMobile_bl ? s.hasPointerEvent_bl ? (s.screenToTest.screen.removeEventListener("pointerdown", s.onMouseOrTouchUpdate), s.screenToTest.screen.removeEventListener("MSPointerMove", s.onMouseOrTouchUpdate)) : s.screenToTest.screen.removeEventListener("touchstart", s.onMouseOrTouchUpdate) : n.removeEventListener ? n.removeEventListener("mousemove", s.onMouseOrTouchUpdate) : document.detachEvent && document.detachEvent("onmousemove", s.onMouseOrTouchUpdate))
            }, s.addMouseOrTouchCheck2 = function() {
                s.addSecondTestEvents_bl || (s.addSecondTestEvents_bl = !0, s.screenToTest.screen.addEventListener ? s.screenToTest.screen.addEventListener("mousemove", s.secondTestMoveDummy) : s.screenToTest.screen.attachEvent && s.screenToTest.screen.attachEvent("onmousemove", s.secondTestMoveDummy))
            }, s.removeMouseOrTouchCheck2 = function() {
                s.addSecondTestEvents_bl && (s.addSecondTestEvents_bl = !1, s.screenToTest.screen.removeEventListener ? s.screenToTest.screen.removeEventListener("mousemove", s.secondTestMoveDummy) : s.screenToTest.screen.detachEvent && s.screenToTest.screen.detachEvent("onmousemove", s.secondTestMoveDummy))
            }, this.secondTestMoveDummy = function() {
                s.removeMouseOrTouchCheck2(), s.addMouseOrTouchCheck()
            }, s.onMouseOrTouchUpdate = function(e) {
                var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                s.globalX != t.screenX && s.globalY != t.screenY && (s.currentTime = (new Date).getTime()), s.globalX = t.screenX, s.globalY = t.screenY, s.isMobile_bl || FWDMSPUtils.hitTest(s.screenToTest.screen, s.globalX, s.globalY) || (s.removeMouseOrTouchCheck(), s.addMouseOrTouchCheck2())
            }, s.update = function(e) {
                (new Date).getTime() > s.currentTime + s.hideDelay ? s.dispatchOnceShow_bl && (s.dispatchOnceHide_bl = !0, s.dispatchOnceShow_bl = !1, s.dispatchEvent(l.HIDE), clearTimeout(s.hideCompleteId_to), s.hideCompleteId_to = setTimeout(function() {
                    s.dispatchEvent(l.HIDE_COMPLETE)
                }, 1e3)) : s.dispatchOnceHide_bl && (clearTimeout(s.hideCompleteId_to), s.dispatchOnceHide_bl = !1, s.dispatchOnceShow_bl = !0, s.dispatchEvent(l.SHOW))
            }, s.reset = function() {
                clearTimeout(s.hideCompleteId_to), s.currentTime = (new Date).getTime(), s.dispatchEvent(l.SHOW)
            }, s.destroy = function() {
                s.removeMouseOrTouchCheck(), clearInterval(s.checkIntervalId_int), s.screenToTest = null, e = null, s.init = null, s.start = null, s.stop = null, s.addMouseOrTouchCheck = null, s.removeMouseOrTouchCheck = null, s.onMouseOrTouchUpdate = null, s.update = null, s.reset = null, s.destroy = null, i.destroy(), s = i = null, l.prototype = null
            }, s.init()
        };
        l.HIDE = "hide", l.SHOW = "show", l.HIDE_COMPLETE = "hideComplete", l.setPrototype = function() {
            l.prototype = new FWDMSPEventDispatcher
        }, n.FWDMSPHider = l
    }(window),
    function(e) {
        var t = function(i, e) {
            var n = this;
            t.prototype;
            this.bk_do = null, this.textHolder_do = null, this.warningIconPath_str = e, this.show_to = null, this.isShowed_bl = !1, this.isShowedOnce_bl = !1, this.allowToRemove_bl = !0, this.init = function() {
                n.setResizableSizeAfterParent(), n.bk_do = new FWDMSPDisplayObject("div"), n.bk_do.setAlpha(.6), n.bk_do.setBkColor("#000000"), n.addChild(n.bk_do), n.textHolder_do = new FWDMSPDisplayObject("div"), FWDMSPUtils.isIEAndLessThen9 || (n.textHolder_do.getStyle().font = "Arial"), n.textHolder_do.getStyle().wordWrap = "break-word", n.textHolder_do.getStyle().padding = "10px", n.textHolder_do.getStyle().paddingLeft = "42px", n.textHolder_do.getStyle().lineHeight = "18px", n.textHolder_do.getStyle().color = "#000000", n.textHolder_do.setBkColor("#EEEEEE");
                var e = new Image;
                e.src = this.warningIconPath_str, this.img_do = new FWDMSPDisplayObject("img"), this.img_do.setScreen(e), this.img_do.setWidth(28), this.img_do.setHeight(28), n.addChild(n.textHolder_do), n.addChild(n.img_do)
            }, this.showText = function(e) {
                n.isShowedOnce_bl || (n.screen.addEventListener ? n.screen.addEventListener("click", n.closeWindow) : n.screen.attachEvent && n.screen.attachEvent("onclick", n.closeWindow), n.isShowedOnce_bl = !0), n.setVisible(!1), n.textHolder_do.getStyle().paddingBottom = "10px", n.textHolder_do.setInnerHTML(e), clearTimeout(n.show_to), n.show_to = setTimeout(n.show, 60), setTimeout(function() {
                    n.positionAndResize()
                }, 10)
            }, this.show = function() {
                var e = Math.min(640, i.stageWidth - 120);
                n.isShowed_bl = !0, n.textHolder_do.setWidth(e), setTimeout(function() {
                    n.setVisible(!0), n.positionAndResize()
                }, 100)
            }, this.positionAndResize = function() {
                var e = n.textHolder_do.getWidth(),
                    t = n.textHolder_do.getHeight(),
                    o = parseInt((i.stageWidth - e) / 2),
                    s = 0;
                i.playlist_do && i.playlist_do.isShowed_bl ? s = parseInt((Math.max(i.main_do.h, i.maxHeight) - t) / 2) : i.controller_do && (s = parseInt((Math.max(i.controller_do.h, i.maxHeight) - t) / 2)), n.bk_do.setWidth(i.stageWidth), n.bk_do.setHeight(Math.max(i.main_do.h, i.maxHeight)), n.textHolder_do.setX(o), n.textHolder_do.setY(s), n.img_do.setX(o + 6), n.img_do.setY(s + parseInt((n.textHolder_do.getHeight() - n.img_do.h) / 2))
            }, this.closeWindow = function() {
                if (n.allowToRemove_bl) {
                    n.isShowed_bl = !1, clearTimeout(n.show_to);
                    try {
                        i.main_do.removeChild(n)
                    } catch (e) {}
                }
            }, this.init()
        };
        t.setPrototype = function() {
            t.prototype = new FWDMSPDisplayObject("div", "relative")
        }, t.prototype = null, e.FWDMSPInfo = t
    }(window),
    function() {
        var i = function(e, t, o) {
            var s = this;
            this.animation_img = e.openerAnimation_img, t == FWDMSP.POSITION_TOP ? (this.openN_img = e.openTopN_img, this.openSPath_str = e.openTopSPath_str) : (this.openN_img = e.openBottomN_img, this.openSPath_str = e.openBottomSPath_str), this.openerPauseN_img = e.openerPauseN_img, this.openerPlayN_img = e.openerPlayN_img, this.closeN_img = e.closeN_img, s.useHEXColorsForSkin_bl = e.useHEXColorsForSkin_bl, s.normalButtonsColor_str = e.normalButtonsColor_str, s.selectedButtonsColor_str = e.selectedButtonsColor_str, this.openerPauseS_str = e.openerPauseS_str, this.openerPlaySPath_str = e.openerPlayS_str, this.closeSPath_str = e.closeSPath_str, this.animationPath_str = e.animationPath_str, this.totalWidth = s.openN_img.width, this.totalHeight = s.openN_img.height, this.mainHolder_do = null, this.dumy_do = null, this.openN_do = null, this.openS_do = null, this.closeN_do = null, this.closeS_do = null, this.animation_do = null, this.playPauseButton_do = null, this.position_str = t, this.alignment_str = e.openerAlignment_str, this.openerEqulizerOffsetLeft = e.openerEqulizerOffsetLeft, this.openerEqulizerOffsetTop = e.openerEqulizerOffsetTop, this.showFirstTime_bl = !0, this.playerIsShowed_bl = o, this.showOpenerPlayPauseButton_bl = e.showOpenerPlayPauseButton_bl, this.isMobile_bl = FWDMSPUtils.isMobile, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, this.init = function() {
                -1 != e.skinPath_str.indexOf("hex_white") ? s.selectedButtonsColor_str = "#FFFFFF" : s.selectedButtonsColor_str = e.selectedButtonsColor_str, s.hasTransform3d_bl = !1, s.hasTransform2d_bl = !1, s.setBackfaceVisibility(), s.getStyle().msTouchAction = "none", s.getStyle().webkitTapHighlightColor = "rgba(0, 0, 0, 0)", s.setupStuff(), s.showOpenerPlayPauseButton_bl && s.setupPlayPauseButton(), s.playerIsShowed_bl && s.showCloseButton(), s.hide(), s.showOpenerPlayPauseButton_bl ? s.setWidth(s.totalWidth + s.openerPauseN_img.width + 1) : s.setWidth(s.totalWidth), s.setHeight(s.totalHeight)
            }, this.setupStuff = function(e) {
                s.mainHolder_do = new FWDMSPDisplayObject("div"), s.mainHolder_do.hasTransform3d_bl = !1, s.mainHolder_do.hasTransform2d_bl = !1, s.mainHolder_do.setBackfaceVisibility(), s.showOpenerPlayPauseButton_bl ? s.mainHolder_do.setWidth(s.totalWidth + s.openerPauseN_img.width + 1) : s.mainHolder_do.setWidth(s.totalWidth), s.mainHolder_do.setHeight(s.totalHeight), s.useHEXColorsForSkin_bl ? (s.openN_do = new FWDMSPDisplayObject("div"), s.openN_canvas = FWDMSPUtils.getCanvasWithModifiedColor(s.openN_img, s.normalButtonsColor_str).canvas, s.openN_do.screen.appendChild(s.openN_canvas)) : (s.openN_do = new FWDMSPDisplayObject("img"), s.openN_do.setScreen(s.openN_img)), s.openN_do.setWidth(s.openN_img.width), s.openN_do.setHeight(s.openN_img.height), s.openS_img = new Image, s.openS_img.src = s.openSPath_str, s.useHEXColorsForSkin_bl ? (s.openS_do = new FWDMSPDisplayObject("div"), s.openS_img.onload = function() {
                    s.openS_canvas = FWDMSPUtils.getCanvasWithModifiedColor(s.openS_img, s.selectedButtonsColor_str).canvas, s.openS_do.setWidth(s.openS_img.width), s.openS_do.setHeight(s.openS_img.height), s.openS_do.screen.appendChild(s.openS_canvas)
                }) : (s.openS_do = new FWDMSPDisplayObject("img"), s.openS_do.setScreen(s.openS_img)), s.openS_do.setWidth(s.openN_do.w), s.openS_do.setHeight(s.openN_do.h), s.openS_do.setAlpha(0), s.useHEXColorsForSkin_bl ? (s.closeN_do = new FWDMSPDisplayObject("div"), s.closeN_canvas = FWDMSPUtils.getCanvasWithModifiedColor(s.closeN_img, s.normalButtonsColor_str).canvas, s.closeN_do.screen.appendChild(s.closeN_canvas)) : (s.closeN_do = new FWDMSPDisplayObject("img"), s.closeN_do.setScreen(s.closeN_img)), s.closeN_do.setWidth(s.closeN_img.width), s.closeN_do.setHeight(s.closeN_img.height), s.closeN_do.hasTransform3d_bl = !1, s.closeN_do.hasTransform2d_bl = !1, s.closeN_do.setBackfaceVisibility(), s.closeS_img = new Image, s.closeS_img.src = s.closeSPath_str, s.useHEXColorsForSkin_bl ? (s.closeS_do = new FWDMSPDisplayObject("div"), s.closeS_img.onload = function() {
                    s.closeS_canvas = FWDMSPUtils.getCanvasWithModifiedColor(s.closeS_img, s.selectedButtonsColor_str).canvas, s.closeS_do.setWidth(s.closeS_img.width), s.closeS_do.setHeight(s.closeS_img.height), s.closeS_do.screen.appendChild(s.closeS_canvas)
                }) : (s.closeS_do = new FWDMSPDisplayObject("img"), s.closeS_do.setScreen(s.closeS_img)), s.closeS_do.setWidth(s.closeS_img.width), s.closeS_do.setHeight(s.closeS_img.height), s.closeS_do.setAlpha(0), s.closeS_do.hasTransform3d_bl = !1, s.closeS_do.hasTransform2d_bl = !1, FWDMSPPreloader.setPrototype(), s.animation_do = new FWDMSPPreloader(s.animationPath_str, 29, 22, 31, 80, !0), s.animation_do.setY(s.openerEqulizerOffsetTop), s.animation_do.show(!1), s.animation_do.stop(), s.dumy_do = new FWDMSPDisplayObject("div"), s.dumy_do.setWidth(s.totalWidth), s.dumy_do.setHeight(s.totalHeight), s.dumy_do.getStyle().zIndex = 2, s.dumy_do.hasTransform3d_bl = !1, s.dumy_do.hasTransform2d_bl = !1, s.dumy_do.setBackfaceVisibility(), s.dumy_do.setButtonMode(!0), (FWDMSPUtils.isIE || FWDMSPUtils.isAndroid) && (s.dumy_do.setBkColor("#FF0000"), s.dumy_do.setAlpha(.01)), s.isMobile_bl ? s.hasPointerEvent_bl ? (s.dumy_do.screen.addEventListener("pointerdown", s.onMouseUp), s.dumy_do.screen.addEventListener("pointerover", s.onMouseOver), s.dumy_do.screen.addEventListener("pointerout", s.onMouseOut)) : s.dumy_do.screen.addEventListener("touchstart", s.onMouseUp) : s.dumy_do.screen.addEventListener ? (s.dumy_do.screen.addEventListener("mouseover", s.onMouseOver), s.dumy_do.screen.addEventListener("mouseout", s.onMouseOut), s.dumy_do.screen.addEventListener("mousedown", s.onMouseUp)) : s.dumy_do.screen.attachEvent && (s.dumy_do.screen.attachEvent("onmouseover", s.onMouseOver), s.dumy_do.screen.attachEvent("onmouseout", s.onMouseOut), s.dumy_do.screen.attachEvent("onmousedown", s.onMouseUp)), s.mainHolder_do.addChild(s.openN_do), s.mainHolder_do.addChild(s.openS_do), s.mainHolder_do.addChild(s.closeN_do), s.mainHolder_do.addChild(s.closeS_do), s.mainHolder_do.addChild(s.animation_do), s.mainHolder_do.addChild(s.dumy_do), s.addChild(s.mainHolder_do)
            }, this.onMouseOver = function(e, t) {
                e.pointerType && e.pointerType != e.MSPOINTER_TYPE_MOUSE || s.setSelectedState(!0)
            }, this.onMouseOut = function(e) {
                e.pointerType && e.pointerType != e.MSPOINTER_TYPE_MOUSE || s.setNormalState()
            }, this.onMouseUp = function(e) {
                e.preventDefault && e.preventDefault(), s.playerIsShowed_bl ? (s.playerIsShowed_bl = !1, s.dispatchEvent(i.HIDE)) : (s.playerIsShowed_bl = !0, s.dispatchEvent(i.SHOW))
            }, this.setupPlayPauseButton = function() {
                FWDMSPComplexButton.setPrototype(), s.playPauseButton_do = new FWDMSPComplexButton(s.openerPlayN_img, s.openerPlaySPath_str, s.openerPauseN_img, s.openerPauseS_str, !0, s.useHEXColorsForSkin_bl, s.normalButtonsColor_str, s.selectedButtonsColor_str), s.playPauseButton_do.addListener(FWDMSPComplexButton.MOUSE_UP, s.playButtonMouseUpHandler), s.addChild(s.playPauseButton_do)
            }, this.showPlayButton = function() {
                s.playPauseButton_do && s.playPauseButton_do.setButtonState(1), s.animation_do.stop()
            }, this.showPauseButton = function() {
                s.playPauseButton_do && s.playPauseButton_do.setButtonState(0), s.animation_do.start(0)
            }, this.playButtonMouseUpHandler = function() {
                0 == s.playPauseButton_do.currentState ? s.dispatchEvent(FWDMSPController.PAUSE) : s.dispatchEvent(FWDMSPController.PLAY)
            }, this.setNormalState = function() {
                s.isMobile_bl && !s.hasPointerEvent_bl || (FWDAnimation.killTweensOf(s.openS_do), FWDAnimation.killTweensOf(s.closeS_do), FWDAnimation.to(s.openS_do, .5, {
                    alpha: 0,
                    ease: Expo.easeOut
                }), FWDAnimation.to(s.closeS_do, .5, {
                    alpha: 0,
                    ease: Expo.easeOut
                }))
            }, this.setSelectedState = function(e) {
                FWDAnimation.killTweensOf(s.openS_do), FWDAnimation.killTweensOf(s.closeS_do), FWDAnimation.to(s.openS_do, .5, {
                    alpha: 1,
                    ease: Expo.easeOut
                }), FWDAnimation.to(s.closeS_do, .5, {
                    alpha: 1,
                    ease: Expo.easeOut
                })
            }, this.showOpenButton = function() {
                s.playerIsShowed_bl = !1, s.closeN_do.setX(150), s.closeS_do.setX(150), s.playPauseButton_do ? "right" == s.alignment_str ? (s.playPauseButton_do.setX(0), s.openN_do.setX(s.playPauseButton_do.w + 1), s.openS_do.setX(s.playPauseButton_do.w + 1), s.dumy_do.setX(s.playPauseButton_do.w + 1), s.dumy_do.setWidth(s.totalWidth), s.animation_do.setX(s.playPauseButton_do.w + 1 + s.openerEqulizerOffsetLeft)) : (s.playPauseButton_do.setX(s.openN_do.w + 1), s.openN_do.setX(0), s.openS_do.setX(0), s.dumy_do.setX(0), s.dumy_do.setWidth(s.totalWidth), s.animation_do.setX(s.openerEqulizerOffsetLeft)) : (s.openN_do.setX(0), s.openS_do.setX(0), s.dumy_do.setX(0), s.dumy_do.setWidth(s.totalWidth), s.animation_do.setX(s.openerEqulizerOffsetLeft)), s.animation_do.setVisible(!0)
            }, this.showCloseButton = function() {
                s.playerIsShowed_bl = !0, s.openN_do.setX(150), s.openS_do.setX(150), s.dumy_do.setWidth(s.closeN_do.w), "right" == s.alignment_str ? s.playPauseButton_do ? (s.closeN_do.setX(s.totalWidth + 1), s.closeS_do.setX(s.totalWidth + 1), s.dumy_do.setX(s.totalWidth + 1)) : (s.closeN_do.setX(s.totalWidth - s.closeN_do.w), s.closeS_do.setX(s.totalWidth - s.closeN_do.w), s.dumy_do.setX(s.totalWidth - s.closeN_do.w)) : (s.closeN_do.setX(0), s.closeS_do.setX(0), s.dumy_do.setX(0)), s.playPauseButton_do && s.playPauseButton_do.setX(150), s.animation_do.setX(150), s.animation_do.setVisible(!1)
            }, this.hide = function() {
                s.mainHolder_do.setX(150)
            }, this.show = function() {
                s.mainHolder_do.setX(0)
            }, s.updateHEXColors = function(e, t) {
                s.normalColor_str = e, s.selectedColor_str = t, s.playPauseButton_do.updateHEXColors(e, t), FWDMSPUtils.changeCanvasHEXColor(s.openN_img, s.openN_canvas, e), FWDMSPUtils.changeCanvasHEXColor(s.closeN_img, s.closeN_canvas, e), FWDMSPUtils.changeCanvasHEXColor(s.openS_img, s.openS_canvas, t), FWDMSPUtils.changeCanvasHEXColor(s.closeS_img, s.closeS_canvas, t)
            }, this.init()
        };
        i.setPrototype = function() {
            i.prototype = new FWDMSPDisplayObject("div")
        }, i.SHOW = "show", i.HIDE = "hise", i.prototype = null, window.FWDMSPOpener = i
    }(window),
    function(e) {
        var s = function(e, t) {
            var o = this;
            s.prototype;
            this.xhr = null, this.passColoseN_img = e.passColoseN_img, this.privateVideoPassword_str = e.privateVideoPassword_str, this.bk_do = null, this.mainHolder_do = null, this.passMainHolder_do = null, this.passMainHolderBk_do = null, this.passLabel_do = null, this.passInput_do = null, this.closeButton_do = null, this.backgrondPath_str = e.shareBkPath_str, this.secondaryLabelsColor_str = e.secondaryLabelsColor_str, this.inputColor_str = e.inputColor_str, this.mainLabelsColor_str = e.mainLabelsColor_str, this.passButtonNPath_str = e.passButtonNPath_str, this.passButtonSPath_str = e.passButtonSPath_str, this.inputBackgroundColor_str = e.inputBackgroundColor_str, this.borderColor_str = e.borderColor_str, this.maxTextWidth = 0, this.totalWidth = 0, this.stageWidth = 0, this.stageHeight = 0, this.buttonWidth = 28, this.buttonHeight = 19, this.embedWindowCloseButtonMargins = 0, this.finalEmbedPath_str = null, this.isShowed_bl = !1, this.isMobile_bl = FWDMSPUtils.isMobile, this.init = function() {
                o.setBackfaceVisibility(), o.mainHolder_do = new FWDMSPDisplayObject("div"), o.mainHolder_do.hasTransform3d_bl = !1, o.mainHolder_do.hasTransform2d_bl = !1, o.mainHolder_do.setBackfaceVisibility(), o.bk_do = new FWDMSPDisplayObject("div"), o.bk_do.getStyle().width = "100%", o.bk_do.getStyle().height = "100%", o.bk_do.setAlpha(.9), o.bk_do.getStyle().background = "url('" + o.backgrondPath_str + "')", o.passMainHolder_do = new FWDMSPDisplayObject("div"), o.passMainHolderBk_do = new FWDMSPDisplayObject("div"), o.passMainHolderBk_do.getStyle().background = "url('" + o.backgrondPath_str + "')", o.passMainHolderBk_do.getStyle().borderStyle = "solid", o.passMainHolderBk_do.getStyle().borderWidth = "1px", o.passMainHolderBk_do.getStyle().borderColor = o.borderColor_str, o.passLabel_do = new FWDMSPDisplayObject("div"), o.passLabel_do.setBackfaceVisibility(), o.passLabel_do.getStyle().fontFamily = "Arial", o.passLabel_do.getStyle().fontSize = "12px", o.passLabel_do.getStyle().color = o.secondaryLabelsColor_str, o.passLabel_do.getStyle().whiteSpace = "nowrap", o.passLabel_do.getStyle().fontSmoothing = "antialiased", o.passLabel_do.getStyle().webkitFontSmoothing = "antialiased", o.passLabel_do.getStyle().textRendering = "optimizeLegibility", o.passLabel_do.getStyle().padding = "0px", o.passLabel_do.setInnerHTML("Please enter password:"), o.passInput_do = new FWDMSPDisplayObject("input"), o.passInput_do.setBackfaceVisibility(), o.passInput_do.getStyle().fontFamily = "Arial", o.passInput_do.getStyle().fontSize = "12px", o.passInput_do.getStyle().backgroundColor = o.inputBackgroundColor_str, o.passInput_do.getStyle().color = o.inputColor_str, o.passInput_do.getStyle().outline = 0, o.passInput_do.getStyle().whiteSpace = "nowrap", o.passInput_do.getStyle().fontSmoothing = "antialiased", o.passInput_do.getStyle().webkitFontSmoothing = "antialiased", o.passInput_do.getStyle().textRendering = "optimizeLegibility", o.passInput_do.getStyle().padding = "6px", o.passInput_do.getStyle().paddingTop = "4px", o.passInput_do.getStyle().paddingBottom = "4px", o.passInput_do.screen.setAttribute("type", "password"), FWDMSPSimpleSizeButton.setPrototype(), o.passButton_do = new FWDMSPSimpleSizeButton(o.passButtonNPath_str, o.passButtonSPath_str, o.buttonWidth, o.buttonHeight, e.useHEXColorsForSkin_bl, e.normalButtonsColor_str, e.selectedButtonsColor_str), o.passButton_do.addListener(FWDMSPSimpleSizeButton.CLICK, o.passClickHandler), FWDMSPSimpleButton.setPrototype(), o.closeButton_do = new FWDMSPSimpleButton(o.passColoseN_img, e.embedWindowClosePathS_str, void 0, !0, e.useHEXColorsForSkin_bl, e.normalButtonsColor_str, e.selectedButtonsColor_str), o.closeButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, o.closeButtonOnMouseUpHandler), o.addChild(o.mainHolder_do), o.mainHolder_do.addChild(o.bk_do), o.passMainHolder_do.addChild(o.passMainHolderBk_do), o.passMainHolder_do.addChild(o.passLabel_do), o.passMainHolder_do.addChild(o.passInput_do), o.passMainHolder_do.addChild(o.passButton_do), o.mainHolder_do.addChild(o.passMainHolder_do), o.mainHolder_do.addChild(o.closeButton_do)
            }, this.closeButtonOnMouseUpHandler = function() {
                o.isShowed_bl && o.hide()
            }, this.positionAndResize = function() {
                o.stageWidth = t.stageWidth, o.stageHeight = t.stageHeight, o.maxTextWidth = Math.min(o.stageWidth - 150, 300), o.totalWidth = o.maxTextWidth + o.buttonWidth, o.positionFinal(), o.closeButton_do.setX(o.stageWidth - o.closeButton_do.w - o.embedWindowCloseButtonMargins), o.closeButton_do.setY(o.embedWindowCloseButtonMargins), finalY = t.playlist_do && t.position_str == FWDMSP.POSITION_TOP ? t.playlist_do.h : o.embedWindowCloseButtonMargins, o.setY(finalY), o.setWidth(o.stageWidth), o.setHeight(o.stageHeight), o.mainHolder_do.setWidth(o.stageWidth), o.mainHolder_do.setHeight(o.stageHeight)
            }, this.positionFinal = function() {
                var e, t = o.passLabel_do.getHeight();
                o.passLabel_do.setX(12), o.passLabel_do.setY(14), o.passInput_do.setX(10), o.passInput_do.setWidth(parseInt(o.totalWidth - 40 - o.buttonWidth)), o.passInput_do.setY(o.passLabel_do.y + t + 5), o.passButton_do.setX(10 + o.passInput_do.w + 20), o.passButton_do.setY(o.passLabel_do.y + t + 6), o.passMainHolderBk_do.setY(o.passLabel_do.y - 9), o.passMainHolderBk_do.setWidth(o.totalWidth - 2), o.passMainHolderBk_do.setHeight(o.passButton_do.y + o.passButton_do.h + 2), o.passMainHolder_do.setWidth(o.totalWidth), o.passMainHolder_do.setHeight(o.passButton_do.y + o.passButton_do.h + 14), o.passMainHolder_do.setX(Math.round((o.stageWidth - o.totalWidth) / 2)), e = o.passMainHolderBk_do.getHeight(), o.passMainHolder_do.setY(Math.round((o.stageHeight - e) / 2) - 6)
            }, this.passClickHandler = function() {
                o.privateVideoPassword_str = e.privateVideoPassword_str, e.playlist_ar[t.id].privateVideoPassword_str && (o.privateVideoPassword_str = e.playlist_ar[t.id].privateVideoPassword_str), o.privateVideoPassword_str == FWDMSPUtils.MD5(o.passInput_do.screen.value) ? o.dispatchEvent(s.CORRECT) : FWDAnimation.isTweening(o.passInput_do.screen) || FWDAnimation.to(o.passInput_do.screen, .1, {
                    css: {
                        backgroundColor: "#FF0000"
                    },
                    yoyo: !0,
                    repeat: 3
                })
            }, this.updateHEXColors = function(e, t) {
                o.passButton_do.updateHEXColors(e, t), o.closeButton_do.updateHEXColors(e, t)
            }, this.showInfo = function(e, t) {
                o.infoText_do.setInnerHTML(e), o.passMainHolder_do.addChild(o.infoText_do), o.infoText_do.setWidth(o.buttonWidth), o.infoText_do.setHeight(o.buttonHeight - 4), o.infoText_do.setX(o.passButton_do.x), o.infoText_do.setY(o.passButton_do.y - 23), o.infoText_do.setAlpha(0), o.infoText_do.getStyle().color = t ? "#FF0000" : o.mainLabelsColor_str, FWDAnimation.killTweensOf(o.infoText_do), FWDAnimation.to(o.infoText_do, .16, {
                    alpha: 1,
                    yoyo: !0,
                    repeat: 7
                })
            }, this.show = function(e) {
                o.isShowed_bl || (o.isShowed_bl = !0, t.main_do.addChild(o), o.positionAndResize(), o.passButton_do.setSelectedState(), o.passInput_do.setInnerHTML(""), (!FWDMSPUtils.isMobile || FWDMSPUtils.isMobile && FWDMSPUtils.hasPointerEvent) && t.main_do.setSelectable(!0), clearTimeout(o.hideCompleteId_to), clearTimeout(o.showCompleteId_to), o.mainHolder_do.setY(-o.stageHeight), o.showCompleteId_to = setTimeout(o.showCompleteHandler, 900), setTimeout(function() {
                    FWDAnimation.to(o.mainHolder_do, .8, {
                        y: 0,
                        delay: .1,
                        ease: Expo.easeInOut
                    })
                }, 100))
            }, this.showCompleteHandler = function() {}, this.hide = function() {
                o.isShowed_bl && (o.isShowed_bl = !1, t.customContextMenu_do && t.customContextMenu_do.enable(), o.positionAndResize(), clearTimeout(o.hideCompleteId_to), clearTimeout(o.showCompleteId_to), (!FWDMSPUtils.isMobile || FWDMSPUtils.isMobile && FWDMSPUtils.hasPointerEvent) && t.main_do.setSelectable(!1), o.hideCompleteId_to = setTimeout(o.hideCompleteHandler, 800), FWDAnimation.killTweensOf(o.mainHolder_do), FWDAnimation.to(o.mainHolder_do, .8, {
                    y: -o.stageHeight,
                    ease: Expo.easeInOut
                }))
            }, this.hideCompleteHandler = function() {
                t.main_do.removeChild(o), o.dispatchEvent(s.HIDE_COMPLETE)
            }, this.init()
        };
        s.setPrototype = function() {
            s.prototype = new FWDMSPDisplayObject("div")
        }, s.ERROR = "error", s.CORRECT = "correct", s.HIDE_COMPLETE = "hideComplete", s.prototype = null, e.FWDMSPPassword = s
    }(window),
    function(n) {
        var l = function(s, o) {
            var i = this;
            l.prototype;
            this.embedColoseN_img = s.embedColoseN_img, this.bk_do = null, this.mainHolder_do = null, this.closeButton_do = null, this.buttons_ar = [], this.embedWindowBackground_str = s.shareBkPath_str, this.embedWindowCloseButtonMargins = 0, this.scrubbersHeight = s.mainScrubberBkLeft_img.height, this.scrubberBkMiddlePath_str = s.mainScrubberBkMiddlePath_str, this.scrubbersBkLeftAndRightWidth = s.mainScrubberBkLeft_img.width, this.useHEXColorsForSkin_bl = s.useHEXColorsForSkin_bl, this.normalButtonsColor_str = s.normalButtonsColor_str, this.selectedButtonsColor_str = s.selectedButtonsColor_str, this.mainScrubberDragMiddlePath_str = s.mainScrubberDragMiddlePath_str, this.scrubberDragLeftWidth = s.mainScrubberDragLeft_img.width, this.playbackRateWindowTextColor_str = s.playbackRateWindowTextColor_str, this.defaultPlaybackRate = s.defaultPlaybackRate,this.toopTipPointerUp_str = s.toopTipPointer_str, this.toopTipBk_str = s.toopTipBk_str, this.totalWidth = 0, this.stageWidth = 0, this.stageHeight = 0, this.minMarginXSpace = 20, this.hSpace = 20, this.minHSpace = 10, this.vSpace = 15, this.minValue = .5, this.maxValue = 3, this.pointerWidth = 7, this.pointerHeight = 4, this.percent = 0, this.isScrubbing_bl = !1, this.isShowed_bl = !1, this.isMobile_bl = FWDMSPUtils.isMobile, this.init = function() {
                i.setBackfaceVisibility(), i.mainHolder_do = new FWDMSPDisplayObject("div"), i.mainHolder_do.hasTransform3d_bl = !1, i.mainHolder_do.hasTransform2d_bl = !1, i.mainHolder_do.setBackfaceVisibility(), i.bk_do = new FWDMSPDisplayObject("div"), i.bk_do.getStyle().width = "100%", i.bk_do.getStyle().height = "100%", i.bk_do.setAlpha(.9), i.bk_do.getStyle().background = "url('" + i.embedWindowBackground_str + "')", FWDMSPSimpleButton.setPrototype(), i.closeButton_do = new FWDMSPSimpleButton(s.playbackRateWindowClooseN_img, s.playbackRateClosePathS_str, void 0, !0, s.useHEXColorsForSkin_bl, s.normalButtonsColor_str, s.selectedButtonsColor_str), i.closeButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, i.closeButtonOnMouseUpHandler), i.addChild(i.mainHolder_do), i.mainHolder_do.addChild(i.bk_do), i.mainHolder_do.addChild(i.closeButton_do), this.setupScrubber()
            }, this.closeButtonOnMouseUpHandler = function() {
                i.isShowed_bl && i.hide(!0)
            }, this.positionAndResize = function() {
                i.stageWidth = o.stageWidth, i.stageHeight = o.stageHeight;
                var e = i.stageWidth - i.closeButton_do.w - i.embedWindowCloseButtonMargins,
                    t = 0;
                t = o.playlist_do && o.position_str == FWDMSP.POSITION_TOP ? o.playlist_do.h : i.embedWindowCloseButtonMargins, i.closeButton_do.setX(e), i.closeButton_do.setY(0), i.setY(t), i.setWidth(i.stageWidth), i.setHeight(i.stageHeight), i.mainHolder_do.setWidth(i.stageWidth), i.mainHolder_do.setHeight(i.stageHeight), i.positionScruber(), i.updateScrubber(i.percent)
            }, this.setupScrubber = function() {
                i.scrubber_do = new FWDMSPDisplayObject("div"), i.scrubber_do.setHeight(i.scrubbersHeight), i.scrubber_do.setButtonMode(!0), i.scrubberBkLeft_do = new FWDMSPDisplayObject("img");
                var e = new Image;
                e.src = s.mainScrubberBkLeft_img.src, i.scrubberBkLeft_do.setScreen(e), i.scrubberBkLeft_do.setWidth(s.mainScrubberBkLeft_img.wideth), i.scrubberBkLeft_do.setHeight(s.mainScrubberBkLeft_img.height), i.scrubberBkRight_do = new FWDMSPDisplayObject("img");
                var t = new Image;
                t.src = s.mainScrubberBkRight_img.src, i.scrubberBkRight_do.setScreen(t), i.scrubberBkRight_do.setWidth(s.mainScrubberBkRight_img.width), i.scrubberBkRight_do.setHeight(s.mainScrubberBkRight_img.height), (new Image).src = i.scrubberBkMiddlePath_str, i.scrubberBkMiddle_do = new FWDMSPDisplayObject("div"), i.scrubberBkMiddle_do.getStyle().background = "url('" + i.scrubberBkMiddlePath_str + "')", i.scrubberBkMiddle_do.setHeight(i.scrubbersHeight), i.scrubberBkMiddle_do.setX(i.scrubbersBkLeftAndRightWidth), i.scrubberDrag_do = new FWDMSPDisplayObject("div"), i.scrubberDrag_do.setHeight(i.scrubbersHeight), i.useHEXColorsForSkin_bl ? (i.scrubberDragLeft_do = new FWDMSPDisplayObject("div"), i.scrubberDragLeft_do.setWidth(s.mainScrubberDragLeft_img.width), i.scrubberDragLeft_do.setHeight(s.mainScrubberDragLeft_img.height), i.scrubberDragLeft_canvas = FWDMSPUtils.getCanvasWithModifiedColor(s.mainScrubberDragLeft_img, i.normalButtonsColor_str).canvas, i.scrubberDragLeft_do.screen.appendChild(i.scrubberDragLeft_canvas)) : (i.mainScrubberDragLeft_img = new Image, i.mainScrubberDragLeft_img.src = s.mainScrubberDragLeft_img.src, i.mainScrubberDragLeft_img.width = s.mainScrubberDragLeft_img.width, i.mainScrubberDragLeft_img.height = s.mainScrubberDragLeft_img.height, i.scrubberDragLeft_do = new FWDMSPDisplayObject("img"), i.scrubberDragLeft_do.setScreen(i.mainScrubberDragLeft_img)), i.mainScrubberMiddleImage = new Image, i.mainScrubberMiddleImage.src = s.mainScrubberDragMiddlePath_str, i.useHEXColorsForSkin_bl ? (i.mainScrubberDragMiddle_do = new FWDMSPDisplayObject("div"), i.mainScrubberMiddleImage.onload = function() {
                    i.mainScrubberDragMiddle_canvas = FWDMSPUtils.getCanvasWithModifiedColor(i.mainScrubberMiddleImage, i.normalButtonsColor_str, !0), i.mainSCrubberMiddleCanvas = i.mainScrubberDragMiddle_canvas.canvas, i.mainSCrubberDragMiddleImageBackground = i.mainScrubberDragMiddle_canvas.image, i.mainScrubberDragMiddle_do.getStyle().background = "url('" + i.mainSCrubberDragMiddleImageBackground.src + "') repeat-x"
                }) : (i.mainScrubberDragMiddle_do = new FWDMSPDisplayObject("div"), i.mainScrubberDragMiddle_do.getStyle().background = "url('" + i.mainScrubberDragMiddlePath_str + "') repeat-x"), i.mainScrubberDragMiddle_do.setHeight(i.scrubbersHeight), i.mainScrubberDragMiddle_do.setX(i.scrubberDragLeftWidth), i.scrubberBarLine_do = new FWDMSPDisplayObject("img");
                var o = new Image;
                o.src = s.mainScrubberLine_img.src, i.scrubberBarLine_do.setScreen(o), i.scrubberBarLine_do.setWidth(s.mainScrubberLine_img.width), i.scrubberBarLine_do.setHeight(s.mainScrubberLine_img.height), i.scrubberBarLine_do.setAlpha(0), i.scrubberBarLine_do.hasTransform3d_bl = !1, i.scrubberBarLine_do.hasTransform2d_bl = !1, i.minTime_do = new FWDMSPDisplayObject("div"), i.minTime_do.hasTransform3d_bl = !1, i.minTime_do.hasTransform2d_bl = !1, i.minTime_do.getStyle().fontFamily = "Arial", i.minTime_do.getStyle().fontSize = "12px", i.minTime_do.getStyle().whiteSpace = "nowrap", i.minTime_do.getStyle().textAlign = "left", i.minTime_do.getStyle().color = i.playbackRateWindowTextColor_str, i.minTime_do.getStyle().fontSmoothing = "antialiased", i.minTime_do.getStyle().webkitFontSmoothing = "antialiased", i.minTime_do.getStyle().textRendering = "optimizeLegibility", i.minTime_do.setInnerHTML("0.5"), i.mainHolder_do.addChild(i.minTime_do), i.maxTime_do = new FWDMSPDisplayObject("div"), i.maxTime_do.hasTransform3d_bl = !1, i.maxTime_do.hasTransform2d_bl = !1, i.maxTime_do.getStyle().fontFamily = "Arial", i.maxTime_do.getStyle().fontSize = "12px", i.maxTime_do.getStyle().whiteSpace = "nowrap", i.maxTime_do.getStyle().textAlign = "left", i.maxTime_do.getStyle().color = i.playbackRateWindowTextColor_str, i.maxTime_do.getStyle().fontSmoothing = "antialiased", i.maxTime_do.getStyle().webkitFontSmoothing = "antialiased", i.maxTime_do.getStyle().textRendering = "optimizeLegibility", i.maxTime_do.setInnerHTML("3.0"), i.mainHolder_do.addChild(i.maxTime_do), i.scrubber_do.addChild(i.scrubberBkLeft_do), i.scrubber_do.addChild(i.scrubberBkMiddle_do), i.scrubber_do.addChild(i.scrubberBkRight_do), i.scrubber_do.addChild(i.scrubberBarLine_do), i.scrubberDrag_do.addChild(i.scrubberDragLeft_do), i.scrubberDrag_do.addChild(i.mainScrubberDragMiddle_do), i.scrubber_do.addChild(i.scrubberDrag_do), i.scrubber_do.addChild(i.scrubberBarLine_do), i.mainHolder_do.addChild(i.scrubber_do), i.isMobile_bl ? i.hasPointerEvent_bl ? (i.scrubber_do.screen.addEventListener("pointerover", i.mainScrubberOnOverHandler), i.scrubber_do.screen.addEventListener("pointerout", i.mainScrubberOnOutHandler), i.scrubber_do.screen.addEventListener("pointerdown", i.mainScrubberOnDownHandler)) : i.scrubber_do.screen.addEventListener("touchstart", i.mainScrubberOnDownHandler) : i.screen.addEventListener ? (i.scrubber_do.screen.addEventListener("mouseover", i.mainScrubberOnOverHandler), i.scrubber_do.screen.addEventListener("mouseout", i.mainScrubberOnOutHandler), i.scrubber_do.screen.addEventListener("mousedown", i.mainScrubberOnDownHandler)) : i.screen.attachEvent && (i.scrubber_do.screen.attachEvent("onmouseover", i.mainScrubberOnOverHandler), i.scrubber_do.screen.attachEvent("onmouseout", i.mainScrubberOnOutHandler), i.scrubber_do.screen.attachEvent("onmousedown", i.mainScrubberOnDownHandler))
            }, this.mainScrubberOnOverHandler = function(e) {}, this.mainScrubberOnOutHandler = function(e) {}, this.mainScrubberOnDownHandler = function(e) {
                e.preventDefault && e.preventDefault(), i.isScrubbing_bl = !0;
                var t = FWDMSPUtils.getViewportMouseCoordinates(e).screenX - i.scrubber_do.getGlobalX();
                t < 0 ? t = 0 : t > i.scruberWidth - i.scrubbersOffsetWidth && (t = i.scruberWidth - i.scrubbersOffsetWidth);
                var o = t / i.scruberWidth,
                    s = t / i.scruberWidth;
                i.disable_do && i.addChild(i.disable_do), i.updateScrubber(o), i.dispatchEvent(FWDMSPController.START_TO_SCRUB), i.dispatchEvent(FWDMSPController.SCRUB_PLAYLIST_ITEM, {
                    percent: s
                }), i.dispatchEvent(FWDMSPController.SCRUB, {
                    percent: o
                }), i.isMobile_bl ? i.hasPointerEvent_bl ? (n.addEventListener("pointermove", i.mainScrubberMoveHandler), n.addEventListener("pointerup", i.mainScrubberEndHandler)) : (n.addEventListener("touchmove", i.mainScrubberMoveHandler), n.addEventListener("touchend", i.mainScrubberEndHandler)) : n.addEventListener ? (n.addEventListener("mousemove", i.mainScrubberMoveHandler), n.addEventListener("mouseup", i.mainScrubberEndHandler)) : document.attachEvent && (document.attachEvent("onmousemove", i.mainScrubberMoveHandler), document.attachEvent("onmouseup", i.mainScrubberEndHandler))
            }, this.mainScrubberMoveHandler = function(e) {
                e.preventDefault && e.preventDefault();
                var t = FWDMSPUtils.getViewportMouseCoordinates(e).screenX - i.scrubber_do.getGlobalX();
                t < 0 ? t = 0 : t > i.scruberWidth - i.scrubbersOffsetWidth && (t = i.scruberWidth - i.scrubbersOffsetWidth);
                var o = t / i.scruberWidth,
                    s = t / i.scruberWidth;
                i.updateScrubber(o), i.dispatchEvent(FWDMSPController.SCRUB_PLAYLIST_ITEM, {
                    percent: s
                }), i.dispatchEvent(FWDMSPController.SCRUB, {
                    percent: o
                })
            }, this.mainScrubberEndHandler = function(e) {
                i.isScrubbing_bl = !1, i.disable_do && i.contains(i.disable_do) && i.removeChild(i.disable_do), i.updateScrubber(), i.dispatchEvent(FWDMSPController.STOP_TO_SCRUB), i.isMobile_bl ? i.hasPointerEvent_bl ? (n.removeEventListener("pointermove", i.mainScrubberMoveHandler), n.removeEventListener("pointerup", i.mainScrubberEndHandler)) : (n.removeEventListener("touchmove", i.mainScrubberMoveHandler), n.removeEventListener("touchend", i.mainScrubberEndHandler)) : n.removeEventListener ? (n.removeEventListener("mousemove", i.mainScrubberMoveHandler), n.removeEventListener("mouseup", i.mainScrubberEndHandler)) : document.detachEvent && (document.detachEvent("onmousemove", i.mainScrubberMoveHandler), document.detachEvent("onmouseup", i.mainScrubberEndHandler))
            }, this.updateScrubber = function(e) {
                (i.percent = e) < 0 ? e = 0 : 1 < e && (e = 1);
                var t = parseInt(e * i.scruberWidth);
                i.isScrubbing_bl ? i.defaultPlaybackRate = Number(i.minValue + (i.maxValue - i.minValue) * t / i.scruberWidth).toFixed(1) : t = (i.defaultPlaybackRate - i.minValue) / (i.maxValue - i.minValue) * i.scruberWidth, t < 1 && i.isMainScrubberLineVisible_bl ? (i.isMainScrubberLineVisible_bl = !1, FWDAnimation.to(i.scrubberBarLine_do, .5, {
                    alpha: 0
                })) : 2 < t && !i.isMainScrubberLineVisible_bl && (i.isMainScrubberLineVisible_bl = !0, FWDAnimation.to(i.scrubberBarLine_do, .5, {
                    alpha: 1
                })), i.scrubberDrag_do.setWidth(t), t > i.scruberWidth - i.scrubbersOffsetWidth && (t = i.scruberWidth - i.scrubbersOffsetWidth), FWDAnimation.to(i.scrubberBarLine_do, .8, {
                    x: t,
                    ease: Expo.easeOut
                }), i.dispatchEvent(l.SET_PLAYBACK_RATE, {
                    rate: i.defaultPlaybackRate
                })
            }, this.positionScruber = function() {
                i.scruberWidth = Math.min(600, i.stageWidth - 100), i.scrubber_do.setWidth(i.scruberWidth), i.scrubber_do.setX(Math.round((i.stageWidth - i.scruberWidth) / 2)), i.scrubber_do.setY(Math.round((i.stageHeight - i.scrubbersHeight) / 2)), i.scrubberBkMiddle_do.setWidth(i.scruberWidth - 2 * i.scrubbersBkLeftAndRightWidth), i.scrubberBkRight_do.setX(i.scruberWidth - i.scrubbersBkLeftAndRightWidth), i.mainScrubberDragMiddle_do.setWidth(i.scruberWidth - i.scrubbersBkLeftAndRightWidth), i.minTime_do.setX(i.scrubber_do.x - 26), i.minTime_do.setY(i.scrubber_do.y + 4), i.maxTime_do.setX(i.scrubber_do.x + i.scrubber_do.w + 8), i.maxTime_do.setY(i.scrubber_do.y + 4)
            }, this.show = function(e) {
                i.isShowed_bl || (i.isShowed_bl = !0, o.main_do.addChild(i), (!FWDMSPUtils.isMobile || FWDMSPUtils.isMobile && FWDMSPUtils.hasPointerEvent) && o.main_do.setSelectable(!0), i.positionAndResize(), clearTimeout(i.hideCompleteId_to), clearTimeout(i.showCompleteId_to), i.mainHolder_do.setY(-i.stageHeight), i.positionScruber(), setTimeout(function() {
                    i.updateScrubber(i.percent)
                }, 200), i.showCompleteId_to = setTimeout(i.showCompleteHandler, 900), setTimeout(function() {
                    FWDAnimation.to(i.mainHolder_do, .8, {
                        y: 0,
                        delay: .1,
                        ease: Expo.easeInOut
                    })
                }, 100))
            }, this.showCompleteHandler = function() {}, this.hide = function(e) {
                i.isShowed_bl && (i.isShowed_bl = !1, o.customContextMenu_do && o.customContextMenu_do.enable(), clearTimeout(i.hideCompleteId_to), clearTimeout(i.showCompleteId_to), (!FWDMSPUtils.isMobile || FWDMSPUtils.isMobile && FWDMSPUtils.hasPointerEvent) && o.main_do.setSelectable(!1), i.hideCompleteId_to = setTimeout(i.hideCompleteHandler, 800), FWDAnimation.killTweensOf(i.mainHolder_do), e ? FWDAnimation.to(i.mainHolder_do, .8, {
                    y: -i.stageHeight,
                    ease: Expo.easeInOut
                }) : i.hideCompleteHandler())
            }, this.hideCompleteHandler = function() {
                o.main_do.contains(i) && o.main_do.removeChild(i), i.dispatchEvent(l.HIDE_COMPLETE)
            }, this.updateHEXColors = function(e, t) {
                -1 != s.skinPath_str.indexOf("hex_white") ? i.selectedColor_str = "#FFFFFF" : i.selectedColor_str = t, i.closeButton_do.updateHEXColors(e, i.selectedColor_str), FWDMSPUtils.changeCanvasHEXColor(i.mainScrubberDragLeft_img, i.scrubberDragLeft_canvas, e);
                var o = FWDMSPUtils.changeCanvasHEXColor(i.mainScrubberMiddleImage, i.mainSCrubberMiddleCanvas, e, !0);
                i.mainScrubberDragMiddle_do.getStyle().background = "url('" + o.src + "') repeat-x"
            }, this.init()
        };
        l.setPrototype = function() {
            l.prototype = new FWDMSPDisplayObject("div")
        }, l.HIDE_COMPLETE = "hideComplete", l.SET_PLAYBACK_RATE = "setPlaybackRate", l.prototype = null, n.FWDMSPPlaybackRateWindow = l
    }(window),
    function() {
        var n = function(p, m) {
            var b = this;
            b.data = p;
            n.prototype;
            this.playlist_ar = null, this.items_ar = null, this.playlistItemBk1_img = p.playlistItemBk1_img, this.playlistItemBk2_img = p.playlistItemBk2_img, this.playlistSeparator_img = p.playlistSeparator_img, this.playlistScrBkTop_img = p.playlistScrBkTop_img, this.playlistScrBkMiddle_img = p.playlistScrBkMiddle_img, this.playlistScrBkBottom_img = p.playlistScrBkBottom_img, this.playlistScrDragTop_img = p.playlistScrDragTop_img, this.playlistScrDragMiddle_img = p.playlistScrDragMiddle_img, this.playlistScrDragBottom_img = p.playlistScrDragBottom_img, this.playlistPlayButtonN_img = p.playlistPlayButtonN_img, this.playlistScrLines_img = p.playlistScrLines_img, this.playlistScrLinesOver_img = p.playlistScrLinesOver_img, this.playlistDownloadButtonN_img = p.playlistDownloadButtonN_img, this.playlistBuyButtonN_img = p.playlistBuyButtonN_img, this.disable_do = null, this.separator_do = null, this.itemsHolder_do = null, this.curItem_do = null, this.scrMainHolder_do = null, this.scrTrack_do = null, this.scrTrackTop_do = null, this.scrTrackMiddle_do = null, this.scrTrackBottom_do = null, this.scrHandler_do = null, this.scrHandlerTop_do = null, this.scrHandlerMiddle_do = null, this.scrHandlerBottom_do = null, this.scrHandlerLines_do = null, this.scrHandlerLinesN_do = null, this.scrHandlerLinesS_do = null, this.playlistPlayButtonN_str = p.playlistPlayButtonN_str, this.playlistPlayButtonS_str = p.playlistPlayButtonS_str, this.playlistPauseButtonN_str = p.playlistPauseButtonN_str, this.playlistPauseButtonS_str = p.playlistPauseButtonS_str, this.controllerBkPath_str = p.controllerBkPath_str, this.playlistBackgroundColor_str = p.playlistBackgroundColor_str, this.searchInputColor_str = p.searchInputColor_str, b.useHEXColorsForSkin_bl = p.useHEXColorsForSkin_bl, b.normalButtonsColor_str = p.normalButtonsColor_str, b.selectedButtonsColor_str = p.selectedButtonsColor_str, this.countTrack = 0, this.inputSearchTextOffsetTop = p.inputSearchTextOffsetTop, this.inputSearchOffsetLeft = p.inputSearchOffsetLeft, this.startSpaceBetweenButtons = p.startSpaceBetweenButtons, this.spaceBetweenButtons = p.spaceBetweenButtons, 15 < this.spaceBetweenButtons && (this.spaceBetweenButtons = 10), this.searchBarHeight = p.searchBarHeight, this.countID3 = 0, this.id = 0, this.stageWidth = 0, this.stageHeight = 0, this.itemsTotalHeight = 0, this.scrollbarOffestWidth = p.scrollbarOffestWidth, this.scrWidth = b.playlistScrBkTop_img.width, this.trackTitleOffsetLeft = p.trackTitleOffsetLeft, this.downloadButtonOffsetRight = p.downloadButtonOffsetRight, this.itemHeight = b.playlistItemBk1_img.height, this.playPuaseIconWidth = b.playlistPlayButtonN_img.width, this.playPuaseIconHeight = b.playlistPlayButtonN_img.height, this.nrOfVisiblePlaylistItems = p.nrOfVisiblePlaylistItems, this.durationOffsetRight = p.durationOffsetRight, this.totalPlayListItems = 0, this.visibleNrOfItems = 0, this.yPositionOnPress = 0, this.lastPresedY = 0, this.lastListY = 0, this.playListFinalY = 0, this.scrollBarHandlerFinalY = 0, this.scrollBarHandlerFinalY = 0, this.vy = 0, this.vy2 = 0, this.friction = .9, this.comboboxHeight = 31, this.updateMobileScrollBarId_int, this.updateMoveMobileScrollbarId_int, this.disableOnMoveId_to, this.updateMobileScrollbarOnPlaylistLoadId_to, this.usePlaylistsSelectBox_bl = p.usePlaylistsSelectBox_bl, this.allowToTweenPlaylistItems_bl = !1, this.expandPlaylistBackground_bl = p.expandControllerBackground_bl, this.isSortedNumerical_bl = !0, this.showSortButtons_bl = p.showSortButtons_bl, this.showSearchBar_bl = p.showSearchBar_bl, this.showPlaylistItemBuyButton_bl = p.showPlaylistItemBuyButton_bl, this.addScrollBarMouseWheelSupport_bl = p.addScrollBarMouseWheelSupport_bl, this.allowToScrollAndScrollBarIsActive_bl = !1, this.isDragging_bl = !1, this.showPlaylistItemPlayButton_bl = p.showPlaylistItemPlayButton_bl, this.showPlaylistItemDownloadButton_bl = p.showPlaylistItemDownloadButton_bl, this.isShowed_bl = p.showPlayListByDefault_bl, this.isShowedFirstTime_bl = !1, this.animateOnIntro_bl = p.animateOnIntro_bl, this.isListCreated_bl = !1, this.isMobile_bl = FWDMSPUtils.isMobile, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, b.init = function() {
                if (b.hasTransform3d_bl = !1, b.hasTransform2d_bl = !1, b.setBackfaceVisibility(), b.mainHolder_do = new FWDMSPDisplayObject("div"), b.mainHolder_do.hasTransform3d_bl = !1, b.mainHolder_do.hasTransform2d_bl = !1, b.mainHolder_do.setBackfaceVisibility(), b.itemsHolder_do = new FWDMSPDisplayObject("div"), b.itemsHolder_do.setOverflow("visible"), b.itemsHolder_do.setY(0), b.itemsHolder_do.setBackfaceVisibility(), b.setupSeparator(), b.itemsHolder_do.setY(0), b.mainHolder_do.addChild(b.itemsHolder_do), b.addChild(b.mainHolder_do), b.isMobile_bl ? (b.setupMobileScrollbar(), b.hasPointerEvent_bl && b.setupDisable()) : (b.setupDisable(), b.setupScrollbar(), b.addScrollBarMouseWheelSupport_bl && b.addMouseWheelSupport()), b.usePlaylistsSelectBox_bl && b.setupcomboBox(), b.showSearchBar_bl) {
                    if (b.searchBar_do = new FWDMSPDisplayObject("div"), b.searchBar_do.setOverflow("visible"), b.expandPlaylistBackground_bl) {
                        b.controllerBk_do = new FWDMSPDisplayObject("img");
                        var e = new Image;
                        e.src = b.controllerBkPath_str, b.controllerBk_do.setScreen(e)
                    } else b.controllerBk_do = new FWDMSPDisplayObject("div"), b.controllerBk_do.getStyle().background = "url('" + b.controllerBkPath_str + "')";
                    b.controllerBk_do.getStyle().width = "100%", b.searchSeparator_do = new FWDMSPDisplayObject("div"), b.searchSeparator_do.setBackfaceVisibility(), b.searchSeparator_do.hasTransform3d_bl = !1, b.searchSeparator_do.hasTransform2d_bl = !1, b.searchSeparator_do.getStyle().background = "url('" + b.playlistSeparator_img.src + "')", b.searchSeparator_do.setHeight(b.playlistSeparator_img.height), b.searchBar_do.setHeight(b.searchBarHeight + b.searchSeparator_do.h), b.controllerBk_do.setHeight(b.searchBar_do.h + 1), b.searchBar_do.addChild(b.controllerBk_do), b.searchBar_do.addChild(b.searchSeparator_do), b.setupInput(), b.showSortButtons_bl && (b.setupButtons()), b.mainHolder_do.addChild(b.searchBar_do)
                }
                b.addChild(b.separator_do), b.mainHolder_do.setWidth(500), b.mainHolder_do.setHeight(500)
            }, b.disableSearchBar = function() {
                b.isSearchBarDisabled_bl || (b.isSearchBarDisabled_bl = !0, b.input_do.screen.value = "Search will be available when all tracks data is loaded!", b.input_do.screen.disabled = !0, b.sortNButton_do && (b.sortNButton_do.disable(), b.sortAButton_do.disable(), b.ascDscButton_do.disable()))
            }, b.enableSearchBar = function() {
                b.isSearchBarDisabled_bl && (b.isSearchBarDisabled_bl = !1, b.input_do.screen.value = "Search for track", b.input_do.screen.disabled = !1, b.sortNButton_do && (b.sortNButton_do.enable(), b.sortAButton_do.enable(), b.ascDscButton_do.enable()))
            }, b.resizeAndPosition = function(e) {
                (m.stageWidth != b.stageWidth || m.stageHeight != b.stageHeight || e) && b.isListCreated_bl && (b.stageWidth = m.stageWidth, b.stageWidth = m.stageWidth, b.comboBox_do && b.comboBox_do.resizeAndPosition(), b.positionList(), b.searchBar_do && b.positionSearchBar(), b.scrMainHolder_do && b.allowToScrollAndScrollBarIsActive_bl && b.scrMainHolder_do.setX(b.stageWidth - b.scrWidth))
            }, b.positionList = function(e) {
                if (b.isListCreated_bl) {
                    var t, o = 0;
                    if (b.usePlaylistsSelectBox_bl && (o = b.comboboxHeight), b.copy_ar = [].concat(b.items_ar), b.isSearched_bl = !1, b.input_do && (inputValue = b.input_do.screen.value, "Search for track" != inputValue && !b.isSearchBarDisabled_bl)) {
                        inputValue = b.input_do.screen.value.toLowerCase();
                        for (var s = 0; s < b.copy_ar.length; s++) - 1 == (t = b.copy_ar[s]).titleText_str.toLowerCase().indexOf(inputValue.toLowerCase()) && (FWDAnimation.killTweensOf(t), 1 != t.alpha && t.setAlpha(1), t.setX(-t.w), b.copy_ar.splice(s, 1), s--)
                    }
                    for (s = 0; s < b.copy_ar.length; s++)(t = b.copy_ar[s]).changeSource(s % 2);
                    var i = b.copy_ar.length;
                    b.totalSearchedItems = i, b.itemsTotalHeight = i * b.itemHeight, b.visibleNrOfItems >= i ? b.allowToScrollAndScrollBarIsActive_bl = !1 : b.allowToScrollAndScrollBarIsActive_bl = !0;
                    for (s = 0; s < i; s++) t = b.copy_ar[s], b.allowToTweenPlaylistItems_bl && t.x < 0 && !b.isMobile_bl ? FWDAnimation.isTweening(t) || FWDAnimation.to(t, .8, {
                        x: 0,
                        ease: Expo.easeInOut
                    }) : (FWDAnimation.killTweensOf(t), t.setX(0)), t.setY(b.itemHeight * s), b.allowToScrollAndScrollBarIsActive_bl && b.scrMainHolder_do ? t.resize(b.stageWidth - b.scrollbarOffestWidth, b.itemHeight) : t.resize(b.stageWidth, b.itemHeight), 1 != t.alpha && t.setAlpha(1);
                    b.allowToScrollAndScrollBarIsActive_bl && b.scrMainHolder_do ? b.itemsHolder_do.setWidth(b.stageWidth - b.scrollbarOffestWidth) : b.itemsHolder_do.setWidth(b.stageWidth), b.input_do && (0 == i ? b.showNothingFound() : b.hideNothingFound()), b.scrHandler_do && b.updateScrollBarSizeActiveAndDeactivate(), b.separator_do.setWidth(b.stageWidth), b.mainHolder_do.setWidth(b.stageWidth), b.mainHolder_do.setY(o), b.mainHolder_do.setHeight(b.stageHeight + o), b.setWidth(b.stageWidth), b.setHeight(b.stageHeight + o)
                }
            }, this.setupcomboBox = function() {
                b.labels_ar = [];
                for (var e = 0; e < p.cats_ar.length; e++) {
                    b.labels_ar[e] = p.cats_ar[e].playlistsName;
                    var t = "";
                    p.showPlaylistsSelectBoxNumbers_bl ? (e < 9 && (t = "0"), t = t + (e + 1) + ". ", b.labels_ar[e] = t + p.cats_ar[e].playlistsName) : b.labels_ar[e] = p.cats_ar[e].playlistsName
                }
                var o = {
                    categories_ar: b.labels_ar,
                    selectorLabel: b.labels_ar[0],
                    bk1_str: p.comboboxBk1_str,
                    bk2_str: p.comboboxBk2_str,
                    selectorBackgroundNormalColor: p.mainSelectorBackgroundSelectedColor,
                    selectorTextNormalColor: p.mainSelectorTextNormalColor,
                    selectorTextSelectedColor: p.mainSelectorTextSelectedColor,
                    buttonBackgroundNormalColor: p.mainButtonBackgroundNormalColor,
                    buttonBackgroundSelectedColor: p.mainButtonBackgroundSelectedColor,
                    buttonTextNormalColor: p.mainButtonTextNormalColor,
                    buttonTextSelectedColor: p.mainButtonTextSelectedColor,
                    buttonHeight: b.comboboxHeight,
                    arrowN_str: p.arrowN_str,
                    arrowS_str: p.arrowS_str,
                    arrowW: 11,
                    arrowH: 6
                };
                FWDMSPComboBox.setPrototype(), b.comboBox_do = new FWDMSPComboBox(b, o), b.comboBox_do.addListener(FWDMSPComboBox.BUTTON_PRESSED, b.changePlaylistOnClick), b.addChild(b.comboBox_do)
            }, this.changePlaylistOnClick = function(e) {
                b.dispatchEvent(n.CHANGE_PLAYLIST, {
                    id: e.id
                })
            }, this.updatePlaylist = function(e) {
                if (!b.isListCreated_bl) {
                    b.playlist_ar = e, b.isShowedFirstTime_bl = !0, b.stageHeight = 0, b.isListCreated_bl = !0, b.input_do && (b.input_do.screen.value = "Search for track"), b.allowToScrollAndScrollBarIsActive_bl = !1, b.countID3, b.countTrack = 0, b.visibleNrOfItems = b.nrOfVisiblePlaylistItems, b.totalPlayListItems = b.playlist_ar.length, b.nrOfVisiblePlaylistItems > b.totalPlayListItems && (b.visibleNrOfItems = b.totalPlayListItems), b.nrOfVisiblePlaylistItems > b.totalPlayListItems && (b.nrOfVisiblePlaylistItems = b.totalPlayListItems), b.stageHeight = b.visibleNrOfItems * b.itemHeight + b.separator_do.h, b.searchBar_do && (b.stageHeight += b.separator_do.h + b.searchBarHeight), b.itemsTotalHeight = b.totalPlayListItems * b.itemHeight, b.mainHolder_do.setY(-b.stageHeight), b.itemsHolder_do.setY(0), b.sortNButton_do && (b.disableSortNButton(), b.ascDscButton_do.setButtonState(1), b.srotAscending_bl = !0), b.showSearchBar_bl && b.enableSearchBar(), b.createPlayList(), b.loadId3();
                    var t = b.items_ar.length;
                    clearTimeout(b.updateMobileScrollbarOnPlaylistLoadId_to), b.updateMobileScrollbarOnPlaylistLoadId_to = setTimeout(b.updateScrollBarHandlerAndContent, 900), clearTimeout(b.showAnimationIntroId_to), b.showAnimationIntroId_to = setTimeout(function() {
                        for (var e = 0; e < t; e++) b.items_ar[e].setTextSizes();
                        b.isListCreated_bl = !0, b.visibleNrOfItems >= b.totalPlayListItems ? b.allowToScrollAndScrollBarIsActive_bl = !1 : b.allowToScrollAndScrollBarIsActive_bl = !0, b.scrHandler_do && b.updateScrollBarSizeActiveAndDeactivate(), b.scrMainHolder_do && b.allowToScrollAndScrollBarIsActive_bl && b.scrMainHolder_do.setX(b.stageWidth - b.scrWidth), m.position_str == FWDMSP.POSITION_TOP ? (b.mainHolder_do.setY(0), b.usePlaylistsSelectBox_bl ? b.separator_do.setY(b.stageHeight - b.separator_do.h + b.comboboxHeight) : b.separator_do.setY(b.stageHeight - b.separator_do.h)) : (b.mainHolder_do.setY(b.separator_do.h), b.separator_do.setY(0)), b.positionList(), b.allowToTweenPlaylistItems_bl = !0
                    }, 100)
                }
            }, this.destroyPlaylist = function() {
                if (b.isListCreated_bl) {
                    var e, t = b.items_ar.length;
                    b.isListCreated_bl = !1, b.allowToTweenPlaylistItems_bl = !1, clearTimeout(b.showAnimationIntroId_to);
                    for (var o = 0; o < t; o++) e = b.items_ar[o], b.itemsHolder_do.removeChild(e), e.destroy();
                    b.items_ar = null, b.stageHeight = 0, b.setHeight(b.stageHeight)
                }
            }, this.createPlayList = function() {
                var e, t;
                b.itemsHolder_do.setHeight(b.totalPlayListItems * b.itemHeight), b.mainHolder_do.setBkColor(b.playlistBackgroundColor_str), b.items_ar = [];
                for (var o = 0; o < b.totalPlayListItems; o++) {
                    t = null == b.playlist_ar[o].duration ? void 0 : FWDMSP.formatTotalTime(b.playlist_ar[o].duration);
                    var s = b.playlist_ar[o].downloadable;
                    b.showPlaylistItemDownloadButton_bl || (s = !1);
                    var i = Boolean(b.playlist_ar[o].buy);
                    b.showPlaylistItemBuyButton_bl || (i = !1), FWDMSPPlaylistItem.setPrototype(), (e = new FWDMSPPlaylistItem(b.playlist_ar[o].title, b.playlist_ar[o].titleText, b.playlistDownloadButtonN_img, p.playlistDownloadButtonS_str, b.playlistBuyButtonN_img, p.playlistBuyButtonS_str, p.playlistItemGrad1_img, p.playlistItemGrad2_img, p.playlistItemProgress1_img, p.playlistItemProgress2_img, p.playlistPlayButtonN_img, p.playlistItemBk1_img.src, p.playlistItemBk2_img.src, b.playlistPlayButtonN_str, b.playlistPlayButtonS_str, b.playlistPauseButtonN_str, b.playlistPauseButtonS_str, p.trackTitleNormalColor_str, p.trackTitleSelected_str, p.trackDurationColor_str, o, p.playPauseButtonOffsetLeftAndRight, b.trackTitleOffsetLeft, b.durationOffsetRight, b.downloadButtonOffsetRight, b.showPlaylistItemPlayButton_bl, s, i, t, b.useHEXColorsForSkin_bl, b.normalButtonsColor_str, b.selectedButtonsColor_str, b)).addListener(FWDMSPPlaylistItem.MOUSE_UP, b.itemOnUpHandler), e.addListener(FWDMSPPlaylistItem.DOWNLOAD, b.downloadHandler), e.addListener(FWDMSPPlaylistItem.BUY, b.buyHandler), b.items_ar[o] = e, b.itemsHolder_do.addChild(e)
                }
            }, this.addTrack = function(e, t, o, s, i, n, l) {
                var r;
                b.isSortedNumerical_bl = !0, b.srotAscending_bl = !0, b.ascDscButton_do && b.ascDscButton_do.setButtonState(1), b.disableSortNButton(), b.sortList();
                var a, d = 0;
                b.addAtThePlaylistEnd_bl = !1, b.addAtThePlaylistBeggingin_bl = !1, a = i ? (b.addAtThePlaylistBeggingin_bl = !0, 0) : (b.addAtThePlaylistEnd_bl = !0, b.totalPlayListItems + 1), clearTimeout(b.resetItemsAddOrderId_to), b.resetItemsAddOrderId_to = setTimeout(function() {
                    b.addAtThePlaylistEnd_bl = !1, b.addAtThePlaylistBeggingin_bl = !1
                }, 100);
                var u = Boolean(l);
                b.showPlaylistItemBuyButton_bl || (u = !1), r = t = p.showTracksNumbers_bl ? (a < 9 && (d = "0" + (a + 1)), d + ". " + t) : t, FWDMSPPlaylistItem.setPrototype();
                var c = new FWDMSPPlaylistItem(t, r, b.playlistDownloadButtonN_img, p.playlistDownloadButtonS_str, b.playlistBuyButtonN_img, p.playlistBuyButtonS_str, p.playlistItemGrad1_img, p.playlistItemGrad2_img, p.playlistItemProgress1_img, p.playlistItemProgress2_img, p.playlistPlayButtonN_img, p.playlistItemBk1_img.src, p.playlistItemBk2_img.src, b.playlistPlayButtonN_str, b.playlistPlayButtonS_str, b.playlistPauseButtonN_str, b.playlistPauseButtonS_str, p.trackTitleNormalColor_str, p.trackTitleSelected_str, p.trackDurationColor_str, a, p.playPauseButtonOffsetLeftAndRight, b.trackTitleOffsetLeft, b.durationOffsetRight, b.downloadButtonOffsetRight, b.showPlaylistItemPlayButton_bl, n, u, s, b.useHEXColorsForSkin_bl, b.normalButtonsColor_str, b.selectedButtonsColor_str, b),
                    h = {};
                h.title = t, h.titleText = t, h.source = e, h.duration = s, h.thumbPath = o, h.downloadable = n, h.buy = l, u && (h.buy = l), b.playlist_ar.splice(a, 0, h), b.items_ar.splice(a, 0, c), b.itemsHolder_do.addChild(c), b.totalPlayListItems = b.playlist_ar.length, m.totalAudio = b.totalPlayListItems;
                for (var _ = 0; _ < b.totalPlayListItems; _++) {
                    var f = b.items_ar[_];
                    f.id = f.sortId = _, t = (t = b.playlist_ar[_].title).substr(t.indexOf(".") + 1), t = p.showTracksNumbers_bl ? (d = _ < 9 ? "0" + (_ + 1) : _ + 1) + ". " + t : t, f.title_str = t, f.updateTitle(), f.setTextSizes(!0)
                }
                setTimeout(function() {
                    c && (c.setTextSizes(!0), b.allowToScrollAndScrollBarIsActive_bl && b.scrMainHolder_do ? c.resize(b.stageWidth - b.scrollbarOffestWidth, b.itemHeight) : c.resize(b.stageWidth, b.itemHeight), FWDAnimation.to(c, .1, {
                        alpha: 1,
                        ease: Expo.easeOut,
                        overwrite: !1
                    }), FWDAnimation.to(c, .1, {
                        alpha: .5,
                        delay: .1,
                        ease: Expo.easeOut,
                        overwrite: !1
                    }), FWDAnimation.to(c, .1, {
                        alpha: 1,
                        delay: .2,
                        ease: Expo.easeOut,
                        overwrite: !1
                    }), FWDAnimation.to(c, .1, {
                        alpha: .5,
                        delay: .3,
                        ease: Expo.easeOut,
                        overwrite: !1
                    }), FWDAnimation.to(c, .1, {
                        alpha: 1,
                        delay: .4,
                        ease: Expo.easeOut,
                        overwrite: !1
                    }))
                }, 50), c.addListener(FWDMSPPlaylistItem.MOUSE_UP, b.itemOnUpHandler), c.addListener(FWDMSPPlaylistItem.DOWNLOAD, b.downloadHandler), c.addListener(FWDMSPPlaylistItem.BUY, b.buyHandler), b.positionList(), b.updateScrollBarHandlerAndContent(!0, !0), c.setAlpha(0)
            }, this.itemOnUpHandler = function(e) {
                b.dispatchEvent(FWDMSPPlaylistItem.MOUSE_UP, {
                    id: e.id
                })
            }, this.downloadHandler = function(e) {
                b.dispatchEvent(FWDMSPPlaylistItem.DOWNLOAD, {
                    id: e.id
                })
            }, this.buyHandler = function(e) {
                b.dispatchEvent(FWDMSPPlaylistItem.BUY, {
                    id: e.id
                })
            }, this.loadId3 = function() {
                clearTimeout(b.populateNextItemId_to);
                for (var e = 0; e < b.totalPlayListItems; e++)
                    if ("..." != b.playlist_ar[e].title) return void(b.countID3 = 2001);
                b.showSearchBar_bl && b.disableSearchBar(), b.countID3 = 0, b.loadID3AndPopulate()
            }, this.loadID3AndPopulate = function() {
                if (b.items_ar)
                    if (b.playlist_ar[b.countID3]) {
                        var t = "",
                            o = b.items_ar[b.countID3],
                            s = b.playlist_ar[b.countID3].source + "?rand=" + parseInt(99999999 * Math.random()),
                            i = b.playlist_ar[b.countID3];
                        ID3.loadTags(s, function() {
                            if (b.countID3 > b.playlist_ar.length || 2001 == b.countID3) clearTimeout(b.populateNextItemId_to);
                            else {
                                var e = ID3.getAllTags(s);
                                e.artist && (i.titleText_str = e.artist + " - " + e.title, p.showTracksNumbers_bl ? (b.countTrack < 9 && (t = "0"), t = t + (b.countTrack + 1) + ". ", i.title = t + i.titleText_str) : i.title = i.titleText_str, b.countTrack++), o.title_str = i.title, o.titleText_str = i.titleText_str, b.countID3 == b.id && b.dispatchEvent(n.UPDATE_TRACK_TITLE_if_FOLDER, {
                                    title: o.title_str
                                }), o.updateTitle(), setTimeout(function() {
                                    o && (o.setTextSizes(!0), b.allowToScrollAndScrollBarIsActive_bl && b.scrMainHolder_do ? o.resize(b.stageWidth - b.scrollbarOffestWidth, b.itemHeight) : o.resize(b.stageWidth, b.itemHeight))
                                }, 50), b.countID3++, b.populateNextItemId_to = setTimeout(b.loadID3AndPopulate, 150)
                            }
                        })
                    } else b.showSearchBar_bl && b.enableSearchBar()
            }, this.activateItems = function(e, t) {
                var o;
                if (b.id = e, b.items_ar) {
                    for (var s = 0; s < b.totalPlayListItems; s++)
                        if ((o = b.items_ar[s]).id == b.id) {
                            b.sortId = o.sortId;
                            break
                        } b.curItem_do = b.items_ar[b.sortId], b.id = b.curItem_do.id;
                    for (s = 0; s < b.totalPlayListItems; s++) o = b.items_ar[s], s == b.sortId ? o.setActive() : o.setInActive();
                    t || b.updateScrollBarHandlerAndContent(!0)
                }
            }, this.setCurItemPlayState = function() {
                b.curItem_do && b.curItem_do.showPlayButton()
            }, this.setCurItemPauseState = function() {
                b.curItem_do && b.curItem_do.showPauseButton()
            }, this.updateCurItemProgress = function(e) {
                b.curItem_do && b.curItem_do.updateProgressPercent(e)
            }, this.setupInput = function() {
                b.titlebarHeight = p.titlebarLeftPath_img.height, b.mainSearchInput_do = new FWDMSPDisplayObject("div"), b.mainSearchInput_do.getStyle().background = "url('" + p.titlebarBkMiddlePattern_str + "')", b.mainSearchInput_do.setHeight(b.titlebarHeight);
                var e = new Image;
                e.src = p.titleBarLeft_img.src, b.titleBarLeft_do = new FWDMSPDisplayObject("img"), b.titleBarLeft_do.setScreen(e), b.titleBarLeft_do.setWidth(p.titleBarLeft_img.width), b.titleBarLeft_do.setHeight(p.titleBarLeft_img.height);
                var t = new Image;
                t.src = p.titleBarRigth_img.src, b.titleBarRight_do = new FWDMSPDisplayObject("img"), b.titleBarRight_do.setScreen(t), b.titleBarRight_do.setWidth(p.titleBarRigth_img.width), b.titleBarRight_do.setHeight(p.titleBarRigth_img.height), b.input_do = new FWDMSPDisplayObject("input"), b.input_do.screen.maxLength = 20, b.input_do.getStyle().textAlign = "left", b.input_do.getStyle().outline = "none", b.input_do.getStyle().boxShadow = "none", b.input_do.getStyle().fontSmoothing = "antialiased", b.input_do.getStyle().webkitFontSmoothing = "antialiased", b.input_do.getStyle().textRendering = "optimizeLegibility", b.input_do.getStyle().fontFamily = "Arial", b.input_do.getStyle().fontSize = "12px", b.input_do.getStyle().padding = "6px", FWDMSPUtils.isIEAndLessThen9 || (b.input_do.getStyle().paddingRight = "-6px"), b.input_do.getStyle().paddingTop = "2px", b.input_do.getStyle().paddingBottom = "3px", b.input_do.getStyle().color = b.searchInputColor_str, b.input_do.screen.value = "Search for track", b.noSearchFound_do = new FWDMSPDisplayObject("div"), b.noSearchFound_do.setX(0), b.noSearchFound_do.getStyle().textAlign = "center", b.noSearchFound_do.getStyle().width = "100%", b.noSearchFound_do.getStyle().fontSmoothing = "antialiased", b.noSearchFound_do.getStyle().webkitFontSmoothing = "antialiased", b.noSearchFound_do.getStyle().textRendering = "optimizeLegibility", b.noSearchFound_do.getStyle().fontFamily = "Arial", b.noSearchFound_do.getStyle().fontSize = "12px", b.noSearchFound_do.getStyle().color = b.searchInputColor_str, b.noSearchFound_do.setInnerHTML("NOTHING FOUND!"), b.noSearchFound_do.setVisible(!1), b.mainHolder_do.addChild(b.noSearchFound_do), b.input_do.screen.addEventListener ? (b.input_do.screen.addEventListener("focus", b.inputFocusInHandler), b.input_do.screen.addEventListener("blur", b.inputFocusOutHandler), b.input_do.screen.addEventListener("keyup", b.keyUpHandler)) : b.input_do.screen.attachEvent && (b.input_do.screen.attachEvent("onfocus", b.inputFocusInHandler), b.input_do.screen.attachEvent("onblur", b.inputFocusOutHandler), b.input_do.screen.attachEvent("onkeyup", b.keyUpHandler)), b.inputArrow_img = new Image, b.inputArrow_img.src = p.inputArrowPath_str, b.useHEXColorsForSkin_bl ? (b.inputArrow_do = new FWDMSPDisplayObject("div"), b.inputArrow_img.onload = function() {
                    b.mainScrubberDragLeft_canvas = FWDMSPUtils.getCanvasWithModifiedColor(b.inputArrow_img, b.normalButtonsColor_str).canvas, b.inputArrow_do.setWidth(b.inputArrow_img.width), b.inputArrow_do.setHeight(b.inputArrow_img.height), b.inputArrow_do.screen.appendChild(b.mainScrubberDragLeft_canvas)
                }) : (b.inputArrow_do = new FWDMSPDisplayObject("img"), b.inputArrow_do.setScreen(b.inputArrow_img), b.inputArrow_do.setWidth(14), b.inputArrow_do.setHeight(12)), setTimeout(function() {
                    b.input_do.setY(parseInt((b.titlebarHeight - b.input_do.getHeight()) / 2) + b.inputSearchTextOffsetTop)
                }, 50), b.mainSearchInput_do.addChild(b.titleBarLeft_do), b.mainSearchInput_do.addChild(b.titleBarRight_do), b.mainSearchInput_do.addChild(b.input_do), b.searchBar_do.addChild(b.inputArrow_do), b.searchBar_do.addChild(b.mainSearchInput_do)
            }, this.inputFocusInHandler = function() {
                b.hasInputFocus_bl || (b.hasInputFocus_bl = !0, FWDMSP.isSearchedFocused_bl = !0, b.isSearchBarDisabled_bl ? b.input_do.screen.value : "Search for track" == b.input_do.screen.value && (b.input_do.screen.value = ""))
            }, this.inputFocusOutHandler = function(e) {
                if (b.hasInputFocus_bl) {
                    FWDMSP.isSearchedFocused_bl = !1;
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                    return FWDMSPUtils.hitTest(b.input_do.screen, t.screenX, t.screenY) ? void 0 : (b.hasInputFocus_bl = !1, void("" == b.input_do.screen.value && (b.input_do.screen.value = "Search for track")))
                }
            }, this.keyUpHandler = function(e) {
                e.stopPropagation && e.stopPropagation(), b.prevInputValue_str != b.input_do.screen.value && (b.isMobile_bl, b.positionList()), b.prevInputValue_str = b.input_do.screen.value, b.scrHandler_do && (b.updateScrollBarSizeActiveAndDeactivate(), b.updateScrollBarHandlerAndContent(!1))
            }, this.showNothingFound = function() {
                b.isShowNothingFound_bl || (b.isShowNothingFound_bl = !0, b.noSearchFound_do.setVisible(!0), b.noSearchFound_do.setY(parseInt((b.stageHeight - b.noSearchFound_do.getHeight() - b.searchBar_do.h) / 2)), b.noSearchFound_do.setAlpha(0), FWDAnimation.to(b.noSearchFound_do, .1, {
                    alpha: 1,
                    yoyo: !0,
                    repeat: 4
                }))
            }, this.hideNothingFound = function() {
                b.isShowNothingFound_bl && (b.isShowNothingFound_bl = !1, FWDAnimation.killTweensOf(b.noSearchFound_do), b.noSearchFound_do.setVisible(!1))
            }, this.setupButtons = function() {
                b.searchBarButtons_ar = [], FWDMSPSimpleButton.setPrototype(), b.sortNButton_do = new FWDMSPSimpleButton(p.sortNN_img, p.sortNSPath_str, null, !0, p.useHEXColorsForSkin_bl, p.normalButtonsColor_str, p.selectedButtonsColor_str), b.searchBarButtons_ar.push(b.sortNButton_do), b.sortNButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, b.sortNButtonOnMouseUpHandler), b.searchBar_do.addChild(b.sortNButton_do), b.sortNButton_do.setX(410), FWDMSPSimpleButton.setPrototype(), b.sortAButton_do = new FWDMSPSimpleButton(p.sortAN_img, p.sortASPath_str, null, !0, p.useHEXColorsForSkin_bl, p.normalButtonsColor_str, p.selectedButtonsColor_str), b.searchBarButtons_ar.push(b.sortAButton_do), b.sortAButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, b.sortAButtonOnMouseUpHandler), b.searchBar_do.addChild(b.sortAButton_do), b.sortAButton_do.setX(450), FWDMSPComplexButton.setPrototype(), b.ascDscButton_do = new FWDMSPComplexButton(p.ascendingN_img, p.ascendingSpath_str, p.decendingN_img, p.decendingSpath_str, !0, p.useHEXColorsForSkin_bl, p.normalButtonsColor_str, p.selectedButtonsColor_str), b.ascDscButton_do.setX(500), b.searchBarButtons_ar.push(b.ascDscButton_do), b.ascDscButton_do.addListener(FWDMSPComplexButton.MOUSE_UP, b.ascDscMouseUpHandler), b.searchBar_do.addChild(b.ascDscButton_do), b.isSortedNumerical_bl ? b.disableSortNButton() : b.disableSortAButton()
            }, this.ascDscMouseUpHandler = function() {
                b.srotAscending_bl ? (b.ascDscButton_do.setButtonState(0), b.srotAscending_bl = !1) : (b.ascDscButton_do.setButtonState(1), b.srotAscending_bl = !0), b.sortList()
            }, this.sortAButtonOnMouseUpHandler = function() {
                b.disableSortAButton(), b.sortList()
            }, this.sortNButtonOnMouseUpHandler = function() {
                b.disableSortNButton(), b.sortList()
            }, this.disableSortAButton = function() {
                b.sortAButton_do.disableForGood(), b.sortAButton_do.setSelectedState(), b.sortNButton_do.enableForGood(), b.sortNButton_do.setNormalState(), b.isSortedNumerical_bl = !1
            }, this.disableSortNButton = function() {
                b.sortNButton_do && (b.sortNButton_do.disableForGood(), b.sortNButton_do.setSelectedState(), b.sortAButton_do.enableForGood(), b.sortAButton_do.setNormalState()), b.isSortedNumerical_bl = !0
            }, this.sortList = function() {
                b.isSortedNumerical_bl ? b.items_ar.sort(function(e, t) {
                    return e.id < t.id ? -1 : e.id > t.id ? 1 : 0
                }) : b.items_ar.sort(function(e, t) {
                    return e.titleText_str < t.titleText_str ? -1 : e.titleText_str > t.titleText_str ? 1 : 0
                }), b.srotAscending_bl || b.items_ar.reverse();
                for (var e = 0; e < b.items_ar.length; e++) b.items_ar[e].sortId = e;
                b.positionList(), b.updateScrollBarHandlerAndContent(!1)
            }, b.positionSearchBar = function() {
                var e, t = 0;
                if (inputWidth = b.stageWidth - 2 * b.startSpaceBetweenButtons - b.inputArrow_do.w - 12, 430 < inputWidth && (inputWidth = 430), b.showSortButtons_bl)
                    for (var o = b.searchBarButtons_ar.length - 1; 0 <= o; o--) e = b.searchBarButtons_ar[o], o == b.searchBarButtons_ar.length - 1 ? e.setX(b.stageWidth - e.w - b.startSpaceBetweenButtons) : e.setX(b.searchBarButtons_ar[o + 1].x - e.w - b.spaceBetweenButtons), e.setY(b.searchSeparator_do.h + parseInt((b.searchBar_do.h - b.searchSeparator_do.h - e.h) / 2)), t += e.w + b.spaceBetweenButtons;
                t += b.startSpaceBetweenButtons, inputWidth -= t, b.mainSearchInput_do.setWidth(inputWidth), b.input_do.setWidth(inputWidth), b.mainSearchInput_do.setX(b.startSpaceBetweenButtons + b.inputSearchOffsetLeft), b.mainSearchInput_do.setY(parseInt(b.searchSeparator_do.h + parseInt((b.searchBar_do.h - b.searchSeparator_do.h - b.mainSearchInput_do.h) / 2))), b.titleBarRight_do.setX(b.mainSearchInput_do.w - b.titleBarRight_do.w), b.inputArrow_do.setX(parseInt(b.mainSearchInput_do.x + inputWidth) + 4), b.inputArrow_do.setY(b.searchSeparator_do.h + parseInt((b.searchBar_do.h - b.searchSeparator_do.h - b.inputArrow_do.h) / 2)), b.searchSeparator_do.setWidth(b.stageWidth), b.searchBar_do.setWidth(b.stageWidth), b.searchBar_do.setY(b.stageHeight - b.searchSeparator_do.h - b.searchBar_do.h)
            }, this.setupDisable = function() {
                b.disable_do = new FWDMSPDisplayObject("div"), FWDMSPUtils.isIE && (b.disable_do.setBkColor("#FFFFFF"), b.disable_do.setAlpha(0)), b.addChild(b.disable_do)
            }, this.showDisable = function() {
                b.disable_do && 0 == b.disable_do.w && (b.scrMainHolder_do ? b.disable_do.setWidth(b.stageWidth - b.scrollbarOffestWidth) : b.disable_do.setWidth(b.stageWidth), b.disable_do.setHeight(b.stageHeight))
            }, this.hideDisable = function() {
                b.disable_do && 0 != b.disable_do.w && (b.disable_do.setWidth(0), b.disable_do.setHeight(0))
            }, this.setupSeparator = function() {
                b.separator_do = new FWDMSPDisplayObject("div"), b.separator_do.setBackfaceVisibility(), b.separator_do.hasTransform3d_bl = !1, b.separator_do.hasTransform2d_bl = !1, b.separator_do.getStyle().background = "url('" + b.playlistSeparator_img.src + "')", b.separator_do.setHeight(b.playlistSeparator_img.height), b.separator_do.setY(-b.separator_do.h)
            }, this.setupScrollbar = function() {
                b.scrMainHolder_do = new FWDMSPDisplayObject("div"), b.scrMainHolder_do.setWidth(b.scrWidth), b.scrTrack_do = new FWDMSPDisplayObject("div"), b.scrTrack_do.setWidth(b.scrWidth), b.scrTrackTop_do = new FWDMSPDisplayObject("img"), b.scrTrackTop_do.setScreen(b.playlistScrBkTop_img), b.scrTrackMiddle_do = new FWDMSPDisplayObject("div"), b.scrTrackMiddle_do.getStyle().background = "url('" + p.scrBkMiddlePath_str + "')", b.scrTrackMiddle_do.setWidth(b.scrWidth), b.scrTrackMiddle_do.setY(b.scrTrackTop_do.h);
                var e = new Image;
                e.src = p.scrBkBottomPath_str, b.scrTrackBottom_do = new FWDMSPDisplayObject("img"), b.scrTrackBottom_do.setScreen(e), b.scrTrackBottom_do.setWidth(b.scrTrackTop_do.w), b.scrTrackBottom_do.setHeight(b.scrTrackTop_do.h), b.scrHandler_do = new FWDMSPDisplayObject("div"), b.scrHandler_do.setWidth(b.scrWidth), b.scrHandlerTop_do = new FWDMSPDisplayObject("img"), b.useHEXColorsForSkin_bl ? (b.scrHandlerTop_do = new FWDMSPDisplayObject("div"), b.scrHandlerTop_do.setWidth(b.playlistScrDragTop_img.width), b.scrHandlerTop_do.setHeight(b.playlistScrDragTop_img.height), b.mainScrubberDragTop_canvas = FWDMSPUtils.getCanvasWithModifiedColor(b.playlistScrDragTop_img, b.normalButtonsColor_str).canvas, b.scrHandlerTop_do.screen.appendChild(b.mainScrubberDragTop_canvas)) : (b.scrHandlerTop_do = new FWDMSPDisplayObject("img"), b.scrHandlerTop_do.setScreen(b.playlistScrDragTop_img)), b.scrHandlerMiddle_do = new FWDMSPDisplayObject("div"), b.middleImage = new Image, b.middleImage.src = p.scrDragMiddlePath_str, b.useHEXColorsForSkin_bl ? b.middleImage.onload = function() {
                    b.scrubberDragMiddle_canvas = FWDMSPUtils.getCanvasWithModifiedColor(b.middleImage, b.normalButtonsColor_str, !0), b.scrubberDragImage_img = b.scrubberDragMiddle_canvas.image, b.scrHandlerMiddle_do.getStyle().background = "url('" + b.scrubberDragImage_img.src + "') repeat-y"
                } : b.scrHandlerMiddle_do.getStyle().background = "url('" + p.scrDragMiddlePath_str + "')", b.scrHandlerMiddle_do.setWidth(b.scrWidth), b.scrHandlerMiddle_do.setY(b.scrHandlerTop_do.h), b.scrHandlerBottom_do = new FWDMSPDisplayObject("div"), b.scrHandlerBottom_img = new Image, b.scrHandlerBottom_img.src = p.scrDragMiddlePath_str, b.useHEXColorsForSkin_bl ? b.scrHandlerBottom_img.onload = function() {
                    b.scrubberDragBottom_canvas = FWDMSPUtils.getCanvasWithModifiedColor(b.scrHandlerBottom_img, b.normalButtonsColor_str, !0), b.scrubberDragBottomImage_img = b.scrubberDragBottom_canvas.image, b.scrHandlerBottom_do.getStyle().background = "url('" + b.scrubberDragBottomImage_img.src + "') repeat-y"
                } : b.scrHandlerBottom_do.getStyle().background = "url('" + p.scrDragBottomPath_str + "')", b.scrHandlerBottom_do.setWidth(b.scrWidth), b.scrHandlerBottom_do.setWidth(b.scrHandlerTop_do.w), b.scrHandlerBottom_do.setHeight(b.scrHandlerTop_do.h), b.scrHandler_do.setButtonMode(!0), b.useHEXColorsForSkin_bl ? (b.scrHandlerLinesN_do = new FWDMSPDisplayObject("div"), b.scrHandlerLinesN_do.setWidth(b.playlistScrLines_img.width), b.scrHandlerLinesN_do.setHeight(b.playlistScrLines_img.height), b.mainhandlerN_canvas = FWDMSPUtils.getCanvasWithModifiedColor(b.playlistScrLines_img, b.selectedButtonsColor_str).canvas, b.scrHandlerLinesN_do.screen.appendChild(b.mainhandlerN_canvas)) : (b.scrHandlerLinesN_do = new FWDMSPDisplayObject("img"), b.scrHandlerLinesN_do.setScreen(b.playlistScrLines_img)), b.scrHandlerLinesS_img = new Image, b.scrHandlerLinesS_img.src = p.scrLinesSPath_str, b.useHEXColorsForSkin_bl ? (b.scrHandlerLinesS_do = new FWDMSPDisplayObject("div"), b.scrHandlerLinesS_img.onload = function() {
                    b.scrHandlerLinesS_do.setWidth(b.scrHandlerLinesN_do.w), b.scrHandlerLinesS_do.setHeight(b.scrHandlerLinesN_do.h), b.scrubberLines_s_canvas = FWDMSPUtils.getCanvasWithModifiedColor(b.scrHandlerLinesS_img, b.selectedButtonsColor_str, !0), b.scrubbelinesSImage_img = b.scrubberLines_s_canvas.image, b.scrHandlerLinesS_do.getStyle().background = "url('" + b.scrubbelinesSImage_img.src + "') repeat-y"
                }) : (b.scrHandlerLinesS_do = new FWDMSPDisplayObject("img"), b.scrHandlerLinesS_do.setScreen(b.scrHandlerLinesS_img), b.scrHandlerLinesS_do.setWidth(b.scrHandlerLinesN_do.w), b.scrHandlerLinesS_do.setHeight(b.scrHandlerLinesN_do.h)), b.scrHandlerLinesS_do.setAlpha(0), b.scrHandlerLines_do = new FWDMSPDisplayObject("div"), b.scrHandlerLines_do.hasTransform3d_bl = !1, b.scrHandlerLines_do.hasTransform2d_bl = !1, b.scrHandlerLines_do.setBackfaceVisibility(), b.scrHandlerLines_do.setWidth(b.scrHandlerLinesN_do.w), b.scrHandlerLines_do.setHeight(b.scrHandlerLinesN_do.h), b.scrHandlerLines_do.setButtonMode(!0), b.scrTrack_do.addChild(b.scrTrackTop_do), b.scrTrack_do.addChild(b.scrTrackMiddle_do), b.scrTrack_do.addChild(b.scrTrackBottom_do), b.scrHandler_do.addChild(b.scrHandlerTop_do), b.scrHandler_do.addChild(b.scrHandlerMiddle_do), b.scrHandler_do.addChild(b.scrHandlerBottom_do), b.scrHandlerLines_do.addChild(b.scrHandlerLinesN_do), b.scrHandlerLines_do.addChild(b.scrHandlerLinesS_do), b.scrMainHolder_do.addChild(b.scrTrack_do), b.scrMainHolder_do.addChild(b.scrHandler_do), b.scrMainHolder_do.addChild(b.scrHandlerLines_do), b.mainHolder_do.addChild(b.scrMainHolder_do), b.scrHandler_do.screen.addEventListener ? (b.scrHandler_do.screen.addEventListener("mouseover", b.scrollBarHandlerOnMouseOver), b.scrHandler_do.screen.addEventListener("mouseout", b.scrollBarHandlerOnMouseOut), b.scrHandler_do.screen.addEventListener("mousedown", b.scrollBarHandlerOnMouseDown), b.scrHandlerLines_do.screen.addEventListener("mouseover", b.scrollBarHandlerOnMouseOver), b.scrHandlerLines_do.screen.addEventListener("mouseout", b.scrollBarHandlerOnMouseOut), b.scrHandlerLines_do.screen.addEventListener("mousedown", b.scrollBarHandlerOnMouseDown)) : b.scrHandler_do.screen.attachEvent && (b.scrHandler_do.screen.attachEvent("onmouseover", b.scrollBarHandlerOnMouseOver), b.scrHandler_do.screen.attachEvent("onmouseout", b.scrollBarHandlerOnMouseOut), b.scrHandler_do.screen.attachEvent("onmousedown", b.scrollBarHandlerOnMouseDown), b.scrHandlerLines_do.screen.attachEvent("onmouseover", b.scrollBarHandlerOnMouseOver), b.scrHandlerLines_do.screen.attachEvent("onmouseout", b.scrollBarHandlerOnMouseOut), b.scrHandlerLines_do.screen.attachEvent("onmousedown", b.scrollBarHandlerOnMouseDown))
            }, this.scrollBarHandlerOnMouseOver = function(e) {
                FWDAnimation.to(b.scrHandlerLinesS_do, .8, {
                    alpha: 1,
                    ease: Expo.easeOut
                })
            }, this.scrollBarHandlerOnMouseOut = function(e) {
                b.isDragging_bl || FWDAnimation.to(b.scrHandlerLinesS_do, .8, {
                    alpha: 0,
                    ease: Expo.easeOut
                })
            }, this.scrollBarHandlerOnMouseDown = function(e) {
                if (b.allowToScrollAndScrollBarIsActive_bl) {
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                    b.isDragging_bl = !0, b.yPositionOnPress = b.scrHandler_do.y, b.lastPresedY = t.screenY, FWDAnimation.killTweensOf(b.scrHandler_do), b.showDisable(), window.addEventListener ? (window.addEventListener("mousemove", b.scrollBarHandlerMoveHandler), window.addEventListener("mouseup", b.scrollBarHandlerEndHandler)) : document.attachEvent && (document.attachEvent("onmousemove", b.scrollBarHandlerMoveHandler), document.attachEvent("onmouseup", b.scrollBarHandlerEndHandler)), b.prevSortId = -1
                }
            }, this.scrollBarHandlerMoveHandler = function(e) {
                e.preventDefault && e.preventDefault();
                var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                b.scrollBarHandlerFinalY = Math.round(b.yPositionOnPress + t.screenY - b.lastPresedY), b.scrollBarHandlerFinalY >= b.scrTrack_do.h - b.scrHandler_do.h - 1 ? b.scrollBarHandlerFinalY = b.scrTrack_do.h - b.scrHandler_do.h - 1 : b.scrollBarHandlerFinalY <= 0 && (b.scrollBarHandlerFinalY = 0), b.scrHandler_do.setY(b.scrollBarHandlerFinalY), FWDAnimation.to(b.scrHandlerLines_do, .8, {
                    y: b.scrollBarHandlerFinalY + parseInt((b.scrHandler_do.h - b.scrHandlerLines_do.h) / 2),
                    ease: Quart.easeOut
                }), b.updateScrollBarHandlerAndContent(!0, !0)
            }, b.scrollBarHandlerEndHandler = function(e) {
                var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                b.isDragging_bl = !1, FWDMSPUtils.hitTest(b.scrHandler_do.screen, t.screenX, t.screenY) || FWDAnimation.to(b.scrHandlerLinesS_do, .8, {
                    alpha: 0,
                    ease: Expo.easeOut
                }), b.scrollBarHandlerFinalY = -1 * parseInt((b.scrTrack_do.h - b.scrHandler_do.h) * (b.playListFinalY / ((b.totalSearchedItems - b.nrOfVisiblePlaylistItems) * b.itemHeight))), b.scrollBarHandlerFinalY.y < 0 ? b.scrollBarHandlerFinalY = 0 : b.scrollBarHandlerFinalY > b.scrTrack_do.h - b.scrHandler_do.h - 1 && (b.scrollBarHandlerFinalY = b.scrTrack_do.h - b.scrHandler_do.h - 1), b.hideDisable(), FWDAnimation.killTweensOf(b.scrHandler_do), FWDAnimation.to(b.scrHandler_do, .5, {
                    y: b.scrollBarHandlerFinalY,
                    ease: Quart.easeOut
                }), window.removeEventListener ? (window.removeEventListener("mousemove", b.scrollBarHandlerMoveHandler), window.removeEventListener("mouseup", b.scrollBarHandlerEndHandler)) : document.detachEvent && (document.detachEvent("onmousemove", b.scrollBarHandlerMoveHandler), document.detachEvent("onmouseup", b.scrollBarHandlerEndHandler))
            }, this.updateScrollBarSizeActiveAndDeactivate = function() {
                if (b.allowToScrollAndScrollBarIsActive_bl) {
                    var e = 0;
                    b.allowToScrollAndScrollBarIsActive_bl = !0, b.searchBar_do && (e = b.searchBar_do.h), b.scrMainHolder_do.setHeight(b.stageHeight - b.separator_do.h - e), b.scrTrack_do.setHeight(b.stageHeight - b.separator_do.h - e), b.scrTrackMiddle_do.setHeight(b.scrTrack_do.h - 2 * b.scrTrackTop_do.h), b.scrTrackBottom_do.setY(b.scrTrackMiddle_do.y + b.scrTrackMiddle_do.h), b.scrHandler_do.setHeight(Math.min(b.stageHeight - b.separator_do.h - e, Math.round((b.stageHeight - b.separator_do.h - e) / b.itemsTotalHeight * b.stageHeight))), b.scrHandlerMiddle_do.setHeight(b.scrHandler_do.h - 2 * b.scrHandlerTop_do.h), b.scrHandlerTop_do.setY(b.scrHandlerMiddle_do.y + b.scrHandlerMiddle_do.h), b.scrHandlerLines_do.setY(b.scrollBarHandlerFinalY + parseInt((b.scrHandler_do.h - b.scrHandlerLines_do.h) / 2)), b.scrMainHolder_do.setX(b.stageWidth - b.scrWidth), b.updateScrollBarHandlerAndContent()
                } else b.allowToScrollAndScrollBarIsActive_bl = !1, b.scrMainHolder_do.setX(-500), b.scrHandler_do.setY(0)
            }, this.updateScrollBarHandlerAndContent = function(e, t) {
                if (b.curItem_do && b.allowToScrollAndScrollBarIsActive_bl && (b.curItem_do && (b.sortId = b.curItem_do.sortId), b.prevSortId != b.sortId || t)) {
                    var o = 0,
                        s = 0;
                    b.addAtThePlaylistEnd_bl ? b.sortId = b.totalPlayListItems - 1 : b.addAtThePlaylistBeggingin_bl && (b.sortId = 0), b.prevSortId = b.sortId, b.isDragging_bl && !b.isMobile_bl ? ("Infinity" == (o = b.scrHandler_do.y / (b.scrMainHolder_do.h - b.scrHandler_do.h)) ? o = 0 : 1 <= o && (scrollPercent = 1), b.playListFinalY = Math.round(o * (b.totalSearchedItems - b.nrOfVisiblePlaylistItems)) * b.itemHeight * -1) : ((s = b.totalSearchedItems != b.totalPlayListItems ? 0 : parseInt(b.sortId / b.nrOfVisiblePlaylistItems) * b.nrOfVisiblePlaylistItems) + b.nrOfVisiblePlaylistItems >= b.totalPlayListItems && (s = b.totalPlayListItems - b.nrOfVisiblePlaylistItems), s < 0 && (s = 0), b.playListFinalY = parseInt(s * b.itemHeight * -1), b.scrMainHolder_do && (b.scrollBarHandlerFinalY = -1 * Math.round((b.scrMainHolder_do.h - b.scrHandler_do.h) * (b.playListFinalY / ((b.totalSearchedItems - b.nrOfVisiblePlaylistItems) * b.itemHeight))), b.scrollBarHandlerFinalY < 0 ? b.scrollBarHandlerFinalY = 0 : b.scrollBarHandlerFinalY > b.scrMainHolder_do.h - b.scrHandler_do.h - 1 && (b.scrollBarHandlerFinalY = b.scrMainHolder_do.h - b.scrHandler_do.h - 1), FWDAnimation.killTweensOf(b.scrHandler_do), FWDAnimation.killTweensOf(b.scrHandlerLines_do), e ? (FWDAnimation.to(b.scrHandler_do, .5, {
                        y: b.scrollBarHandlerFinalY,
                        ease: Quart.easeOut
                    }), FWDAnimation.to(b.scrHandlerLines_do, .8, {
                        y: b.scrollBarHandlerFinalY + parseInt((b.scrHandler_do.h - b.scrHandlerLinesN_do.h) / 2),
                        ease: Quart.easeOut
                    })) : (b.scrHandler_do.setY(b.scrollBarHandlerFinalY), b.scrHandlerLines_do.setY(b.scrollBarHandlerFinalY + parseInt((b.scrHandler_do.h - b.scrHandlerLinesN_do.h) / 2))))), b.prevPlaylistY != b.playListFinalY && (b.prevPlaylistY = b.playListFinalY, isNaN(b.playListFinalY) || (b.lastListY != b.playListFinalY && (FWDAnimation.killTweensOf(b.itemsHolder_do), e ? FWDAnimation.to(b.itemsHolder_do, .5, {
                        y: b.playListFinalY,
                        ease: Quart.easeOut
                    }) : b.itemsHolder_do.setY(b.playListFinalY)), b.lastListY = b.playListFinalY))
                }
            }, this.addMouseWheelSupport = function() {
                window.addEventListener ? (b.screen.addEventListener("mousewheel", b.mouseWheelHandler), b.screen.addEventListener("DOMMouseScroll", b.mouseWheelHandler)) : document.attachEvent && b.screen.attachEvent("onmousewheel", b.mouseWheelHandler)
            }, this.mouseWheelHandler = function(e) {
                if (b.allowToScrollAndScrollBarIsActive_bl && !b.isDragging_bl && (!b.comboBox_do || !b.comboBox_do.isShowed_bl)) {
                    var t = e.detail || e.wheelDelta;
                    if (e.wheelDelta && (t *= -1), FWDMSPUtils.isOpera && (t *= -1), 0 < t ? b.playListFinalY -= b.itemHeight : b.playListFinalY += b.itemHeight, leftId = parseInt(b.playListFinalY / b.itemHeight), 0 <= leftId ? leftId = 0 : Math.abs(leftId) + b.nrOfVisiblePlaylistItems >= b.totalSearchedItems && (leftId = -1 * (b.totalSearchedItems - b.nrOfVisiblePlaylistItems)), b.prevSortId = -1, b.prevPlaylistY = -100, b.playListFinalY = leftId * b.itemHeight, b.lastListY != b.playListFinalY) {
                        if (b.scrollBarHandlerFinalY = -1 * Math.round((b.scrMainHolder_do.h - b.scrHandler_do.h) * (b.playListFinalY / ((b.totalSearchedItems - b.nrOfVisiblePlaylistItems) * b.itemHeight))), b.scrollBarHandlerFinalY < 0 ? b.scrollBarHandlerFinalY = 0 : b.scrollBarHandlerFinalY > b.scrMainHolder_do.h - b.scrHandler_do.h - 1 && (b.scrollBarHandlerFinalY = b.scrMainHolder_do.h - b.scrHandler_do.h - 1), FWDAnimation.killTweensOf(b.itemsHolder_do), FWDAnimation.to(b.itemsHolder_do, .5, {
                                y: b.playListFinalY,
                                ease: Expo.easeOut
                            }), FWDAnimation.killTweensOf(b.scrHandler_do), FWDAnimation.to(b.scrHandler_do, .5, {
                                y: b.scrollBarHandlerFinalY,
                                ease: Expo.easeOut
                            }), FWDAnimation.to(b.scrHandlerLines_do, .8, {
                                y: b.scrollBarHandlerFinalY + parseInt((b.scrHandler_do.h - b.scrHandlerLinesN_do.h) / 2),
                                ease: Quart.easeOut
                            }), b.lastListY = b.playListFinalY, !e.preventDefault) return !1;
                        e.preventDefault()
                    }
                }
            }, b.setupMobileScrollbar = function() {
                b.hasPointerEvent_bl ? b.screen.addEventListener("pointerdown", b.scrollBarTouchStartHandler) : b.screen.addEventListener("touchstart", b.scrollBarTouchStartHandler), b.updateMobileScrollBarId_int = setInterval(b.updateMobileScrollBar, 16)
            }, b.scrollBarTouchStartHandler = function(e) {
                if (!(b.stageHeight > b.itemsTotalHeight || b.comboBox_do && b.comboBox_do.isShowed_bl)) {
                    e.preventDefault && e.preventDefault(), FWDAnimation.killTweensOf(b.itemsHolder_do);
                    var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                    b.isDragging_bl = !0, b.isScrollingOnMove_bl = !1, b.lastPresedY = t.screenY, b.checkLastPresedY = t.screenY, b.hasPointerEvent_bl ? (window.addEventListener("pointerup", b.scrollBarTouchEndHandler), window.addEventListener("pointermove", b.scrollBarTouchMoveHandler)) : (window.addEventListener("touchend", b.scrollBarTouchEndHandler), window.addEventListener("touchmove", b.scrollBarTouchMoveHandler)), clearInterval(b.updateMoveMobileScrollbarId_int), b.updateMoveMobileScrollbarId_int = setInterval(b.updateMoveMobileScrollbar, 20)
                }
            }, b.scrollBarTouchMoveHandler = function(e) {
                e.preventDefault && e.preventDefault(), b.showDisable();
                var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                (t.screenY >= b.checkLastPresedY + 6 || t.screenY <= b.checkLastPresedY - 6) && (b.isScrollingOnMove_bl = !0);
                var o = t.screenY - b.lastPresedY;
                b.playListFinalY += o, b.playListFinalY = Math.round(b.playListFinalY), b.lastPresedY = t.screenY, b.vy = 2 * o
            }, b.scrollBarTouchEndHandler = function(e) {
                b.isDragging_bl = !1, clearInterval(b.updateMoveMobileScrollbarId_int), clearTimeout(b.disableOnMoveId_to), b.disableOnMoveId_to = setTimeout(function() {
                    b.hideDisable()
                }, 50), b.hasPointerEvent_bl ? (window.removeEventListener("pointerup", b.scrollBarTouchEndHandler), window.removeEventListener("pointermove", b.scrollBarTouchMoveHandler)) : (window.removeEventListener("touchend", b.scrollBarTouchEndHandler), window.removeEventListener("touchmove", b.scrollBarTouchMoveHandler))
            }, b.updateMoveMobileScrollbar = function() {
                b.itemsHolder_do.setY(b.playListFinalY)
            }, b.updateMobileScrollBar = function(e) {
                b.isDragging_bl || FWDAnimation.isTweening(b.itemsHolder_do) || (b.vy *= b.friction, b.playListFinalY += b.vy, 0 < b.playListFinalY ? (b.vy2 = .3 * (0 - b.playListFinalY), b.vy *= b.friction, b.playListFinalY += b.vy2) : b.playListFinalY < b.stageHeight - b.separator_do.h - b.itemsTotalHeight - b.searchBar_do.h && (b.vy2 = .3 * (b.stageHeight - b.separator_do.h - b.itemsTotalHeight - b.searchBar_do.h - b.playListFinalY), b.vy *= b.friction, b.playListFinalY += b.vy2), b.stageHeight > b.itemsTotalHeight && (b.playListFinalY = 0), b.itemsHolder_do.setY(Math.round(b.playListFinalY)))
            }, this.hide = function() {
                b.isShowed_bl = !1
            }, this.show = function(e) {
                e && (b.isShowed_bl = !0), b.setX(0)
            }, b.updateHEXColors = function(e, t) {
                b.normalColor_str = e, b.selectedColor_str = t, b.sortNButton_do && b.sortNButton_do.updateHEXColors(e, t), b.sortAButton_do && b.sortAButton_do.updateHEXColors(e, t), b.ascDscButton_do && b.ascDscButton_do.updateHEXColors(e, t), FWDMSPUtils.changeCanvasHEXColor(b.inputArrow_img, b.mainScrubberDragLeft_canvas, e);
                for (var o = 0; o < b.items_ar.length; o++) b.items_ar[o].updateHEXColors(e, t)
            }, this.init()
        };
        n.setPrototype = function() {
            n.prototype = new FWDMSPDisplayObject("div")
        }, n.CHANGE_PLAYLIST = "changePlaylist", n.PLAY = "play", n.PAUSE = "pause", n.UPDATE_TRACK_TITLE_if_FOLDER = "update_trak_title", n.prototype = null, window.FWDMSPPlaylist = n
    }(),
    function() {
        var k = function(e, t, o, s, i, n, l, r, a, d, u, c, h, _, f, p, m, b, g, S, y, v, P, T, w, D, B, M, F, W, H, C, E) {
            var O = this;
            k.prototype;
            this.playlistItemGrad1_img = l, this.playlistItemGrad2_img = r, this.playlistItemProgress_img = a, this.playlistItemProgress2_img = d, this.playlistPlayButtonN_img = u, this.playlistDownloadButtonN_img = o, this.playlistDownloadButtonS_str = s, this.playlistBuyButtonN_img = i, this.playlistBuyButtonS_str = n, this.progress_do = null, this.playPause_do = null, this.playN_do = null, this.playS_do = null, this.pauseN_do = null, this.pauseS_do = null, this.titleText_do = null, this.grad_do = null, this.durationText_do = null, this.dumy_do = null, this.title_str = e, this.titleText_str = t, O.useHEXColorsForSkin_bl = W, O.normalButtonsColor_str = H, O.selectedButtonsColor_str = C, this.playlistItemBk1Path_str = c, this.playlistItemBk2Path_str = h, this.playlistPlayButtonN_str = _, this.playlistPlayButtonS_str = f, this.playlistPauseButtonN_str = p, this.playlistPauseButtonS_str = m, this.titleNormalColor_str = b, this.trackTitleSelected_str = g, this.durationColor_str = S, this.itemHeight = O.playlistItemGrad1_img.height, this.id = y, this.sortId = y, this.playPauseButtonOffsetLeftAndRight = v, this.trackTitleOffsetLeft = P, this.duration = F, this.durationOffsetRight = T, this.textHeight, this.durationWidth = 0, this.titleWidth = 0, this.playPauseButtonWidth = O.playlistPlayButtonN_img.width, this.playPauseButtonHeight = O.playlistPlayButtonN_img.height, this.progressPercent = 0, this.stageWidth = 0, this.downloadButtonOffsetRight = w, this.type = -1, this.setTextsSizeId_to, this.showDownloadButton_bl = B, this.showBuyButton_bl = M, this.showPlayPauseButton_bl = D, this.showDuration_bl = F, this.isActive_bl = !1, this.isSelected_bl = !1, this.isMobile_bl = FWDMSPUtils.isMobile, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, O.init = function() {
                O.setupProgress(), O.setupTitle(), O.showPlayPauseButton_bl && O.setupPlayPauseButton(), O.setupGrad(), O.showDuration_bl && O.setupDuration(), O.setNormalState(!1, !0), O.setupDumy(), O.showDownloadButton_bl && O.setupDownloadButton(), O.showBuyButton_bl && O.setupBuyButton(), O.id % 2 == 0 ? (O.getStyle().background = "url('" + O.playlistItemBk1Path_str + "')", O.grad_do.getStyle().background = "url('" + O.playlistItemGrad1_img.src + "')", O.progress_do.getStyle().background = "url('" + O.playlistItemProgress_img.src + "')", O.type = 1) : (O.getStyle().background = "url('" + O.playlistItemBk2Path_str + "')", O.grad_do.getStyle().background = "url('" + O.playlistItemGrad2_img.src + "')", O.progress_do.getStyle().background = "url('" + O.playlistItemProgress2_img.src + "')", O.type = 2), O.isMobile_bl ? O.hasPointerEvent_bl ? (O.dumy_do.screen.addEventListener("pointerup", O.onMouseUp), O.dumy_do.screen.addEventListener("pointerover", O.onMouseOver), O.dumy_do.screen.addEventListener("pointerout", O.onMouseOut)) : O.dumy_do.screen.addEventListener("touchend", O.onMouseUp) : O.dumy_do.screen.addEventListener ? (O.dumy_do.screen.addEventListener("mouseover", O.onMouseOver), O.dumy_do.screen.addEventListener("mouseout", O.onMouseOut), O.dumy_do.screen.addEventListener("mouseup", O.onMouseUp)) : O.screen.attachEvent && (O.dumy_do.screen.attachEvent("onmouseover", O.onMouseOver), O.dumy_do.screen.attachEvent("onmouseout", O.onMouseOut), O.dumy_do.screen.attachEvent("onmouseup", O.onMouseUp))
            }, O.onMouseOver = function(e, t) {
                O.isActive_bl || e.pointerType && "mouse" != e.pointerType || O.setSelectedState(!0)
            }, O.onMouseOut = function(e) {
                O.isActive_bl || e.pointerType && "mouse" != e.pointerType || O.setNormalState(!0)
            }, O.onMouseUp = function(e) {
                E.isScrollingOnMove_bl || 2 == e.button || (e.preventDefault && e.preventDefault(), O.dispatchEvent(k.MOUSE_UP, {
                    id: O.id
                }))
            }, O.changeSource = function(e) {
                0 == e ? 1 != O.type && (O.grad_do.getStyle().background = "url('" + O.playlistItemGrad1_img.src + "')", O.getStyle().background = "url('" + O.playlistItemBk1Path_str + "')", O.progress_do.getStyle().background = "url('" + O.playlistItemProgress_img.src + "')", O.type = 1) : 2 != O.type && (O.grad_do.getStyle().background = "url('" + O.playlistItemGrad2_img.src + "')", O.getStyle().background = "url('" + O.playlistItemBk2Path_str + "')", O.progress_do.getStyle().background = "url('" + O.playlistItemProgress2_img.src + "')", O.type = 2)
            }, O.resize = function(e, t) {
                if ((!FWDMSPUtils.isIEAndLessThen9 || O.textHeight) && null != O) {
                    O.stageWidth = e;
                    var o = 0,
                        s = parseInt((t - O.textHeight) / 2) + 1;
                    O.playPause_do ? (O.titleText_do.setX(2 * O.playPauseButtonOffsetLeftAndRight + O.playPause_do.w + O.trackTitleOffsetLeft - 2), O.playPause_do.setY(parseInt((t - O.playPause_do.h) / 2))) : O.titleText_do.setX(O.trackTitleOffsetLeft), O.titleText_do.setY(s), O.buyButton_do && O.downloadButton_do ? (o = O.durationText_do ? (O.durationText_do.setX(e - O.durationWidth - O.durationOffsetRight + 1), O.durationText_do.setY(s), O.durationText_do.x) : e, O.downloadButton_do.setX(o - O.downloadButton_do.w - O.downloadButtonOffsetRight + 3), O.downloadButton_do.setY(parseInt((t - O.downloadButton_do.h) / 2)), O.buyButton_do.setX(O.downloadButton_do.x - O.buyButton_do.w - 4), O.buyButton_do.setY(parseInt((t - O.buyButton_do.h) / 2)), O.titleText_do.x + O.titleWidth + O.downloadButton_do.w + O.buyButton_do.w + O.downloadButtonOffsetRight + 4 > o ? O.grad_do.setX(O.buyButton_do.x - O.downloadButtonOffsetRight + 2) : O.grad_do.setX(-300)) : O.downloadButton_do ? (o = O.durationText_do ? (O.durationText_do.setX(e - O.durationWidth - O.durationOffsetRight + 1), O.durationText_do.setY(s), O.durationText_do.x) : e, O.downloadButton_do.setX(o - O.downloadButton_do.w - O.downloadButtonOffsetRight + 3), O.downloadButton_do.setY(parseInt((t - O.downloadButton_do.h) / 2)), O.titleText_do.x + O.titleWidth + O.downloadButton_do.w + O.downloadButtonOffsetRight > o ? O.grad_do.setX(O.downloadButton_do.x - O.downloadButtonOffsetRight + 2) : O.grad_do.setX(-300)) : O.buyButton_do ? (o = O.durationText_do ? (O.durationText_do.setX(e - O.durationWidth - O.durationOffsetRight + 1), O.durationText_do.setY(s), O.durationText_do.x) : e, O.buyButton_do.setX(o - O.buyButton_do.w - O.downloadButtonOffsetRight + 3), O.buyButton_do.setY(parseInt((t - O.buyButton_do.h) / 2)), O.titleText_do.x + O.titleWidth + O.buyButton_do.w + O.downloadButtonOffsetRight > o ? O.grad_do.setX(O.buyButton_do.x - O.downloadButtonOffsetRight + 2) : O.grad_do.setX(-300)) : O.durationText_do ? (O.durationText_do.setX(e - O.durationWidth - O.durationOffsetRight + 1), O.durationText_do.setY(s), O.titleText_do.x + O.titleWidth > O.durationText_do.x ? O.grad_do.setX(O.durationText_do.x - O.durationOffsetRight + 2) : O.grad_do.setX(-300)) : O.downloadButton_do ? (O.downloadButton_do.setX(e - O.downloadButton_do.w - O.downloadButtonOffsetRight + 2), O.titleText_do.x + O.titleWidth > O.downloadButton_do.x ? O.grad_do.setX(O.downloadButton_do.x - O.downloadButtonOffsetRight + 2) : O.grad_do.setX(-300), O.downloadButton_do.setY(parseInt((t - O.downloadButton_do.h) / 2))) : O.titleText_do.x + O.titleWidth > e - 10 ? O.grad_do.setX(e - 15) : O.grad_do.setX(-300), O.dumy_do.setWidth(e), O.dumy_do.setHeight(t), O.setWidth(e), O.setHeight(t)
                }
            }, this.setupDownloadButton = function() {
                FWDMSPSimpleSizeButton.setPrototype(), O.downloadButton_do = new FWDMSPSimpleSizeButton(O.playlistDownloadButtonS_str, O.playlistDownloadButtonN_img.src, O.playlistDownloadButtonN_img.width, O.playlistDownloadButtonN_img.height, O.useHEXColorsForSkin_bl, O.normalButtonsColor_str, O.selectedButtonsColor_str), O.downloadButton_do.getStyle().position = "absolute", O.downloadButton_do.addListener(FWDMSPSimpleSizeButton.CLICK, O.dwButtonClickHandler), O.addChild(O.downloadButton_do)
            }, this.dwButtonClickHandler = function() {
                O.dispatchEvent(k.DOWNLOAD, {
                    id: O.id
                })
            }, this.setupBuyButton = function() {
                FWDMSPSimpleSizeButton.setPrototype(), O.buyButton_do = new FWDMSPSimpleSizeButton(O.playlistBuyButtonS_str, O.playlistBuyButtonN_img.src, O.playlistBuyButtonN_img.width, O.playlistBuyButtonN_img.height, O.useHEXColorsForSkin_bl, O.normalButtonsColor_str, O.selectedButtonsColor_str), O.buyButton_do.getStyle().position = "absolute", O.buyButton_do.addListener(FWDMSPSimpleSizeButton.CLICK, O.buyButtonClickHandler), O.addChild(O.buyButton_do)
            }, this.buyButtonClickHandler = function() {
                O.dispatchEvent(k.BUY, {
                    id: O.id
                })
            }, this.setupProgress = function() {
                O.progress_do = new FWDMSPDisplayObject("div"), O.progress_do.setBackfaceVisibility(), O.progress_do.setHeight(a.height), O.addChild(O.progress_do)
            }, this.updateProgressPercent = function(e) {
                null != O && O.progressPercent != e && (O.progressPercent = e, O.progress_do.setWidth(parseInt(O.stageWidth * e)))
            }, this.setupPlayPauseButton = function() {
                O.playPause_do = new FWDMSPDisplayObject("div"), O.playPause_do.setWidth(O.playPauseButtonWidth), O.playPause_do.setHeight(O.playPauseButtonHeight), O.playN_do = new FWDMSPDisplayObject("div"), O.useHEXColorsForSkin_bl ? (O.playNImage_img = new Image, O.playNImage_img.src = O.playlistPlayButtonN_str, O.playNImage_img.onload = function() {
                    var e = FWDMSPUtils.getCanvasWithModifiedColor(O.playNImage_img, O.normalButtonsColor_str, !0);
                    O.playNImageCanvas = e.canvas, O.playNImageBackground = e.image, O.playN_do.getStyle().background = "url('" + O.playNImageBackground.src + "')"
                }) : O.playN_do.getStyle().background = "url('" + O.playlistPlayButtonN_str + "') no-repeat", O.playN_do.setWidth(O.playPauseButtonWidth), O.playN_do.setHeight(O.playPauseButtonHeight), O.playS_do = new FWDMSPDisplayObject("div"), O.useHEXColorsForSkin_bl ? (O.playSImage_img = new Image, O.playSImage_img.src = O.playlistPlayButtonS_str, O.playSImage_img.onload = function() {
                    var e = FWDMSPUtils.getCanvasWithModifiedColor(O.playSImage_img, O.selectedButtonsColor_str, !0);
                    O.playSImageCanvas = e.canvas, O.playSImageBackground = e.image, O.playS_do.getStyle().background = "url('" + O.playSImageBackground.src + "')"
                }) : O.playS_do.getStyle().background = "url('" + O.playlistPlayButtonS_str + "') no-repeat", O.playS_do.setWidth(O.playPauseButtonWidth), O.playS_do.setHeight(O.playPauseButtonHeight), O.playS_do.setAlpha(0), O.pauseN_do = new FWDMSPDisplayObject("div"), O.useHEXColorsForSkin_bl ? (O.pauseNImage_img = new Image, O.pauseNImage_img.src = O.playlistPauseButtonN_str, O.pauseNImage_img.onload = function() {
                    var e = FWDMSPUtils.getCanvasWithModifiedColor(O.pauseNImage_img, O.normalButtonsColor_str, !0);
                    O.pauseNImageCanvas = e.canvas, O.pauseNImageBackground = e.image, O.pauseN_do.getStyle().background = "url('" + O.pauseNImageBackground.src + "')"
                }) : O.pauseN_do.getStyle().background = "url('" + O.playlistPauseButtonN_str + "') no-repeat", O.pauseN_do.setWidth(O.playPauseButtonWidth), O.pauseN_do.setHeight(O.playPauseButtonHeight), O.pauseS_do = new FWDMSPDisplayObject("div"), O.useHEXColorsForSkin_bl ? (O.pauseSImage_img = new Image, O.pauseSImage_img.src = O.playlistPauseButtonS_str, O.pauseSImage_img.onload = function() {
                    var e = FWDMSPUtils.getCanvasWithModifiedColor(O.pauseSImage_img, O.selectedButtonsColor_str, !0);
                    O.pauseSImageCanvas = e.canvas, O.pauseSImageBackground = e.image, O.pauseS_do.getStyle().background = "url('" + O.pauseSImageBackground.src + "')"
                }) : O.pauseS_do.getStyle().background = "url('" + O.playlistPauseButtonS_str + "') no-repeat", O.pauseS_do.setWidth(O.playPauseButtonWidth), O.pauseS_do.setHeight(O.playPauseButtonHeight), O.pauseN_do.setX(-300), O.pauseS_do.setX(-300), O.pauseS_do.setAlpha(0), O.playPause_do.setX(O.playPauseButtonOffsetLeftAndRight), O.playPause_do.addChild(O.playN_do), O.playPause_do.addChild(O.playS_do), O.playPause_do.addChild(O.pauseN_do), O.playPause_do.addChild(O.pauseS_do), O.addChild(O.playPause_do)
            }, this.setupTitle = function() {
                O.titleText_do = new FWDMSPDisplayObject("div"), FWDMSPUtils.isApple && (O.titleText_do.hasTransform3d_bl = !1, O.titleText_do.hasTransform2d_bl = !1), O.titleText_do.setOverflow("visible"), O.titleText_do.setBackfaceVisibility(), O.titleText_do.getStyle().fontFamily = "Arial", O.titleText_do.getStyle().fontSize = "12px", O.titleText_do.getStyle().whiteSpace = "nowrap", O.titleText_do.getStyle().textAlign = "left", O.titleText_do.getStyle().fontSmoothing = "antialiased", O.titleText_do.getStyle().webkitFontSmoothing = "antialiased", O.titleText_do.getStyle().textRendering = "optimizeLegibility", O.titleText_do.setInnerHTML(O.title_str), O.addChild(O.titleText_do)
            }, this.updateTitle = function() {
                null != O && O.titleText_do.setInnerHTML(O.title_str)
            }, this.setTextSizes = function(e) {
                null != O && (O.textHeight && !e || (O.titleWidth = O.titleText_do.screen.offsetWidth, O.textHeight = O.titleText_do.screen.offsetHeight, O.durationText_do && (O.durationWidth = O.durationText_do.screen.offsetWidth), O.grad_do.setWidth(150)))
            }, this.setupGrad = function() {
                O.grad_do = new FWDMSPDisplayObject("div"), O.grad_do.setOverflow("visible"), FWDMSPUtils.isApple && (O.grad_do.hasTransform3d_bl = !1, O.grad_do.hasTransform2d_bl = !1), O.grad_do.setBackfaceVisibility(), O.grad_do.setHeight(O.itemHeight), O.addChild(O.grad_do)
            }, this.setupDuration = function() {
                O.durationText_do = new FWDMSPDisplayObject("div"), FWDMSPUtils.isApple && (O.durationText_do.hasTransform3d_bl = !1, O.durationText_do.hasTransform2d_bl = !1), O.durationText_do.setOverflow("visible"), O.durationText_do.setBackfaceVisibility(), O.durationText_do.getStyle().fontFamily = "Arial", O.durationText_do.getStyle().fontSize = "12px", O.durationText_do.getStyle().whiteSpace = "nowrap", O.durationText_do.getStyle().textAlign = "left", O.durationText_do.getStyle().color = O.titleColor_str, O.durationText_do.getStyle().fontSmoothing = "antialiased", O.durationText_do.getStyle().webkitFontSmoothing = "antialiased", O.durationText_do.getStyle().textRendering = "optimizeLegibility", O.durationText_do.getStyle().color = O.durationColor_str, O.durationText_do.setInnerHTML(O.duration), O.addChild(O.durationText_do)
            }, this.setupDumy = function() {
                O.dumy_do = new FWDMSPDisplayObject("div"), O.dumy_do.setButtonMode(!0), FWDMSPUtils.isIE && (O.dumy_do.setBkColor("#FFFFFF"), O.dumy_do.setAlpha(.001)), O.addChild(O.dumy_do)
            }, this.setNormalState = function(e, t) {
                (O.isSelected_bl || t) && (O.isSelected_bl = !1, e ? (FWDAnimation.to(O.titleText_do.screen, .8, {
                    css: {
                        color: O.titleNormalColor_str
                    },
                    ease: Expo.easeOut
                }), O.durationText_do && FWDAnimation.to(O.durationText_do.screen, .8, {
                    css: {
                        color: O.durationColor_str
                    },
                    ease: Expo.easeOut
                }), O.playPause_do && (FWDAnimation.to(O.pauseS_do, .8, {
                    alpha: 0,
                    ease: Expo.easeOut
                }), FWDAnimation.to(O.playS_do, .8, {
                    alpha: 0,
                    ease: Expo.easeOut
                }))) : (FWDAnimation.killTweensOf(O.titleText_do), O.titleText_do.getStyle().color = O.titleNormalColor_str, O.durationText_do && (O.durationText_do.getStyle().color = O.durationColor_str), O.playPause_do && (FWDAnimation.killTweensOf(O.pauseS_do), FWDAnimation.killTweensOf(O.playS_do), O.pauseS_do.setAlpha(0), O.playS_do.setAlpha(0))))
            }, this.setSelectedState = function(e) {
                O.isSelected_bl || (O.isSelected_bl = !0, e ? (FWDAnimation.to(O.titleText_do.screen, .8, {
                    css: {
                        color: O.trackTitleSelected_str
                    },
                    ease: Expo.easeOut
                }), O.durationText_do && FWDAnimation.to(O.durationText_do.screen, .8, {
                    css: {
                        color: O.trackTitleSelected_str
                    },
                    ease: Expo.easeOut
                }), O.playPause_do && (FWDAnimation.to(O.pauseS_do, .8, {
                    alpha: 1,
                    ease: Expo.easeOut
                }), FWDAnimation.to(O.playS_do, .8, {
                    alpha: 1,
                    ease: Expo.easeOut
                }))) : (FWDAnimation.killTweensOf(O.titleText_do), O.durationText_do && (O.durationText_do.getStyle().color = O.trackTitleSelected_str), O.titleText_do.getStyle().color = O.trackTitleSelected_str, O.playPause_do && (FWDAnimation.killTweensOf(O.pauseS_do), FWDAnimation.killTweensOf(O.playS_do), O.pauseS_do.setAlpha(1), O.playS_do.setAlpha(1))))
            }, this.setActive = function() {
                O.isActive_bl || (O.isActive_bl = !0, O.setSelectedState(!0))
            }, this.setInActive = function() {
                O.isActive_bl && (O.isActive_bl = !1, O.setNormalState(!0), O.updateProgressPercent(0), O.showPlayButton())
            }, this.showPlayButton = function() {
                null != O && O.playN_do && (O.playN_do.setX(0), O.playS_do.setX(0), O.pauseN_do.setX(-300), O.pauseS_do.setX(-300))
            }, this.showPauseButton = function() {
                O.playN_do && (O.playN_do.setX(-300), O.playS_do.setX(-300), O.pauseN_do.setX(0), O.pauseS_do.setX(0))
            }, this.destroy = function() {
                this.playlistItemGrad1_img = null, this.playlistItemProgress_img = null, this.playlistPlayButtonN_img = null, this.playlistDownloadButtonN_img = null, this.playlistDownloadButtonS_str = null, this.playlistBuyButtonN_img = null, this.playlistBuyButtonS_str = null, this.progress_do = null, this.playPause_do = null, this.playN_do = null, this.playS_do = null, this.pauseN_do = null, this.pauseS_do = null, this.titleText_do = null, this.grad_do = null, this.durationText_do = null, this.dumy_do = null, this.title_str = null, this.playlistItemBk1Path_str = null, this.playlistItemBk2Path_str = null, this.playlistPlayButtonN_str = null, this.playlistPlayButtonS_str = null, this.playlistPauseButtonN_str = null, this.playlistPauseButtonS_str = null, this.titleNormalColor_str = null, this.trackTitleSelected_str = null, this.durationColor_str = S, O.setInnerHTML(""), O = null, k.prototype = null
            }, O.updateHEXColors = function(e, t) {
                if (O.normalColor_str = e, O.selectedColor_str = t, O.buyButton_do && O.buyButton_do.updateHEXColors(e, t), O.downloadButton_do && O.downloadButton_do.updateHEXColors(e, t), O.playNImage_img) {
                    var o = FWDMSPUtils.changeCanvasHEXColor(O.playNImage_img, O.playNImageCanvas, e, !0),
                        s = FWDMSPUtils.changeCanvasHEXColor(O.playSImage_img, O.playSImageCanvas, t, !0);
                    O.playN_do.getStyle().background = "url('" + o.src + "')", O.playS_do.getStyle().background = "url('" + s.src + "')";
                    var i = FWDMSPUtils.changeCanvasHEXColor(O.pauseNImage_img, O.pauseNImageCanvas, e, !0),
                        n = FWDMSPUtils.changeCanvasHEXColor(O.pauseSImage_img, O.pauseSImageCanvas, t, !0);
                    O.pauseN_do.getStyle().background = "url('" + i.src + "')", O.pauseS_do.getStyle().background = "url('" + n.src + "')"
                }
            }, this.init()
        };
        k.setPrototype = function() {
            k.prototype = new FWDMSPDisplayObject("div")
        }, k.PLAY = "play", k.PAUSE = "pause", k.MOUSE_UP = "mouseUp", k.DOWNLOAD = "download", k.BUY = "buy", k.prototype = null, window.FWDMSPPlaylistItem = k
    }(),
    function(e) {
        var r = function(e, t, o, s, i, n) {
            var l = this;
            r.prototype;
            this.imageSource_img = null, this.image_sdo = null, this.imageSourcePath_str = e, this.segmentWidth = t, this.segmentHeight = o, this.totalSegments = s, this.totalWidth = t * s, this.animDelay = i || 300, this.count = 0, this.delayTimerId_int, this.isShowed_bl = !1, this.skipFirstFrame_bl = n, this.init = function() {
                l.setWidth(l.segmentWidth), l.setHeight(l.segmentHeight), l.imageSource_img = new Image, l.imageSource_img.src = l.imageSourcePath_str, l.image_sdo = new FWDMSPDisplayObject("img"), l.image_sdo.setScreen(l.imageSource_img), l.image_sdo.setWidth(l.totalWidth), l.image_sdo.setHeight(l.segmentHeight), l.addChild(this.image_sdo), l.hide(!1)
            }, this.start = function() {
                null != l && (clearInterval(l.delayTimerId_int), l.delayTimerId_int = setInterval(l.updatePreloader, l.animDelay))
            }, this.stop = function() {
                clearInterval(l.delayTimerId_int), l.image_sdo.setX(0)
            }, this.updatePreloader = function() {
                if (null != l) {
                    l.count++, l.count > l.totalSegments - 1 && (l.skipFirstFrame_bl ? l.count = 1 : l.count = 0);
                    var e = l.count * l.segmentWidth;
                    l.image_sdo.setX(-e)
                }
            }, this.show = function() {
                this.setVisible(!0), this.start(), FWDAnimation.killTweensOf(this), FWDAnimation.to(this, 1, {
                    alpha: 1
                }), this.isShowed_bl = !0
            }, this.hide = function(e) {
                this.isShowed_bl && (FWDAnimation.killTweensOf(this), e ? FWDAnimation.to(this, 1, {
                    alpha: 0,
                    onComplete: this.onHideComplete
                }) : (this.setVisible(!1), this.setAlpha(0)), this.isShowed_bl = !1)
            }, this.onHideComplete = function() {
                l.stop(), l.setVisible(!1), l.dispatchEvent(r.HIDE_COMPLETE)
            }, this.setForFixedPosition = function() {
                l.setBackfaceVisibility(), l.hasTransform3d_bl = !1, l.hasTransform2d_bl = !1, l.image_sdo.setBackfaceVisibility(), l.image_sdo.hasTransform3d_bl = !1, l.image_sdo.hasTransform2d_bl = !1
            }, this.init()
        };
        r.setPrototype = function() {
            r.prototype = new FWDMSPDisplayObject("div")
        }, r.HIDE_COMPLETE = "hideComplete", r.prototype = null, e.FWDMSPPreloader = r
    }(window),
    function(e) {
        var l = function(e, t, o, s, i) {
            var n = this;
            l.prototype;
            this.buttonRef_do = e, this.bkColor = t, this.text_do = null, this.pointer_do = null, this.fontColor_str = o, this.pointerWidth = 7, this.pointerHeight = 4, this.showWithDelayId_to, this.isMobile_bl = FWDMSPUtils.isMobile, this.isShowed_bl = !0, this.init = function() {
                n.setOverflow("visible"), n.setupMainContainers(), n.setLabel(s), n.hide(), n.setVisible(!1), n.getStyle().backgroundColor = n.bkColor, n.getStyle().zIndex = 9999999999999, n.getStyle().pointerEvents = "none"
            }, this.setupMainContainers = function() {
                n.pointerHolder_do = new FWDMSPDisplayObject("div"), n.pointerHolder_do.setOverflow("visible"), n.addChild(n.pointerHolder_do), n.text_do = new FWDMSPDisplayObject("div"), n.text_do.hasTransform3d_bl = !1, n.text_do.hasTransform2d_bl = !1, n.text_do.setBackfaceVisibility(), n.text_do.setDisplay("inline-block"), n.text_do.getStyle().fontFamily = "Arial", n.text_do.getStyle().fontSize = "12px", n.text_do.getStyle().color = n.fontColor_str, n.text_do.getStyle().whiteSpace = "nowrap", n.text_do.getStyle().fontSmoothing = "antialiased", n.text_do.getStyle().webkitFontSmoothing = "antialiased", n.text_do.getStyle().textRendering = "optimizeLegibility", n.text_do.getStyle().padding = "6px", n.text_do.getStyle().paddingTop = "4px", n.text_do.getStyle().paddingBottom = "4px", n.addChild(n.text_do), n.pointer_do = new FWDMSPDisplayObject("div"), n.pointer_do.setBkColor(n.bkColor), n.pointer_do.screen.style = "border: 4px solid transparent; border-top-color: " + n.bkColor + ";", n.pointerHolder_do.addChild(n.pointer_do)
            }, this.setLabel = function(e) {
                void 0 !== e && (n.text_do.setInnerHTML(e), setTimeout(function() {
                    null != n && (n.setWidth(n.text_do.getWidth()), n.setHeight(n.text_do.getHeight()), n.positionPointer())
                }, 20))
            }, this.positionPointer = function(e) {
                var t, o;
                e = e || 0, t = parseInt((n.w - 8) / 2) + e, o = n.h, n.pointerHolder_do.setX(t), n.pointerHolder_do.setY(o)
            }, this.show = function() {
                n.isShowed_bl = !0, clearTimeout(n.hideWithDelayId_to), FWDAnimation.killTweensOf(n), clearTimeout(n.showWithDelayId_to), n.showWithDelayId_to = setTimeout(n.showFinal)
            }, this.showFinal = function() {
                n.setVisible(!0), FWDAnimation.to(n, .4, {
                    alpha: 1,
                    onComplete: function() {
                        n.setVisible(!0)
                    },
                    ease: Quart.easeOut
                })
            }, this.hide = function() {
                n.isShowed_bl && (clearTimeout(n.showWithDelayId_to), clearTimeout(n.hideWithDelayId_to), n.hideWithDelayId_to = setTimeout(function() {
                    FWDAnimation.killTweensOf(n), n.setVisible(!1), n.isShowed_bl = !1, n.setAlpha(0)
                }, 100))
            }, this.init()
        };
        l.setPrototype = function() {
            l.prototype = null, l.prototype = new FWDMSPDisplayObject("div")
        }, l.CLICK = "onClick", l.MOUSE_DOWN = "onMouseDown", l.prototype = null
    }(window),
    function(t) {
        var e = function(o, s) {
            var f = this;
            e.prototype;
            this.embedColoseN_img = o.embedColoseN_img, this.bk_do = null, this.mainHolder_do = null, this.closeButton_do = null, this.buttons_ar = [], this.embedWindowBackground_str = o.shareBkPath_str, this.embedWindowCloseButtonMargins = 0, this.totalWidth = 0, this.stageWidth = 0, this.stageHeight = 0, this.minMarginXSpace = 20, this.hSpace = 20, this.minHSpace = 10, this.vSpace = 15, this.isShowed_bl = !1, this.isMobile_bl = FWDMSPUtils.isMobile, this.init = function() {
                f.setBackfaceVisibility(), f.mainHolder_do = new FWDMSPDisplayObject("div"), f.mainHolder_do.hasTransform3d_bl = !1, f.mainHolder_do.hasTransform2d_bl = !1, f.mainHolder_do.setBackfaceVisibility(), f.bk_do = new FWDMSPDisplayObject("div"), f.bk_do.getStyle().width = "100%", f.bk_do.getStyle().height = "100%", f.bk_do.setAlpha(.9), f.bk_do.getStyle().background = "url('" + f.embedWindowBackground_str + "')", FWDMSPSimpleButton.setPrototype(), f.closeButton_do = new FWDMSPSimpleButton(o.shareClooseN_img, o.embedWindowClosePathS_str, void 0, !0, o.useHEXColorsForSkin_bl, o.normalButtonsColor_str, o.selectedButtonsColor_str), f.closeButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, f.closeButtonOnMouseUpHandler), f.addChild(f.mainHolder_do), f.mainHolder_do.addChild(f.bk_do), f.mainHolder_do.addChild(f.closeButton_do), this.setupButtons()
            }, this.closeButtonOnMouseUpHandler = function() {
                f.isShowed_bl && f.hide(!0)
            }, this.positionAndResize = function() {
                f.stageWidth = s.stageWidth, f.stageHeight = s.stageHeight;
                var e = f.stageWidth - f.closeButton_do.w - f.embedWindowCloseButtonMargins,
                    t = 0;
                t = s.playlist_do && s.position_str == FWDMSP.POSITION_TOP ? s.playlist_do.h : f.embedWindowCloseButtonMargins, f.closeButton_do.setX(e), f.closeButton_do.setY(0), f.setY(t), f.setWidth(f.stageWidth), f.setHeight(f.stageHeight), f.mainHolder_do.setWidth(f.stageWidth), f.mainHolder_do.setHeight(f.stageHeight), f.positionButtons()
            }, this.setupButtons = function() {
                FWDMSPSimpleButton.setPrototype(), f.facebookButton_do = new FWDMSPSimpleButton(o.facebookN_img, o.facebookSPath_str, void 0, !0, o.useHEXColorsForSkin_bl, o.normalButtonsColor_str, o.selectedButtonsColor_str), f.facebookButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, f.facebookOnMouseUpHandler), this.buttons_ar.push(f.facebookButton_do), FWDMSPSimpleButton.setPrototype(), f.googleButton_do = new FWDMSPSimpleButton(o.googleN_img, o.googleSPath_str, void 0, !0, o.useHEXColorsForSkin_bl, o.normalButtonsColor_str, o.selectedButtonsColor_str), f.googleButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, f.googleOnMouseUpHandler), this.buttons_ar.push(f.googleButton_do), FWDMSPSimpleButton.setPrototype(), f.twitterButton_do = new FWDMSPSimpleButton(o.twitterN_img, o.twitterSPath_str, void 0, !0, o.useHEXColorsForSkin_bl, o.normalButtonsColor_str, o.selectedButtonsColor_str), f.twitterButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, f.twitterOnMouseUpHandler), this.buttons_ar.push(f.twitterButton_do), FWDMSPSimpleButton.setPrototype(), f.likedinButton_do = new FWDMSPSimpleButton(o.likedInkN_img, o.likedInSPath_str, void 0, !0, o.useHEXColorsForSkin_bl, o.normalButtonsColor_str, o.selectedButtonsColor_str), f.likedinButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, f.likedinOnMouseUpHandler), this.buttons_ar.push(f.likedinButton_do), FWDMSPSimpleButton.setPrototype(), f.bufferButton_do = new FWDMSPSimpleButton(o.bufferkN_img, o.bufferSPath_str, void 0, !0, o.useHEXColorsForSkin_bl, o.normalButtonsColor_str, o.selectedButtonsColor_str), f.bufferButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, f.bufferOnMouseUpHandler), this.buttons_ar.push(f.bufferButton_do), FWDMSPSimpleButton.setPrototype(), f.diggButton_do = new FWDMSPSimpleButton(o.diggN_img, o.diggSPath_str, void 0, !0, o.useHEXColorsForSkin_bl, o.normalButtonsColor_str, o.selectedButtonsColor_str), f.diggButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, f.diggOnMouseUpHandler), this.buttons_ar.push(f.diggButton_do), FWDMSPSimpleButton.setPrototype(), f.redditButton_do = new FWDMSPSimpleButton(o.redditN_img, o.redditSPath_str, void 0, !0, o.useHEXColorsForSkin_bl, o.normalButtonsColor_str, o.selectedButtonsColor_str), f.redditButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, f.redditOnMouseUpHandler), this.buttons_ar.push(f.redditButton_do), FWDMSPSimpleButton.setPrototype(), f.thumbrlButton_do = new FWDMSPSimpleButton(o.thumbrlN_img, o.thumbrlSPath_str, void 0, !0, o.useHEXColorsForSkin_bl, o.normalButtonsColor_str, o.selectedButtonsColor_str), f.thumbrlButton_do.addListener(FWDMSPSimpleButton.MOUSE_UP, f.thumbrlOnMouseUpHandler), this.buttons_ar.push(f.thumbrlButton_do), f.mainHolder_do.addChild(f.facebookButton_do), f.mainHolder_do.addChild(f.googleButton_do), f.mainHolder_do.addChild(f.twitterButton_do), f.mainHolder_do.addChild(f.likedinButton_do), f.mainHolder_do.addChild(f.bufferButton_do), f.mainHolder_do.addChild(f.diggButton_do), f.mainHolder_do.addChild(f.redditButton_do), f.mainHolder_do.addChild(f.thumbrlButton_do)
            }, this.facebookOnMouseUpHandler = function() {
                var e = "http://www.facebook.com/share.php?u=" + encodeURIComponent(location.href);
                t.open(e, "", "menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=600")
            }, this.googleOnMouseUpHandler = function() {
                var e = "https://plus.google.com/share?url=" + encodeURIComponent(location.href);
                t.open(e, "", "menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=600")
            }, this.twitterOnMouseUpHandler = function() {
                var e = "http://twitter.com/home?status=" + encodeURIComponent(location.href);
                t.open(e, "", "menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=600")
            }, this.likedinOnMouseUpHandler = function() {
                var e = "https://www.linkedin.com/cws/share?url=" + location.href;
                t.open(e, "", "menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=600")
            }, this.bufferOnMouseUpHandler = function() {
                var e = "https://buffer.com/add?url=" + location.href;
                t.open(e, "", "menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=600")
            }, this.diggOnMouseUpHandler = function() {
                var e = "http://digg.com/submit?url=" + location.href;
                t.open(e, "", "menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=600")
            }, this.redditOnMouseUpHandler = function() {
                var e = "https://www.reddit.com/?submit=" + location.href;
                t.open(e, "", "menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=600")
            }, this.thumbrlOnMouseUpHandler = function() {
                var e = "http://www.tumblr.com/share/link?url=" + location.href;
                t.open(e, "", "menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=400,width=600")
            }, this.positionButtons = function() {
                var e, t, o, s = [],
                    i = [],
                    n = [],
                    l = 0,
                    r = 0,
                    a = 0;
                s[a] = [0], i[a] = f.buttons_ar[0].totalWidth, n[a] = f.buttons_ar[0].totalWidth, f.totalButtons = f.buttons_ar.length;
                for (var d = 1; d < f.totalButtons; d++) e = f.buttons_ar[d], i[a] + e.totalWidth + f.minHSpace > f.stageWidth - f.minMarginXSpace ? (s[++a] = [], s[a].push(d), i[a] = e.totalWidth, n[a] = e.totalWidth) : (s[a].push(d), i[a] += e.totalWidth + f.minHSpace, n[a] += e.totalWidth);
                l = parseInt((f.stageHeight - ((a + 1) * (e.totalHeight + f.vSpace) - f.vSpace)) / 2);
                for (d = 0; d < a + 1; d++) {
                    var u, c = 0;
                    if (1 < s[d].length) {
                        u = Math.min((f.stageWidth - f.minMarginXSpace - n[d]) / (s[d].length - 1), f.hSpace);
                        var h = n[d] + u * (s[d].length - 1);
                        c = parseInt((f.stageWidth - h) / 2)
                    } else c = parseInt((f.stageWidth - i[d]) / 2);
                    0 < d && (l += e.h + f.vSpace);
                    for (var _ = 0; _ < s[d].length; _++) e = f.buttons_ar[s[d][_]], o = 0 == _ ? c : (t = f.buttons_ar[s[d][_] - 1]).finalX + t.totalWidth + u, e.finalX = o, e.finalY = l, r < e.finalY && (r = e.finalY), f.buttonsBarTotalHeight = r + e.totalHeight + f.startY, e.setX(e.finalX), e.setY(e.finalY)
                }
            }, this.show = function(e) {
                f.isShowed_bl || (f.isShowed_bl = !0, s.main_do.addChild(f), (!FWDMSPUtils.isMobile || FWDMSPUtils.isMobile && FWDMSPUtils.hasPointerEvent) && s.main_do.setSelectable(!0), f.positionAndResize(), clearTimeout(f.hideCompleteId_to), clearTimeout(f.showCompleteId_to), f.mainHolder_do.setY(-f.stageHeight), f.showCompleteId_to = setTimeout(f.showCompleteHandler, 900), setTimeout(function() {
                    FWDAnimation.to(f.mainHolder_do, .8, {
                        y: 0,
                        delay: .1,
                        ease: Expo.easeInOut
                    })
                }, 100))
            }, this.showCompleteHandler = function() {}, this.hide = function(e) {
                f.isShowed_bl && (f.isShowed_bl = !1, s.customContextMenu_do && s.customContextMenu_do.enable(), clearTimeout(f.hideCompleteId_to), clearTimeout(f.showCompleteId_to), (!FWDMSPUtils.isMobile || FWDMSPUtils.isMobile && FWDMSPUtils.hasPointerEvent) && s.main_do.setSelectable(!1), f.hideCompleteId_to = setTimeout(f.hideCompleteHandler, 800), FWDAnimation.killTweensOf(f.mainHolder_do), e ? FWDAnimation.to(f.mainHolder_do, .8, {
                    y: -f.stageHeight,
                    ease: Expo.easeInOut
                }) : f.hideCompleteHandler())
            }, this.hideCompleteHandler = function() {
                s.main_do.contains(f) && s.main_do.removeChild(f), f.dispatchEvent(e.HIDE_COMPLETE)
            }, this.updateHEXColors = function(e, t) {
                -1 != o.skinPath_str.indexOf("hex_white") ? f.selectedColor_str = "#FFFFFF" : f.selectedColor_str = t, f.closeButton_do.updateHEXColors(e, f.selectedColor_str), f.facebookButton_do.updateHEXColors(e, t), f.googleButton_do.updateHEXColors(e, t), f.twitterButton_do.updateHEXColors(e, t), f.likedinButton_do.updateHEXColors(e, t), f.bufferButton_do.updateHEXColors(e, t), f.diggButton_do.updateHEXColors(e, t), f.redditButton_do.updateHEXColors(e, t), f.thumbrlButton_do.updateHEXColors(e, t)
            }, this.init()
        };
        e.setPrototype = function() {
            e.prototype = new FWDMSPDisplayObject("div")
        }, e.HIDE_COMPLETE = "hideComplete", e.prototype = null, t.FWDMSPShareWindow = e
    }(window),
    function(e) {
        var d = function(e, t, o, s, i, n, l, r) {
            var a = this;
            d.prototype;
            this.nImg = e, this.sPath_str = t, this.dPath_str = o, this.n_sdo, this.s_sdo, this.d_sdo, this.totalWidth = this.nImg.width, this.totalHeight = this.nImg.height, this.useHEXColorsForSkin_bl = i, this.normalButtonsColor_str = n, this.selectedButtonsColor_str = l, this.inverseHEXColors_bl = r, this.isShowed_bl = !0, this.isSetToDisabledState_bl = !1, this.isDisabled_bl = !1, this.isDisabledForGood_bl = !1, this.isSelectedFinal_bl = !1, this.isActive_bl = !1, this.isMobile_bl = FWDMSPUtils.isMobile, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, this.allowToCreateSecondButton_bl = !a.isMobile_bl || a.hasPointerEvent_bl || s, a.init = function() {
                a.setupMainContainers()
            }, a.setupMainContainers = function() {
                if (a.useHEXColorsForSkin_bl ? (a.n_sdo = new FWDMSPTransformDisplayObject("div"), a.n_sdo.setWidth(a.totalWidth), a.n_sdo.setHeight(a.totalHeight), a.n_sdo_canvas = FWDMSPUtils.getCanvasWithModifiedColor(a.nImg, a.normalButtonsColor_str).canvas, a.n_sdo.screen.appendChild(a.n_sdo_canvas)) : (a.n_sdo = new FWDMSPTransformDisplayObject("img"), a.n_sdo.setScreen(a.nImg)), a.addChild(a.n_sdo), a.allowToCreateSecondButton_bl) {
                    a.img1 = new Image, a.img1.src = a.sPath_str;
                    var e = new Image;
                    a.sImg = e, a.useHEXColorsForSkin_bl ? (a.s_sdo = new FWDMSPTransformDisplayObject("div"), a.s_sdo.setWidth(a.totalWidth), a.s_sdo.setHeight(a.totalHeight), a.img1.onload = function() {
                        a.inverseHEXColors_bl ? a.s_sdo_canvas = FWDMSPUtils.getCanvasWithModifiedColor(a.img1, a.normalButtonsColor_str).canvas : a.s_sdo_canvas = FWDMSPUtils.getCanvasWithModifiedColor(a.img1, a.selectedButtonsColor_str).canvas, a.s_sdo.screen.appendChild(a.s_sdo_canvas)
                    }) : (a.s_sdo = new FWDMSPDisplayObject("img"), a.s_sdo.setScreen(a.img1), a.s_sdo.setWidth(a.totalWidth), a.s_sdo.setHeight(a.totalHeight)), a.s_sdo.setAlpha(0), a.addChild(a.s_sdo), a.dPath_str && (e.src = a.dPath_str, a.d_sdo = new FWDMSPDisplayObject("img"), a.d_sdo.setScreen(e), a.d_sdo.setWidth(a.totalWidth), a.d_sdo.setHeight(a.totalHeight), a.d_sdo.setX(-100), a.addChild(a.d_sdo))
                }
                a.setWidth(a.totalWidth), a.setHeight(a.totalHeight), a.setButtonMode(!0), a.screen.style.yellowOverlayPointerEvents = "none", a.isMobile_bl ? a.hasPointerEvent_bl ? (a.screen.addEventListener("pointerup", a.onMouseUp), a.screen.addEventListener("pointerover", a.onMouseOver), a.screen.addEventListener("pointerout", a.onMouseOut)) : a.screen.addEventListener("touchend", a.onMouseUp) : a.screen.addEventListener ? (a.screen.addEventListener("mouseover", a.onMouseOver), a.screen.addEventListener("mouseout", a.onMouseOut), a.screen.addEventListener("mouseup", a.onMouseUp)) : a.screen.attachEvent && (a.screen.attachEvent("onmouseover", a.onMouseOver), a.screen.attachEvent("onmouseout", a.onMouseOut), a.screen.attachEvent("onmouseup", a.onMouseUp))
            }, a.onMouseOver = function(e) {
                !(a.isDisabledForGood_bl || e.pointerType && e.pointerType != e.MSPOINTER_TYPE_MOUSE && "mouse" != e.pointerType) {
                    if (a.isDisabled_bl || a.isSelectedFinal_bl) return;
                    a.dispatchEvent(d.MOUSE_OVER, {
                        e: e
                    }), a.setSelectedState()
                }
            }, a.onMouseOut = function(e) {
                if (!(a.isDisabledForGood_bl || e.pointerType && e.pointerType != e.MSPOINTER_TYPE_MOUSE && "mouse" != e.pointerType)) {
                    if (a.isDisabled_bl || a.isSelectedFinal_bl) return;
                    a.dispatchEvent(d.MOUSE_OUT, {
                        e: e
                    }), a.setNormalState()
                }
            }, a.onMouseUp = function(e) {
                a.isDisabledForGood_bl || (e.preventDefault && e.preventDefault(), a.isDisabled_bl || 2 == e.button || a.dispatchEvent(d.MOUSE_UP, {
                    e: e
                }))
            }, a.setSelected = function() {
                a.isSelectedFinal_bl = !0, a.s_sdo && (FWDAnimation.killTweensOf(a.s_sdo), FWDAnimation.to(a.s_sdo, .8, {
                    alpha: 1,
                    ease: Expo.easeOut
                }))
            }, a.setUnselected = function() {
                a.isSelectedFinal_bl = !1, a.s_sdo && FWDAnimation.to(a.s_sdo, .8, {
                    alpha: 0,
                    delay: .1,
                    ease: Expo.easeOut
                })
            }, this.setNormalState = function() {
                FWDAnimation.killTweensOf(a.s_sdo), FWDAnimation.to(a.s_sdo, .5, {
                    alpha: 0,
                    ease: Expo.easeOut
                })
            }, this.setSelectedState = function() {
                FWDAnimation.killTweensOf(a.s_sdo), FWDAnimation.to(a.s_sdo, .5, {
                    alpha: 1,
                    delay: .1,
                    ease: Expo.easeOut
                })
            }, this.setDisabledState = function() {
                a.isSetToDisabledState_bl || (a.isSetToDisabledState_bl = !0, a.d_sdo && a.d_sdo.setX(0))
            }, this.setEnabledState = function() {
                a.isSetToDisabledState_bl && (a.isSetToDisabledState_bl = !1, a.d_sdo && a.d_sdo.setX(-100))
            }, this.disable = function() {
                a.isDisabledForGood_bl || a.isDisabled_bl || (a.isDisabled_bl = !0, FWDAnimation.killTweensOf(a), a.setButtonMode(!1), FWDAnimation.to(a, .6, {
                    alpha: .4
                }), a.setNormalState())
            }, this.enable = function() {
                !a.isDisabledForGood_bl && a.isDisabled_bl && (a.isDisabled_bl = !1, FWDAnimation.killTweensOf(a), a.setButtonMode(!0), FWDAnimation.to(a, .6, {
                    alpha: 1
                }))
            }, this.disableForGood = function() {
                a.isDisabledForGood_bl = !0, a.setButtonMode(!1)
            }, this.disableForGood = function() {
                a.isDisabledForGood_bl = !0, a.setButtonMode(!1)
            }, this.enableForGood = function() {
                a.isDisabledForGood_bl = !1, a.setButtonMode(!0)
            }, this.showDisabledState = function() {
                0 != a.d_sdo.x && a.d_sdo.setX(0)
            }, this.hideDisabledState = function() {
                -100 != a.d_sdo.x && a.d_sdo.setX(-100)
            }, this.show = function() {
                a.isShowed_bl || (a.isShowed_bl = !0, FWDAnimation.killTweensOf(a), FWDMSPUtils.isIEAndLessThen9 ? (FWDMSPUtils.isIEAndLessThen9 || (a.setAlpha(0), FWDAnimation.to(a, .4, {
                    alpha: 1,
                    delay: .4
                })), a.setVisible(!0)) : FWDMSPUtils.isIEWebKit ? (FWDAnimation.killTweensOf(a.n_sdo), a.n_sdo.setScale2(0), FWDAnimation.to(a.n_sdo, .8, {
                    scale: 1,
                    delay: .4,
                    onStart: function() {
                        a.setVisible(!0)
                    },
                    ease: Elastic.easeOut
                })) : (a.setScale2(0), FWDAnimation.to(a, .8, {
                    scale: 1,
                    delay: .4,
                    onStart: function() {
                        a.setVisible(!0)
                    },
                    ease: Elastic.easeOut
                })))
            }, this.hide = function(e) {
                a.isShowed_bl && (a.isShowed_bl = !1, FWDAnimation.killTweensOf(a), FWDAnimation.killTweensOf(a.n_sdo), a.setVisible(!1))
            }, a.updateHEXColors = function(e, t) {
                FWDMSPUtils.changeCanvasHEXColor(a.nImg, a.n_sdo_canvas, e), FWDMSPUtils.changeCanvasHEXColor(a.img1, a.s_sdo_canvas, t)
            }, a.init()
        };
        d.setPrototype = function() {
            d.prototype = null, d.prototype = new FWDMSPTransformDisplayObject("div")
        }, d.CLICK = "onClick", d.MOUSE_OVER = "onMouseOver", d.MOUSE_OUT = "onMouseOut", d.MOUSE_UP = "onMouseDown", d.prototype = null, e.FWDMSPSimpleButton = d
    }(window),
    function(e) {
        var a = function(e, t, o, s, i, n, l) {
            var r = this;
            a.prototype;
            this.nImg_img = null, this.sImg_img = null, this.n_do, this.s_do, this.useHEXColorsForSkin_bl = i, this.normalButtonsColor_str = l, this.selectedButtonsColor_str = n, this.nImgPath_str = e, this.sImgPath_str = t, this.buttonWidth = o, this.buttonHeight = s, this.isMobile_bl = FWDMSPUtils.isMobile, this.hasPointerEvent_bl = FWDMSPUtils.hasPointerEvent, this.isDisabled_bl = !1, this.init = function() {
                r.setupMainContainers(), r.setWidth(r.buttonWidth), r.setHeight(r.buttonHeight), r.setButtonMode(!0)
            }, this.setupMainContainers = function() {
                r.nImg = new Image, r.nImg.src = r.nImgPath_str, r.useHEXColorsForSkin_bl ? (r.n_do = new FWDMSPTransformDisplayObject("div"), r.n_do.setWidth(r.buttonWidth), r.n_do.setHeight(r.buttonHeight), r.nImg.onload = function() {
                    r.n_do_canvas = FWDMSPUtils.getCanvasWithModifiedColor(r.nImg, r.normalButtonsColor_str).canvas, r.n_do.screen.appendChild(r.n_do_canvas)
                }) : (r.n_do = new FWDMSPDisplayObject("img"), r.n_do.setScreen(r.nImg), r.n_do.setWidth(r.buttonWidth), r.n_do.setHeight(r.buttonHeight)), r.addChild(r.n_do), r.sImg = new Image, r.sImg.src = r.sImgPath_str, r.useHEXColorsForSkin_bl ? (r.s_do = new FWDMSPTransformDisplayObject("div"), r.s_do.setWidth(r.buttonWidth), r.s_do.setHeight(r.buttonHeight), r.sImg.onload = function() {
                    r.s_do_canvas = FWDMSPUtils.getCanvasWithModifiedColor(r.sImg, r.selectedButtonsColor_str).canvas, r.s_do.screen.appendChild(r.s_do_canvas)
                }) : (r.s_do = new FWDMSPDisplayObject("img"), r.s_do.setScreen(r.sImg), r.s_do.setWidth(r.buttonWidth), r.s_do.setHeight(r.buttonHeight)), r.addChild(r.s_do), r.hasPointerEvent_bl ? (r.screen.addEventListener("pointerup", r.onMouseUp), r.screen.addEventListener("pointerover", r.setNormalState), r.screen.addEventListener("pointerout", r.setSelectedState)) : r.screen.addEventListener && (r.isMobile_bl || (r.screen.addEventListener("mouseover", r.setNormalState), r.screen.addEventListener("mouseout", r.setSelectedState), r.screen.addEventListener("mouseup", r.onMouseUp)), r.screen.addEventListener("touchend", r.onMouseUp))
            }, this.setNormalState = function(e) {
                FWDAnimation.killTweensOf(r.s_do), FWDAnimation.to(r.s_do, .5, {
                    alpha: 0,
                    ease: Expo.easeOut
                })
            }, this.setSelectedState = function(e) {
                FWDAnimation.killTweensOf(r.s_do), FWDAnimation.to(r.s_do, .5, {
                    alpha: 1,
                    ease: Expo.easeOut
                })
            }, this.onMouseUp = function(e) {
                r.dispatchEvent(a.CLICK)
            }, r.updateHEXColors = function(e, t) {
                FWDMSPUtils.changeCanvasHEXColor(r.nImg, r.n_do_canvas, t), FWDMSPUtils.changeCanvasHEXColor(r.sImg, r.s_do_canvas, e)
            }, this.destroy = function() {
                FWDAnimation.killTweensOf(r.n_do), r.n_do.destroy(), this.s_do.destroy(), r.screen.onmouseover = null, r.screen.onmouseout = null, r.screen.onclick = null, r.nImg_img = null, r.sImg_img = null, r = null, a.prototype = null
            }, r.init()
        };
        a.setPrototype = function() {
            a.prototype = null, a.prototype = new FWDMSPTransformDisplayObject("div", "relative")
        }, a.CLICK = "onClick", a.prototype = null, e.FWDMSPSimpleSizeButton = a
    }(window),
    function(a) {
        var d = function(e, t, o, s, i, n, l) {
            var r = this;
            d.prototype;
            this.buttonRef_do = e, this.bkPath_str = t, this.pointerPath_str = o, this.text_do = null, this.pointer_do = null, this.pointerUp_do = null, this.fontColor_str = n, this.toopTipPointerUp_str = s, this.pointerWidth = 7, this.pointerHeight = 4, this.showWithDelayId_to, this.isMobile_bl = FWDMSPUtils.isMobile, this.isShowed_bl = !0, this.init = function() {
                r.setOverflow("visible"), r.setupMainContainers(), r.hide(), r.getStyle().background = "url('" + r.bkPath_str + "')", r.getStyle().zIndex = 9999999999
            }, this.setupMainContainers = function() {
                r.text_do = new FWDMSPDisplayObject("div"), r.text_do.hasTransform3d_bl = !1, r.text_do.hasTransform2d_bl = !1, r.text_do.setBackfaceVisibility(), r.text_do.setDisplay("inline"), r.text_do.getStyle().fontFamily = "Arial", r.text_do.getStyle().fontSize = "12px", r.text_do.getStyle().color = r.fontColor_str, r.text_do.getStyle().whiteSpace = "nowrap", r.text_do.getStyle().fontSmoothing = "antialiased", r.text_do.getStyle().webkitFontSmoothing = "antialiased", r.text_do.getStyle().textRendering = "optimizeLegibility", r.text_do.getStyle().padding = "6px", r.text_do.getStyle().paddingTop = "4px", r.text_do.getStyle().paddingBottom = "4px", r.setLabel(), r.addChild(r.text_do);
                var e = new Image;
                e.src = r.pointerPath_str, r.pointer_do = new FWDMSPDisplayObject("img"), r.pointer_do.setScreen(e), r.pointer_do.setWidth(r.pointerWidth), r.pointer_do.setHeight(r.pointerHeight), r.addChild(r.pointer_do);
                var t = new Image;
                t.src = r.toopTipPointerUp_str, r.pointerUp_do = new FWDMSPDisplayObject("img"), r.pointerUp_do.setScreen(t), r.pointerUp_do.setWidth(r.pointerWidth), r.pointerUp_do.setHeight(r.pointerHeight), r.addChild(r.pointerUp_do)
            }, this.setLabel = function(e) {
                r.text_do.setInnerHTML(i), setTimeout(function() {
                    null != r && (r.setWidth(r.text_do.getWidth()), r.setHeight(r.text_do.getHeight()), r.positionPointer())
                }, 50)
            }, this.positionPointer = function(e, t) {
                var o, s;
                e = e || 0, o = parseInt((r.w - r.pointerWidth) / 2) + e, t ? (s = -3, r.pointerUp_do.setX(o), r.pointerUp_do.setY(s), r.pointer_do.setX(0), r.pointer_do.setY(0)) : (s = r.h, r.pointer_do.setX(o), r.pointer_do.setY(s), r.pointerUp_do.setX(0), r.pointerUp_do.setY(0))
            }, this.show = function() {
                r.isShowed_bl || (r.isShowed_bl = !0, FWDAnimation.killTweensOf(r), clearTimeout(r.showWithDelayId_to), r.showWithDelayId_to = setTimeout(r.showFinal), a.addEventListener ? a.addEventListener("mousemove", r.moveHandler) : document.attachEvent && (document.detachEvent("onmousemove", r.moveHandler), document.attachEvent("onmousemove", r.moveHandler)))
            }, this.showFinal = function() {
                r.setVisible(!0), r.setAlpha(0), FWDAnimation.to(r, .4, {
                    alpha: 1,
                    onComplete: function() {
                        r.setVisible(!0)
                    },
                    ease: Quart.easeOut
                })
            }, this.moveHandler = function(e) {
                var t = FWDMSPUtils.getViewportMouseCoordinates(e);
                FWDMSPUtils.hitTest(r.buttonRef_do.screen, t.screenX, t.screenY) || r.hide()
            }, this.hide = function() {
                r.isShowed_bl && (clearTimeout(r.showWithDelayId_to), a.removeEventListener ? a.removeEventListener("mousemove", r.moveHandler) : document.detachEvent && document.detachEvent("onmousemove", r.moveHandler), FWDAnimation.killTweensOf(r), r.setVisible(!1), r.isShowed_bl = !1)
            }, this.init()
        };
        d.setPrototype = function() {
            d.prototype = null, d.prototype = new FWDMSPDisplayObject("div", "fixed")
        }, d.CLICK = "onClick", d.MOUSE_DOWN = "onMouseDown", d.prototype = null
    }(window), window.FWDMSPTransformDisplayObject = function(e, t, o, s) {
        this.listeners = {
            events_ar: []
        };
        var i = this;
        if ("div" != e && "img" != e && "canvas" != e) throw Error("Type is not valid! " + e);
        this.type = e, this.children_ar = [], this.style, this.screen, this.numChildren, this.transform, this.position = t || "absolute", this.overflow = o || "hidden", this.display = s || "block", this.visible = !0, this.buttonMode, this.x = 0, this.y = 0, this.scale = 1, this.rotation = 0, this.w = 0, this.h = 0, this.rect, this.alpha = 1, this.innerHTML = "", this.opacityType = "", this.isHtml5_bl = !1, this.hasTransform2d_bl = FWDMSPUtils.hasTransform2d, this.init = function() {
            this.setScreen()
        }, this.getTransform = function() {
            for (var e, t = ["transform", "msTransform", "WebkitTransform", "MozTransform", "OTransform"]; e = t.shift();)
                if (void 0 !== this.screen.style[e]) return e;
            return !1
        }, this.getOpacityType = function() {
            return void 0 !== this.screen.style.opacity ? "opacity" : "filter"
        }, this.setScreen = function(e) {
            "img" == this.type && e ? this.screen = e : this.screen = document.createElement(this.type), this.setMainProperties()
        }, this.setMainProperties = function() {
            this.transform = this.getTransform(), this.setPosition(this.position), this.setOverflow(this.overflow), this.opacityType = this.getOpacityType(), "opacity" == this.opacityType && (this.isHtml5_bl = !0), "filter" == i.opacityType && (i.screen.style.filter = "inherit"), this.screen.style.left = "0px", this.screen.style.top = "0px", this.screen.style.margin = "0px", this.screen.style.padding = "0px", this.screen.style.maxWidth = "none", this.screen.style.maxHeight = "none", this.screen.style.border = "none", this.screen.style.lineHeight = "1", this.screen.style.backgroundColor = "transparent", this.screen.style.backfaceVisibility = "hidden", this.screen.style.webkitBackfaceVisibility = "hidden", this.screen.style.MozBackfaceVisibility = "hidden", this.screen.style.MozImageRendering = "optimizeSpeed", this.screen.style.WebkitImageRendering = "optimizeSpeed", "img" == e && (this.setWidth(this.screen.width), this.setHeight(this.screen.height), this.screen.onmousedown = function(e) {
                return !1
            })
        }, i.setBackfaceVisibility = function() {
            i.screen.style.backfaceVisibility = "visible", i.screen.style.webkitBackfaceVisibility = "visible", i.screen.style.MozBackfaceVisibility = "visible"
        }, i.removeBackfaceVisibility = function() {
            i.screen.style.backfaceVisibility = "hidden", i.screen.style.webkitBackfaceVisibility = "hidden", i.screen.style.MozBackfaceVisibility = "hidden"
        }, this.setSelectable = function(e) {
            if (!e) {
                try {
                    this.screen.style.userSelect = "none"
                } catch (e) {}
                try {
                    this.screen.style.MozUserSelect = "none"
                } catch (e) {}
                try {
                    this.screen.style.webkitUserSelect = "none"
                } catch (e) {}
                try {
                    this.screen.style.khtmlUserSelect = "none"
                } catch (e) {}
                try {
                    this.screen.style.oUserSelect = "none"
                } catch (e) {}
                try {
                    this.screen.style.msUserSelect = "none"
                } catch (e) {}
                try {
                    this.screen.msUserSelect = "none"
                } catch (e) {}
                this.screen.ondragstart = function(e) {
                    return !1
                }, this.screen.onselectstart = function() {
                    return !1
                }, this.screen.style.webkitTouchCallout = "none"
            }
        }, this.getScreen = function() {
            return i.screen
        }, this.setVisible = function(e) {
            this.visible = e, 1 == this.visible ? this.screen.style.visibility = "visible" : this.screen.style.visibility = "hidden"
        }, this.getVisible = function() {
            return this.visible
        }, this.setResizableSizeAfterParent = function() {
            this.screen.style.width = "100%", this.screen.style.height = "100%"
        }, this.getStyle = function() {
            return this.screen.style
        }, this.setOverflow = function(e) {
            i.overflow = e, i.screen.style.overflow = i.overflow
        }, this.setPosition = function(e) {
            i.position = e, i.screen.style.position = i.position
        }, this.setDisplay = function(e) {
            this.display = e, this.screen.style.display = this.display
        }, this.setButtonMode = function(e) {
            this.buttonMode = e, 1 == this.buttonMode ? this.screen.style.cursor = "pointer" : this.screen.style.cursor = "default"
        }, this.setBkColor = function(e) {
            i.screen.style.backgroundColor = e
        }, this.setInnerHTML = function(e) {
            i.innerHTML = e, i.screen.innerHTML = i.innerHTML
        }, this.getInnerHTML = function() {
            return i.innerHTML
        }, this.getRect = function() {
            return i.screen.getBoundingClientRect()
        }, this.setAlpha = function(e) {
            i.alpha = e, "opacity" == i.opacityType ? i.screen.style.opacity = i.alpha : "filter" == i.opacityType && (i.screen.style.filter = "alpha(opacity=" + 100 * i.alpha + ")", i.screen.style.filter = "progid:DXImageTransform.Microsoft.Alpha(Opacity=" + Math.round(100 * i.alpha) + ")")
        }, this.getAlpha = function() {
            return i.alpha
        }, this.getRect = function() {
            return this.screen.getBoundingClientRect()
        }, this.getGlobalX = function() {
            return this.getRect().left
        }, this.getGlobalY = function() {
            return this.getRect().top
        }, this.setX = function(e) {
            i.x = e, i.hasTransform2d_bl ? i.screen.style[i.transform] = "translate(" + i.x + "px," + i.y + "px) scale(" + i.scale + " , " + i.scale + ") rotate(" + i.rotation + "deg)" : i.screen.style.left = i.x + "px"
        }, this.getX = function() {
            return i.x
        }, this.setY = function(e) {
            i.y = e, i.hasTransform2d_bl ? i.screen.style[i.transform] = "translate(" + i.x + "px," + i.y + "px) scale(" + i.scale + " , " + i.scale + ") rotate(" + i.rotation + "deg)" : i.screen.style.top = i.y + "px"
        }, this.getY = function() {
            return i.y
        }, this.setScale2 = function(e) {
            i.scale = e, i.hasTransform2d_bl && (i.screen.style[i.transform] = "translate(" + i.x + "px," + i.y + "px) scale(" + i.scale + " , " + i.scale + ") rotate(" + i.rotation + "deg)")
        }, this.getScale = function() {
            return i.scale
        }, this.setRotation = function(e) {
            i.rotation = e, i.hasTransform2d_bl && (i.screen.style[i.transform] = "translate(" + i.x + "px," + i.y + "px) scale(" + i.scale + " , " + i.scale + ") rotate(" + i.rotation + "deg)")
        }, i.setWidth = function(e) {
            i.w = e, "img" == i.type && (i.screen.width = i.w), i.screen.style.width = i.w + "px"
        }, this.getWidth = function() {
            return "div" == i.type ? 0 != i.screen.offsetWidth ? i.screen.offsetWidth : i.w : "img" == i.type ? 0 != i.screen.offsetWidth ? i.screen.offsetWidth : 0 != i.screen.width ? i.screen.width : i._w : "canvas" == i.type ? 0 != i.screen.offsetWidth ? i.screen.offsetWidth : i.w : void 0
        }, i.setHeight = function(e) {
            i.h = e, "img" == i.type && (i.screen.height = i.h), i.screen.style.height = i.h + "px"
        }, this.getHeight = function() {
            return "div" == i.type ? 0 != i.screen.offsetHeight ? i.screen.offsetHeight : i.h : "img" == i.type ? 0 != i.screen.offsetHeight ? i.screen.offsetHeight : 0 != i.screen.height ? i.screen.height : i.h : "canvas" == i.type ? 0 != i.screen.offsetHeight ? i.screen.offsetHeight : i.h : void 0
        }, this.getNumChildren = function() {
            return i.children_ar.length
        }, this.addChild = function(e) {
            this.contains(e) && this.children_ar.splice(FWDMSPUtils.indexOfArray(this.children_ar, e), 1), this.children_ar.push(e), this.screen.appendChild(e.screen)
        }, this.removeChild = function(e) {
            if (!this.contains(e)) throw Error("##removeChild()## Child doesn't exist, it can't be removed!");
            this.children_ar.splice(FWDMSPUtils.indexOfArray(this.children_ar, e), 1), this.screen.removeChild(e.screen)
        }, this.contains = function(e) {
            return -1 != FWDMSPUtils.indexOfArray(this.children_ar, e)
        }, this.addChildAtZero = function(e) {
            0 == this.numChildren ? (this.children_ar.push(e), this.screen.appendChild(e.screen)) : (this.screen.insertBefore(e.screen, this.children_ar[0].screen), this.contains(e) && this.children_ar.splice(FWDMSPUtils.indexOfArray(this.children_ar, e), 1), this.children_ar.unshift(e))
        }, this.getChildAt = function(e) {
            if (e < 0 || e > this.numChildren - 1) throw Error("##getChildAt()## Index out of bounds!");
            if (0 == this.numChildren) throw Errror("##getChildAt## Child dose not exist!");
            return this.children_ar[e]
        }, this.removeChildAtZero = function() {
            this.screen.removeChild(this.children_ar[0].screen), this.children_ar.shift()
        }, this.addListener = function(e, t) {
            if (null == e) throw Error("type is required.");
            if ("object" == typeof e) throw Error("type must be of type String.");
            if ("function" != typeof t) throw Error("listener must be of type Function.");
            var o = {};
            o.type = e, o.listener = t, (o.target = this).listeners.events_ar.push(o)
        }, this.dispatchEvent = function(e, t) {
            if (null == e) throw Error("type is required.");
            if ("object" == typeof e) throw Error("type must be of type String.");
            for (var o = 0, s = this.listeners.events_ar.length; o < s; o++)
                if (this.listeners.events_ar[o].target === this && this.listeners.events_ar[o].type === e) {
                    if (t)
                        for (var i in t) this.listeners.events_ar[o][i] = t[i];
                    this.listeners.events_ar[o].listener.call(this, this.listeners.events_ar[o]);
                    break
                }
        }, this.removeListener = function(e, t) {
            if (null == e) throw Error("type is required.");
            if ("object" == typeof e) throw Error("type must be of type String.");
            if ("function" != typeof t) throw Error("listener must be of type Function." + e);
            for (var o = 0, s = this.listeners.events_ar.length; o < s; o++)
                if (this.listeners.events_ar[o].target === this && this.listeners.events_ar[o].type === e && this.listeners.events_ar[o].listener === t) {
                    this.listeners.events_ar.splice(o, 1);
                    break
                }
        }, this.disposeImage = function() {
            "img" == this.type && (this.screen.src = null)
        }, this.destroy = function() {
            try {
                this.screen.parentNode.removeChild(this.screen)
            } catch (e) {}
            this.screen.onselectstart = null, this.screen.ondragstart = null, this.screen.ontouchstart = null, this.screen.ontouchmove = null, this.screen.ontouchend = null, this.screen.onmouseover = null, this.screen.onmouseout = null, this.screen.onmouseup = null, this.screen.onmousedown = null, this.screen.onmousemove = null, this.screen.onclick = null, delete this.screen, delete this.style, delete this.rect, delete this.selectable, delete this.buttonMode, delete this.position, delete this.overflow, delete this.visible, delete this.innerHTML, delete this.numChildren, delete this.x, delete this.y, delete this.w, delete this.h, delete this.opacityType, delete this.isHtml5_bl, delete this.hasTransform2d_bl, this.children_ar = null, this.style = null, this.screen = null, this.numChildren = null, this.transform = null, this.position = null, this.overflow = null, this.display = null, this.visible = null, this.buttonMode = null, this.globalX = null, this.globalY = null, this.x = null, this.y = null, this.w = null, this.h = null, this.rect = null, this.alpha = null, this.innerHTML = null, this.opacityType = null, this.isHtml5_bl = null, this.hasTransform3d_bl = null, this.hasTransform2d_bl = null, i = null
        }, this.init()
    },
    function(o) {
        var i = function(t, e) {
            var l = this;
            i.prototype;
            this.video_el = null, this.sourcePath_str = null, this.bk_do = null, this.controllerHeight = t.data.controllerHeight, this.stageWidth = 0, this.stageHeight = 0, this.lastPercentPlayed = 0, this.volume = e, this.curDuration = 0, this.countNormalMp3Errors = 0, this.countShoutCastErrors = 0, this.maxShoutCastCountErrors = 5, this.maxNormalCountErrors = 1, this.disableClickForAWhileId_to, this.showErrorWithDelayId_to, this.playWithDelayId_to, this.disableClick_bl = !1, this.allowScrubing_bl = !1, this.hasError_bl = !0, this.isPlaying_bl = !1, this.isStopped_bl = !0, this.hasPlayedOnce_bl = !1, this.isStartEventDispatched_bl = !1, this.isSafeToBeControlled_bl = !1, this.isMobile_bl = FWDMSPUtils.isMobile, this.init = function() {
                l.getStyle().width = "100%", l.getStyle().height = "100%", l.setBkColor(t.videoBackgroundColor_str), l.setupVideo()
            }, this.setupVideo = function() {
                null == l.video_el && (l.video_el = document.createElement("video"), l.video_el.controls = !1, l.video_el.volume = l.volume, l.video_el.WebKitPlaysInline = !0, l.video_el.playsinline = !0, l.video_el.setAttribute("playsinline", ""), l.video_el.setAttribute("webkit-playsinline", ""), l.video_el.style.position = "relative", l.video_el.style.left = "0px", l.video_el.style.top = "0px", l.video_el.style.width = "100%", l.video_el.style.height = "100%", l.video_el.style.margin = "0px", l.video_el.style.padding = "0px", l.video_el.style.maxWidth = "none", l.video_el.style.maxHeight = "none", l.video_el.style.border = "none", l.video_el.style.lineHeight = "0", l.video_el.style.msTouchAction = "none", l.screen.appendChild(l.video_el)), l.video_el.addEventListener("error", l.errorHandler), l.video_el.addEventListener("canplay", l.safeToBeControlled), l.video_el.addEventListener("canplaythrough", l.safeToBeControlled), l.video_el.addEventListener("progress", l.updateProgress), l.video_el.addEventListener("timeupdate", l.updateVideo), l.video_el.addEventListener("pause", l.pauseHandler), l.video_el.addEventListener("play", l.playHandler), FWDMSPUtils.isIE || l.video_el.addEventListener("waiting", l.startToBuffer), l.video_el.addEventListener("playing", l.stopToBuffer), l.video_el.addEventListener("ended", l.endedHandler), l.resizeAndPosition()
            }, this.destroyVideo = function() {
                clearTimeout(l.showErrorWithDelayId_to), l.video_el && (l.video_el.removeEventListener("error", l.errorHandler), l.video_el.removeEventListener("canplay", l.safeToBeControlled), l.video_el.removeEventListener("canplaythrough", l.safeToBeControlled), l.video_el.removeEventListener("progress", l.updateProgress), l.video_el.removeEventListener("timeupdate", l.updateVideo), l.video_el.removeEventListener("pause", l.pauseHandler), l.video_el.removeEventListener("play", l.playHandler), FWDMSPUtils.isIE || l.video_el.removeEventListener("waiting", l.startToBuffer), l.video_el.removeEventListener("playing", l.stopToBuffer), l.video_el.removeEventListener("ended", l.endedHandler), l.isMobile_bl ? (l.screen.removeChild(l.video_el), l.video_el = null) : (l.video_el.style.visibility = "hidden", l.video_el.src = "", l.video_el.load()))
            }, this.startToBuffer = function(e) {
                l.dispatchEvent(i.START_TO_BUFFER)
            }, this.stopToBuffer = function() {
                l.dispatchEvent(i.STOP_TO_BUFFER)
            }, this.errorHandler = function(e) {
                var t;
                l.hasError_bl = !0, t = 0 == l.video_el.networkState ? "error 'self.video_el.networkState = 0'" : 1 == l.video_el.networkState ? "error 'self.video_el.networkState = 1'" : 2 == l.video_el.networkState ? "'self.video_el.networkState = 2'" : 3 == l.video_el.networkState ? "source not found <font color='#ff0000'>" + l.sourcePath_str + "</font>" : e, o.console && o.console.log(l.video_el.networkState), clearTimeout(l.showErrorWithDelayId_to), l.showErrorWithDelayId_to = setTimeout(function() {
                    l.dispatchEvent(i.ERROR, {
                        text: t
                    })
                }, 200)
            }, this.resizeAndPosition = function(e, t, o, s) {}, this.setSource = function(e) {
                l.sourcePath_str = e, t.is360 && l.video_el && (l.video_el.style.visibility = "hidden"), l.video_el && l.stop(), l.video_el && FWDMSPUtils.isIphone && (l.video_el.src = e)
            }, this.play = function(e) {
                if (clearTimeout(l.playWithDelayId_to), FWDMSP.curInstance = t, l.isStopped_bl) l.initVideo(), l.setVolume(), l.video_el.src = l.sourcePath_str, l.isMobile_bl ? l.play() : l.playWithDelayId_to = setTimeout(l.play, 1e3), l.hastStaredToPlayHLS_bl = !0, l.startToBuffer(!0), l.isPlaying_bl = !0;
                else if (!l.video_el.ended || e) try {
                    l.hastStaredToPlayHLS_bl = !0, l.isPlaying_bl = !0, l.hasPlayedOnce_bl = !0, l.video_el.play(), l.safeToBeControlled(), FWDMSPUtils.isIE && l.dispatchEvent(i.PLAY)
                } catch (e) {}
                t.is360 && l.add360Vid()
            }, this.initVideo = function() {
                l.isPlaying_bl = !1, l.hasError_bl = !1, l.allowScrubing_bl = !1, l.isStopped_bl = !1, l.setupVideo(), l.setVolume(), l.video_el.src = l.sourcePath_str
            }, this.pause = function() {
                if (null != l && !l.isStopped_bl && !l.hasError_bl && !l.video_el.ended) try {
                    l.video_el.pause(), l.isPlaying_bl = !1, FWDMSPUtils.isIE && l.dispatchEvent(i.PAUSE)
                } catch (e) {}
            }, this.togglePlayPause = function() {
                null != l && l.isSafeToBeControlled_bl && (l.isPlaying_bl ? l.pause() : l.play())
            }, this.resume = function() {
                l.isStopped_bl || l.play()
            }, this.pauseHandler = function() {
                l.allowScrubing_bl || l.dispatchEvent(i.PAUSE)
            }, this.playHandler = function() {
                l.allowScrubing_bl || (l.isStartEventDispatched_bl || (l.dispatchEvent(i.START), l.isStartEventDispatched_bl = !0), t.is360 && l.start360Render(), l.dispatchEvent(i.PLAY))
            }, this.endedHandler = function() {
                l.dispatchEvent(i.PLAY_COMPLETE)
            }, this.stop = function(e) {
                (null != l && null != l.video_el && !l.isStopped_bl || e) && (l.isPlaying_bl = !1, l.isStopped_bl = !0, l.hasPlayedOnce_bl = !0, l.hastStaredToPlayHLS_bl = !1, l.isSafeToBeControlled_bl = !1, l.isStartEventDispatched_bl = !1, clearTimeout(l.playWithDelayId_to), l.stop360Render(), l.destroyVideo(), l.dispatchEvent(i.LOAD_PROGRESS, {
                    percent: 0
                }), l.dispatchEvent(i.UPDATE_TIME, {
                    curTime: "00:00",
                    totalTime: "00:00"
                }), l.dispatchEvent(i.STOP), l.stopToBuffer())
            }, this.safeToBeControlled = function() {
                t.videoType_str == FWDMSP.HLS_JS && !l.hastStaredToPlayHLS_bl || (l.stopToScrub(), l.isSafeToBeControlled_bl || (l.hasHours_bl = 0 < Math.floor(l.video_el.duration / 3600), l.isPlaying_bl = !0, l.isSafeToBeControlled_bl = !0, t.is360 || (l.video_el.style.visibility = "visible"), setTimeout(function() {
                    l.renderer && (l.renderer.domElement.style.left = "0px")
                }, 1e3), l.dispatchEvent(i.SAFE_TO_SCRUBB)))
            }, this.updateProgress = function() {
                if (t.videoType_str != FWDMSP.HLS_JS || l.hastStaredToPlayHLS_bl) {
                    var e = 0;
                    0 < l.video_el.buffered.length && (e = l.video_el.buffered.end(l.video_el.buffered.length - 1).toFixed(1) / l.video_el.duration.toFixed(1), !isNaN(e) && e || (e = 0)), 1 == e && l.video_el.removeEventListener("progress", l.updateProgress), l.dispatchEvent(i.LOAD_PROGRESS, {
                        percent: e
                    })
                }
            }, this.updateVideo = function() {
                var e;
                l.allowScrubing_bl || (e = l.video_el.currentTime / l.video_el.duration, l.dispatchEvent(i.UPDATE, {
                    percent: e
                }));
                var t = i.formatTime(l.video_el.duration),
                    o = i.formatTime(l.video_el.currentTime);
                isNaN(l.video_el.duration) ? l.dispatchEvent(i.UPDATE_TIME, {
                    curTime: "00:00",
                    totalTime: "00:00",
                    seconds: 0,
                    totalTimeInSeconds: 0
                }) : l.dispatchEvent(i.UPDATE_TIME, {
                    curTime: o,
                    totalTime: t,
                    seconds: parseInt(l.video_el.currentTime),
                    totalTimeInSeconds: l.video_el.duration
                }), l.lastPercentPlayed = e, l.curDuration = o
            }, this.startToScrub = function() {
                l.allowScrubing_bl = !0
            }, this.stopToScrub = function() {
                l.allowScrubing_bl = !1
            }, this.scrubbAtTime = function(e) {
                l.video_el.currentTime = e;
                var t = i.formatTime(l.video_el.duration),
                    o = i.formatTime(l.video_el.currentTime);
                l.dispatchEvent(i.UPDATE_TIME, {
                    curTime: o,
                    totalTime: t
                })
            }, this.scrub = function(e, t) {
                t && l.startToScrub();
                try {
                    l.video_el.currentTime = l.video_el.duration * e;
                    var o = i.formatTime(l.video_el.duration),
                        s = i.formatTime(l.video_el.currentTime);
                    l.dispatchEvent(i.UPDATE_TIME, {
                        curTime: s,
                        totalTime: o
                    })
                } catch (t) {
                    console.log(t)
                }
            }, this.replay = function() {
                l.scrub(0), l.play()
            }, this.setVolume = function(e) {
                null != e && (l.volume = e), l.video_el && (l.video_el.volume = l.volume)
            }, this.setPlaybackRate = function(e) {
                l.video_el && (l.video_el.defaultPlaybackRate = e, l.video_el.playbackRate = e)
            }, this.add360Vid = function() {
                l.renderer ? l.screen.appendChild(l.renderer.domElement) : null != o.THREE && (l.renderer = new THREE.WebGLRenderer({
                    antialias: !0
                }), l.renderer.setSize(l.stageWidth, l.stageHeight), l.renderer.domElement.style.position = "absolute", l.renderer.domElement.style.left = "0px", l.renderer.domElement.style.top = "0px", l.renderer.domElement.style.margin = "0px", l.renderer.domElement.style.padding = "0px", l.renderer.domElement.style.maxWidth = "none", l.renderer.domElement.style.maxHeight = "none", l.renderer.domElement.style.border = "none", l.renderer.domElement.style.lineHeight = "1", l.renderer.domElement.style.backgroundColor = "transparent", l.renderer.domElement.style.backfaceVisibility = "hidden", l.renderer.domElement.style.webkitBackfaceVisibility = "hidden", l.renderer.domElement.style.MozBackfaceVisibility = "hidden", l.renderer.domElement.style.MozImageRendering = "optimizeSpeed", l.renderer.domElement.style.WebkitImageRendering = "optimizeSpeed", l.screen.appendChild(l.renderer.domElement), l.scene = new THREE.Scene, l.video_el.setAttribute("crossorigin", "anonymous"), l.canvas = document.createElement("canvas"), l.context = l.canvas.getContext("2d"), FWDMSPUtils.isFirefox ? l.videoTexture = new THREE.Texture(l.video_el) : l.videoTexture = new THREE.Texture(l.canvas), l.videoTexture.minFilter = THREE.LinearFilter, l.videoTexture.magFilter = THREE.LinearFilter, l.videoTexture.format = THREE.RGBFormat, l.cubeGeometry = new THREE.SphereGeometry(500, 60, 40), l.sphereMat = new THREE.MeshBasicMaterial({
                    map: l.videoTexture
                }), l.sphereMat.side = THREE.BackSide, l.cube = new THREE.Mesh(l.cubeGeometry, l.sphereMat), l.scene.add(l.cube), l.camera = new THREE.PerspectiveCamera(45, l.stageWidth / l.stageHeight, .1, 1e4), l.camera.position.y = 0, l.camera.position.z = 500, l.camera.position.x = 0, l.scene.add(l.camera), l.controls = new THREE.OrbitControls(l.camera, t.dumyClick_do.screen), l.controls.enableDamping = !0, l.controls.enableZoom = !1, l.controls.dampingFactor = .25, l.controls.maxDistance = 500, l.controls.minDistance = 500, l.controls.rotateLeft(90 * Math.PI / 180), l.controls.enabled = !0, l.render())
            }, this.start360Render = function() {
                l.is360Rendering_bl = !0, cancelAnimationFrame(l.requestId), l.requestId = requestAnimationFrame(l.render)
            }, this.stop360Render = function() {
                if (l.is360Rendering_bl = !1, l.camera) {
                    l.camera.position.y = 0, l.camera.position.z = 500, l.camera.position.x = 0, l.renderer.domElement.style.left = "-10000px", cancelAnimationFrame(l.requestId);
                    try {
                        l.screen.removeChild(l.renderer.domElement)
                    } catch (e) {}
                }
            }, this.render = function() {
                l.is360Rendering_bl && l.camera && t.is360 ? (l.video_el.readyState === l.video_el.HAVE_ENOUGH_DATA && (l.videoTexture.needsUpdate = !0), FWDMSPUtils.isFirefox || !l.context || l.isStopped_bl || (0 != l.video_el.videoWidth && (l.canvas.width = l.video_el.videoWidth, l.canvas.height = l.video_el.videoHeight), l.context.save(), l.context.scale(-1, 1), l.context.drawImage(l.video_el, 0, 0, -1 * l.canvas.width, l.canvas.height), l.context.restore()), l.controls.update(), l.renderer.render(l.scene, l.camera), l.requestId = requestAnimationFrame(l.render)) : cancelAnimationFrame(l.requestId)
            }, this.getDuration = function() {
                return i.formatTime(l.video_el.duration)
            }, this.getCurrentTime = function() {
                return i.formatTime(l.video_el.currentTime)
            }, i.formatTime = function(e) {
                var t = Math.floor(e / 3600),
                    o = e % 3600,
                    s = Math.floor(o / 60),
                    i = o % 60,
                    n = Math.ceil(i);
                return s = 10 <= s ? s : "0" + s, n = 10 <= n ? n : "0" + n, isNaN(n) ? "00:00" : l.hasHours_bl ? t + ":" + s + ":" + n : s + ":" + n
            }, this.init()
        };
        i.setPrototype = function() {
            i.prototype = new FWDMSPDisplayObject("div")
        }, i.ERROR = "error", i.UPDATE = "update", i.UPDATE_TIME = "updateTime", i.SAFE_TO_SCRUBB = "safeToControll", i.LOAD_PROGRESS = "loadProgress", i.START = "start", i.PLAY = "play", i.PAUSE = "pause", i.STOP = "stop", i.PLAY_COMPLETE = "playComplete", i.START_TO_BUFFER = "startToBuffer", i.STOP_TO_BUFFER = "stopToBuffer", o.FWDMSPVideoScreen = i
    }(window),
    function(e) {
        var s = function(t, e) {
            var l = this;
            s.prototype;
            this.videoHolder_do = null, this.ytb = null, this.lastQuality_str = "auto", this.volume = e, this.updateVideoId_int, this.updatePreloadId_int, this.controllerHeight = t.data.controllerHeight, this.hasHours_bl = !1, this.hasBeenCreatedOnce_bl = !1, this.allowScrubing_bl = !1, this.hasError_bl = !1, this.isPlaying_bl = !1, this.isStopped_bl = !0, this.isStartEventDispatched_bl = !1, this.isSafeToBeControlled_bl = !1, this.isPausedInEvent_bl = !0, this.isShowed_bl = !0, this.isReady_bl = !1, this.isQualityArrayDisapatched_bl = !1, this.isMobile_bl = FWDMSPUtils.isMobile, this.init = function() {
                l.getStyle().width = "100%", l.getStyle().height = "100%", l.hasTransform3d_bl = !1, l.hasTransform2d_bl = !1, l.setBkColor("#000000"), l.setBackfaceVisibility(), l.id = "youtubePlayer", t.main_do.addChild(l), l.resizeAndPosition(), l.setupVideo()
            }, this.setupVideo = function() {
                l.ytb || (l.videoHolder_do = new FWDMSPDisplayObject("div"), l.videoHolder_do.hasTransform3d_bl = !1, l.videoHolder_do.hasTransform2d_bl = !1, l.videoHolder_do.screen.setAttribute("id", t.instanceName_str + "youtube"), l.videoHolder_do.getStyle().width = "100%", l.videoHolder_do.getStyle().height = "100%", l.videoHolder_do.setBackfaceVisibility(), l.addChild(l.videoHolder_do), l.ytb = new YT.Player(t.instanceName_str + "youtube", {
                    width: "100%",
                    height: "100%",
                    playerVars: {
                        controls: 0,
                        disablekb: 0,
                        loop: 0,
                        autoplay: 0,
                        wmode: "opaque",
                        showinfo: 0,
                        rel: 0,
                        modestbranding: 1,
                        iv_load_policy: 3,
                        cc_load_policy: 0,
                        fs: 0,
                        html5: 0
                    },
                    events: {
                        onReady: l.playerReadyHandler,
                        onError: l.playerErrorHandler,
                        onStateChange: l.stateChangeHandler,
                        onPlaybackQualityChange: l.qualityChangeHandler
                    }
                }))
            }, this.playerReadyHandler = function() {
                l.isReady_bl = !0, l.resizeAndPosition(), l.dispatchEvent(s.READY), l.hasBeenCreatedOnce_bl = !0
            }, this.stateChangeHandler = function(e) {
                if (-1 == e.data && l.isCued_bl && l.isMobile_bl && (l.isStopped_bl = !1, FWDMSP.stopAllAudio(t)), e.data == YT.PlayerState.PLAYING) l.isSafeToBeControlled_bl || (l.isStopped_bl = !1, l.isSafeToBeControlled_bl = !0, l.isPlaying_bl = !0, l.hasHours_bl = 0 < Math.floor(l.ytb.getDuration() / 3600), l.setVolume(l.volume), l.startToUpdate(), l.startToPreload(), l.scrub(1e-5), l.isMobile_bl || l.setQuality(l.lastQuality_str), l.ytb.getAvailableQualityLevels() && 0 != l.ytb.getAvailableQualityLevels().length && l.dispatchEvent(s.QUALITY_CHANGE, {
                    qualityLevel: l.ytb.getPlaybackQuality(),
                    levels: l.ytb.getAvailableQualityLevels()
                }), l.setPlaybackRate(), l.dispatchEvent(s.SAFE_TO_SCRUBB)), l.isPausedInEvent_bl && l.dispatchEvent(s.PLAY), l.isPausedInEvent_bl = !1, l.hasError_bl = !1;
                else if (e.data == YT.PlayerState.PAUSED) {
                    if (!l.isSafeToBeControlled_bl) return;
                    l.isStopped_bl = !1, l.isPausedInEvent_bl || l.dispatchEvent(s.PAUSE), l.isPausedInEvent_bl = !0
                } else e.data == YT.PlayerState.ENDED ? l.ytb.getCurrentTime() && 0 < l.ytb.getCurrentTime() && (l.isStopped_bl = !1, setTimeout(function() {
                    l.dispatchEvent(s.PLAY_COMPLETE)
                }, 100)) : e.data == YT.PlayerState.CUED && (l.isStopped_bl || l.dispatchEvent(s.CUED), l.isCued_bl = !0, l.isStopped_bl = !1)
            }, this.qualityChangeHandler = function(e) {
                l.ytb.getAvailableQualityLevels() && 0 != l.ytb.getAvailableQualityLevels().length && l.dispatchEvent(s.QUALITY_CHANGE, {
                    qualityLevel: l.ytb.getPlaybackQuality()
                })
            }, this.playerErrorHandler = function(e) {
                if (l.isPausedInEvent_bl = !0, !l.isStopped_bl && !l.hasError_bl && l.isReady_bl) {
                    var t = "";
                    l.hasError_bl = !0, console.log(e.data), 2 == e.data ? t = "The youtube id is not well formatted, make sure it has exactly 11 characters and that it dosn't contain invalid characters such as exclamation points or asterisks." : 5 == e.data ? t = "The requested content cannot be played in an HTML5 player or another error related to the HTML5 player has occurred." : 100 == e.data ? t = "The youtube video request was not found, probably the video ID is incorrect." : 101 != e.data && 150 != e.data || (t = "The owner of the requested video does not allow it to be played in embedded players."), l.dispatchEvent(s.ERROR, {
                        text: t
                    })
                }
            }, this.resizeAndPosition = function() {}, this.setSource = function(e) {
                e && (l.sourcePath_str = e), l.ytb.cueVideoById(l.sourcePath_str), l.isStopped_bl = !1
            }, this.play = function(e) {
                FWDMSP.curInstance = t, l.isPlaying_bl = !0, l.hasError_bl = !1;
                try {
                    l.ytb.playVideo(), l.startToUpdate()
                } catch (e) {}
                l.isStopped_bl = !1
            }, this.pause = function() {
                if (!l.isStopped_bl && !l.hasError_bl) {
                    l.isPlaying_bl = !1;
                    try {
                        l.ytb.pauseVideo()
                    } catch (e) {}
                    l.stopToUpdate()
                }
            }, this.togglePlayPause = function() {
                l.isPlaying_bl ? l.pause() : l.play()
            }, this.resume = function() {
                l.isStopped_bl || l.play()
            }, this.togglePlayPause = function() {
                l.isPlaying_bl ? l.pause() : l.play()
            }, this.startToUpdate = function() {
                clearInterval(l.updateVideoId_int), l.updateVideoId_int = setInterval(l.updateVideo, 500)
            }, this.stopToUpdate = function() {
                clearInterval(l.updateVideoId_int)
            }, this.updateVideo = function() {
                var e;
                if (l.ytb) {
                    l.allowScrubing_bl || (e = l.ytb.getCurrentTime() / l.ytb.getDuration(), l.dispatchEvent(s.UPDATE, {
                        percent: e
                    }));
                    var t = l.formatTime(l.ytb.getDuration()),
                        o = l.formatTime(l.ytb.getCurrentTime());
                    l.lastPercentPlayed = e, l.dispatchEvent(s.UPDATE_TIME, {
                        curTime: o,
                        totalTime: t,
                        seconds: Math.round(l.ytb.getCurrentTime()),
                        totalTimeInSeconds: l.ytb.getDuration()
                    })
                } else stopToUpdate()
            }, this.getDuration = function() {
                return l.formatTime(l.ytb.getDuration())
            }, this.getCurrentTime = function() {
                return l.formatTime(l.ytb.getCurrentTime())
            }, this.startToPreload = function() {
                clearInterval(l.preloadVideoId_int), l.updatePreloadId_int = setInterval(l.updateProgress, 500)
            }, this.stopToPreload = function() {
                clearInterval(l.updatePreloadId_int)
            }, this.updateProgress = function() {
                if (l.ytb) {
                    var e = l.ytb.getVideoLoadedFraction();
                    l.dispatchEvent(s.LOAD_PROGRESS, {
                        percent: e
                    })
                } else stopToPreload()
            }, this.stop = function() {
                l.isStopped_bl || (l.isPlaying_bl = !1, l.isStopped_bl = !0, l.isCued_bl = !1, l.allowScrubing_bl = !1, l.isSafeToBeControlled_bl = !1, l.isQualityArrayDisapatched_bl = !1, l.isPausedInEvent_bl = !0, l.stopToUpdate(), l.stopToPreload(), l.stopVideo(), l.dispatchEvent(s.STOP), l.dispatchEvent(s.LOAD_PROGRESS, {
                    percent: 0
                }), l.dispatchEvent(s.UPDATE_TIME, {
                    curTime: "00:00",
                    totalTime: "00:00"
                }))
            }, this.destroyYoutube = function() {
                l.videoHolder_do && (l.videoHolder_do.screen.removeAttribute("id", t.instanceName_str + "youtube"), l.videoHolder_do.destroy(), l.videoHolder_do = null), l.ytb && l.ytb.destroy(), l.ytb = null
            }, this.stopVideo = function() {
                l.ytb.cueVideoById(l.sourcePath_str)
            }, this.startToScrub = function() {
                l.isSafeToBeControlled_bl && (l.allowScrubing_bl = !0)
            }, this.stopToScrub = function() {
                l.isSafeToBeControlled_bl && (l.allowScrubing_bl = !1)
            }, this.scrubbAtTime = function(e) {
                l.isSafeToBeControlled_bl && l.ytb.seekTo(e)
            }, this.scrub = function(e) {
                l.isSafeToBeControlled_bl && l.ytb.seekTo(e * l.ytb.getDuration())
            }, this.setVolume = function(e) {
                l.ytb && (null != e && (l.volume = e), l.ytb && l.ytb.setVolume(100 * e))
            }, this.setQuality = function(e) {
                l.lastQuality_str = e, l.ytb.setPlaybackQuality(e)
            }, this.formatTime = function(e) {
                var t = Math.floor(e / 3600),
                    o = e % 3600,
                    s = Math.floor(o / 60),
                    i = o % 60,
                    n = Math.ceil(i);
                return s = 10 <= s ? s : "0" + s, n = 10 <= n ? n : "0" + n, isNaN(n) ? "00:00" : l.hasHours_bl ? t + ":" + s + ":" + n : s + ":" + n
            }, this.setPlaybackRate = function(e) {
                l.ytb && !l.isMobile_bl && (e && (l.rate = e), l.ytb.setPlaybackRate(l.rate))
            }, this.init()
        };
        s.setPrototype = function() {
            s.prototype = new FWDMSPDisplayObject("div")
        }, s.READY = "ready", s.ERROR = "error", s.UPDATE = "update", s.UPDATE_TIME = "updateTime", s.SAFE_TO_SCRUBB = "safeToControll", s.LOAD_PROGRESS = "loadProgress", s.PLAY = "play", s.PAUSE = "pause", s.STOP = "stop", s.PLAY_COMPLETE = "playComplete", s.CUED = "cued", s.QUALITY_CHANGE = "qualityChange", e.FWDMSPYoutubeScreen = s
    }(window);
