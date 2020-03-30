
function A(e, t, n) {
    var r = t || 0,
        i = 0;
    "string" == typeof e ? (i = n || e.length, this.a = function(t) {
        return e.charCodeAt(t + r) & 255
    }) : "unknown" == typeof e && (i = n || IEBinary_getLength(e), this.a = function(t) {
        return IEBinary_getByteAt(e, t + r)
    });
    this.l = function(e, t) {
        for (var n = Array(t), r = 0; r < t; r++) n[r] = this.a(e + r);
        return n
    };
    this.h = function() {
        return i
    };
    this.d = function(e, t) {
        return 0 != (this.a(e) & 1 << t)
    };
    this.w = function(e) {
        e = (this.a(e + 1) << 8) + this.a(e);
        0 > e && (e += 65536);
        return e
    };
    this.i = function(e) {
        var t = this.a(e),
            n = this.a(e + 1),
            r = this.a(e + 2);
        e = this.a(e + 3);
        t = (((t << 8) + n << 8) + r << 8) + e;
        0 > t && (t += 4294967296);
        return t
    };
    this.o = function(e) {
        var t = this.a(e),
            n = this.a(e + 1);
        e = this.a(e + 2);
        t = ((t << 8) + n << 8) + e;
        0 > t && (t += 16777216);
        return t
    };
    this.c = function(e, t) {
        for (var n = [], r = e, i = 0; r < e + t; r++, i++) n[i] = String.fromCharCode(this.a(r));
        return n.join("")
    };
    this.e = function(e, t, n) {
        e = this.l(e, t);
        switch (n.toLowerCase()) {
            case "utf-16":
            case "utf-16le":
            case "utf-16be":
                t = n;
                var r, i = 0,
                    s = 1;
                n = 0;
                r = Math.min(r || e.length, e.length);
                254 == e[0] && 255 == e[1] ? (t = !0, i = 2) : 255 == e[0] && 254 == e[1] && (t = !1, i = 2);
                t && (s = 0, n = 1);
                t = [];
                for (var o = 0; i < r; o++) {
                    var u = e[i + s],
                        a = (u << 8) + e[i + n],
                        i = i + 2;
                    if (0 == a) break;
                    else 216 > u || 224 <= u ? t[o] = String.fromCharCode(a) : (u = (e[i + s] << 8) + e[i + n], i += 2, t[o] = String.fromCharCode(a, u))
                }
                e = new String(t.join(""));
                e.g = i;
                break;
            case "utf-8":
                r = 0;
                i = Math.min(i || e.length, e.length);
                239 == e[0] && 187 == e[1] && 191 == e[2] && (r = 3);
                s = [];
                for (n = 0; r < i && (t = e[r++], 0 != t); n++) 128 > t ? s[n] = String.fromCharCode(t) : 194 <= t && 224 > t ? (o = e[r++], s[n] = String.fromCharCode(((t & 31) << 6) + (o & 63))) : 224 <= t && 240 > t ? (o = e[r++], a = e[r++], s[n] = String.fromCharCode(((t & 255) << 12) + ((o & 63) << 6) + (a & 63))) : 240 <= t && 245 > t && (o = e[r++], a = e[r++], u = e[r++], t = ((t & 7) << 18) + ((o & 63) << 12) + ((a & 63) << 6) + (u & 63) - 65536, s[n] = String.fromCharCode((t >> 10) + 55296, (t & 1023) + 56320));
                e = new String(s.join(""));
                e.g = r;
                break;
            default:
                i = [];
                s = s || e.length;
                for (r = 0; r < s;) {
                    n = e[r++];
                    if (0 == n) break;
                    i[r - 1] = String.fromCharCode(n)
                }
                e = new String(i.join(""));
                e.g = r
        }
        return e
    };
    this.f = function(e, t) {
        t()
    }
}

function B(e, t, n) {
    function r(e, t, n, r, s, o) {
        var u = i();
        u ? ("undefined" === typeof o && (o = !0), t && ("undefined" != typeof u.onload ? u.onload = function() {
            "200" == u.status || "206" == u.status ? (u.fileSize = s || u.getResponseHeader("Content-Length"), t(u)) : n && n();
            u = null
        } : u.onreadystatechange = function() {
            4 == u.readyState && ("200" == u.status || "206" == u.status ? (u.fileSize = s || u.getResponseHeader("Content-Length"), t(u)) : n && n(), u = null)
        }), u.open("GET", e, o), u.overrideMimeType && u.overrideMimeType("text/plain; charset=x-user-defined"), r && u.setRequestHeader("Range", "bytes=" + r[0] + "-" + r[1]), u.setRequestHeader("If-Modified-Since", "Sat, 1 Jan 1970 00:00:00 GMT"), u.send(null)) : n && n()
    }

    function i() {
        var e = null;
        window.XMLHttpRequest ? e = new XMLHttpRequest : window.ActiveXObject && (e = new ActiveXObject("Microsoft.XMLHTTP"));
        return e
    }

    function s(e, t) {
        var n = i();
        n && (t && ("undefined" != typeof n.onload ? n.onload = function() {
            "200" == n.status && t(this);
            n = null
        } : n.onreadystatechange = function() {
            4 == n.readyState && ("200" == n.status && t(this), n = null)
        }), n.open("HEAD", e, !0), n.send(null))
    }

    function o(e, t) {
        function o(e) {
            var t = ~~(e[0] / i) - s;
            e = ~~(e[1] / i) + 1 + s;
            0 > t && (t = 0);
            e >= blockTotal && (e = blockTotal - 1);
            return [t, e]
        }

        function u(s, o) {
            for (; l[s[0]];)
                if (s[0]++, s[0] > s[1]) {
                    o && o();
                    return
                } for (; l[s[1]];)
                if (s[1]--, s[0] > s[1]) {
                    o && o();
                    return
                } var u = [s[0] * i, (s[1] + 1) * i - 1];
            r(e, function(e) {
                parseInt(e.getResponseHeader("Content-Length"), 10) == t && (s[0] = 0, s[1] = blockTotal - 1, u[0] = 0, u[1] = t - 1);
                e = {
                    data: e.N || e.responseText,
                    offset: u[0]
                };
                for (var n = s[0]; n <= s[1]; n++) l[n] = e;
                o && o()
            }, n, u, a, !!o)
        }
        var i, s;
        var a, f = new A("", 0, t),
            l = [];
        i = i || 2048;
        s = "undefined" === typeof s ? 0 : s;
        blockTotal = ~~((t - 1) / i) + 1;
        for (var c in f) f.hasOwnProperty(c) && "function" === typeof f[c] && (this[c] = f[c]);
        this.a = function(e) {
            var t;
            u(o([e, e]));
            t = l[~~(e / i)];
            if ("string" == typeof t.data) return t.data.charCodeAt(e - t.offset) & 255;
            if ("unknown" == typeof t.data) return IEBinary_getByteAt(t.data, e - t.offset)
        };
        this.f = function(e, t) {
            u(o(e), t)
        }
    }(function() {
        s(e, function(n) {
            n = parseInt(n.getResponseHeader("Content-Length"), 10) || -1;
            t(new o(e, n))
        })
    })()
}(function(e) {
    function n() {
        var e = ["transform", "msTransform", "WebkitTransform", "MozTransform", "OTransform", "KhtmlTransform"];
        var n;
        var r;
        while (n = e.shift()) {
            if (typeof t.dumy.style[n] !== "undefined") {
                t.dumy.style.position = "absolute";
                r = t.dumy.getBoundingClientRect().left;
                t.dumy.style[n] = "translate3d(500px, 0px, 0px)";
                r = Math.abs(t.dumy.getBoundingClientRect().left - r);
                if (r > 100 && r < 900) {
                    try {
                        document.documentElement.removeChild(t.dumy)
                    } catch (i) {}
                    return true
                }
            }
        }
        try {
            document.documentElement.removeChild(t.dumy)
        } catch (i) {}
        return false
    }

    function r() {
        var e = ["transform", "msTransform", "WebkitTransform", "MozTransform", "OTransform", "KhtmlTransform"];
        var n;
        while (n = e.shift()) {
            if (typeof t.dumy.style[n] !== "undefined") {
                return true
            }
        }
        try {
            document.documentElement.removeChild(t.dumy)
        } catch (r) {}
        return false
    }
    var t = function() {};
    t.dumy = document.createElement("div");
    t.trim = function(e) {
        return e.replace(/\s/gi, "")
    };
    t.splitAndTrim = function(e, n) {
        var r = e.split(",");
        var i = r.length;
        for (var s = 0; s < i; s++) {
            if (n) r[s] = t.trim(r[s])
        }
        return r
    };
    t.indexOfArray = function(e, t) {
        var n = e.length;
        for (var r = 0; r < n; r++) {
            if (e[r] === t) return r
        }
        return -1
    };
    t.randomizeArray = function(e) {
        var t = [];
        var n = e.concat();
        var r = n.length;
        for (var i = 0; i < r; i++) {
            var s = Math.floor(Math.random() * n.length);
            t.push(n[s]);
            n.splice(s, 1)
        }
        return t
    };
    t.parent = function(e, t) {
        if (t === undefined) t = 1;
        while (t-- && e) e = e.parentNode;
        if (!e || e.nodeType !== 1) return null;
        return e
    };
    t.sibling = function(e, t) {
        while (e && t !== 0) {
            if (t > 0) {
                if (e.nextElementSibling) {
                    e = e.nextElementSibling
                } else {
                    for (var e = e.nextSibling; e && e.nodeType !== 1; e = e.nextSibling);
                }
                t--
            } else {
                if (e.previousElementSibling) {
                    e = e.previousElementSibling
                } else {
                    for (var e = e.previousSibling; e && e.nodeType !== 1; e = e.previousSibling);
                }
                t++
            }
        }
        return e
    };
    t.getChildAt = function(e, n) {
        var r = t.getChildren(e);
        if (n < 0) n += r.length;
        if (n < 0) return null;
        return r[n]
    };
    t.getChildById = function(e) {
        return document.getElementById(e) || undefined
    };
    t.getChildren = function(e, t) {
        var n = [];
        for (var r = e.firstChild; r != null; r = r.nextSibling) {
            if (t) {
                n.push(r)
            } else if (r.nodeType === 1) {
                n.push(r)
            }
        }
        return n
    };
    t.getChildrenFromAttribute = function(e, n, r) {
        var i = [];
        for (var s = e.firstChild; s != null; s = s.nextSibling) {
            if (r && t.hasAttribute(s, n)) {
                i.push(s)
            } else if (s.nodeType === 1 && t.hasAttribute(s, n)) {
                i.push(s)
            }
        }
        return i.length == 0 ? undefined : i
    };
    t.getChildFromNodeListFromAttribute = function(e, n, r) {
        for (var i = e.firstChild; i != null; i = i.nextSibling) {
            if (r && t.hasAttribute(i, n)) {
                return i
            } else if (i.nodeType === 1 && t.hasAttribute(i, n)) {
                return i
            }
        }
        return undefined
    };
    t.getAttributeValue = function(e, n) {
        if (!t.hasAttribute(e, n)) return undefined;
        return e.getAttribute(n)
    };
    t.hasAttribute = function(e, t) {
        if (e.hasAttribute) {
            return e.hasAttribute(t)
        } else {
            var n = e.getAttribute(t);
            return n ? true : false
        }
    };
    t.insertNodeAt = function(e, n, r) {
        var i = t.children(e);
        if (r < 0 || r > i.length) {
            throw new Error("invalid index!")
        } else {
            e.insertBefore(n, i[r])
        }
    };
    t.hasCanvas = function() {
        return Boolean(document.createElement("canvas"))
    };
    t.hitTest = function(e, t, n) {
        var r = false;
        if (!e) throw Error("Hit test target is null!");
        var i = e.getBoundingClientRect();
        if (t >= i.left && t <= i.left + (i.right - i.left) && n >= i.top && n <= i.top + (i.bottom - i.top)) return true;
        return false
    };
    t.getScrollOffsets = function() {
        if (e.pageXOffset != null) return {
            x: e.pageXOffset,
            y: e.pageYOffset
        };
        if (document.compatMode == "CSS1Compat") {
            return {
                x: document.documentElement.scrollLeft,
                y: document.documentElement.scrollTop
            }
        }
    };
    t.getViewportSize = function() {
        if (t.hasPointerEvent && navigator.msMaxTouchPoints > 1) {
            return {
                w: document.documentElement.clientWidth || e.innerWidth,
                h: document.documentElement.clientHeight || e.innerHeight
            }
        }
        if (t.isMobile) return {
            w: e.innerWidth,
            h: e.innerHeight
        };
        return {
            w: document.documentElement.clientWidth || e.innerWidth,
            h: document.documentElement.clientHeight || e.innerHeight
        }
    };
    t.getViewportMouseCoordinates = function(e) {
        var n = t.getScrollOffsets();
        if (e.touches) {
            return {
                screenX: e.touches[0] == undefined ? e.touches.pageX - n.x : e.touches[0].pageX - n.x,
                screenY: e.touches[0] == undefined ? e.touches.pageY - n.y : e.touches[0].pageY - n.y
            }
        }
        return {
            screenX: e.clientX == undefined ? e.pageX - n.x : e.clientX,
            screenY: e.clientY == undefined ? e.pageY - n.y : e.clientY
        }
    };
    t.hasPointerEvent = function() {
        return Boolean(e.navigator.msPointerEnabled)
    }();
    t.isMobile = function() {
        if (t.hasPointerEvent && navigator.msMaxTouchPoints > 1) return true;
        var e = ["android", "webos", "iphone", "ipad", "blackberry"];
        for (i in e) {
            if (navigator.userAgent.toLowerCase().indexOf(String(e[i]).toLowerCase()) != -1) {
                return true
            }
        }
        return false
    }();
    t.isAndroid = function() {
        return navigator.userAgent.toLowerCase().indexOf("android".toLowerCase()) != -1
    }();
    t.isChrome = function() {
        return navigator.userAgent.toLowerCase().indexOf("chrome") != -1
    }();
    t.isSafari = function() {
        return navigator.userAgent.toLowerCase().indexOf("safari") != -1 && navigator.userAgent.toLowerCase().indexOf("chrome") == -1
    }();
    t.isOpera = function() {
        return navigator.userAgent.toLowerCase().indexOf("opera") != -1 && navigator.userAgent.toLowerCase().indexOf("chrome") == -1
    }();
    t.isFirefox = function() {
        return navigator.userAgent.toLowerCase().indexOf("firefox") != -1
    }();
    t.isIE = function() {
        var e = navigator.userAgent.toLowerCase().indexOf("msie") != -1;
        return e || Boolean(!t.isIE && document.documentElement.msRequestFullscreen)
    }();
    t.isIE11 = function() {
        return Boolean(!t.isIE && document.documentElement.msRequestFullscreen)
    }();
    t.isIEAndLessThen9 = function() {
        return navigator.userAgent.toLowerCase().indexOf("msie 7") != -1 || navigator.userAgent.toLowerCase().indexOf("msie 8") != -1
    }();
    t.isIEAndLessThen10 = function() {
        return navigator.userAgent.toLowerCase().indexOf("msie 7") != -1 || navigator.userAgent.toLowerCase().indexOf("msie 8") != -1 || navigator.userAgent.toLowerCase().indexOf("msie 9") != -1
    }();
    t.isIE7 = function() {
        return navigator.userAgent.toLowerCase().indexOf("msie 7") != -1
    }();
    t.isApple = function() {
        return navigator.appVersion.toLowerCase().indexOf("mac") != -1
    }();
    t.hasFullScreen = function() {
        return t.dumy.requestFullScreen || t.dumy.mozRequestFullScreen || t.dumy.webkitRequestFullScreen || t.dumy.msieRequestFullScreen
    }();
    t.onReady = function(e) {
        if (document.addEventListener) {
            document.addEventListener("DOMContentLoaded", function() {
                t.checkIfHasTransofrms();
                e()
            })
        } else {
            document.onreadystatechange = function() {
                t.checkIfHasTransofrms();
                if (document.readyState == "complete") e()
            }
        }
    };
    t.checkIfHasTransofrms = function() {
        document.documentElement.appendChild(t.dumy);
        t.hasTransform3d = n();
        t.hasTransform2d = r();
        t.isReadyMethodCalled_bl = true
    };
    t.disableElementSelection = function(e) {
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
            return false
        }
    };
    t.getUrlArgs = function(t) {
        var n = {};
        var r = t.substr(t.indexOf("?") + 1) || location.search.substring(1);
        var i = r.split("&");
        for (var s = 0; s < i.length; s++) {
            var o = i[s].indexOf("=");
            var u = i[s].substring(0, o);
            var a = i[s].substring(o + 1);
            a = decodeURIComponent(a);
            n[u] = a
        }
        return n
    };
    t.isReadyMethodCalled_bl = false;
    e.MUSICUtils = t
})(window);
(function(e) {
    var t = function() {
        var n = this;
        var r = t.prototype;
        this.main_do = null;
        this.init = function() {
            this.setupScreen();
            e.onerror = this.showError;
            this.screen.style.zIndex = 100000009;
            this.screen.classList.add("screeeen");
            setTimeout(this.addConsoleToDom, 100);
            setInterval(this.position, 100)
        };
        this.position = function() {
            var e = MUSICUtils.getScrollOffsets();
            n.setX(e.x + 100);
            n.setY(e.y)
        };
        this.addConsoleToDom = function() {
            if (navigator.userAgent.toLowerCase().indexOf("msie 7") != -1) {
                document.getElementsByTagName("body")[0].appendChild(n.screen)
            } else {
                document.documentElement.appendChild(n.screen)
            }
        };
        this.setupScreen = function() {
            this.main_do = new MUSICDisplayObject("div", "absolute");
            this.main_do.setOverflow("auto");
            this.main_do.setWidth(200);
            this.main_do.setHeight(300);
            this.setWidth(200);
            this.setHeight(300);
            this.main_do.setBkColor("#FFFFFF");
            this.addChild(this.main_do)
        };
        this.showError = function(e, t, r) {
            var i = n.main_do.getInnerHTML() + "<br>" + "JavaScript error: " + e + " on line " + r + " for " + t;
            n.main_do.setInnerHTML(i);
            n.main_do.screen.scrollTop = n.main_do.screen.scrollHeight
        };
        this.log = function(e) {
            var t = n.main_do.getInnerHTML() + "<br>" + e;
            n.main_do.setInnerHTML(t);
            n.main_do.getScreen().scrollTop = 1e4
        };
        this.init()
    };
    t.setPrototype = function() {
        t.prototype = new MUSICDisplayObject("div", "absolute")
    };
    t.prototype = null;
    e.FWDConsole = t
})(window);
if (typeof asual == "undefined") {
    var asual = {}
}
if (typeof asual.util == "undefined") {
    asual.util = {}
}
asual.util.Browser = new function() {
    var e = navigator.userAgent.toLowerCase(),
        t = /webkit/.test(e),
        n = /opera/.test(e),
        r = /msie/.test(e) && !/opera/.test(e),
        i = /mozilla/.test(e) && !/(compatible|webkit)/.test(e),
        s = parseFloat(r ? e.substr(e.indexOf("msie") + 4) : (e.match(/.+(?:rv|it|ra|ie)[\/: ]([\d.]+)/) || [0, "0"])[1]);
    this.toString = function() {
        return "[class Browser]"
    };
    this.getVersion = function() {
        return s
    };
    this.isMSIE = function() {
        return r
    };
    this.isSafari = function() {
        return t
    };
    this.isOpera = function() {
        return n
    };
    this.isMozilla = function() {
        return i
    }
};
asual.util.Events = new function() {
    var e = "DOMContentLoaded",
        t = "onstop",
        n = window,
        r = document,
        i = [],
        s = asual.util,
        o = s.Browser,
        u = o.isMSIE(),
        a = o.isSafari();
    this.toString = function() {
        return "[class Events]"
    };
    this.addListener = function(t, n, r) {
        i.push({
            o: t,
            t: n,
            l: r
        });
        if (!(n == e && (u || a))) {
            if (t.addEventListener) {
                t.addEventListener(n, r, false)
            } else {
                if (t.attachEvent) {
                    t.attachEvent("on" + n, r)
                }
            }
        }
    };
    this.removeListener = function(t, n, r) {
        for (var s = 0, o; o = i[s]; s++) {
            if (o.o == t && o.t == n && o.l == r) {
                i.splice(s, 1);
                break
            }
        }
        if (!(n == e && (u || a))) {
            if (t.removeEventListener) {
                t.removeEventListener(n, r, false)
            } else {
                if (t.detachEvent) {
                    t.detachEvent("on" + n, r)
                }
            }
        }
    };
    var f = function() {
        for (var t = 0, n; n = i[t]; t++) {
            if (n.t != e) {
                s.Events.removeListener(n.o, n.t, n.l)
            }
        }
    };
    var l = function() {
        if (r.readyState == "interactive") {
            function e() {
                r.detachEvent(t, e);
                f()
            }
            r.attachEvent(t, e);
            n.setTimeout(function() {
                r.detachEvent(t, e)
            }, 0)
        }
    };
    if (u || a) {
        (function() {
            try {
                if (u && r.body || !/loaded|complete/.test(r.readyState)) {
                    r.documentElement.doScroll("left")
                }
            } catch (t) {
                return setTimeout(arguments.callee, 0)
            }
            for (var n = 0, t; t = i[n]; n++) {
                if (t.t == e) {
                    t.l.call(null)
                }
            }
        })()
    }
    if (u) {
        n.attachEvent("onbeforeunload", l)
    }
    this.addListener(n, "unload", f)
};
asual.util.Functions = new function() {
    this.toString = function() {
        return "[class Functions]"
    };
    this.bind = function(e, t, n) {
        for (var r = 2, i, s = []; i = arguments[r]; r++) {
            s.push(i)
        }
        return function() {
            return e.apply(t, s)
        }
    }
};
var FWDAddressEvent = function(e) {
    this.toString = function() {
        return "[object FWDAddressEvent]"
    };
    this.type = e;
    this.target = [FWDAddress][0];
    this.value = FWDAddress.getValue();
    this.path = FWDAddress.getPath();
    this.pathNames = FWDAddress.getPathNames();
    this.parameters = {};
    var t = FWDAddress.getParameterNames();
    for (var n = 0, r = t.length; n < r; n++) {
        this.parameters[t[n]] = FWDAddress.getParameter(t[n])
    }
    this.parameterNames = t
};
FWDAddressEvent.INIT = "init";
FWDAddressEvent.CHANGE = "change";
FWDAddressEvent.INTERNAL_CHANGE = "internalChange";
FWDAddressEvent.EXTERNAL_CHANGE = "externalChange";
var FWDAddress = new function() {
    var _getHash = function() {
        var e = _l.href.indexOf("#");
        return e != -1 ? _ec(_dc(_l.href.substr(e + 1))) : ""
    };
    var _getWindow = function() {
        try {
            top.document;
            return top
        } catch (e) {
            return window
        }
    };
    var _strictCheck = function(e, t) {
        if (_opts.strict) {
            e = t ? e.substr(0, 1) != "/" ? "/" + e : e : e == "" ? "/" : e
        }
        return e
    };
    var _ieLocal = function(e, t) {
        return _msie && _l.protocol == "file:" ? t ? _value.replace(/\?/, "%3F") : _value.replace(/%253F/, "?") : e
    };
    var _searchScript = function(e) {
        if (e.childNodes) {
            for (var t = 0, n = e.childNodes.length, r; t < n; t++) {
                if (e.childNodes[t].src) {
                    _url = String(e.childNodes[t].src)
                }
                if (r = _searchScript(e.childNodes[t])) {
                    return r
                }
            }
        }
    };
    var _titleCheck = function() {
        if (_d.title != _title && _d.title.indexOf("#") != -1) {
            _d.title = _title
        }
    };
    var _listen = function() {
        if (!_silent) {
            var e = _getHash();
            var t = !(_value == e);
            if (_safari && _version < 523) {
                if (_length != _h.length) {
                    _length = _h.length;
                    if (typeof _stack[_length - 1] != UNDEFINED) {
                        _value = _stack[_length - 1]
                    }
                    _update.call(this, false)
                }
            } else {
                if (_msie && t) {
                    if (_version < 7) {
                        _l.reload()
                    } else {
                        this.setValue(e)
                    }
                } else {
                    if (t) {
                        _value = e;
                        _update.call(this, false)
                    }
                }
            }
            if (_msie) {
                _titleCheck.call(this)
            }
        }
    };
    var _bodyClick = function(e) {
        if (_popup.length > 0) {
            var popup = window.open(_popup[0], _popup[1], eval(_popup[2]));
            if (typeof _popup[3] != UNDEFINED) {
                eval(_popup[3])
            }
        }
        _popup = []
    };
    var _swfChange = function() {
        for (var e = 0, t, n, r = FWDAddress.getValue(), i = "setFWDAddressValue"; t = _ids[e]; e++) {
            n = document.getElementById(t);
            if (n) {
                if (n.parentNode && typeof n.parentNode.so != UNDEFINED) {
                    n.parentNode.so.call(i, r)
                } else {
                    if (!(n && typeof n[i] != UNDEFINED)) {
                        var s = n.getElementsByTagName("object");
                        var o = n.getElementsByTagName("embed");
                        n = s[0] && typeof s[0][i] != UNDEFINED ? s[0] : o[0] && typeof o[0][i] != UNDEFINED ? o[0] : null
                    }
                    if (n) {
                        n[i](r)
                    }
                }
            } else {
                if (n = document[t]) {
                    if (typeof n[i] != UNDEFINED) {
                        n[i](r)
                    }
                }
            }
        }
    };
    var _jsDispatch = function(e) {
        this.dispatchEvent(new FWDAddressEvent(e));
        e = e.substr(0, 1).toUpperCase() + e.substr(1);
        if (typeof this["on" + e] == FUNCTION) {
            this["on" + e]()
        }
    };
    var _jsInit = function() {
        if (_util.Browser.isSafari()) {
            _d.body.addEventListener("click", _bodyClick)
        }
        _jsDispatch.call(this, "init")
    };
    var _jsChange = function() {
        _swfChange();
        _jsDispatch.call(this, "change")
    };
    var _update = function(e) {
        _jsChange.call(this);
        if (e) {
            _jsDispatch.call(this, "internalChange")
        } else {
            _jsDispatch.call(this, "externalChange")
        }
        _st(_functions.bind(_track, this), 10)
    };
    var _track = function() {
        var e = (_l.pathname + (/\/$/.test(_l.pathname) ? "" : "/") + this.getValue()).replace(/\/\//, "/").replace(/^\/$/, "");
        var t = _t[_opts.tracker];
        if (typeof t == FUNCTION) {
            t(e)
        } else {
            if (typeof _t.pageTracker != UNDEFINED && typeof _t.pageTracker._trackPageview == FUNCTION) {
                _t.pageTracker._trackPageview(e)
            } else {
                if (typeof _t.urchinTracker == FUNCTION) {
                    _t.urchinTracker(e)
                }
            }
        }
    };
    var _htmlWrite = function() {
        var e = _frame.contentWindow.document;
        e.open();
        e.write("<html><head><title>" + _d.title + "</title><script>var " + ID + ' = "' + _getHash() + '";</script></head></html>');
        e.close()
    };
    var _htmlLoad = function() {
        var e = _frame.contentWindow;
        var t = e.location.href;
        _value = typeof e[ID] != UNDEFINED ? e[ID] : "";
        if (_value != _getHash()) {
            _update.call(FWDAddress, false);
            _l.hash = _ieLocal(_value, TRUE)
        }
    };
    var _load = function() {
        if (!_loaded) {
            _loaded = TRUE;
            if (_msie && _version < 8) {
                var e = _d.getElementsByTagName("frameset")[0];
                _frame = _d.createElement((e ? "" : "i") + "frame");
                if (e) {
                    e.insertAdjacentElement("beforeEnd", _frame);
                    e[e.cols ? "cols" : "rows"] += ",0";
                    _frame.src = "javascript:false";
                    _frame.noResize = true;
                    _frame.frameBorder = _frame.frameSpacing = 0
                } else {
                    _frame.src = "javascript:false";
                    _frame.style.display = "none";
                    _d.body.insertAdjacentElement("afterBegin", _frame)
                }
                _st(function() {
                    _events.addListener(_frame, "load", _htmlLoad);
                    if (typeof _frame.contentWindow[ID] == UNDEFINED) {
                        _htmlWrite()
                    }
                }, 50)
            } else {
                if (_safari) {
                    if (_version < 418) {
                        _d.body.innerHTML += '<form id="' + ID + '" style="position:absolute;top:-9999px;" method="get"></form>';
                        _form = _d.getElementById(ID)
                    }
                    if (typeof _l[ID] == UNDEFINED) {
                        _l[ID] = {}
                    }
                    if (typeof _l[ID][_l.pathname] != UNDEFINED) {
                        _stack = _l[ID][_l.pathname].split(",")
                    }
                }
            }
            _st(_functions.bind(function() {
                _jsInit.call(this);
                _jsChange.call(this);
                _track.call(this)
            }, this), 1);
            if (_msie && _version >= 8) {
                _d.body.onhashchange = _functions.bind(_listen, this);
                _si(_functions.bind(_titleCheck, this), 50)
            } else {
                _si(_functions.bind(_listen, this), 50)
            }
        }
    };
    var ID = "swfaddress",
        FUNCTION = "function",
        UNDEFINED = "undefined",
        TRUE = true,
        FALSE = false,
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
    if (_msie && _d.documentMode && _d.documentMode != _version) {
        _version = _d.documentMode != 8 ? 7 : 8
    }
    _supported = _mozilla && _version >= 1 || _msie && _version >= 6 || _opera && _version >= 9.5 || _safari && _version >= 312;
    if (_supported) {
        if (_opera) {
            history.navigationMode = "compatible"
        }
        for (var i = 1; i < _length; i++) {
            _stack.push("")
        }
        _stack.push(_getHash());
        if (_msie && _l.hash != _getHash()) {
            _l.hash = "#" + _ieLocal(_getHash(), TRUE)
        }
        _searchScript(document);
        var _qi = _url ? _url.indexOf("?") : -1;
        if (_qi != -1) {
            var param, params = _url.substr(_qi + 1).split("&");
            for (var i = 0, p; p = params[i]; i++) {
                param = p.split("=");
                if (/^(history|strict)$/.test(param[0])) {
                    _opts[param[0]] = isNaN(param[1]) ? /^(true|yes)$/i.test(param[1]) : parseInt(param[1]) != 0
                }
                if (/^tracker$/.test(param[0])) {
                    _opts[param[0]] = param[1]
                }
            }
        }
        if (_msie) {
            _titleCheck.call(this)
        }
        if (window == _t) {
            _events.addListener(document, "DOMContentLoaded", _functions.bind(_load, this))
        }
        _events.addListener(_t, "load", _functions.bind(_load, this))
    } else {
        if (!_supported && _l.href.indexOf("#") != -1 || _safari && _version < 418 && _l.href.indexOf("#") != -1 && _l.search != "") {
            _d.open();
            _d.write('<html><head><meta http-equiv="refresh" content="0;url=' + _l.href.substr(0, _l.href.indexOf("#")) + '" /></head></html>');
            _d.close()
        } else {
            _track()
        }
    }
    this.toString = function() {
        return "[class FWDAddress]"
    };
    this.back = function() {
        _h.back()
    };
    this.forward = function() {
        _h.forward()
    };
    this.up = function() {
        var e = this.getPath();
        this.setValue(e.substr(0, e.lastIndexOf("/", e.length - 2) + (e.substr(e.length - 1) == "/" ? 1 : 0)))
    };
    this.go = function(e) {
        _h.go(e)
    };
    this.href = function(e, t) {
        t = typeof t != UNDEFINED ? t : "_self";
        if (t == "_self") {
            self.location.href = e
        } else {
            if (t == "_top") {
                _l.href = e
            } else {
                if (t == "_blank") {
                    window.open(e)
                } else {
                    _t.frames[t].location.href = e
                }
            }
        }
    };
    this.popup = function(url, name, options, handler) {
        try {
            var popup = window.open(url, name, eval(options));
            if (typeof handler != UNDEFINED) {
                eval(handler)
            }
        } catch (ex) {}
        _popup = arguments
    };
    this.getIds = function() {
        return _ids
    };
    this.getId = function(e) {
        return _ids[0]
    };
    this.setId = function(e) {
        _ids[0] = e
    };
    this.addId = function(e) {
        this.removeId(e);
        _ids.push(e)
    };
    this.removeId = function(e) {
        for (var t = 0; t < _ids.length; t++) {
            if (e == _ids[t]) {
                _ids.splice(t, 1);
                break
            }
        }
    };
    this.addEventListener = function(e, t) {
        if (typeof _listeners[e] == UNDEFINED) {
            _listeners[e] = []
        }
        _listeners[e].push(t)
    };
    this.removeEventListener = function(e, t) {
        if (typeof _listeners[e] != UNDEFINED) {
            for (var n = 0, r; r = _listeners[e][n]; n++) {
                if (r == t) {
                    break
                }
            }
            _listeners[e].splice(n, 1)
        }
    };
    this.dispatchEvent = function(e) {
        if (this.hasEventListener(e.type)) {
            e.target = this;
            for (var t = 0, n; n = _listeners[e.type][t]; t++) {
                n(e)
            }
            return TRUE
        }
        return FALSE
    };
    this.hasEventListener = function(e) {
        return typeof _listeners[e] != UNDEFINED && _listeners[e].length > 0
    };
    this.getBaseURL = function() {
        var e = _l.href;
        if (e.indexOf("#") != -1) {
            e = e.substr(0, e.indexOf("#"))
        }
        if (e.substr(e.length - 1) == "/") {
            e = e.substr(0, e.length - 1)
        }
        return e
    };
    this.getStrict = function() {
        return _opts.strict
    };
    this.setStrict = function(e) {
        _opts.strict = e
    };
    this.getHistory = function() {
        return _opts.history
    };
    this.setHistory = function(e) {
        _opts.history = e
    };
    this.getTracker = function() {
        return _opts.tracker
    };
    this.setTracker = function(e) {
        _opts.tracker = e
    };
    this.getTitle = function() {
        return _d.title
    };
    this.setTitle = function(e) {
        if (!_supported) {
            return null
        }
        if (typeof e == UNDEFINED) {
            return
        }
        if (e == "null") {
            e = ""
        }
        e = _dc(e);
        _st(function() {
            _title = _d.title = e;
            if (_juststart && _frame && _frame.contentWindow && _frame.contentWindow.document) {
                _frame.contentWindow.document.title = e;
                _juststart = FALSE
            }
            if (!_justset && _mozilla) {
                _l.replace(_l.href.indexOf("#") != -1 ? _l.href : _l.href + "#")
            }
            _justset = FALSE
        }, 10)
    };
    this.getStatus = function() {
        return _t.status
    };
    this.setStatus = function(e) {
        if (!_supported) {
            return null
        }
        if (typeof e == UNDEFINED) {
            return
        }
        if (e == "null") {
            e = ""
        }
        e = _dc(e);
        if (!_safari) {
            e = _strictCheck(e != "null" ? e : "", TRUE);
            if (e == "/") {
                e = ""
            }
            if (!/http(s)?:\/\//.test(e)) {
                var t = _l.href.indexOf("#");
                e = (t == -1 ? _l.href : _l.href.substr(0, t)) + "#" + e
            }
            _t.status = e
        }
    };
    this.resetStatus = function() {
        _t.status = ""
    };
    this.getValue = function() {
        if (!_supported) {
            return null
        }
        return _dc(_strictCheck(_ieLocal(_value, FALSE), FALSE))
    };
    this.setValue = function(e) {
        if (!_supported) {
            return null
        }
        if (typeof e == UNDEFINED) {
            return
        }
        if (e == "null") {
            e = ""
        }
        e = _ec(_dc(_strictCheck(e, TRUE)));
        if (e == "/") {
            e = ""
        }
        if (_value == e) {
            return
        }
        _justset = TRUE;
        _value = e;
        _silent = TRUE;
        _update.call(FWDAddress, true);
        _stack[_h.length] = _value;
        if (_safari) {
            if (_opts.history) {
                _l[ID][_l.pathname] = _stack.toString();
                _length = _h.length + 1;
                if (_version < 418) {
                    if (_l.search == "") {
                        _form.action = "#" + _value;
                        _form.submit()
                    }
                } else {
                    if (_version < 523 || _value == "") {
                        var t = _d.createEvent("MouseEvents");
                        t.initEvent("click", TRUE, TRUE);
                        var n = _d.createElement("a");
                        n.href = "#" + _value;
                        n.dispatchEvent(t)
                    } else {
                        _l.hash = "#" + _value
                    }
                }
            } else {
                _l.replace("#" + _value)
            }
        } else {
            if (_value != _getHash()) {
                if (_opts.history) {
                    _l.hash = "#" + _dc(_ieLocal(_value, TRUE))
                } else {
                    _l.replace("#" + _dc(_value))
                }
            }
        }
        if (_msie && _version < 8 && _opts.history) {
            _st(_htmlWrite, 50)
        }
        if (_safari) {
            _st(function() {
                _silent = FALSE
            }, 1)
        } else {
            _silent = FALSE
        }
    };
    this.getPath = function() {
        var e = this.getValue();
        if (e.indexOf("?") != -1) {
            return e.split("?")[0]
        } else {
            if (e.indexOf("#") != -1) {
                return e.split("#")[0]
            } else {
                return e
            }
        }
    };
    this.getPathNames = function() {
        var e = this.getPath(),
            t = e.split("/");
        if (e.substr(0, 1) == "/" || e.length == 0) {
            t.splice(0, 1)
        }
        if (e.substr(e.length - 1, 1) == "/") {
            t.splice(t.length - 1, 1)
        }
        return t
    };
    this.getQueryString = function() {
        var e = this.getValue(),
            t = e.indexOf("?");
        if (t != -1 && t < e.length) {
            return e.substr(t + 1)
        }
    };
    this.getParameter = function(e) {
        var t = this.getValue();
        var n = t.indexOf("?");
        if (n != -1) {
            t = t.substr(n + 1);
            var r, i = t.split("&"),
                s = i.length,
                o = [];
            while (s--) {
                r = i[s].split("=");
                if (r[0] == e) {
                    o.push(r[1])
                }
            }
            if (o.length != 0) {
                return o.length != 1 ? o : o[0]
            }
        }
    };
    this.getParameterNames = function() {
        var e = this.getValue();
        var t = e.indexOf("?");
        var n = [];
        if (t != -1) {
            e = e.substr(t + 1);
            if (e != "" && e.indexOf("=") != -1) {
                var r = e.split("&"),
                    i = 0;
                while (i < r.length) {
                    n.push(r[i].split("=")[0]);
                    i++
                }
            }
        }
        return n
    };
    this.onInit = null;
    this.onChange = null;
    this.onInternalChange = null;
    this.onExternalChange = null;
    (function() {
        var e;
        if (typeof FlashObject != UNDEFINED) {
            SWFObject = FlashObject
        }
        if (typeof SWFObject != UNDEFINED && SWFObject.prototype && SWFObject.prototype.write) {
            var t = SWFObject.prototype.write;
            SWFObject.prototype.write = function() {
                e = arguments;
                if (this.getAttribute("version").major < 8) {
                    this.addVariable("$swfaddress", FWDAddress.getValue());
                    (typeof e[0] == "string" ? document.getElementById(e[0]) : e[0]).so = this
                }
                var n;
                if (n = t.apply(this, e)) {
                    _ref.addId(this.getAttribute("id"))
                }
                return n
            }
        }
        if (typeof swfobject != UNDEFINED) {
            var n = swfobject.registerObject;
            swfobject.registerObject = function() {
                e = arguments;
                n.apply(this, e);
                _ref.addId(e[0])
            };
            var r = swfobject.createSWF;
            swfobject.createSWF = function() {
                e = arguments;
                var t = r.apply(this, e);
                if (t) {
                    _ref.addId(e[0].id)
                }
                return t
            };
            var i = swfobject.embedSWF;
            swfobject.embedSWF = function() {
                e = arguments;
                if (typeof e[8] == UNDEFINED) {
                    e[8] = {}
                }
                if (typeof e[8].id == UNDEFINED) {
                    e[8].id = e[1]
                }
                i.apply(this, e);
                _ref.addId(e[8].id)
            }
        }
        if (typeof UFO != UNDEFINED) {
            var s = UFO.create;
            UFO.create = function() {
                e = arguments;
                s.apply(this, e);
                _ref.addId(e[0].id)
            }
        }
        if (typeof AC_FL_RunContent != UNDEFINED) {
            var o = AC_FL_RunContent;
            AC_FL_RunContent = function() {
                e = arguments;
                o.apply(this, e);
                for (var t = 0, n = e.length; t < n; t++) {
                    if (e[t] == "id") {
                        _ref.addId(e[t + 1])
                    }
                }
            }
        }
    })()
};
var FWDFlashTest = function() {
    function c() {
        var n = o.getElementsByTagName("body")[0];
        var r = createElement(t);
        r.setAttribute("type", i);
        var s = n.appendChild(r);
        if (s) {
            var u = 0;
            (function() {
                if (typeof s.GetVariable != e) {
                    var t = s.GetVariable("$version");
                    if (t) {
                        t = t.split(" ")[1].split(",");
                        l.pv = [parseInt(t[0], 10), parseInt(t[1], 10), parseInt(t[2], 10)]
                    }
                } else if (u < 10) {
                    u++;
                    setTimeout(arguments.callee, 10);
                    return
                }
                n.removeChild(r);
                s = null;
                h()
            })()
        } else {
            h()
        }
    }

    function h() {
        var t = f.length;
        if (t > 0) {
            for (var n = 0; n < t; n++) {
                var r = f[n].id;
                var i = f[n].callbackFn;
                var s = {
                    success: false,
                    id: r
                };
                if (l.pv[0] > 0) {
                    var o = getElementById(r);
                    if (o) {
                        if (p(f[n].swfVersion) && !(l.wk && l.wk < 312)) {
                            setVisibility(r, true);
                            if (i) {
                                s.success = true;
                                s.ref = getObjectById(r);
                                i(s)
                            }
                        } else if (f[n].expressInstall && canExpressInstall()) {
                            var u = {};
                            u.data = f[n].expressInstall;
                            u.width = o.getAttribute("width") || "0";
                            u.height = o.getAttribute("height") || "0";
                            if (o.getAttribute("class")) {
                                u.styleclass = o.getAttribute("class")
                            }
                            if (o.getAttribute("align")) {
                                u.align = o.getAttribute("align")
                            }
                            var a = {};
                            var c = o.getElementsByTagName("param");
                            var h = c.length;
                            for (var d = 0; d < h; d++) {
                                if (c[d].getAttribute("name").toLowerCase() != "movie") {
                                    a[c[d].getAttribute("name")] = c[d].getAttribute("value")
                                }
                            }
                            showExpressInstall(u, a, r, i)
                        } else {
                            displayAltContent(o);
                            if (i) {
                                i(s)
                            }
                        }
                    }
                } else {
                    setVisibility(r, true);
                    if (i) {
                        var v = getObjectById(r);
                        if (v && typeof v.SetVariable != e) {
                            s.success = true;
                            s.ref = v
                        }
                        i(s)
                    }
                }
            }
        }
    }

    function p(e) {
        var t = l.pv,
            n = e.split(".");
        n[0] = parseInt(n[0], 10);
        n[1] = parseInt(n[1], 10) || 0;
        n[2] = parseInt(n[2], 10) || 0;
        return t[0] > n[0] || t[0] == n[0] && t[1] > n[1] || t[0] == n[0] && t[1] == n[1] && t[2] >= n[2] ? true : false
    }

    function d(t) {
        var n = /[\\\"<>\.;]/;
        var r = n.exec(t) != null;
        return r && typeof encodeURIComponent != e ? encodeURIComponent(t) : t
    }
    var e = "undefined",
        t = "object",
        n = "Shockwave Flash",
        r = "ShockwaveFlash.ShockwaveFlash",
        i = "application/x-shockwave-flash",
        s = window,
        o = document,
        u = navigator,
        a = false,
        f = [],
        l = function() {
            var f = typeof o.getElementById != e && typeof o.getElementsByTagName != e && typeof o.createElement != e,
                l = u.userAgent.toLowerCase(),
                c = u.platform.toLowerCase(),
                h = c ? /win/.test(c) : /win/.test(l),
                p = c ? /mac/.test(c) : /mac/.test(l),
                d = /webkit/.test(l) ? parseFloat(l.replace(/^.*webkit\/(\d+(\.\d+)?).*$/, "$1")) : false,
                v = !+"1",
                m = [0, 0, 0],
                g = null;
            if (typeof u.plugins != e && typeof u.plugins[n] == t) {
                g = u.plugins[n].description;
                if (g && !(typeof u.mimeTypes != e && u.mimeTypes[i] && !u.mimeTypes[i].enabledPlugin)) {
                    a = true;
                    v = false;
                    g = g.replace(/^.*\s+(\S+\s+\S+$)/, "$1");
                    m[0] = parseInt(g.replace(/^(.*)\..*$/, "$1"), 10);
                    m[1] = parseInt(g.replace(/^.*\.(.*)\s.*$/, "$1"), 10);
                    m[2] = /[a-zA-Z]/.test(g) ? parseInt(g.replace(/^.*[a-zA-Z]+(.*)$/, "$1"), 10) : 0
                }
            } else if (typeof s.ActiveXObject != e) {
                try {
                    var y = new ActiveXObject(r);
                    if (y) {
                        g = y.GetVariable("$version");
                        if (g) {
                            v = true;
                            g = g.split(" ")[1].split(",");
                            m = [parseInt(g[0], 10), parseInt(g[1], 10), parseInt(g[2], 10)]
                        }
                    }
                } catch (b) {}
            }
            return {
                w3: f,
                pv: m,
                wk: d,
                ie: v,
                win: h,
                mac: p
            }
        }();
    return {
        hasFlashPlayerVersion: p
    }
}();
document.write("<script type='text/vbscript'>\r\nFunction IEBinary_getByteAt(strBinary, iOffset)\r\n	IEBinary_getByteAt = AscB(MidB(strBinary,iOffset+1,1))\r\nEnd Function\r\nFunction IEBinary_getLength(strBinary)\r\n	IEBinary_getLength = LenB(strBinary)\r\nEnd Function\r\n</script>\r\n");
(function(e) {
    e.FileAPIReader = function(e, t) {
        return function(n, r) {
            var i = t || new FileReader;
            i.onload = function(e) {
                r(new A(e.target.result))
            };
            i.readAsBinaryString(e)
        }
    }
})(this);
(function(e) {
    var t = e.p = {},
        n = {},
        r = [0, 7];
    t.t = function(e) {
        delete n[e]
    };
    t.s = function() {
        n = {}
    };
    t.B = function(e, t, i) {
        i = i || {};
        (i.dataReader || B)(e, function(s) {
            s.f(r, function() {
                var r = "ftypM4A" == s.c(4, 7) ? ID4 : "ID3" == s.c(0, 3) ? ID3v2 : ID3v1;
                r.m(s, function() {
                    var o = i.tags,
                        u = r.n(s, o),
                        o = n[e] || {},
                        l;
                    for (l in u) u.hasOwnProperty(l) && (o[l] = u[l]);
                    n[e] = o;
                    t && t()
                })
            })
        })
    };
    t.v = function(e) {
        if (!n[e]) return null;
        var t = {},
            r;
        for (r in n[e]) n[e].hasOwnProperty(r) && (t[r] = n[e][r]);
        return t
    };
    t.A = function(e, t) {
        return n[e] ? n[e][t] : null
    };
    e.ID3 = e.p;
    t.loadTags = t.B;
    t.getAllTags = t.v;
    t.getTag = t.A;
    t.clearTags = t.t;
    t.clearAll = t.s
})(this);
(function(e) {
    var t = e.q = {},
        n = "Blues;Classic Rock;Country;Dance;Disco;Funk;Grunge;Hip-Hop;Jazz;Metal;New Age;Oldies;Other;Pop;R&B;Rap;Reggae;Rock;Techno;Industrial;Alternative;Ska;Death Metal;Pranks;Soundtrack;Euro-Techno;Ambient;Trip-Hop;Vocal;Jazz+Funk;Fusion;Trance;Classical;Instrumental;Acid;House;Game;Sound Clip;Gospel;Noise;AlternRock;Bass;Soul;Punk;Space;Meditative;Instrumental Pop;Instrumental Rock;Ethnic;Gothic;Darkwave;Techno-Industrial;Electronic;Pop-Folk;Eurodance;Dream;Southern Rock;Comedy;Cult;Gangsta;Top 40;Christian Rap;Pop/Funk;Jungle;Native American;Cabaret;New Wave;Psychadelic;Rave;Showtunes;Trailer;Lo-Fi;Tribal;Acid Punk;Acid Jazz;Polka;Retro;Musical;Rock & Roll;Hard Rock;Folk;Folk-Rock;National Folk;Swing;Fast Fusion;Bebob;Latin;Revival;Celtic;Bluegrass;Avantgarde;Gothic Rock;Progressive Rock;Psychedelic Rock;Symphonic Rock;Slow Rock;Big Band;Chorus;Easy Listening;Acoustic;Humour;Speech;Chanson;Opera;Chamber Music;Sonata;Symphony;Booty Bass;Primus;Porn Groove;Satire;Slow Jam;Club;Tango;Samba;Folklore;Ballad;Power Ballad;Rhythmic Soul;Freestyle;Duet;Punk Rock;Drum Solo;Acapella;Euro-House;Dance Hall".split(";");
    t.m = function(e, t) {
        var n = e.h();
        e.f([n - 128 - 1, n], t)
    };
    t.n = function(e) {
        var t = e.h() - 128;
        if ("TAG" == e.c(t, 3)) {
            var r = e.c(t + 3, 30).replace(/\0/g, ""),
                i = e.c(t + 33, 30).replace(/\0/g, ""),
                s = e.c(t + 63, 30).replace(/\0/g, ""),
                o = e.c(t + 93, 4).replace(/\0/g, "");
            if (0 == e.a(t + 97 + 28)) var u = e.c(t + 97, 28).replace(/\0/g, ""),
                a = e.a(t + 97 + 29);
            else u = "", a = 0;
            e = e.a(t + 97 + 30);
            return {
                version: "1.1",
                title: r,
                artist: i,
                album: s,
                year: o,
                comment: u,
                track: a,
                genre: 255 > e ? n[e] : ""
            }
        }
        return {}
    };
    e.ID3v1 = e.q
})(this);
(function(e) {
    function t(e, t) {
        var n = t.a(e),
            r = t.a(e + 1),
            i = t.a(e + 2);
        return t.a(e + 3) & 127 | (i & 127) << 7 | (r & 127) << 14 | (n & 127) << 21
    }
    var n = e.D = {};
    n.b = {};
    n.frames = {
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
    var r = {
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
        i = ["title", "artist", "album", "track"];
    n.m = function(e, n) {
        e.f([0, t(6, e)], n)
    };
    n.n = function(e, s) {
        var o = 0,
            u = e.a(o + 3);
        if (4 < u) return {
            version: ">2.4"
        };
        var a = e.a(o + 4),
            f = e.d(o + 5, 7),
            l = e.d(o + 5, 6),
            h = e.d(o + 5, 5),
            p = t(o + 6, e),
            o = o + 10;
        if (l) var d = e.i(o),
            o = o + (d + 4);
        var u = {
                version: "2." + u + "." + a,
                major: u,
                revision: a,
                flags: {
                    unsynchronisation: f,
                    extended_header: l,
                    experimental_indicator: h
                },
                size: p
            },
            v;
        if (f) v = {};
        else {
            for (var p = p - 10, f = e, a = s, l = {}, h = u.major, d = [], m = 0, y; y = (a || i)[m]; m++) d = d.concat(r[y] || [y]);
            for (a = d; o < p;) {
                d = null;
                m = f;
                y = o;
                var w = null;
                switch (h) {
                    case 2:
                        v = m.c(y, 3);
                        var E = m.o(y + 3),
                            S = 6;
                        break;
                    case 3:
                        v = m.c(y, 4);
                        E = m.i(y + 4);
                        S = 10;
                        break;
                    case 4:
                        v = m.c(y, 4), E = t(y + 4, m), S = 10
                }
                if ("" == v) break;
                o += S + E;
                0 > a.indexOf(v) || (2 < h && (w = {
                    message: {
                        P: m.d(y + 8, 6),
                        I: m.d(y + 8, 5),
                        M: m.d(y + 8, 4)
                    },
                    k: {
                        K: m.d(y + 8 + 1, 7),
                        F: m.d(y + 8 + 1, 3),
                        H: m.d(y + 8 + 1, 2),
                        C: m.d(y + 8 + 1, 1),
                        u: m.d(y + 8 + 1, 0)
                    }
                }), y += S, w && w.k.u && (t(y, m), y += 4, E -= 4), w && w.k.C || (v in n.b ? d = n.b[v] : "T" == v[0] && (d = n.b["T*"]), d = d ? d(y, E, m, w) : void 0, d = {
                    id: v,
                    size: E,
                    description: v in n.frames ? n.frames[v] : "Unknown",
                    data: d
                }, v in l ? (l[v].id && (l[v] = [l[v]]), l[v].push(d)) : l[v] = d))
            }
            v = l
        }
        for (var x in r)
            if (r.hasOwnProperty(x)) {
                e: {
                    E = r[x];
                    "string" == typeof E && (E = [E]);S = 0;
                    for (o = void 0; o = E[S]; S++)
                        if (o in v) {
                            e = v[o].data;
                            break e
                        } e = void 0
                }
                e && (u[x] = e)
            } for (var T in v) v.hasOwnProperty(T) && (u[T] = v[T]);
        return u
    };
    e.ID3v2 = n
})(this);
(function() {
    function e(e) {
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
    var t = "32x32 pixels 'file icon' (PNG only);Other file icon;Cover (front);Cover (back);Leaflet page;Media (e.g. lable side of CD);Lead artist/lead performer/soloist;Artist/performer;Conductor;Band/Orchestra;Composer;Lyricist/text writer;Recording Location;During recording;During performance;Movie/video screen capture;A bright coloured fish;Illustration;Band/artist logotype;Publisher/Studio logotype".split(";");
    ID3v2.b.APIC = function(n, r, i, s, o) {
        o = o || "3";
        s = n;
        var u = e(i.a(n));
        switch (o) {
            case "2":
                var a = i.c(n + 1, 3);
                n += 4;
                break;
            case "3":
            case "4":
                a = i.e(n + 1, r - (n - s), u), n += 1 + a.g
        }
        o = i.a(n, 1);
        o = t[o];
        u = i.e(n + 1, r - (n - s), u);
        n += 1 + u.g;
        return {
            format: a.toString(),
            type: o,
            description: u.toString(),
            data: i.l(n, s + r - n)
        }
    };
    ID3v2.b.COMM = function(t, n, r) {
        var i = t,
            s = e(r.a(t)),
            o = r.c(t + 1, 3),
            u = r.e(t + 4, n - 4, s);
        t += 4 + u.g;
        t = r.e(t, i + n - t, s);
        return {
            language: o,
            O: u.toString(),
            text: t.toString()
        }
    };
    ID3v2.b.COM = ID3v2.b.COMM;
    ID3v2.b.PIC = function(e, t, n, r) {
        return ID3v2.b.APIC(e, t, n, r, "2")
    };
    ID3v2.b.PCNT = function(e, t, n) {
        return n.J(e)
    };
    ID3v2.b.CNT = ID3v2.b.PCNT;
    ID3v2.b["T*"] = function(t, n, r) {
        var i = e(r.a(t));
        return r.e(t + 1, n - 1, i).toString()
    };
    ID3v2.b.TCON = function(e, t, n) {
        return ID3v2.b["T*"].apply(this, arguments).replace(/^\(\d+\)/, "")
    };
    ID3v2.b.TCO = ID3v2.b.TCON;
    ID3v2.b.USLT = function(t, n, r) {
        var i = t,
            s = e(r.a(t)),
            o = r.c(t + 1, 3),
            u = r.e(t + 4, n - 4, s);
        t += 4 + u.g;
        t = r.e(t, i + n - t, s);
        return {
            language: o,
            G: u.toString(),
            L: t.toString()
        }
    };
    ID3v2.b.ULT = ID3v2.b.USLT
})();
(function(e) {
    function t(e, n, i, s) {
        var o = e.i(n);
        if (0 == o) s();
        else {
            var u = e.c(n + 4, 4); - 1 < ["moov", "udta", "meta", "ilst"].indexOf(u) ? ("meta" == u && (n += 4), e.f([n + 8, n + 8 + 8], function() {
                t(e, n + 8, o - 8, s)
            })) : e.f([n + (u in r.j ? 0 : o), n + o + 8], function() {
                t(e, n + o, i, s)
            })
        }
    }

    function n(e, t, i, s, o) {
        o = void 0 === o ? "" : o + "  ";
        for (var u = i; u < i + s;) {
            var a = t.i(u);
            if (0 == a) break;
            var f = t.c(u + 4, 4);
            if (-1 < ["moov", "udta", "meta", "ilst"].indexOf(f)) {
                "meta" == f && (u += 4);
                n(e, t, u + 8, a - 8, o);
                break
            }
            if (r.j[f]) {
                var l = t.o(u + 16 + 1),
                    c = r.j[f],
                    l = r.types[l];
                if ("trkn" == f) e[c[0]] = t.a(u + 16 + 11), e.count = t.a(u + 16 + 13);
                else {
                    var f = u + 16 + 4 + 4,
                        h = a - 16 - 4 - 4,
                        p;
                    switch (l) {
                        case "text":
                            p = t.e(f, h, "UTF-8");
                            break;
                        case "uint8":
                            p = t.w(f);
                            break;
                        case "jpeg":
                        case "png":
                            p = {
                                k: "image/" + l,
                                data: t.l(f, h)
                            }
                    }
                    e[c[0]] = "comment" === c[0] ? {
                        text: p
                    } : p
                }
            }
            u += a
        }
    }
    var r = e.r = {};
    r.types = {
        0: "uint8",
        1: "text",
        13: "jpeg",
        14: "png",
        21: "uint8"
    };
    r.j = {
        "©alb": ["album"],
        "©art": ["artist"],
        "©ART": ["artist"],
        aART: ["artist"],
        "©day": ["year"],
        "©nam": ["title"],
        "©gen": ["genre"],
        trkn: ["track"],
        "©wrt": ["composer"],
        "©too": ["encoder"],
        cprt: ["copyright"],
        covr: ["picture"],
        "©grp": ["grouping"],
        keyw: ["keyword"],
        "©lyr": ["lyrics"],
        "©cmt": ["comment"],
        tmpo: ["tempo"],
        cpil: ["compilation"],
        disk: ["disc"]
    };
    r.m = function(e, n) {
        e.f([0, 7], function() {
            t(e, 0, e.h(), n)
        })
    };
    r.n = function(e) {
        var t = {};
        n(t, e, 0, e.h());
        return t
    };
    e.ID4 = e.r
})(this);
(function(e) {
    function c(t, n, r) {
        function u() {
            if (s) {
                s.apply(e, arguments);
                if (!o) {
                    delete n[i];
                    s = null
                }
            }
        }
        var i, s = r[0],
            o = t === a;
        r[0] = u;
        i = t.apply(e, r);
        n[i] = {
            args: r,
            created: Date.now(),
            cb: s,
            id: i
        };
        return i
    }

    function h(t, n, r, i, s) {
        function c() {
            if (o.cb) {
                o.cb.apply(e, arguments);
                if (!u) {
                    delete r[i];
                    o.cb = null
                }
            }
        }
        var o = r[i];
        if (!o) {
            return
        }
        var u = t === a;
        n(o.id);
        if (!u) {
            var f = o.args[1];
            var l = Date.now() - o.created;
            if (l < 0) {
                l = 0
            }
            f -= l;
            if (f < 0) {
                f = 0
            }
            o.args[1] = f
        }
        o.args[0] = c;
        o.created = Date.now();
        o.id = t.apply(e, o.args)
    }
    var t = navigator.platform;
    var n = false;
    if (t == "iPad" || t == "iPhone") n = true;
    if (!n) return;
    var r = navigator.userAgent;
    var i = false;
    if (r.indexOf("6") != -1) i = true;
    if (!i) return;
    var s = {};
    var o = {};
    var u = e.setTimeout;
    var a = e.setInterval;
    var f = e.clearTimeout;
    var l = e.clearInterval;
    e.setTimeout = function() {
        return c(u, s, arguments)
    };
    e.setInterval = function() {
        return c(a, o, arguments)
    };
    e.clearTimeout = function(e) {
        var t = s[e];
        if (t) {
            delete s[e];
            f(t.id)
        }
    };
    e.clearInterval = function(e) {
        var t = o[e];
        if (t) {
            delete o[e];
            l(t.id)
        }
    };
    e.addEventListener("scroll", function() {
        var e;
        for (e in s) {
            h(u, f, s, e)
        }
        for (e in o) {
            h(a, l, o, e)
        }
    })
})(window);
(function(window) {
    var MUSIC = function(props) {
        var self = this;
        self.init = function() {
            TweenLite.ticker.useRAF(false);
            this.props_obj = props;
            this.instanceName_str = this.props_obj.instanceName;
            if (!this.instanceName_str) {
                alert("MUSIC instance name is requires please make sure that the instanceName parameter exsists and it's value is uinique.");
                return
            }
            if (window[this.instanceName_str]) {
                alert("MUSIC instance name " + this.instanceName_str + " is already defined and contains a different instance reference, set a different instance name.");
                return
            } else {
                window[this.instanceName_str] = this
            }
            if (!this.props_obj) {
                alert("MUSIC constructor properties object is not defined!");
                return
            }
            this.position_str = self.props_obj.position;
            if (!this.position_str) this.position_str = MUSIC.POSITION_TOP;
            if (this.position_str == "bottom") {
                this.position_str = MUSIC.POSITION_BOTTOM
            } else {
                this.position_str = MUSIC.POSITION_TOP
            }
            this.stageContainer = document.createElement("div");
            this.stageContainer.style.position = "fixed";
            if (MUSICUtils.isIEAndLessThen9) {
                this.stageContainer.style.zIndex = "2147483630"
            } else {
                this.stageContainer.style.zIndex = "99999999990"
            }
            this.stageContainer.style.overflow = "visible";
            self.stageContainer.style.height = "0px";
            if (MUSICUtils.isIE) {
                document.getElementsByTagName("body")[0].appendChild(this.stageContainer)
            } else {
                document.documentElement.appendChild(this.stageContainer)
            }
            this.listeners = {
                events_ar: []
            };
            this.popupWindow;
            this.ws = null;
            this.so = null;
            this.data = null;
            this.opener_do = null;
            this.customContextMenu_do = null;
            this.info_do = null;
            this.main_do = null;
            this.background_do = null;
            this.preloader_do = null;
            this.controller_do = null;
            this.categories_do = null;
            this.playlist_do = null;
            this.audioScreen_do = null;
            this.flash_do = null;
            this.flashObject = null;
            this.flashObjectMarkup_str = null;
            this.popupWindowBackgroundColor = this.props_obj.popupWindowBackgroundColor || "#000000";
            this.prevCatId = -1;
            this.catId = -1;
            this.id = -1;
            this.prevId = -1;
            this.totalAudio = 0;
            this.stageWidth = 0;
            this.stageHeight = 0;
            this.maxWidth = self.props_obj.maxWidth || 2e3;
            this.maxHeight = 0;
            this.prevAddToHeight = -1;
            this.lastPercentPlayed = 0;
            this.popupWindowWidth = self.props_obj.popupWindowWidth || 500;
            this.popupWindowHeight = self.props_obj.popupWindowHeight || 400;
            if (MUSICUtils.isIE) this.popupWindowHeight -= 3;
            this.resizeHandlerId_to;
            this.resizeHandler2Id_to;
            this.hidePreloaderId_to;
            this.orientationChangeId_to;
            this.showCatWidthDelayId_to;
            this.showPlaylistWithDelayId_to;
            this.disablePlaylistForAWhileId_to;
            this.allowToResizeAndPosition_bl = false;
            this.isAPIReady_bl = false;
            this.isPlaylistLoaded_bl = false;
            this.isFlashScreenReady_bl = false;
            this.orintationChangeComplete_bl = true;
            this.animate_bl = false;
            this.isFirstPlaylistLoaded_bl = false;
            this.scrubbedFirstTimeInPopup_bl = false;
            this.showedFirstTime_bl = false;
            self.isPlaylistShowed_bl = false;
            this.useDeepLinking_bl = self.props_obj.useDeepLinking;
            this.useDeepLinking_bl = self.useDeepLinking_bl == "yes" ? true : false;
            this.openInPopup_bl = false;
            this.isMobile_bl = MUSICUtils.isMobile;
            this.hasPointerEvent_bl = MUSICUtils.hasPointerEvent;
            try {
                if (window.opener && window.opener[this.instanceName_str] && window.opener[this.instanceName_str].instanceName_str == this.instanceName_str) {
                    this.openInPopup_bl = true;
                    this.popupWindow = window.opener[this.instanceName_str];
                    window.opener[this.instanceName_str].removeAndDisablePlayer();
                    if (!self.isMobile_bl) {
                        document.cookie = "MUSIC=" + self.instanceName_str + "; path=/";
                        window.onbeforeunload = function(e) {
                            document.cookie = "MUSIC=; expires=Thu, 01-Jan-70 00:00:01 GMT; path=/"
                        }
                    }
                }
            } catch (e) {}
            this.setupMainDo();
            this.startResizeHandler();
            this.setupInfo();
            this.setupData();
            MUSIC.instaces_ar.push(this)
        };
        this.popup = function() {
            if (self.popupWindow && !self.popupWindow.closed) return;
            var e;
            var t = screen.width / 2 - self.popupWindowWidth / 2;
            var n = screen.height / 2 - self.popupWindowHeight / 2;
            var r = "no";
            if (MUSICUtils.isSafari) r = "yes";
            try {
                if (MUSICUtils.isMobile) {
                    self.popupWindow = window.open(location.href, self.instanceName_str)
                } else {
                    self.popupWindow = window.open(location.href, self.instanceName_str, "location=" + r + ", width=" + self.popupWindowWidth + ", height=" + self.popupWindowHeight + ", top=" + n + ", left=" + t)
                }
                if (self.popupWindow) {
                    self.stageContainer.style.display = "none";
                    if (self.preloader_do) self.preloader_do.hide(false);
                    self.data.closeData();
                    self.stop();
                    self.isAPIReady_bl = false
                }
                self.stopResizeHandler();
                self.dispatchEvent(MUSIC.POPUP)
            } catch (i) {}
        };
        this.removeAndDisablePlayer = function() {
            self.stageContainer.style.display = "none"
        };
        self.setupMainDo = function() {
            self.background_do = new MUSICDisplayObject("div");
            self.background_do.getStyle().width = "100%";
            self.main_do = new MUSICDisplayObject("div");
            self.main_do.getStyle().msTouchAction = "none";
            self.main_do.getStyle().webkitTapHighlightColor = "rgba(0, 0, 0, 0)";
            self.main_do.setBackfaceVisibility();
            if (!MUSICUtils.isMobile || MUSICUtils.isMobile && MUSICUtils.hasPointerEvent) self.main_do.setSelectable(false);
            if (self.openInPopup_bl) {
                document.documentElement.appendChild(self.main_do.screen);
                self.stageContainer.style.position = "absolute";
                document.documentElement.style.overflow = "hidden";
                document.documentElement.style.backgroundColor = self.popupWindowBackgroundColor;
                self.main_do.setBkColor(self.popupWindowBackgroundColor);
                if (MUSICUtils.isIEAndLessThen9) {
                    this.main_do.getStyle().zIndex = "2147483631"
                } else {
                    this.main_do.getStyle().zIndex = "99999999991"
                }
                if (MUSICUtils.isIE) {
                    document.getElementsByTagName("body")[0].appendChild(self.main_do.screen)
                } else {
                    document.getElementsByTagName("body")[0].style.display = "none"
                }
                self.main_do.setHeight(3e3)
            } else {
                self.stageContainer.appendChild(self.background_do.screen);
                self.stageContainer.appendChild(self.main_do.screen)
            }
        };
        self.setupInfo = function() {
            MUSICInfo.setPrototype();
            self.info_do = new MUSICInfo(self);
            if (MUSICUtils.isIEAndLessThen9) {
                self.info_do.getStyle().zIndex = "2147483632"
            } else {
                self.info_do.getStyle().zIndex = "99999999992"
            }
        };
        self.startResizeHandler = function() {
            if (window.addEventListener) {
                window.addEventListener("resize", self.onResizeHandler);
                if (MUSICUtils.isAndroid) window.addEventListener("orientationchange", self.orientationChange)
            } else if (window.attachEvent) {
                window.attachEvent("onresize", self.onResizeHandler)
            }
        };
        self.stopResizeHandler = function() {
            clearTimeout(self.resizeHandlerId_to);
            clearTimeout(self.resizeHandler2Id_to);
            clearTimeout(self.orientationChangeId_to);
            if (window.removeEventListener) {
                window.removeEventListener("resize", self.onResizeHandler);
                window.removeEventListener("orientationchange", self.orientationChange)
            } else if (window.detachEvent) {
                window.detachEvent("onresize", self.onResizeHandler)
            }
        };
        self.onScrollHandler = function() {
            self.onResizeHandler()
        };
        self.onResizeHandler = function(e) {
            self.resizeHandler()
        };
        this.orientationChange = function() {
            self.orintationChangeComplete_bl = false;
            clearTimeout(self.resizeHandlerId_to);
            clearTimeout(self.resizeHandler2Id_to);
            clearTimeout(self.orientationChangeId_to);
            self.orientationChangeId_to = setTimeout(function() {
                self.orintationChangeComplete_bl = true;
                self.resizeHandler(true)
            }, 1e3);
            self.stageContainer.style.left = "-5000px";
            if (self.preloader_do) self.preloader_do.setX(-5e3)
        };
        self.resizeHandler = function(e, t) {
            if (!self.orintationChangeComplete_bl) return;
            self.ws = MUSICUtils.getViewportSize();
            self.stageWidth = document.documentElement.offsetWidth;
            self.stageContainer.style.width = "100%";
            self.stageContainer.style.left = "0px";
            if (self.stageWidth > self.maxWidth && !self.openInPopup_bl) {
                self.stageWidth = self.maxWidth
            }
            if (self.controller_do) self.maxHeight = self.controller_do.h;
            self.stageHeight = self.maxHeight;
            self.main_do.setX(parseInt((self.ws.w - self.stageWidth) / 2));
            self.main_do.setWidth(self.stageWidth);
            if (self.preloader_do) self.positionPreloader();
            if (self.controller_do) self.controller_do.resizeAndPosition();
            if (self.categories_do) self.categories_do.resizeAndPosition();
            if (self.playlist_do) self.playlist_do.resizeAndPosition();
            if (self.isFirstPlaylistLoaded_bl) self.setStageContainerFinalHeightAndPosition(false)
        };
        this.setStageContainerFinalHeightAndPosition = function(e) {
            if (!self.ws) self.ws = MUSICUtils.getViewportSize();
            if (!self.controller_do || !self.allowToResizeAndPosition_bl) return;
            if (self.openInPopup_bl) {
                self.main_do.setX(0);
                self.main_do.setY(0);
                self.main_do.getStyle().width = "100%";
                self.main_do.setHeight(self.ws.h);
                self.controller_do.setX(0);
                MUSICTweenMax.killTweensOf(self.controller_do);
                if (e) {
                    if (self.controller_do.y != 0) MUSICTweenMax.to(self.controller_do, .8, {
                        y: 0,
                        ease: Expo.easeInOut
                    })
                } else {
                    self.controller_do.setY(0)
                }
                if (self.playlist_do) {
                    MUSICTweenMax.killTweensOf(self.playlist_do);
                    self.playlist_do.setX(0);
                    if (e) {
                        MUSICTweenMax.to(self.playlist_do, .8, {
                            y: self.controller_do.h,
                            delay: .4,
                            ease: Expo.easeInOut
                        })
                    } else {
                        self.playlist_do.setY(self.controller_do.h)
                    }
                }
                return
            }
            clearTimeout(self.showPlaylistWithDelayId_to);
            if (self.playlist_do && self.playlist_do.isShowed_bl) addToHeight = self.playlist_do.h;
            if (self.position_str == MUSIC.POSITION_TOP) {
                if (self.playlist_do) {
                    self.background_do.setHeight(self.playlist_do.h + self.controller_do.h);
                    self.playlist_do.setY(0);
                    self.controller_do.setY(self.playlist_do.h);
                    self.main_do.setHeight(self.playlist_do.h + self.controller_do.h)
                } else {
                    self.background_do.setHeight(self.controller_do.h);
                    self.controller_do.setY(0);
                    self.main_do.setHeight(self.controller_do.h)
                }
            } else {
                if (self.playlist_do) {
                    self.background_do.setHeight(self.playlist_do.h + self.controller_do.h + 150);
                    self.playlist_do.setY(self.controller_do.h);
                    self.controller_do.setY(0);
                    self.main_do.setHeight(self.playlist_do.h + self.controller_do.h)
                } else {
                    self.background_do.setHeight(self.controller_do.h);
                    self.controller_do.setY(0);
                    self.main_do.setHeight(self.controller_do.h)
                }
            }
            if (self.data.openerAlignment_str == "right") {
                self.opener_do.setX(parseInt((self.ws.w - self.stageWidth) / 2) + self.stageWidth - self.opener_do.w)
            } else {
                if (self.main_do.x > 0) self.opener_do.setX(self.main_do.x)
            }
            MUSICTweenMax.killTweensOf(self.stageContainer);
            MUSICTweenMax.killTweensOf(self.background_do);
            MUSICTweenMax.killTweensOf(self.controller_do);
            MUSICTweenMax.killTweensOf(self.opener_do);
            self.center();
            if (e) {
                if (self.position_str == MUSIC.POSITION_TOP) {
                    if (self.playlist_do && self.playlist_do.isShowed_bl && self.controller_do.isShowed_bl) {
                        MUSICTweenMax.to(self.stageContainer, .8, {
                            css: {
                                top: 0
                            },
                            ease: Expo.easeInOut
                        });
                        MUSICTweenMax.to(self.opener_do, .8, {
                            y: self.playlist_do.h + self.controller_do.h,
                            ease: Expo.easeInOut
                        })
                    } else if (self.controller_do.isShowed_bl && self.playlist_do) {
                        MUSICTweenMax.to(self.stageContainer, .8, {
                            css: {
                                top: -self.playlist_do.h
                            },
                            ease: Expo.easeInOut
                        });
                        MUSICTweenMax.to(self.opener_do, .8, {
                            y: self.playlist_do.h + self.controller_do.h,
                            ease: Expo.easeInOut
                        })
                    } else if (!self.controller_do.isShowed_bl && self.playlist_do) {
                        MUSICTweenMax.to(self.stageContainer, .8, {
                            css: {
                                top: -self.playlist_do.h - self.controller_do.h
                            },
                            ease: Expo.easeInOut
                        });
                        MUSICTweenMax.to(self.opener_do, .8, {
                            y: self.playlist_do.h + self.controller_do.h,
                            ease: Expo.easeInOut,
                            onComplete: self.moveWheyLeft
                        })
                    } else if (self.controller_do.isShowed_bl) {
                        MUSICTweenMax.to(self.stageContainer, .8, {
                            css: {
                                top: 0
                            },
                            ease: Expo.easeInOut
                        });
                        MUSICTweenMax.to(self.opener_do, .8, {
                            y: self.controller_do.h,
                            ease: Expo.easeInOut
                        })
                    } else {
                        MUSICTweenMax.to(self.stageContainer, .8, {
                            css: {
                                top: -self.controller_do.h
                            },
                            ease: Expo.easeInOut
                        });
                        MUSICTweenMax.to(self.opener_do, .8, {
                            y: self.controller_do.h,
                            ease: Expo.easeInOut
                        })
                    }
                } else {
                    if (self.playlist_do && self.playlist_do.isShowed_bl && self.controller_do.isShowed_bl) {
                        MUSICTweenMax.to(self.stageContainer, .8, {
                            css: {
                                top: self.ws.h - self.controller_do.h - self.playlist_do.h
                            },
                            ease: Expo.easeInOut
                        })
                    } else if (self.controller_do.isShowed_bl && self.playlist_do) {
                        MUSICTweenMax.to(self.stageContainer, .8, {
                            css: {
                                top: self.ws.h - self.controller_do.h
                            },
                            ease: Expo.easeInOut
                        })
                    } else if (self.controller_do.isShowed_bl) {
                        MUSICTweenMax.to(self.stageContainer, .8, {
                            css: {
                                top: self.ws.h - self.controller_do.h
                            },
                            ease: Expo.easeInOut
                        })
                    } else if (self.controller_do.isShowed_bl) {
                        MUSICTweenMax.to(self.stageContainer, .8, {
                            css: {
                                top: 0
                            },
                            ease: Expo.easeInOut
                        })
                    } else {
                        MUSICTweenMax.to(self.stageContainer, .8, {
                            css: {
                                top: self.ws.h
                            },
                            ease: Expo.easeInOut,
                            onComplete: self.moveWheyLeft
                        })
                    }
                    MUSICTweenMax.to(self.opener_do, .8, {
                        y: -self.opener_do.h,
                        ease: Expo.easeInOut
                    })
                }
            } else {
                if (self.position_str == MUSIC.POSITION_TOP) {
                    if (self.playlist_do && self.playlist_do.isShowed_bl && self.controller_do.isShowed_bl) {
                        self.stageContainer.style.top = "0px";
                        self.opener_do.setY(self.playlist_do.h + self.controller_do.h)
                    } else if (self.controller_do.isShowed_bl && self.playlist_do) {
                        self.stageContainer.style.top = -self.playlist_do.h + "px";
                        self.opener_do.setY(self.playlist_do.h + self.controller_do.h)
                    } else if (!self.controller_do.isShowed_bl && self.playlist_do) {
                        self.stageContainer.style.top = -self.playlist_do.h - self.controller_do.h + "px";
                        self.opener_do.setY(self.playlist_do.h + self.controller_do.h)
                    } else if (self.controller_do.isShowed_bl) {
                        self.stageContainer.style.top = "0px";
                        self.opener_do.setY(self.controller_do.h)
                    } else {
                        self.stageContainer.style.top = -self.controller_do.h + "px";
                        self.opener_do.setY(self.controller_do.h);
                        self.moveWheyLeft()
                    }
                } else {
                    if (self.playlist_do && self.playlist_do.isShowed_bl && self.controller_do.isShowed_bl) {
                        self.stageContainer.style.top = self.ws.h - self.controller_do.h - self.playlist_do.h + "px"
                    } else if (self.controller_do.isShowed_bl && self.playlist_do) {
                        self.stageContainer.style.top = self.ws.h - self.controller_do.h + "px"
                    } else if (self.controller_do.isShowed_bl) {
                        self.stageContainer.style.top = self.ws.h - self.controller_do.h + "px"
                    } else {
                        self.stageContainer.style.top = self.ws.h + "px";
                        self.moveWheyLeft()
                    }
                    self.opener_do.setY(-self.opener_do.h)
                }
            }
        };
        this.moveWheyLeft = function() {
            self.main_do.setX(-5e3);
            self.background_do.setWidth(0)
        };
        this.center = function() {
            self.main_do.setX(parseInt((self.ws.w - self.stageWidth) / 2));
            self.background_do.getStyle().width = "100%"
        };
        this.setupContextMenu = function() {
            self.customContextMenu_do = new MUSICContextMenu(self.main_do, self.data.rightClickContextMenu_str)
        };
        this.setupMainInstances = function() {
            if (self.controller_do) return;
            if (MUSIC.hasHTML5Audio) self.setupAudioScreen();
            if (self.data.showPlaylistsButtonAndPlaylists_bl) self.setupCategories();
            if (self.data.showPlayListButtonAndPlaylist_bl) self.setupPlaylist();
            self.setupController();
            self.setupOpener();
            self.controller_do.resizeAndPosition()
        };
        this.setupData = function() {
            MUSICAudioData.setPrototype();
            self.data = new MUSICAudioData(self.props_obj, self.rootElement_el, self);
            self.data.addListener(MUSICAudioData.PRELOADER_LOAD_DONE, self.onPreloaderLoadDone);
            self.data.addListener(MUSICAudioData.LOAD_ERROR, self.dataLoadError);
            self.data.addListener(MUSICAudioData.SKIN_LOAD_COMPLETE, self.dataSkinLoadComplete);
            self.data.addListener(MUSICAudioData.PLAYLIST_LOAD_COMPLETE, self.dataPlayListLoadComplete)
        };
        self.onPreloaderLoadDone = function() {
            self.maxHeight = 32;
            self.background_do.getStyle().background = "url('" + self.data.skinPath_str + "main-background.png" + "')";
            self.setupPreloader();
            if (!self.isMobile_bl && self.data.showContextMenu_bl) self.setupContextMenu();
            self.resizeHandler();
            self.main_do.setHeight(self.stageHeight);
            if (self.openInPopup_bl) self.main_do.setHeight(3e3)
        };
        self.dataLoadError = function(e) {
            self.maxHeight = 120;
            if (self.preloader_do) self.preloader_do.hide(false);
            self.main_do.addChild(self.info_do);
            self.info_do.showText(e.text);
            if (!self.controller_do) {
                if (!self.ws) self.ws = MUSICUtils.getViewportSize();
                if (self.position_str == MUSIC.POSITION_TOP) {
                    self.stageContainer.style.top = "0px"
                } else {
                    self.stageContainer.style.top = self.ws.h - self.maxHeight + "px"
                }
                self.main_do.setHeight(self.maxHeight)
            }
            self.resizeHandler();
            self.dispatchEvent(MUSIC.ERROR, {
                error: e.text
            })
        };
        self.dataSkinLoadComplete = function() {
            self.animate_bl = self.data.animate_bl;
            if (self.useDeepLinking_bl) {
                setTimeout(function() {
                    self.setupDL()
                }, 200)
            } else {
                if (self.openInPopup_bl) {
                    self.catId = self.popupWindow.catId;
                    self.id = self.popupWindow.id
                } else {
                    self.catId = self.data.startAtPlaylist;
                    self.id = self.data.startAtTrack
                }
                self.loadInternalPlaylist()
            }
        };
        this.dataPlayListLoadComplete = function() {
            if (!self.isAPIReady_bl) self.dispatchEvent(MUSIC.READY);
            self.isAPIReady_bl = true;
            self.isPlaylistLoaded_bl = true;
            if (MUSIC.hasHTML5Audio) {
                self.setupMainInstances();
                self.updatePlaylist()
            } else {
                if (self.flash_do) {
                    self.updatePlaylist()
                } else {
                    self.setupFlashScreen()
                }
            }
            self.dispatchEvent(MUSIC.LOAD_PLAYLIST_COMPLETE)
        };
        this.updatePlaylist = function() {
            if (self.main_do)
                if (self.main_do.contains(self.info_do)) self.main_do.removeChild(self.info_do);
            self.preloader_do.hide(true);
            self.prevId = -1;
            self.totalAudio = self.data.playlist_ar.length;
            self.controller_do.enableControllerWhileLoadingPlaylist();
            self.controller_do.cleanThumbnails(true);
            if (self.playlist_do) {
                self.playlist_do.updatePlaylist(self.data.playlist_ar);
                self.playlist_do.resizeAndPosition()
            }
            if (self.openInPopup_bl && self.popupWindow.audioScreen_do) self.lastPercentPlayed = self.popupWindow.audioScreen_do.lastPercentPlayed;
            self.setSource();
            if (self.data.autoPlay_bl) self.play();
            self.setStageContainerFinalHeightAndPosition(false);
            if (self.openInPopup_bl && !self.showedFirstTime_bl) {
                self.controller_do.setY(-self.controller_do.h);
                if (self.playlist_do) self.playlist_do.setY(-self.playlist_do.h)
            } else {
                if (self.playlist_do) self.playlist_do.setY(-self.playlist_do.h + self.controller_do.h)
            }
            if (self.openInPopup_bl) {
                clearTimeout(self.showPlaylistWithDelayId_to);
                if (!self.showedFirstTime_bl) {
                    self.showPlaylistWithDelayId_to = setTimeout(function() {
                        self.setStageContainerFinalHeightAndPosition(true)
                    }, 900)
                } else {
                    self.showPlaylistWithDelayId_to = setTimeout(function() {
                        self.setStageContainerFinalHeightAndPosition(true)
                    }, 100)
                }
                self.showedFirstTime_bl = true;
                self.allowToResizeAndPosition_bl = true;
                return
            }
            self.allowToResizeAndPosition_bl = true;
            if (self.position_str == MUSIC.POSITION_TOP) {
                if (self.playlist_do && self.controller_do.isShowed_bl) {
                    if (!self.showedFirstTime_bl) {
                        self.stageContainer.style.top = -self.controller_do.h - self.playlist_do.h + "px";
                        self.opener_do.setY(self.controller_do.h + self.playlist_do.h - self.opener_do.h)
                    } else {
                        self.stageContainer.style.top = -self.playlist_do.h + "px";
                        self.opener_do.setY(self.controller_do.h + self.playlist_do.h)
                    }
                } else if (self.controller_do.isShowed_bl) {
                    if (self.playlist_do) {
                        self.stageContainer.style.top = self.controller_do.h + "px";
                        self.opener_do.setY(self.controller_do.h + self.playlist_do.h - self.opener_do.h)
                    } else {
                        if (!self.showedFirstTime_bl) {
                            self.stageContainer.style.top = -self.controller_do.h + "px";
                            self.opener_do.setY(self.controller_do.h - self.opener_do.h)
                        }
                    }
                } else {
                    if (self.playlist_do) {
                        self.stageContainer.style.top = -self.controller_do.h - self.playlist_do.h + "px";
                        self.opener_do.setY(0)
                    } else {
                        if (!self.showedFirstTime_bl) {
                            self.stageContainer.style.top = -self.controller_do.h + "px";
                            self.opener_do.setY(-self.opener_do.h)
                        } else {
                            self.stageContainer.style.top = -self.controller_do.h + "px";
                            self.opener_do.setY(0)
                        }
                    }
                }
            } else {
                if (self.controller_do.isShowed_bl || self.playlist_do && self.controller_do.isShowed_bl) {
                    if (!self.showedFirstTime_bl) {
                        self.stageContainer.style.top = self.ws.h + "px";
                        self.opener_do.setY(0)
                    } else {
                        self.stageContainer.style.top = self.ws.h - self.controller_do.h + "px";
                        self.opener_do.setY(-self.opener_do.h)
                    }
                } else {
                    if (!self.showedFirstTime_bl) {
                        self.stageContainer.style.top = self.ws.h + "px";
                        self.opener_do.setY(0)
                    } else {
                        self.stageContainer.style.top = self.ws.h + "px";
                        self.opener_do.setY(-self.opener_do.h)
                    }
                }
            }
            clearTimeout(self.showPlaylistWithDelayId_to);
            self.showPlaylistWithDelayId_to = setTimeout(function() {
                self.setStageContainerFinalHeightAndPosition(true)
            }, 900);
            self.showedFirstTime_bl = true
        };
        this.loadInternalPlaylist = function() {
            self.isPlaylistLoaded_bl = false;
            self.data.loadPlaylist(self.catId);
            self.stop();
            self.preloader_do.show(true);
            if (self.controller_do) {
                self.controller_do.disableControllerWhileLoadingPlaylist();
                self.controller_do.loadThumb()
            }
            if (self.playlist_do) self.playlist_do.destroyPlaylist();
            self.positionPreloader();
            self.setStageContainerFinalHeightAndPosition(false);
            self.dispatchEvent(MUSIC.START_TO_LOAD_PLAYLIST)
        };
        this.setupDL = function() {
            FWDAddress.onChange = self.dlChangeHandler;
            self.dlChangeHandler()
        };
        this.dlChangeHandler = function() {
            var e = false;
            if (self.categories_do && self.categories_do.isOnDOM_bl) {
                self.categories_do.hide();
                return
            }
            self.catId = parseInt(FWDAddress.getParameter("catid"));
            self.id = parseInt(FWDAddress.getParameter("trackid"));
            if (self.catId == undefined || self.id == undefined || isNaN(self.catId) || isNaN(self.id)) {
                self.catId = self.data.startAtPlaylist;
                self.id = self.data.startAtTrack;
                e = true
            }
            if (self.catId < 0 || self.catId > self.data.totalCategories - 1 && !e) {
                self.catId = self.data.startAtPlaylist;
                self.id = self.data.startAtTrack;
                e = true
            }
            if (self.data.playlist_ar) {
                if (self.id < 0 && !e) {
                    self.id = self.data.startAtTrack;
                    e = true
                } else if (self.prevCatId == self.catId && self.id > self.data.playlist_ar.length - 1 && !e) {
                    self.id = self.data.playlist_ar.length - 1;
                    e = true
                }
            }
            if (e) {
                location.hash = self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id;
                return
            }
            if (self.prevCatId != self.catId) {
                self.loadInternalPlaylist();
                self.prevCatId = self.catId
            } else {
                self.setSource(false);
                self.play()
            }
        };
        this.setupPreloader = function() {
            MUSICPreloader.setPrototype();
            self.preloader_do = new MUSICPreloader(self.data.preloaderPath_str, 53, 34, 30, 80);
            self.preloader_do.addListener(MUSICPreloader.HIDE_COMPLETE, self.preloaderHideComplete);
            if (MUSICUtils.isIEAndLessThen9) {
                self.preloader_do.getStyle().zIndex = "2147483633"
            } else {
                self.preloader_do.getStyle().zIndex = "99999999993"
            }
            self.preloader_do.setPosition("fixed");
            self.preloader_do.setForFixedPosition();
            self.preloader_do.show(true);
            document.documentElement.appendChild(self.preloader_do.screen)
        };
        this.positionPreloader = function() {
            self.preloader_do.setX(parseInt((self.ws.w - self.preloader_do.w) / 2));
            if (self.openInPopup_bl) {
                if (self.controller_do) {
                    self.preloader_do.setY(parseInt((self.controller_do.h - self.preloader_do.h) / 2))
                } else {
                    self.preloader_do.setY(0)
                }
            } else if (self.position_str == MUSIC.POSITION_TOP) {
                if (self.controller_do && !self.controller_do.isShowed_bl) {
                    self.preloader_do.setY(-200)
                } else if (self.controller_do) {
                    self.preloader_do.setY(parseInt((self.controller_do.h - self.preloader_do.h) / 2))
                } else {
                    self.preloader_do.setY(parseInt((self.stageHeight - self.preloader_do.h) / 2))
                }
            } else {
                if (self.controller_do && !self.controller_do.isShowed_bl) {
                    self.preloader_do.setY(self.ws.h)
                } else if (self.controller_do) {
                    self.preloader_do.setY(self.ws.h - self.controller_do.h + parseInt((self.controller_do.h - self.preloader_do.h) / 2))
                } else {
                    self.preloader_do.setY(self.ws.h - self.preloader_do.h)
                }
            }
        };
        this.preloaderHideComplete = function() {
            self.controller_do.show();
            self.opener_do.show();
            if (self.playlist_do) self.playlist_do.show();
            self.isFirstPlaylistLoaded_bl = true;
            self.allowToResizeAndPosition_bl = true;
            if (!self.animate_bl) self.setStageContainerFinalHeightAndPosition(false)
        };
        this.setupOpener = function() {
            MUSICOpener.setPrototype();
            self.opener_do = new MUSICOpener(self.data, self.position_str, self.controller_do.isShowed_bl);
            if (MUSICUtils.isIEAndLessThen9) {
                self.opener_do.getStyle().zIndex = "2147483634"
            } else {
                self.opener_do.getStyle().zIndex = "99999999994"
            }
            self.opener_do.setX(-1e3);
            if (self.controller_do.isShowed_bl) {
                self.opener_do.showCloseButton()
            } else {
                self.opener_do.showOpenButton()
            }
            self.opener_do.addListener(MUSICOpener.SHOW, self.openerShowHandler);
            self.opener_do.addListener(MUSICOpener.HIDE, self.openerHideHandler);
            self.opener_do.addListener(MUSICController.PLAY, self.controllerOnPlayHandler);
            self.opener_do.addListener(MUSICController.PAUSE, self.controllerOnPauseHandler);
            if (self.data.showOpener_bl) self.stageContainer.appendChild(self.opener_do.screen)
        };
        this.openerShowHandler = function() {
            self.showPlayer()
        };
        this.openerHideHandler = function() {
            self.hidePlayer()
        };
        this.setupCategories = function() {
            MUSICCategories.setPrototype();
            self.categories_do = new MUSICCategories(self.data);
            if (MUSICUtils.isIEAndLessThen9) {
                self.categories_do.getStyle().zIndex = "2147483635"
            } else {
                self.categories_do.getStyle().zIndex = "99999999995"
            }
            self.categories_do.addListener(MUSICCategories.HIDE_COMPLETE, self.categoriesHideCompleteHandler);
            if (self.data.showPlaylistsByDefault_bl) {
                self.showCatWidthDelayId_to = setTimeout(function() {
                    self.showCategories()
                }, 1400)
            }
        };
        this.categoriesHideCompleteHandler = function(e) {
            self.controller_do.setCategoriesButtonState("unselected");
            if (self.customContextMenu_do) self.customContextMenu_do.updateParent(self.main_do);
            if (self.useDeepLinking_bl) {
                if (self.categories_do.id != self.catId) {
                    self.catId = self.categories_do.id;
                    self.id = 0;
                    FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id)
                }
            } else {
                if (self.catId == self.categories_do.id) return;
                self.catId = self.categories_do.id;
                self.id = 0;
                self.loadInternalPlaylist(self.catId)
            }
        };
        this.setupPlaylist = function() {
            MUSICPlaylist.setPrototype();
            self.playlist_do = new MUSICPlaylist(self.data, self);
            self.playlist_do.addListener(MUSICPlaylistItem.MOUSE_UP, self.palylistItemOnUpHandler);
            self.playlist_do.addListener(MUSICPlaylistItem.DOWNLOAD, self.palylistItemDownloadHandler);
            self.playlist_do.addListener(MUSICPlaylistItem.BUY, self.palylistItemBuyHandler);
            self.playlist_do.addListener(MUSICPlaylist.UPDATE_TRACK_TITLE_if_FOLDER, self.palylistUpdateFolderTrackTitle);
            self.main_do.addChild(self.playlist_do)
        };
        this.palylistItemOnUpHandler = function(e) {
            if (MUSIC.hasHTML5Audio) {
                if (self.audioScreen_do.isPlaying_bl && e.id == self.id) {
                    self.pause()
                } else if (!self.audioScreen_do.isStopped_bl && e.id == self.id) {
                    self.play()
                } else {
                    if (self.useDeepLinking_bl && self.id != e.id) {
                        FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + e.id);
                        self.id = e.id
                    } else {
                        self.id = e.id;
                        self.setSource(true);
                        self.play()
                    }
                }
            } else if (self.isFlashScreenReady_bl) {
                if (self.flashObject.isAudioPlaying() && e.id == self.id) {
                    self.pause()
                } else if (!self.flashObject.isAudioStopped() && e.id == self.id) {
                    self.play()
                } else {
                    if (self.useDeepLinking_bl && self.id != e.id) {
                        FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + e.id);
                        self.id = e.id
                    } else {
                        self.id = e.id;
                        self.setSource(true);
                        self.play()
                    }
                }
            }
        };
        this.palylistItemDownloadHandler = function(e) {
            self.downloadMP3(e.id)
        };
        this.palylistUpdateFolderTrackTitle = function(e) {
            self.controller_do.setTitle(e.title)
        };
        this.palylistItemBuyHandler = function(e) {
            self.buy(e.id)
        };
        this.setupController = function() {
            MUSICController.setPrototype();
            self.controller_do = new MUSICController(self.data, self);
            self.controller_do.addListener(MUSICController.POPUP, self.controllerOnPopupHandler);
            self.controller_do.addListener(MUSICController.PLAY, self.controllerOnPlayHandler);
            self.controller_do.addListener(MUSICController.PLAY_NEXT, self.controllerPlayNextHandler);
            self.controller_do.addListener(MUSICController.PLAY_PREV, self.controllerPlayPrevHandler);
            self.controller_do.addListener(MUSICController.PAUSE, self.controllerOnPauseHandler);
            self.controller_do.addListener(MUSICController.VOLUME_START_TO_SCRUB, self.volumeStartToScrubbHandler);
            self.controller_do.addListener(MUSICController.VOLUME_STOP_TO_SCRUB, self.volumeStopToScrubbHandler);
            self.controller_do.addListener(MUSICController.START_TO_SCRUB, self.controllerStartToScrubbHandler);
            self.controller_do.addListener(MUSICController.SCRUB, self.controllerScrubbHandler);
            self.controller_do.addListener(MUSICController.SCRUB_PLAYLIST_ITEM, self.controllerPlaylistItemScrubbHandler);
            self.controller_do.addListener(MUSICController.STOP_TO_SCRUB, self.controllerStopToScrubbHandler);
            self.controller_do.addListener(MUSICController.CHANGE_VOLUME, self.controllerChangeVolumeHandler);
            self.controller_do.addListener(MUSICController.SHOW_CATEGORIES, self.showCategoriesHandler);
            self.controller_do.addListener(MUSICController.SHOW_PLAYLIST, self.showPlaylistHandler);
            self.controller_do.addListener(MUSICController.HIDE_PLAYLIST, self.hidePlaylistHandler);
            self.controller_do.addListener(MUSICController.ENABLE_LOOP, self.enableLoopHandler);
            self.controller_do.addListener(MUSICController.DISABLE_LOOP, self.disableLoopHandler);
            self.controller_do.addListener(MUSICController.DOWNLOAD_MP3, self.controllerButtonDownloadMp3Handler);
            self.controller_do.addListener(MUSICController.ENABLE_SHUFFLE, self.enableShuffleHandler);
            self.controller_do.addListener(MUSICController.DISABLE_SHUFFLE, self.disableShuffleHandler);
            self.controller_do.addListener(MUSICController.BUY, self.controllerButtonBuyHandler);
            self.main_do.addChild(self.controller_do);
            if (self.openInPopup_bl && self.data.showPlaylistsButtonAndPlaylists_bl) {
                self.controller_do.setPlaylistButtonState("selected");
                if (self.controller_do.playlistButton_do) self.controller_do.playlistButton_do.disableForGood()
            }
        };
        this.controllerOnPopupHandler = function() {
            self.popup()
        };
        this.controllerOnPlayHandler = function(e) {
            if (MUSIC.hasHTML5Audio) {
                self.audioScreen_do.play()
            } else if (self.isFlashScreenReady_bl) {
                self.flashObject.playAudio()
            }
        };
        this.controllerPlayNextHandler = function(e) {
            if (self.data.shuffle_bl) {
                self.playShuffle()
            } else {
                self.playNext()
            }
        };
        this.controllerPlayPrevHandler = function(e) {
            if (self.data.shuffle_bl) {
                self.playShuffle()
            } else {
                self.playPrev()
            }
        };
        this.controllerOnPauseHandler = function(e) {
            if (MUSIC.hasHTML5Audio) {
                self.audioScreen_do.pause()
            } else if (self.isFlashScreenReady_bl) {
                self.flashObject.pauseAudio()
            }
        };
        this.volumeStartToScrubbHandler = function(e) {
            if (self.playlist_do) self.playlist_do.showDisable()
        };
        this.volumeStopToScrubbHandler = function(e) {
            if (self.playlist_do) self.playlist_do.hideDisable()
        };
        this.controllerStartToScrubbHandler = function(e) {
            if (self.playlist_do) self.playlist_do.showDisable();
            if (MUSIC.hasHTML5Audio) {
                self.audioScreen_do.startToScrub()
            } else if (self.isFlashScreenReady_bl) {
                MUSIC.pauseAllAudio(self);
                self.flashObject.startToScrub()
            }
        };
        this.controllerScrubbHandler = function(e) {
            if (MUSIC.hasHTML5Audio) {
                self.audioScreen_do.scrub(e.percent)
            } else if (self.isFlashScreenReady_bl) {
                self.flashObject.scrub(e.percent)
            }
        };
        this.controllerPlaylistItemScrubbHandler = function(e) {
            if (self.playlist_do) self.playlist_do.updateCurItemProgress(e.percent)
        };
        this.controllerStopToScrubbHandler = function(e) {
            if (self.playlist_do) self.playlist_do.hideDisable();
            if (MUSIC.hasHTML5Audio) {
                self.audioScreen_do.stopToScrub()
            } else if (self.isFlashScreenReady_bl) {
                self.flashObject.stopToScrub()
            }
        };
        this.controllerChangeVolumeHandler = function(e) {
            if (MUSIC.hasHTML5Audio) {
                self.audioScreen_do.setVolume(e.percent)
            } else if (self.isFlashScreenReady_bl) {
                self.flashObject.setVolume(e.percent)
            }
        };
        this.showCategoriesHandler = function(e) {
            self.showCategories();
            self.controller_do.setCategoriesButtonState("selected")
        };
        this.showPlaylistHandler = function(e) {
            self.showPlaylist()
        };
        this.hidePlaylistHandler = function(e) {
            self.hidePlaylist()
        };
        this.enableLoopHandler = function(e) {
            self.data.loop_bl = true;
            self.data.shuffle_bl = false;
            self.controller_do.setLoopStateButton("selected");
            self.controller_do.setShuffleButtonState("unselected")
        };
        this.disableLoopHandler = function(e) {
            self.data.loop_bl = false;
            self.controller_do.setLoopStateButton("unselected")
        };
        this.enableShuffleHandler = function(e) {
            self.data.shuffle_bl = true;
            self.data.loop_bl = false;
            self.controller_do.setShuffleButtonState("selected");
            self.controller_do.setLoopStateButton("unselected")
        };
        this.controllerButtonDownloadMp3Handler = function(e) {
            self.downloadMP3()
        };
        this.disableShuffleHandler = function(e) {
            self.data.shuffle_bl = false;
            self.controller_do.setShuffleButtonState("unselected")
        };
        this.controllerButtonBuyHandler = function() {
            self.buy()
        };
        this.setupAudioScreen = function() {
            MUSICAudioScreen.setPrototype();
            self.audioScreen_do = new MUSICAudioScreen(self.data.volume, self.data.autoPlay_bl, self.data.loop_bl);
            self.audioScreen_do.addListener(MUSICAudioScreen.ERROR, self.audioScreenErrorHandler);
            self.audioScreen_do.addListener(MUSICAudioScreen.START, self.audioScreenSatrtHandler);
            self.audioScreen_do.addListener(MUSICAudioScreen.SAFE_TO_SCRUBB, self.audioScreenSafeToScrubbHandler);
            self.audioScreen_do.addListener(MUSICAudioScreen.STOP, self.audioScreenStopHandler);
            self.audioScreen_do.addListener(MUSICAudioScreen.PLAY, self.audioScreenPlayHandler);
            self.audioScreen_do.addListener(MUSICAudioScreen.PAUSE, self.audioScreenPauseHandler);
            self.audioScreen_do.addListener(MUSICAudioScreen.UPDATE, self.audioScreenUpdateHandler);
            self.audioScreen_do.addListener(MUSICAudioScreen.UPDATE_TIME, self.audioScreenUpdateTimeHandler);
            self.audioScreen_do.addListener(MUSICAudioScreen.LOAD_PROGRESS, self.audioScreenLoadProgressHandler);
            self.audioScreen_do.addListener(MUSICAudioScreen.PLAY_COMPLETE, self.audioScreenPlayCompleteHandler);
            if (self.useOnlyAPI_bl) {
                document.documentElement.appendChild(self.audioScreen_do.screen)
            } else {
                self.main_do.addChild(self.audioScreen_do)
            }
        };
        this.audioScreenErrorHandler = function(e) {
            var t;
            if (MUSIC.hasHTML5Audio) {
                t = e.text;
                if (self.main_do) self.main_do.addChild(self.info_do);
                if (self.info_do) self.info_do.showText(t)
            } else {
                t = e;
                if (self.main_do) self.main_do.addChild(self.info_do);
                if (self.info_do) self.info_do.showText(t)
            }
            if (self.position_str == MUSIC.POSITION_TOP && self.playlist_do) {
                self.info_do.setY(self.playlist_do.h);
                self.info_do.setHeight(self.controller_do.h)
            }
            self.dispatchEvent(MUSIC.ERROR, {
                error: t
            })
        };
        this.audioScreenSatrtHandler = function() {
            self.dispatchEvent(MUSIC.START)
        };
        this.audioScreenSafeToScrubbHandler = function() {
            if (self.controller_do) self.controller_do.enableMainScrubber()
        };
        this.audioScreenStopHandler = function(e) {
            if (self.main_do)
                if (self.main_do.contains(self.info_do)) self.main_do.removeChild(self.info_do);
            if (self.controller_do) {
                self.controller_do.showPlayButton();
                self.controller_do.stopEqulizer();
                self.controller_do.disableMainScrubber()
            }
            self.dispatchEvent(MUSIC.STOP)
        };
        this.audioScreenPlayHandler = function() {
            if (self.controller_do) {
                self.controller_do.showPauseButton();
                self.controller_do.startEqulizer()
            }
            if (self.opener_do) self.opener_do.showPauseButton();
            if (self.playlist_do) self.playlist_do.setCurItemPauseState();
            if (self.openInPopup_bl) {
                setTimeout(function() {
                    if (!self.scrubbedFirstTimeInPopup_bl) self.scrub(self.lastPercentPlayed);
                    self.scrubbedFirstTimeInPopup_bl = true
                }, 600)
            }
            self.dispatchEvent(MUSIC.PLAY)
        };
        this.audioScreenPauseHandler = function() {
            if (self.controller_do) {
                self.controller_do.showPlayButton();
                self.controller_do.stopEqulizer()
            }
            if (self.opener_do) self.opener_do.showPlayButton();
            if (self.playlist_do) {
                self.playlist_do.setCurItemPlayState()
            }
            self.dispatchEvent(MUSIC.PAUSE)
        };
        this.audioScreenUpdateHandler = function(e) {
            var t;
            if (MUSIC.hasHTML5Audio) {
                t = e.percent;
                if (self.controller_do) self.controller_do.updateMainScrubber(t);
                if (self.playlist_do) self.playlist_do.updateCurItemProgress(t)
            } else {
                t = e;
                if (self.controller_do) self.controller_do.updateMainScrubber(t);
                if (self.playlist_do) self.playlist_do.updateCurItemProgress(t)
            }
            self.dispatchEvent(MUSIC.UPDATE, {
                percent: t
            })
        };
        this.audioScreenUpdateTimeHandler = function(e, t) {
            var n;
            var r;
            if (MUSIC.hasHTML5Audio) {
                n = e.curTime;
                r = e.totalTime;
                if (self.controller_do) self.controller_do.updateTime(n, r)
            } else {
                n = e;
                r = t;
                if (r.length > n.length) n = parseInt(r.substring(0, 1)) - 1 + ":" + n;
                if (self.controller_do) self.controller_do.updateTime(n, r)
            }
            self.dispatchEvent(MUSIC.UPDATE_TIME, {
                curTime: n,
                totalTime: r
            })
        };
        this.audioScreenLoadProgressHandler = function(e) {
            if (MUSIC.hasHTML5Audio) {
                if (self.controller_do) self.controller_do.updatePreloaderBar(e.percent)
            } else {
                if (self.controller_do) self.controller_do.updatePreloaderBar(e)
            }
        };
        this.audioScreenPlayCompleteHandler = function() {
            self.dispatchEvent(MUSIC.PLAY_COMPLETE);
            if (MUSIC.hasHTML5Audio) {
                if (self.data.loop_bl) {
                    self.audioScreen_do.replay()
                } else if (self.data.shuffle_bl) {
                    self.playShuffle()
                } else {
                    self.playNext()
                }
            } else if (self.isFlashScreenReady_bl) {
                if (self.data.loop_bl) {
                    self.flashObject.replayAudio()
                } else if (self.data.shuffle_bl) {
                    self.playShuffle()
                } else {
                    self.playNext()
                }
            }
        };
        this.setupFlashScreen = function() {
            if (self.flash_do) return;
            if (!FWDFlashTest.hasFlashPlayerVersion("9.0.18")) {
                if (self.useOnlyAPI_bl) {
                    alert("Please install Adobe flash player! <a href='http://www.adobe.com/go/getflashplayer'>Click here to install.</a>")
                } else {
                    self.main_do.addChild(self.info_do);
                    self.info_do.showText("Please install Adobe flash player! <a href='http://www.adobe.com/go/getflashplayer'>Click here to install.</a>")
                }
                if (self.preloader_do) self.preloader_do.hide(false);
                return
            }
            self.flash_do = new MUSICDisplayObject("div");
            self.flash_do.setBackfaceVisibility();
            self.flash_do.setResizableSizeAfterParent();
            if (self.useOnlyAPI_bl) {
                document.getElementsByTagName("body")[0].appendChild(self.flash_do.screen)
            } else {
                self.main_do.addChild(self.flash_do)
            }
            var e = "not defined!";
            self.flashObjectMarkup_str = '<object id="' + (self.instanceName_str + "1") + '" name="' + (self.instanceName_str + "1") + '" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="100%" height="100%"><param name="movie" value="' + self.data.flashPath_str + '"/><param name="wmode" value="transparent"><param name=FlashVars value="instanceName=' + self.instanceName_str + "&sourcePath=" + e + "&volume=" + self.data.volume + "&autoPlay=" + self.data.autoPlay_bl + "&loop=" + self.data.loop_bl + '"/><param name = "allowScriptAccess" value="always" /><!--[if !IE]>--><object name="myCom" type="application/x-shockwave-flash" data="' + self.data.flashPath_str + '" width="100%" height="100%"><param name="swliveconnect" value="true"/><param name="wmode" value="transparent"><param name=FlashVars value="instanceName=' + self.instanceName_str + "&sourcePath=" + e + "&volume=" + self.data.volume + "&autoPlay=" + self.data.autoPlay_bl + "&loop=" + self.data.loop_bl + '"/><!--<![endif]--><!--[if !IE]>--></object><!--<![endif]--></object>';
            self.flash_do.screen.innerHTML = self.flashObjectMarkup_str;
            self.flashObject = self.flash_do.screen.firstChild;
            if (!MUSICUtils.isIE) self.flashObject = self.flashObject.getElementsByTagName("object")[0]
        };
        this.flashScreenIsReady = function() {
            self.isFlashScreenReady_bl = true;
            self.setupMainInstances();
            self.updatePlaylist()
        };
        this.flashScreenFail = function() {
            self.main_do.addChild(self.info_do);
            self.info_do.showText("External interface error!");
            self.resizeHandler(false)
        };
        this.loadID3IfPlaylistDisabled = function() {
            var e = self.data.playlist_ar[self.id].source;
            var t = self.data.playlist_ar[self.id].title;
            if (t != "...") return;
            e = e + "?rand=" + parseInt(Math.random() * 99999999);
            ID3.loadTags(e, function() {
                var t = self.data.playlist_ar[self.id];
                var n = ID3.getAllTags(e);
                t.title = n.artist + " - " + n.title;
                t.titleText = t.title;
                self.controller_do.setTitle(t.title)
            })
        };
        this.setSource = function(e) {
            if (self.id < 0) {
                self.id = 0
            } else if (self.id > self.totalAudio - 1) {
                self.id = self.totalAudio - 1
            }
            var t = self.data.playlist_ar[self.id].source;
            if (MUSIC.hasHTML5Audio) {
                self.audioScreen_do.setSource(t)
            } else {
                var n = t.split(",");
                for (var r = 0; r < n.length; r++) {
                    t = n[r];
                    n[r] = MUSICUtils.trim(t)
                }
                for (var r = 0; r < n.length; r++) {
                    if (n[r].indexOf(".mp3") != -1) {
                        t = n[r];
                        break
                    }
                }
                self.flashObject.setSource(t)
            }
            self.controller_do.stopEqulizer();
            self.controller_do.setTitle(self.data.playlist_ar[self.id].title);
            if (self.data.playlist_ar[self.id].duration == undefined) {
                self.controller_do.updateTime("00:00", "00:00")
            } else {
                self.controller_do.updateTime("00:00", MUSIC.formatTotalTime(self.data.playlist_ar[self.id].duration))
            }
            self.controller_do.loadThumb(self.data.playlist_ar[self.id].thumbPath);
            if (self.playlist_do) self.playlist_do.activateItems(self.id, e);
            if (self.playlist_do) {
                self.playlist_do.activateItems(self.id, e)
            } else {
                self.loadID3IfPlaylistDisabled()
            }
        };

        this.showPlayer = function() {
            if (!self.isAPIReady_bl) return;
            self.controller_do.isShowed_bl = true;
            self.opener_do.showCloseButton();
            self.setStageContainerFinalHeightAndPosition(self.animate_bl);
            if (self.playlist_do) {
                clearTimeout(self.disablePlaylistForAWhileId_to);
                self.disablePlaylistForAWhileId_to = setTimeout(function() {
                    self.playlist_do.hideDisable()
                }, 500);
                self.playlist_do.showDisable()
            }
        };
        this.hidePlayer = function() {
            if (!self.isAPIReady_bl) return;
            self.controller_do.isShowed_bl = false;
            self.opener_do.showOpenButton();
            self.setStageContainerFinalHeightAndPosition(self.animate_bl)
        };
        this.loadPlaylist = function(e) {
            if (!self.isAPIReady_bl) return;
            if (self.data.prevId == e) return;
            self.catId = e;
            self.id = 0;
            if (self.catId < 0) {
                self.catId = 0
            } else if (self.catId > self.data.totalCategories - 1) {
                self.catId = self.data.totalCategories - 1
            }
            if (self.useDeepLinking_bl) {
                FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id)
            } else {
                self.loadInternalPlaylist()
            }
        };
        this.playNext = function() {
            if (!self.isAPIReady_bl || !self.isPlaylistLoaded_bl) return;
            if (self.data.showPlayListButtonAndPlaylist_bl) {
                if (self.playlist_do.items_ar[self.playlist_do.curItem_do.sortId + 1]) {
                    self.id = self.playlist_do.items_ar[self.playlist_do.curItem_do.sortId + 1].id
                } else {
                    self.id = self.playlist_do.items_ar[0].id
                }
            } else {
                self.id++;
                if (self.id < 0) {
                    self.id = self.totalAudio - 1
                } else if (self.id > self.totalAudio - 1) {
                    self.id = 0
                }
            }
            if (self.useDeepLinking_bl) {
                FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id)
            } else {
                self.setSource();
                self.play()
            }
            self.prevId = self.id
        };
        this.playPrev = function() {
            if (!self.isAPIReady_bl || !self.isPlaylistLoaded_bl) return;
            if (self.data.showPlayListButtonAndPlaylist_bl) {
                if (self.playlist_do.items_ar[self.playlist_do.curItem_do.sortId - 1]) {
                    self.id = self.playlist_do.items_ar[self.playlist_do.curItem_do.sortId - 1].id
                } else {
                    self.id = self.playlist_do.items_ar[self.totalAudio - 1].id
                }
            } else {
                self.id--;
                if (self.id < 0) {
                    self.id = self.totalAudio - 1
                } else if (self.id > self.totalAudio - 1) {
                    self.id = 0
                }
            }
            if (self.useDeepLinking_bl) {
                FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id)
            } else {
                self.setSource();
                self.play()
            }
            self.prevId = self.id
        };
        this.playShuffle = function() {
            if (!self.isAPIReady_bl || !self.isPlaylistLoaded_bl) return;
            var e = parseInt(Math.random() * self.data.playlist_ar.length);
            while (e == self.id) e = parseInt(Math.random() * self.data.playlist_ar.length);
            self.id = e;
            if (self.id < 0) {
                self.id = self.totalAudio - 1
            } else if (self.id > self.totalAudio - 1) {
                self.id = 0
            }
            if (self.useDeepLinking_bl) {
                FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id)
            } else {
                self.setSource();
                self.play()
            }
            self.prevId = self.id
        };
        this.playSpecificTrack = function(e, t) {
            if (!self.isAPIReady_bl || !self.isPlaylistLoaded_bl) return;
            self.catId = e;
            self.id = t;
            if (self.catId < 0) {
                self.catId = 0
            } else if (self.catId > self.data.totalCategories - 1) {
                self.catId = self.data.totalCategories - 1
            }
            if (self.id < 0) self.id = 0;
            if (self.useDeepLinking_bl) {
                FWDAddress.setValue(self.instanceName_str + "?catid=" + self.catId + "&trackid=" + self.id)
            } else {
                self.setSource();
                self.play()
            }
            self.prevId = self.id
        };
        this.play = function() {
            if (!self.isAPIReady_bl || !self.isPlaylistLoaded_bl) return;
            MUSIC.pauseAllAudio(self);
            if (MUSIC.hasHTML5Audio) {
                self.audioScreen_do.play()
            } else if (self.isFlashScreenReady_bl) {
                self.flashObject.playAudio()
            }
        };
        this.pause = function() {
            if (!self.isAPIReady_bl || !self.isPlaylistLoaded_bl) return;
            if (MUSIC.hasHTML5Audio) {
                self.audioScreen_do.pause()
            } else if (self.isFlashScreenReady_bl) {
                self.flashObject.pauseAudio()
            }
        };
        this.stop = function() {
            if (!self.isAPIReady_bl) return;
            if (MUSIC.hasHTML5Audio) {
                self.audioScreen_do.stop()
            } else if (self.isFlashScreenReady_bl) {
                self.flashObject.stopAudio()
            }
        };
        this.startToScrub = function() {
            if (!self.isAPIReady_bl || !self.isPlaylistLoaded_bl) return;
            if (MUSIC.hasHTML5Audio) {
                self.audioScreen_do.startToScrub()
            } else if (self.isFlashScreenReady_bl) {
                self.flashObject.startToScrub()
            }
        };
        this.stopToScrub = function() {
            if (!self.isAPIReady_bl || !self.isPlaylistLoaded_bl) return;
            if (MUSIC.hasHTML5Audio) {
                self.audioScreen_do.stopToScrub()
            } else if (self.isFlashScreenReady_bl) {
                self.flashObject.stopToScrub()
            }
        };
        this.scrub = function(e) {
            if (!self.isAPIReady_bl || !self.isPlaylistLoaded_bl) return;
            if (isNaN(e)) return;
            if (e < 0) {
                e = 0
            } else if (e > 1) {
                e = 1
            }
            if (MUSIC.hasHTML5Audio) {
                if (self.audioScreen_do) self.audioScreen_do.scrub(e)
            } else if (self.isFlashScreenReady_bl) {
                self.flashObject.scrub(e)
            }
        };
        this.setVolume = function(e) {
            if (!self.isAPIReady_bl) return;
            if (self.isMobile_bl) e = 1;
            self.controller_do.updateVolume(e)
        };
        this.showCategories = function() {
            if (!self.isAPIReady_bl) return;
            if (self.categories_do) {
                self.categories_do.show(self.catId);
                if (self.customContextMenu_do) self.customContextMenu_do.updateParent(self.categories_do);
                self.controller_do.setCategoriesButtonState("selected")
            }
        };
        this.hideCategories = function() {
            if (!self.isAPIReady_bl) return;
            if (self.categories_do) {
                self.categories_do.hide();
                self.controller_do.setCategoriesButtonState("unselected")
            }
        };
        this.showPlaylist = function() {
            if (!self.isAPIReady_bl) return;
            if (self.playlist_do) {
                self.isPlaylistShowed_bl = true;
                self.playlist_do.show(true);
                self.controller_do.setPlaylistButtonState("selected");
                clearTimeout(self.disablePlaylistForAWhileId_to);
                self.disablePlaylistForAWhileId_to = setTimeout(function() {
                    self.playlist_do.hideDisable()
                }, 150);
                self.playlist_do.showDisable()
            }
            self.setStageContainerFinalHeightAndPosition(self.animate_bl)
        };
        this.hidePlaylist = function() {
            if (!self.isAPIReady_bl) return;
            if (self.playlist_do) {
                self.isPlaylistShowed_bl = false;
                self.playlist_do.hide();
                self.controller_do.setPlaylistButtonState("unselected");
                self.setStageContainerFinalHeightAndPosition(self.animate_bl)
            }
        };
        this.getIsAPIReady = function() {
            return self.isAPIReady_bl
        };
        this.getCatId = function() {
            return self.catId
        };
        this.getTrackId = function() {
            return self.id
        };
        this.getTrackTitle = function() {
            if (!self.isAPIReady_bl) return;
            return self.data.playlist_ar[self.id].title
        };
        this.downloadMP3 = function(e) {
            if (document.location.protocol == "file:") {
                var t = "Downloading mp3 files local is not allowed or possible!. To function properly please test online.";
                self.main_do.addChild(self.info_do);
                self.info_do.showText(t);
                return
            }
            if (e == undefined) e = self.id;
            var n = self.data.playlist_ar[e].downloadPath;
            var r = self.data.playlist_ar[e].titleText;
            self.data.downloadMp3(n, r)
        };
        this.buy = function(pId) {
            if (!self.isAPIReady_bl) return;
            if (document.location.protocol == "file:") {
                var error = "Buying mp3 files local is not allowed or possible!. To function properly please test online.";
                self.main_do.addChild(self.info_do);
                self.info_do.showText(error);
                return
            }
            if (pId == undefined) pId = self.id;
            var buy = self.data.playlist_ar[pId].buy;
            if (buy.indexOf("http") != -1 && buy.indexOf("http") < 3) {
                window.open(buy)
            } else {
                eval(buy)
            }
        };
        this.addListener = function(e, t) {
            if (!this.listeners) return;
            if (e == undefined) throw Error("type is required.");
            if (typeof e === "object") throw Error("type must be of type String.");
            if (typeof t != "function") throw Error("listener must be of type Function.");
            var n = {};
            n.type = e;
            n.listener = t;
            n.target = this;
            this.listeners.events_ar.push(n)
        };
        this.dispatchEvent = function(e, t) {
            if (this.listeners == null) return;
            if (e == undefined) throw Error("type is required.");
            if (typeof e === "object") throw Error("type must be of type String.");
            for (var n = 0, r = this.listeners.events_ar.length; n < r; n++) {
                if (this.listeners.events_ar[n].target === this && this.listeners.events_ar[n].type === e) {
                    if (t) {
                        for (var i in t) {
                            this.listeners.events_ar[n][i] = t[i]
                        }
                    }
                    this.listeners.events_ar[n].listener.call(this, this.listeners.events_ar[n])
                }
            }
        };
        this.removeListener = function(e, t) {
            if (e == undefined) throw Error("type is required.");
            if (typeof e === "object") throw Error("type must be of type String.");
            if (typeof t != "function") throw Error("listener must be of type Function." + e);
            for (var n = 0, r = this.listeners.events_ar.length; n < r; n++) {
                if (this.listeners.events_ar[n].target === this && this.listeners.events_ar[n].type === e && this.listeners.events_ar[n].listener === t) {
                    this.listeners.events_ar.splice(n, 1);
                    break
                }
            }
        };
        self.init()
    };
    MUSIC.setPrototype = function() {
        MUSIC.prototype = new MUSICEventDispatcher
    };
    MUSIC.pauseAllAudio = function(e) {
        var t = MUSIC.instaces_ar.length;
        var n;
        for (var r = 0; r < t; r++) {
            n = MUSIC.instaces_ar[r];
            if (n != e) n.stop()
        }
    };
    MUSIC.hasHTML5Audio = function() {
        var e = document.createElement("audio");
        var t = false;
        if (e.canPlayType) {
            t = Boolean(e.canPlayType("audio/mpeg") == "probably" || e.canPlayType("audio/mpeg") == "maybe")
        }
        if (self.isMobile_bl) return true;
        return t
    }();
    MUSIC.getAudioFormats = function() {
        var e = document.createElement("audio");
        if (!e.canPlayType) return;
        var t = "";
        var n = [];
        if (e.canPlayType("audio/mpeg") == "probably" || e.canPlayType("audio/mpeg") == "maybe") {
            t += ".mp3"
        }
        if (e.canPlayType("audio/ogg") == "probably" || e.canPlayType("audio/ogg") == "maybe") {
            t += ".ogg"
        }
        if (e.canPlayType("audio/mp4") == "probably" || e.canPlayType("audio/mp4") == "maybe") {
            t += ".webm"
        }
        n = t.split(".");
        n.shift();
        e = null;
        return n
    }();
    MUSIC.hasCanvas = function() {
        return Boolean(document.createElement("canvas"))
    }();
    MUSIC.formatTotalTime = function(e) {
        if (typeof e == "string" && e.indexOf(":") != -1) {
            return e
        }
        e = e / 1e3;
        var t = Math.floor(e / (60 * 60));
        var n = e % (60 * 60);
        var r = Math.floor(n / 60);
        var i = n % 60;
        var s = Math.ceil(i);
        r = r >= 10 ? r : "0" + r;
        s = s >= 10 ? s : "0" + s;
        if (isNaN(s)) return "00:00/00:00";
        if (t > 0) {
            return t + ":" + r + ":" + s
        } else {
            return r + ":" + s
        }
    };
    MUSIC.getAudioFormats = function() {
        var e = document.createElement("audio");
        if (!e.canPlayType) return;
        var t = "";
        var n = [];
        if (e.canPlayType("audio/mpeg") == "probably" || e.canPlayType("audio/mpeg") == "maybe") {
            t += ".mp3"
        }
        if (e.canPlayType("audio/ogg") == "probably" || e.canPlayType("audio/ogg") == "maybe") {
            t += ".ogg"
        }
        if (e.canPlayType("audio/mp4") == "probably" || e.canPlayType("audio/mp4") == "maybe") {
            t += ".webm"
        }
        n = t.split(".");
        n.shift();
        e = null;
        return n
    }();
    MUSIC.instaces_ar = [];
    MUSIC.POPUP = "popup";
    MUSIC.POSITION_TOP = "positionTop";
    MUSIC.POSITION_BOTTOM = "positionBottom";
    MUSIC.READY = "ready";
    MUSIC.START = "start";
    MUSIC.START_TO_LOAD_PLAYLIST = "startToLoadPlaylist";
    MUSIC.LOAD_PLAYLIST_COMPLETE = "loadPlaylistComplete";
    MUSIC.STOP = "stop";
    MUSIC.PLAY = "play";
    MUSIC.PAUSE = "pause";
    MUSIC.UPDATE = "update";
    MUSIC.UPDATE_TIME = "updateTime";
    MUSIC.ERROR = "error";
    MUSIC.PLAY_COMPLETE = "playComplete";
    MUSIC.PLAYLIST_LOAD_COMPLETE = "onPlayListLoadComplete";
    window.MUSIC = MUSIC
})(window);
(function(window) {
    var MUSICAudioData = function(props, playListElement, parent) {
        var self = this;
        var prototype = MUSICAudioData.prototype;
        this.xhr = null;
        this.emailXHR = null;
        this.playlist_ar = null;
        this.dlIframe = null;
        this.mainPreloader_img = null;
        this.bk_img = null;
        this.thumbnail_img = null;
        this.separator1_img = null;
        this.separator2_img = null;
        this.prevN_img = null;
        this.playN_img = null;
        this.pauseN_img = null;
        this.nextN_img = null;
        this.popupN_img = null;
        this.downloaderN_img = null;
        this.toopTipBk_str = null;
        this.toopTipPointer_str = null;
        this.toopTipPointerUp_str = null;
        this.mainScrubberBkLeft_img = null;
        this.mainScrubberBkRight_img = null;
        this.mainScrubberDragLeft_img = null;
        this.mainScrubberLine_img = null;
        this.mainScrubberLeftProgress_img = null;
        this.volumeScrubberBkLeft_img = null;
        this.volumeScrubberBkRight_img = null;
        this.volumeScrubberDragLeft_img = null;
        this.volumeScrubberLine_img = null;
        this.volumeD_img = null;
        this.progressLeft_img = null;
        this.titleBarLeft_img = null;
        this.titleBarRigth_img = null;
        this.openerAnimation_img = null;
        this.openTopN_img = null;
        this.openTopS_img = null;
        this.openBottomN_img = null;
        this.openBottomS_img = null;
        this.closeN_img = null;
        this.closeS_img = null;
        this.openerPauseN_img = null;
        this.openerPauseS_img = null;
        this.openerPlayN_img = null;
        this.openerPlayS_img = null;
        this.categoriesN_img = null;
        this.replayN_img = null;
        this.playlistN_img = null;
        this.shuffleN_img = null;
        this.repost_img = null;
        this.titlebarAnimBkPath_img = null;
        this.titlebarLeftPath_img = null;
        this.titlebarRightPath_img = null;
        this.soundAnimationPath_img = null;
        this.controllerBk_img = null;
        this.playlistItemBk1_img = null;
        this.playlistItemBk2_img = null;
        this.playlistSeparator_img = null;
        this.playlistScrBkTop_img = null;
        this.playlistScrBkMiddle_img = null;
        this.playlistScrBkBottom_img = null;
        this.playlistScrDragTop_img = null;
        this.playlistScrDragMiddle_img = null;
        this.playlistScrDragBottom_img = null;
        this.playlistScrLines_img = null;
        this.playlistScrLinesOver_img = null;
        this.playlistPlayButtonN_img = null;
        this.playlistItemGrad1_img = null;
        this.playlistItemGrad2_img = null;
        this.playlistItemProgress1_img = null;
        this.playlistItemProgress2_img = null;
        this.playlistDownloadButtonN_img = null;
        this.playlistDownloadButtonS_img = null;
        this.catThumbBk_img = null;
        this.catThumbTextBk_img = null;
        this.catNextN_img = null;
        this.catNextS_img = null;
        this.catNextD_img = null;
        this.catPrevN_img = null;
        this.catPrevS_img = null;
        this.catPrevD_img = null;
        this.catCloseN_img = null;
        this.catCloseS_img = null;
        this.categories_el = null;
        this.scs_el = null;
        this.props_obj = props;
        this.skinPaths_ar = [];
        this.images_ar = [];
        this.cats_ar = [];
        this.scClientId_str = "a123083c52a6b06985421d33038e033a";
        this.flashPath_str = null;
        this.mp3DownloaderPath_str = null;
        this.proxyPath_str = null;
        this.proxyFolderPath_str = null;
        this.mailPath_str = null;
        this.skinPath_str = null;
        this.controllerBkPath_str = null;
        this.thumbnailBkPath_str = null;
        this.playlistIdOrPath_str = null;
        this.mainScrubberBkMiddlePath_str = null;
        this.volumeScrubberBkMiddlePath_str = null;
        this.mainScrubberDragMiddlePath_str = null;
        this.volumeScrubberDragMiddlePath_str = null;
        this.timeColor_str = null;
        this.titleColor_str = null;
        this.progressMiddlePath_str = null;
        this.sourceURL_str = null;
        this.titlebarBkMiddlePattern_str = null;
        this.playlistPlayButtonN_str = null;
        this.playlistPlayButtonS_str = null;
        this.playlistPauseButtonN_str = null;
        this.playlistPauseButtonS_str = null;
        this.trackTitleNormalColor_str = null;
        this.trackTitleSelected_str = null;
        this.trackDurationColor_str = null;
        this.categoriesId_str = null;
        this.thumbnailSelectedType_str = null;
        this.openerAlignment_str = null;
        this.prevId = -1;
        this.totalCats = 0;
        this.countLoadedSkinImages = 0;
        this.volume = 1;
        this.startSpaceBetweenButtons = 0;
        this.spaceBetweenButtons = 0;
        this.mainScrubberOffsetTop = 0;
        this.spaceBetweenMainScrubberAndTime = 0;
        this.startTimeSpace = 0;
        this.scrubbersOffsetWidth = 0;
        this.scrubbersOffestTotalWidth = 0;
        this.volumeButtonAndScrubberOffsetTop = 0;
        this.maxPlaylistItems = 0;
        this.separatorOffsetOutSpace = 0;
        this.separatorOffsetInSpace = 0;
        this.lastButtonsOffsetTop = 0;
        this.allButtonsOffsetTopAndBottom = 0;
        this.controllerHeight = 0;
        this.titleBarOffsetTop = 0;
        this.scrubberOffsetBottom = 0;
        this.equlizerOffsetLeft = 0;
        this.nrOfVisiblePlaylistItems = 0;
        this.trackTitleOffsetLeft = 0;
        this.playPauseButtonOffsetLeftAndRight = 0;
        this.durationOffsetRight = 0;
        this.downloadButtonOffsetRight = 0;
        this.scrollbarOffestWidth = 0;
        this.resetLoadIndex = -1;
        this.startAtPlaylist = 0;
        this.startAtTrack = 0;
        this.totalCategories = 0;
        this.thumbnailMaxWidth = 0;
        this.buttonsMargins = 0;
        this.thumbnailMaxHeight = 0;
        this.horizontalSpaceBetweenThumbnails = 0;
        this.verticalSpaceBetweenThumbnails = 0;
        this.openerEqulizerOffsetLeft = 0, this.openerEqulizerOffsetTop = 0;
        this.countID3 = 0;
        this.JSONPRequestTimeoutId_to;
        this.showLoadPlaylistErrorId_to;
        this.dispatchPlaylistLoadCompleteWidthDelayId_to;
        this.loadImageId_to;
        this.loadPreloaderId_to;
        this.isPlaylistDispatchingError_bl = false;
        this.allowToChangeVolume_bl = true;
        this.showContextMenu_bl = false;
        this.autoPlay_bl = false;
        this.loop_bl = false;
        this.shuffle_bl = false;
        this.showLoopButton_bl = false;
        this.showShuffleButton_bl = false;
        this.showDownloadMp3Button_bl = false;
        this.showPlaylistsButtonAndPlaylists_bl = false;
        this.showPlaylistsByDefault_bl = false;
        this.showPlayListButtonAndPlaylist_bl = false;
        this.animate_bl = false;
        this.showControllerByDefault_bl = false;
        this.showPlayListByDefault_bl = false;
        this.isDataLoaded_bl = false;
        this.useDeepLinking_bl = false;
        this.showSoundCloudUserNameInTitle_bl = false;
        this.showThumbnail_bl = false;
        this.showSoundAnimation_bl = false;
        this.expandControllerBackground_bl = false;
        this.showPlaylistItemPlayButton_bl = false;
        this.showPlaylistItemDownloadButton_bl = false;
        this.forceDisableDownloadButtonForPodcast_bl = false;
        this.forceDisableDownloadButtonForOfficialFM_bl = false;
        this.forceDisableDownloadButtonForFolder_bl = false;
        this.loadFromFolder_bl = false;
        this.isMobile_bl = MUSICUtils.isMobile;
        this.hasPointerEvent_bl = MUSICUtils.hasPointerEvent;
        self.init = function() {
            self.parseProperties()
        };
        self.parseProperties = function() {
            self.categoriesId_str = self.props_obj.playlistsId;
            if (!self.categoriesId_str) {
                setTimeout(function() {
                    if (self == null) return;
                    errorMessage_str = "The <font color='#FFFFFF'>playlistsId</font> property is not defined in the constructor function!";
                    self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                        text: errorMessage_str
                    })
                }, 50);
                return
            }
            self.mainFolderPath_str = self.props_obj.mainFolderPath;
            if (!self.mainFolderPath_str) {
                setTimeout(function() {
                    if (self == null) return;
                    errorMessage_str = "The <font color='#FFFFFF'>mainFolderPath</font> property is not defined in the constructor function!";
                    self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                        text: errorMessage_str
                    })
                }, 50);
                return
            }
            if (self.mainFolderPath_str.lastIndexOf("/") + 1 != self.mainFolderPath_str.length) {
                self.mainFolderPath_str += "/"
            }
            self.skinPath_str = self.props_obj.skinPath;
            if (!self.skinPath_str) {
                setTimeout(function() {
                    if (self == null) return;
                    errorMessage_str = "The <font color='#FFFFFF'>skinPath</font> property is not defined in the constructor function!";
                    self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                        text: errorMessage_str
                    })
                }, 50);
                return
            }
            if (self.skinPath_str.lastIndexOf("/") + 1 != self.skinPath_str.length) {
                self.skinPath_str += "/"
            }
            self.skinPath_str = self.mainFolderPath_str + self.skinPath_str;
            self.flashPath_str = self.mainFolderPath_str + "swf.swf";
            self.proxyPath_str = self.mainFolderPath_str + "proxy.php";
            self.proxyFolderPath_str = self.mainFolderPath_str + "proxyFolder.php";
            self.mailPath_str = self.mainFolderPath_str + "sendMail.php";
            self.mp3DownloaderPath_str = self.mainFolderPath_str + "downloader.php";
            self.categories_el = document.getElementById(self.categoriesId_str);
            if (!self.categories_el) {
                setTimeout(function() {
                    if (self == null) return;
                    errorMessage_str = "The html element with id <font color='#FFFFFF'>" + self.categoriesId_str + "</font> is not found in the DOM, this html element represents the player categories.!";
                    self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                        text: errorMessage_str
                    })
                }, 50);
                return
            }
            var e = MUSICUtils.getChildren(self.categories_el);
            self.totalCats = e.length;
            self.categories_el = document.getElementById(self.categoriesId_str);
            if (self.totalCats == 0) {
                setTimeout(function() {
                    if (self == null) return;
                    errorMessage_str = "At least one category is required!";
                    self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                        text: errorMessage_str
                    })
                }, 50);
                return
            }
            for (var t = 0; t < self.totalCats; t++) {
                var n = {};
                child = e[t];
                if (!MUSICUtils.hasAttribute(child, "data-source")) {
                    setTimeout(function() {
                        if (self == null) return;
                        self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                            text: "Attribute <font color='#FFFFFF'>data-source</font> is required in the categories html element at position <font color='#FFFFFF'>" + (t + 1)
                        })
                    }, 50);
                    return
                }
                if (!MUSICUtils.hasAttribute(child, "data-thumbnail-path")) {
                    setTimeout(function() {
                        if (self == null) return;
                        self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                            text: "Attribute <font color='#FFFFFF'>data-thumbnail-path</font> is required in the categories html element at position <font color='#FFFFFF'>" + (t + 1)
                        })
                    }, 50);
                    return
                }
                n.source = MUSICUtils.getAttributeValue(child, "data-source");
                n.thumbnailPath = MUSICUtils.getAttributeValue(child, "data-thumbnail-path");
                n.htmlContent = child.innerHTML;
                self.cats_ar[t] = n
            }
            self.playlistBackgroundColor_str = self.props_obj.playlistBackgroundColor || "transparent";
            self.openerAlignment_str = self.props_obj.openerAlignment || "right";
            if (self.openerAlignment_str != "right" && self.openerAlignment_str != "left") self.openerAlignment_str = "right";
            self.totalCategories = self.cats_ar.length;
            self.playlistIdOrPath_str = self.props_obj.playlistIdOrPath || undefined;
            self.timeColor_str = self.props_obj.timeColor || "#FF0000";
            self.trackTitleNormalColor_str = self.props_obj.trackTitleNormalColor || "#FF0000";
            self.trackTitleSelected_str = self.props_obj.trackTitleSelectedColor || "#FF0000";
            self.trackDurationColor_str = self.props_obj.trackDurationColor || "#FF0000";
            self.titleColor_str = self.props_obj.titleColor || "#FF0000";
            self.thumbnailSelectedType_str = self.props_obj.thumbnailSelectedType || "opacity";
            if (self.thumbnailSelectedType_str != "blackAndWhite" && self.thumbnailSelectedType_str != "threshold" && self.thumbnailSelectedType_str != "opacity") {
                self.thumbnailSelectedType_str = "opacity"
            }
            if (self.isMobile_bl || MUSICUtils.isIEAndLessThen9) self.thumbnailSelectedType_str = "opacity";
            if (document.location.protocol == "file:") self.thumbnailSelectedType_str = "opacity";
            self.playlistBackgroundColor_str = self.props_obj.playlistBackgroundColor || "transparent";
            self.startAtPlaylist = self.props_obj.startAtPlaylist || 0;
            if (isNaN(self.startAtPlaylist)) self.startAtPlaylist = 0;
            if (self.startAtPlaylist < 0) {
                self.startAtPlaylist = 0
            } else if (self.startAtPlaylist > self.totalCats - 1) {
                self.startAtPlaylist = self.totalCats - 1
            }
            self.startAtTrack = self.props_obj.startAtTrack || 0;
            self.volume = self.props_obj.volume;
            if (!self.volume) self.volume = 1;
            if (isNaN(self.volume)) volume = 1;
            if (self.volume > 1 || self.isMobile_bl) {
                self.volume = 1
            } else if (self.volume < 0) {
                self.volume = 0
            }
            self.buttonsMargins = self.props_obj.buttonsMargins || 0;
            self.thumbnailMaxWidth = self.props_obj.thumbnailMaxWidth || 330;
            self.thumbnailMaxHeight = self.props_obj.thumbnailMaxHeight || 330;
            self.horizontalSpaceBetweenThumbnails = self.props_obj.horizontalSpaceBetweenThumbnails;
            if (self.horizontalSpaceBetweenThumbnails == undefined) self.horizontalSpaceBetweenThumbnails = 40;
            self.verticalSpaceBetweenThumbnails = parseInt(self.props_obj.verticalSpaceBetweenThumbnails);
            if (self.verticalSpaceBetweenThumbnails == undefined) self.verticalSpaceBetweenThumbnails = 40;
            self.openerEqulizerOffsetLeft = self.props_obj.openerEqulizerOffsetLeft || 0;
            self.openerEqulizerOffsetTop = self.props_obj.openerEqulizerOffsetTop || 0;
            self.startSpaceBetweenButtons = self.props_obj.startSpaceBetweenButtons || 0;
            self.spaceBetweenButtons = self.props_obj.spaceBetweenButtons || 0;
            self.mainScrubberOffsetTop = self.props_obj.mainScrubberOffsetTop || 100;
            self.spaceBetweenMainScrubberAndTime = self.props_obj.spaceBetweenMainScrubberAndTime;
            self.startTimeSpace = self.props_obj.startTimeSpace;
            self.scrubbersOffsetWidth = self.props_obj.scrubbersOffsetWidth || 0;
            self.scrubbersOffestTotalWidth = self.props_obj.scrubbersOffestTotalWidth || 0;
            self.volumeButtonAndScrubberOffsetTop = self.props_obj.volumeButtonAndScrubberOffsetTop || 0;
            self.spaceBetweenVolumeButtonAndScrubber = self.props_obj.spaceBetweenVolumeButtonAndScrubber || 0;
            self.volumeScrubberOffestWidth = self.props_obj.volumeScrubberOffestWidth || 0;
            self.scrubberOffsetBottom = self.props_obj.scrubberOffsetBottom || 0;
            self.equlizerOffsetLeft = self.props_obj.equlizerOffsetLeft || 0;
            self.nrOfVisiblePlaylistItems = self.props_obj.nrOfVisiblePlaylistItems || 0;
            self.trackTitleOffsetLeft = self.props_obj.trackTitleOffsetLeft || 0;
            self.playPauseButtonOffsetLeftAndRight = self.props_obj.playPauseButtonOffsetLeftAndRight || 0;
            self.durationOffsetRight = self.props_obj.durationOffsetRight || 0;
            self.downloadButtonOffsetRight = self.props_obj.downloadButtonOffsetRight || 0;
            self.scrollbarOffestWidth = self.props_obj.scrollbarOffestWidth || 0;
            self.maxPlaylistItems = self.props_obj.maxPlaylistItems || 200;
            self.controllerHeight = self.props_obj.controllerHeight || 200;
            self.titleBarOffsetTop = self.props_obj.titleBarOffsetTop || 0;
            self.separatorOffsetInSpace = self.props_obj.separatorOffsetInSpace || 0;
            self.lastButtonsOffsetTop = self.props_obj.lastButtonsOffsetTop || 0;
            self.allButtonsOffsetTopAndBottom = self.props_obj.allButtonsOffsetTopAndBottom || 0;
            self.separatorOffsetOutSpace = self.props_obj.separatorOffsetOutSpace || 0;
            self.volumeScrubberWidth = self.props_obj.volumeScrubberWidth || 10;
            if (self.volumeScrubberWidth > 200) self.volumeScrubberWidth = 200;
            if (self.isMobile_bl) self.allowToChangeVolume_bl = false;
            self.showContextMenu_bl = self.props_obj.showContextMenu;
            self.showContextMenu_bl = self.showContextMenu_bl == "no" ? false : true;
            self.autoPlay_bl = self.props_obj.autoPlay;
            self.autoPlay_bl = self.autoPlay_bl == "yes" ? true : false;
            self.loop_bl = self.props_obj.loop;
            self.loop_bl = self.loop_bl == "yes" ? true : false;
            self.shuffle_bl = self.props_obj.shuffle;
            self.shuffle_bl = self.shuffle_bl == "yes" ? true : false;
            self.useDeepLinking_bl = self.props_obj.useDeepLinking;
            self.useDeepLinking_bl = self.useDeepLinking_bl == "yes" ? true : false;
            self.showSoundCloudUserNameInTitle_bl = self.props_obj.showSoundCloudUserNameInTitle;
            self.showSoundCloudUserNameInTitle_bl = self.showSoundCloudUserNameInTitle_bl == "yes" ? true : false;
            self.showThumbnail_bl = self.props_obj.showThumbnail;
            self.showThumbnail_bl = self.showThumbnail_bl == "yes" ? true : false;
            self.showLoopButton_bl = self.props_obj.showLoopButton;
            self.showLoopButton_bl = self.props_obj.showLoopButton == "no" ? false : true;
            self.showPlayListButtonAndPlaylist_bl = self.props_obj.showPlayListButtonAndPlaylist;
            self.showPlayListButtonAndPlaylist_bl = self.showPlayListButtonAndPlaylist_bl == "no" ? false : true;
            if (MUSICUtils.isAndroid && self.showPlayListButtonAndPlaylist_bl && self.props_obj.showPlayListOnAndroid == "no") {
                self.showPlayListButtonAndPlaylist_bl = false
            }
            self.rightClickContextMenu_str = self.props_obj.rightClickContextMenu || "developer";
            test = self.rightClickContextMenu_str == "developer" || self.rightClickContextMenu_str == "disabled" || self.rightClickContextMenu_str == "default";
            if (!test) self.rightClickContextMenu_str = "developer";
            self.showPlaylistsButtonAndPlaylists_bl = self.props_obj.showPlaylistsButtonAndPlaylists;
            self.showPlaylistsButtonAndPlaylists_bl = self.showPlaylistsButtonAndPlaylists_bl == "no" ? false : true;
            self.showPlaylistsByDefault_bl = self.props_obj.showPlaylistsByDefault;
            self.showPlaylistsByDefault_bl = self.showPlaylistsByDefault_bl == "yes" ? true : false;
            self.showShuffleButton_bl = self.props_obj.showShuffleButton;
            self.showShuffleButton_bl = self.showShuffleButton_bl == "no" ? false : true;
            self.showDownloadMp3Button_bl = self.props_obj.showDownloadMp3Button;
            self.showDownloadMp3Button_bl = self.showDownloadMp3Button_bl == "no" ? false : true;
            self.showOpenerPlayPauseButton_bl = self.props_obj.showOpenerPlayPauseButton;
            self.showOpenerPlayPauseButton_bl = self.showOpenerPlayPauseButton_bl == "no" ? false : true;
            self.showOpener_bl = self.props_obj.showOpener;
            self.showOpener_bl = self.showOpener_bl == "no" ? false : true;
            self.showTracksNumbers_bl = self.props_obj.showTracksNumbers;
            self.showTracksNumbers_bl = self.showTracksNumbers_bl == "yes" ? true : false;

            self.animate_bl = self.props_obj.animate;
            self.animate_bl = self.animate_bl == "yes" ? true : false;
            self.showControllerByDefault_bl = self.props_obj.showControllerByDefault;
            self.showControllerByDefault_bl = self.showControllerByDefault_bl == "no" ? false : true;
            self.showPlayListByDefault_bl = self.props_obj.showPlayListByDefault;
            self.showPlayListByDefault_bl = self.showPlayListByDefault_bl == "no" ? false : true;
            self.showSoundAnimation_bl = self.props_obj.showSoundAnimation;
            self.showSoundAnimation_bl = self.showSoundAnimation_bl == "yes" ? true : false;
            self.expandControllerBackground_bl = self.props_obj.expandBackground;
            self.expandControllerBackground_bl = self.expandControllerBackground_bl == "yes" ? true : false;
            self.showPlaylistItemPlayButton_bl = self.props_obj.showPlaylistItemPlayButton;
            self.showPlaylistItemPlayButton_bl = self.showPlaylistItemPlayButton_bl == "no" ? false : true;
            self.showPlaylistItemDownloadButton_bl = self.props_obj.showPlaylistItemDownloadButton;
            self.showPlaylistItemDownloadButton_bl = self.showPlaylistItemDownloadButton_bl == "no" ? false : true;
            self.forceDisableDownloadButtonForPodcast_bl = self.props_obj.forceDisableDownloadButtonForPodcast;
            self.forceDisableDownloadButtonForPodcast_bl = self.forceDisableDownloadButtonForPodcast_bl == "yes" ? true : false;
            self.forceDisableDownloadButtonForOfficialFM_bl = self.props_obj.forceDisableDownloadButtonForOfficialFM;
            self.forceDisableDownloadButtonForOfficialFM_bl = self.forceDisableDownloadButtonForOfficialFM_bl == "yes" ? true : false;
            self.forceDisableDownloadButtonForFolder_bl = self.props_obj.forceDisableDownloadButtonForFolder;
            self.forceDisableDownloadButtonForFolder_bl = self.forceDisableDownloadButtonForFolder_bl == "yes" ? true : false;
            self.addScrollBarMouseWheelSupport_bl = self.props_obj.addScrollBarMouseWheelSupport;
            self.addScrollBarMouseWheelSupport_bl = self.addScrollBarMouseWheelSupport_bl == "no" ? false : true;
            self.showSortButtons_bl = self.props_obj.showSortButtons;
            self.showSortButtons_bl = self.showSortButtons_bl == "no" ? false : true;
            self.preloaderPath_str = self.skinPath_str + "preloader.png";
            self.animationPath_str = self.skinPath_str + "equalizer.png";
            self.mainPreloader_img = new Image;
            self.mainPreloader_img.onerror = self.onSkinLoadErrorHandler;
            self.mainPreloader_img.onload = self.onPreloaderLoadHandler;
            self.mainPreloader_img.src = self.skinPath_str + "preloader.png";
            self.skinPaths_ar = [{
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
                img: self.repost_img = new Image,
                src: self.skinPath_str + "repost.png"
            }, {
                img: self.titlebarAnimBkPath_img = new Image,
                src: self.skinPath_str + "titlebar-equlizer-background.png"
            }, {
                img: self.titlebarLeftPath_img = new Image,
                src: self.skinPath_str + "titlebar-grad-left.png"
            }, {
                img: self.soundAnimationPath_img = new Image,
                src: self.skinPath_str + "equalizer.png"
            }, {
                img: self.titleBarLeft_img = new Image,
                src: self.skinPath_str + "titlebar-left-pattern.png"
            }, {
                img: self.titleBarRigth_img = new Image,
                src: self.skinPath_str + "titlebar-right-pattern.png"
            }];
            self.prevSPath_str = self.skinPath_str + "prev-button-over.png";
            self.playSPath_str = self.skinPath_str + "play-button-over.png";
            self.pauseSPath_str = self.skinPath_str + "pause-button-over.png";
            self.nextSPath_str = self.skinPath_str + "next-button-over.png";
            self.popupSPath_str = self.skinPath_str + "popup-button-over.png";
            self.downloaderSPath_str = self.skinPath_str + "download-button-over.png";
            self.controllerBkPath_str = self.skinPath_str + "controller-background.png";
            self.thumbnailBkPath_str = self.skinPath_str + "thumbnail-background.png";
            self.mainScrubberBkMiddlePath_str = self.skinPath_str + "scrubber-middle-background.png";
            self.mainScrubberDragMiddlePath_str = self.skinPath_str + "scrubber-middle-drag.png";
            self.volumeScrubberBkMiddlePath_str = self.skinPath_str + "scrubber-middle-background.png";
            self.volumeScrubberDragMiddlePath_str = self.skinPath_str + "scrubber-middle-drag.png";
            self.volumeSPath_str = self.skinPath_str + "volume-icon-over.png";
            self.volumeDPath_str = self.skinPath_str + "volume-icon-disabled.png";
            self.openerAnimationPath_str = self.skinPath_str + "equalizer.png";
            self.openTopSPath_str = self.skinPath_str + "open-button-selected-top.png";
            self.openBottomSPath_str = self.skinPath_str + "open-button-selected-bottom.png";
            self.closeSPath_str = self.skinPath_str + "close-button-selected.png";
            self.openerPauseS_str = self.skinPath_str + "open-pause-button-selected.png";
            self.openerPlayS_str = self.skinPath_str + "open-play-button-selected.png";
            self.progressMiddlePath_str = self.skinPath_str + "progress-middle.png";
            self.buySPath_str = self.skinPath_str + "buy-button-over.png";
            if (self.showPlayListButtonAndPlaylist_bl) {
                self.skinPaths_ar.push({
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
                });
                self.playlistDownloadButtonS_str = self.skinPath_str + "playlist-download-button-over.png";
                self.scrBkMiddlePath_str = self.skinPath_str + "playlist-scrollbar-background-middle.png";
                self.scrBkBottomPath_str = self.skinPath_str + "playlist-scrollbar-background-bottom.png";
                self.scrDragMiddlePath_str = self.skinPath_str + "playlist-scrollbar-drag-middle.png";
                self.scrDragBottomPath_str = self.skinPath_str + "playlist-scrollbar-drag-top.png";
                self.scrLinesSPath_str = self.skinPath_str + "playlist-scrollbar-lines-over.png";
                self.playlistPlayButtonN_str = self.skinPath_str + "playlist-play-button.png";
                self.playlistPlayButtonS_str = self.skinPath_str + "playlist-play-button-over.png";
                self.playlistPauseButtonN_str = self.skinPath_str + "playlist-pause-button.png";
                self.playlistPauseButtonS_str = self.skinPath_str + "playlist-pause-button-over.png"
            }
            if (self.showPlaylistsButtonAndPlaylists_bl) {
                self.skinPaths_ar.push({
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
                });
                self.catBkPath_str = self.skinPath_str + "categories-background.png";
                self.catThumbBkPath_str = self.skinPath_str + "categories-thumbnail-background.png";
                self.catThumbBkTextPath_str = self.skinPath_str + "categories-thumbnail-text-backgorund.png";
                self.catNextSPath_str = self.skinPath_str + "categories-next-button-over.png";
                self.catNextDPath_str = self.skinPath_str + "categories-next-button-disabled.png";
                self.catPrevSPath_str = self.skinPath_str + "categories-prev-button-over.png";
                self.catPrevDPath_str = self.skinPath_str + "categories-prev-button-disabled.png";
                self.catCloseSPath_str = self.skinPath_str + "categories-close-button-over.png"
            }
            self.categoriesSPath_str = self.skinPath_str + "categories-button-over.png";
            self.replaySPath_str = self.skinPath_str + "replay-button-over.png";
            var r = self.skinPath_str + "playlist-button.png";
            self.playlistSPath_str = self.skinPath_str + "playlist-button-over.png";
            self.shuffleSPath_str = self.skinPath_str + "shuffle-button-over.png";
            self.animationPath_str = self.skinPath_str + "equalizer.png";
            self.titlebarBkMiddlePattern_str = self.skinPath_str + "titlebar-middle-pattern.png";
            self.totalGraphics = self.skinPaths_ar.length;
            self.loadSkin()
        };
        this.onPreloaderLoadHandler = function() {
            setTimeout(function() {
                self.dispatchEvent(MUSICAudioData.PRELOADER_LOAD_DONE)
            }, 50)
        };
        self.loadSkin = function() {
            var e;
            var t;
            for (var n = 0; n < self.totalGraphics; n++) {
                e = self.skinPaths_ar[n].img;
                t = self.skinPaths_ar[n].src;
                e.onload = self.onSkinLoadHandler;
                e.onerror = self.onSkinLoadErrorHandler;
                e.src = t
            }
        };
        this.onSkinLoadHandler = function(e) {
            self.countLoadedSkinImages++;
            if (self.countLoadedSkinImages == self.totalGraphics) {
                setTimeout(function() {
                    self.dispatchEvent(MUSICAudioData.SKIN_LOAD_COMPLETE)
                }, 50)
            }
        };
        self.onSkinLoadErrorHandler = function(e) {
            if (MUSICUtils.isIEAndLessThen9) {
                message = "Graphics image not found!"
            } else {
                message = "The skin icon with label <font color='#FFFFFF'>" + e.target.src + "</font> can't be loaded, check path!"
            }
            if (window.console) console.log(e);
            var t = {
                text: message
            };
            setTimeout(function() {
                self.dispatchEvent(MUSICAudioData.LOAD_ERROR, t)
            }, 50)
        };
        self.showPropertyError = function(e) {
            self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                text: "The property called <font color='#FFFFFF'>" + e + "</font> is not defined."
            })
        };
        this.downloadMp3 = function(e, t, self) {
          console.log(e, t)
        };
        this.getValidEmail = function() {
            var e = prompt("Please enter your email address where the mp3 download link will be sent:");
            var t = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
            while (!t.test(e) || e == "") {
                if (e === null) return;
                e = prompt("Please enter a valid email address:")
            }
            return e
        };
        this.loadPlaylist = function(e) {
            if (self.isPlaylistDispatchingError_bl) return;
            clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to);
            var t = self.cats_ar[e].source;
            if (!t) {
                self.isPlaylistDispatchingError_bl = true;
                showLoadPlaylistErrorId_to = setTimeout(function() {
                    self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                        text: "<font color='#FFFFFF'>loadPlaylist()</font> - Please specify an html elementid, podcast link, soudcloud link or xml path"
                    });
                    self.isPlaylistDispatchingError_bl = false
                }, 50);
                return
            }
            if (!isNaN(t)) {
                self.isPlaylistDispatchingError_bl = true;
                showLoadPlaylistErrorId_to = setTimeout(function() {
                    self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                        text: "<font color='#FFFFFF'>loadPlaylist()</font> - The parameter must be of type string!"
                    });
                    self.isPlaylistDispatchingError_bl = false
                }, 50);
                return
            }
            if (t.indexOf("soundcloud.com") != -1) {
                self.loadSoundCloudList(t)
            } else if (t.indexOf("official.fm") != -1) {
                self.loadOfficialFmList(t)
            } else if (t.indexOf("folder:") != -1) {
                self.loadFolderPlaylist(t)
            } else if (t.indexOf("http:") != -1 || t.indexOf("https:") != -1 || t.indexOf("www.") != -1) {
                self.loadXMLPlaylist(t)
            } else {
                self.parseDOMPlaylist(t)
            }
            self.prevId = e
        };
        this.loadSoundCloudList = function(e) {
            if (self.isPlaylistDispatchingError_bl) return;
            var e;
            self.closeXHR();
            self.sourceURL_str = e;
            if (self.sourceURL_str.indexOf("likes") != -1) {
                self.sourceURL_str = self.sourceURL_str.replace(/\/likes$/, "/favorites")
            }
            if (self.sourceURL_str.indexOf("api.soundcloud.") == -1) {
                e = "http://api.soundcloud.com/resolve?format=json&url=" + self.sourceURL_str + "&limit=100" + "&client_id=" + self.scClientId_str + "&callback=" + parent.instanceName_str + ".data.parseSoundCloud"
            } else {
                e = self.sourceURL_str + "?format=json&client_id=" + self.scClientId_str + "&limit=100" + "&callback=" + parent.instanceName_str + ".data.parseSoundCloud"
            }
            if (self.scs_el == null) {
                try {
                    self.scs_el = document.createElement("script");
                    self.scs_el.src = e;
                    self.scs_el.id = parent.instanceName_str + ".data.parseSoundCloud";
                    document.documentElement.appendChild(self.scs_el)
                } catch (t) {}
            }
            self.JSONPRequestTimeoutId_to = setTimeout(self.JSONPRequestTimeoutError, 8e3)
        };
        this.JSONPRequestTimeoutError = function() {
            self.isPlaylistDispatchingError_bl = true;
            showLoadPlaylistErrorId_to = setTimeout(function() {
                self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                    text: "Error loading offical.fm url!<font color='#FFFFFF'>" + self.sourceURL_str + "</font>"
                });
                self.isPlaylistDispatchingError_bl = false
            }, 50);
            return
        };
        this.loadOfficialFmList = function(e) {
            if (self.isPlaylistDispatchingError_bl) return;
            self.closeXHR();
            self.sourceURL_str = e;
            var e = "http://api.official.fm/playlists/" + e.substr(e.indexOf("/") + 1) + "/tracks?format=jsonp&fields=streaming&api_version=2&callback=" + parent.instanceName_str + ".data.parseOfficialFM";
            if (self.scs_el == null) {
                try {
                    self.scs_el = document.createElement("script");
                    self.scs_el.src = e;
                    self.scs_el.id = parent.instanceName_str + ".data.parseOfficialFM";
                    document.documentElement.appendChild(self.scs_el)
                } catch (t) {}
            }
            self.JSONPRequestTimeoutId_to = setTimeout(self.JSONPRequestTimeoutError, 8e3)
        };
        this.JSONPRequestTimeoutError = function() {
            self.isPlaylistDispatchingError_bl = true;
            showLoadPlaylistErrorId_to = setTimeout(function() {
                self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                    text: "Error loading official.fm url!<font color='#FFFFFF'>" + self.sourceURL_str + "</font>"
                });
                self.isPlaylistDispatchingError_bl = false
            }, 50);
            return
        };
        this.closeJsonPLoader = function() {
            clearTimeout(self.JSONPRequestTimeoutId_to)
        };
        this.loadXMLPlaylist = function(e) {
            if (self.isPlaylistDispatchingError_bl) return;
            if (document.location.protocol == "file:" && e.indexOf("official.fm") == -1) {
                self.isPlaylistDispatchingError_bl = true;
                showLoadPlaylistErrorId_to = setTimeout(function() {
                    self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                        text: "Loading XML files local is not allowed or possible!. To function properly please test online."
                    });
                    self.isPlaylistDispatchingError_bl = false
                }, 50);
                return
            }
            self.closeXHR();
            self.loadFromFolder_bl = false;
            self.sourceURL_str = e;
            self.xhr = new XMLHttpRequest;
            self.xhr.onreadystatechange = self.ajaxOnLoadHandler;
            self.xhr.onerror = self.ajaxOnErrorHandler;
            try {
                self.xhr.open("get", self.sourceURL_str), true);
                self.xhr.send()
            } catch (t) {
                var n = t;
                if (t) {
                    if (t.message) n = t.message
                }
                self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                    text: "XML file can't be loaded! <font color='#FFFFFF'>" + self.sourceURL_str + "</font>. " + n
                })
            }
        };
        this.loadFolderPlaylist = function(e) {
            if (self.isPlaylistDispatchingError_bl) return;
            if (document.location.protocol == "file:" && e.indexOf("official.fm") == -1) {
                self.isPlaylistDispatchingError_bl = true;
                showLoadPlaylistErrorId_to = setTimeout(function() {
                    self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                        text: "Creating a mp3 playlist from a folder is not allowed or possible local! To function properly please test online."
                    });
                    self.isPlaylistDispatchingError_bl = false
                }, 50);
                return
            }
            self.closeXHR();
            self.loadFromFolder_bl = true;
            self.countID3 = 0;
            self.sourceURL_str = e.substr(e.indexOf(":") + 1);
            self.xhr = new XMLHttpRequest;
            self.xhr.onreadystatechange = self.ajaxOnLoadHandler;
            self.xhr.onerror = self.ajaxOnErrorHandler;
            try {
                self.xhr.open("get", self.proxyFolderPath_str + "?dir=" + encodeURIComponent(self.sourceURL_str) + "&rand=" + parseInt(Math.random() * 9999999), true);
                self.xhr.send()
            } catch (t) {
                var n = t;
                if (t) {
                    if (t.message) n = t.message
                }
                self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                    text: "Folder proxy file path is not found: <font color='#FFFFFF'>" + self.proxyFolderPath_str + "</font>"
                })
            }
        };
        this.ajaxOnLoadHandler = function(e) {
            var response;
            var isXML = false;
            if (self.xhr.readyState == 4) {
                if (self.xhr.status == 404) {
                    if (self.loadFromFolder_bl) {
                        self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                            text: "Folder proxy file path is not found: <font color='#FFFFFF'>" + self.proxyFolderPath_str + "</font>"
                        })
                    } else {
                        self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                            text: "Proxy file path is not found: <font color='#FFFFFF'>" + self.proxyPath_str + "</font>"
                        })
                    }
                } else if (self.xhr.status == 408) {
                    self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                        text: "Proxy file request load timeout!"
                    })
                } else if (self.xhr.status == 200) {
                    if (self.xhr.responseText.indexOf("<b>Warning</b>:") != -1) {
                        self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                            text: "Error loading folder: <font color='#FFFFFF'>" + self.sourceURL_str + "</font>. Make sure that the folder path is correct!"
                        });
                        return
                    }
                    if (window.JSON) {
                        response = JSON.parse(self.xhr.responseText)
                    } else {
                        response = eval("(" + self.xhr.responseText + ")")
                    }
                    if (response.channel) {
                        self.parsePodcast(response)
                    } else if (response.folder) {
                        self.parseFolderJSON(response)
                    } else if (response.li) {
                        self.parseXML(response)
                    } else if (response.error) {
                        self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                            text: "Error loading file: <font color='#FFFFFF'>" + self.sourceURL_str + "</font>. Make sure the file path (xml or podcast) is correct and well formatted!"
                        })
                    }
                }
            }
        };
        this.ajaxOnErrorHandler = function(e) {
            try {
                if (window.console) console.log(e);
                if (window.console) console.log(e.message)
            } catch (e) {}
            if (self.loadFromFolder_bl) {
                self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                    text: "Error loading file : <font color='#FFFFFF'>" + self.proxyFolderPath_str + "</font>. Make sure the path is correct"
                })
            } else {
                self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                    text: "Error loading file : <font color='#FFFFFF'>" + self.proxyPath_str + "</font>. Make sure the path is correct"
                })
            }
        };
        this.parseSoundCloud = function(e) {
            self.closeJsonPLoader();
            self.playlist_ar = [];
            var t;
            var n;
            var r;
            if (e && e.uri) {
                if (e.kind == "track") {
                    self.createSoundcloudPlaylist(e);
                    return
                }
                if (e.uri.indexOf("/tracks") == -1) {
                    r = e.uri + "/tracks"
                } else {
                    r = e.uri + "/favorites"
                }
                self.loadSoundCloudList(r);
                return
            } else if (e.length || e.kind == "track") {
                self.createSoundcloudPlaylist(e)
            } else {
                self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                    text: "Please provide a playlist or track URL : <font color='#FFFFFF'>" + self.sourceURL_str + "</font>."
                })
            }
        };
        this.createSoundcloudPlaylist = function(e) {
            if (e.length) {
                for (var t = 0; t < e.length; t++) {
                    track = e[t];
                    obj = {};
                    obj.source = track["stream_url"] + "?consumer_key=" + self.scClientId_str;
                    obj.downloadPath = track["downloadable"] == true ? track["download_url"] + "?consumer_key=" + self.scClientId_str : undefined;
                    obj.downloadable = track["downloadable"];
                    obj.buy = undefined;
                    obj.thumbPath = track["artwork_url"];
                    if (self.showSoundCloudUserNameInTitle_bl) {
                        var n = "";
                        if (self.showTracksNumbers_bl) {
                            if (t < 9) n = "0";
                            n = n + (t + 1) + ". ";
                            obj.title = n + "<span style='font-weight:bold;'>" + track["user"]["username"] + "</span>" + " - " + track["title"]
                        } else {
                            obj.title = "<span style='font-weight:bold;'>" + track["user"]["username"] + "</span>" + " - " + track["title"]
                        }
                        obj.titleText = track["user"]["username"] + " - " + track["title"]
                    } else {
                        var n = "";
                        if (self.showTracksNumbers_bl) {
                            if (t < 9) n = "0";
                            n = n + (t + 1) + ". ";
                            obj.title = n + track["title"]
                        } else {
                            obj.title = track["title"]
                        }
                        obj.titleText = track["title"]
                    }
                    obj.duration = track["duration"];
                    if (track["streamable"]) self.playlist_ar.push(obj);
                    if (t > self.maxPlaylistItems - 1) break
                }
            } else {
                track = e;
                obj = {};
                obj.source = track["stream_url"] + "?consumer_key=" + self.scClientId_str;
                obj.downloadPath = track["downloadable"] == true ? track["download_url"] + "?consumer_key=" + self.scClientId_str : undefined;
                obj.downloadable = track["downloadable"];
                obj.buy = undefined;
                obj.thumbPath = track["artwork_url"];
                if (self.showSoundCloudUserNameInTitle_bl) {
                    obj.title = "<span style='font-weight:bold;'>" + track["user"]["username"] + "</span>" + " - " + track["title"];
                    obj.titleText = track["user"]["username"] + " - " + track["title"]
                } else {
                    obj.title = track["title"];
                    obj.titleText = track["title"]
                }
                obj.duration = track["duration"];
                if (track["streamable"]) self.playlist_ar.push(obj)
            }
            clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to);
            self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                self.dispatchEvent(MUSICAudioData.PLAYLIST_LOAD_COMPLETE)
            }, 50);
            self.isDataLoaded_bl = true
        };
        this.parseOfficialFM = function(e) {
            self.closeJsonPLoader();
            self.playlist_ar = [];
            var t;
            var n;
            var r = e.tracks;
            var i = undefined;
            for (var s = 0; s < r.length; s++) {
                n = e.tracks[s].track;
                t = {};
                t.id = s;
                t.source = encodeURI(n.streaming.http);
                t.downloadPath = t.source;
                t.downloadable = self.showDownloadMp3Button_bl;
                t.buy = undefined;
                if (self.forceDisableDownloadButtonForOfficialFM_bl) t.downloadable = false;
                t.thumbPath = i;
                var o = "";
                if (self.showTracksNumbers_bl) {
                    if (s < 9) o = "0";
                    o = o + (s + 1) + ". ";
                    t.title = o + "<span style='font-weight:bold;'>" + n["artist"] + "</span>" + " - " + n["title"]
                } else {
                    t.title = "<span style='font-weight:bold;'>" + n["artist"] + "</span>" + " - " + n["title"]
                }
                t.titleText = n["artist"] + " - " + n["title"];
                t.duration = n.duration * 1e3;
                self.playlist_ar[s] = t;
                if (s > self.maxPlaylistItems - 1) break
            }
            clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to);
            self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                self.dispatchEvent(MUSICAudioData.PLAYLIST_LOAD_COMPLETE)
            }, 50);
            self.isDataLoaded_bl = true
        };
        this.parsePodcast = function(e) {
            self.playlist_ar = [];
            var t;
            var n = e.channel.item;
            var r = undefined;
            try {
                r = e["channel"]["image"]["url"]
            } catch (i) {}
            for (var s = 0; s < n.length; s++) {
                t = {};
                if (n[s]["enclosure"]) {
                    t.source = encodeURI(n[s]["enclosure"]["@attributes"]["url"])
                } else {
                    t.source = encodeURI(n[s]["link"])
                }
                t.downloadPath = t.source;
                t.downloadable = self.showDownloadMp3Button_bl;
                t.buy = undefined;
                if (self.forceDisableDownloadButtonForPodcast_bl) t.downloadable = false;
                t.thumbPath = r;
                var o = "";
                if (self.showTracksNumbers_bl) {
                    if (s < 9) o = "0";
                    o = o + (s + 1) + ". ";
                    t.title = o + n[s].title
                } else {
                    t.title = n[s].title
                }
                t.titleText = n[s].title;
                t.duration = undefined;
                self.playlist_ar[s] = t;
                if (s > self.maxPlaylistItems - 1) break
            }
            clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to);
            self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                self.dispatchEvent(MUSICAudioData.PLAYLIST_LOAD_COMPLETE)
            }, 50);
            self.isDataLoaded_bl = true
        };
        this.parseXML = function(e) {
            self.playlist_ar = [];
            var t;
            var n = e.li;
            for (var r = 0; r < n.length; r++) {
                t = {};
                t.source = n[r]["@attributes"]["data-path"]; console.log(t.source);
                var i = encodeURI(t.source.substr(0, t.source.lastIndexOf("/") + 1));
                var s = t.source.substr(t.source.lastIndexOf("/") + 1);
                if (s.indexOf(";.mp3") != -1) {
                    s = t.source.substr(t.source.lastIndexOf("/") + 1)
                } else {
                    s = encodeURIComponent(t.source.substr(t.source.lastIndexOf("/") + 1))
                }
                t.source = i + s;
                t.downloadPath = t.source;
                t.downloadable = n[r]["@attributes"]["data-downloadable"] == "yes" ? true : false;
                t.buy = n[r]["@attributes"]["data-buy-url"] == "yes" ? true : false;
                t.thumbPath = n[r]["@attributes"]["data-thumbpath"];
                t.ids = n[r]["@attributes"]["data-id"];
                var o = "";
                if (self.showTracksNumbers_bl) {
                    if (r < 9) o = "0";
                    o = o + (r + 1) + ". ";
                    t.title = o + n[r]["@attributes"]["data-title"]
                } else {
                    t.title = n[r]["@attributes"]["data-title"]
                }
                t.titleText = n[r]["@attributes"]["data-title"];
                t.duration = n[r]["@attributes"]["data-duration"];
                self.playlist_ar[r] = t;
                if (r > self.maxPlaylistItems - 1) break
            }
            clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to);
            self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                self.dispatchEvent(MUSICAudioData.PLAYLIST_LOAD_COMPLETE)
            }, 50);
            self.isDataLoaded_bl = true
        };
        this.parseFolderJSON = function(e) {
            self.playlist_ar = [];
            var t;
            var n = e.folder;
            var r = 0;
            for (var i = 0; i < n.length; i++) {
                t = {};
                t.source = n[i]["@attributes"]["data-path"]; console.log(t.source);
                var s = encodeURI(t.source.substr(0, t.source.lastIndexOf("/") + 1));
                var o = encodeURIComponent(t.source.substr(t.source.lastIndexOf("/") + 1));
                t.source = s + o;
                t.downloadPath = t.source;
                t.downloadable = self.showDownloadMp3Button_bl;
                t.buy = undefined;
                if (self.forceDisableDownloadButtonForFolder_bl) t.downloadable = false;
                t.thumbPath = n[i]["@attributes"]["data-thumbpath"];
                t.ids = n[r]["@attributes"]["data-id"];
                t.title = "...";
                t.titleText = "...";
                if (MUSICUtils.isIEAndLessThen9) {
                    var u = "";
                    if (self.showTracksNumbers_bl) {
                        if (i < 9) u = "0";
                        u = u + (i + 1) + ". ";
                        t.title = u + "track ";
                        t.titleText = "track"
                    } else {
                        if (i < 9) u = "0";
                        u = u + (i + 1);
                        t.title = "track " + u;
                        t.titleText = "track " + u
                    }
                }
                self.playlist_ar[i] = t;
                if (i > self.maxPlaylistItems - 1) break
            }
            clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to);
            self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                self.dispatchEvent(MUSICAudioData.PLAYLIST_LOAD_COMPLETE)
            }, 50);
            self.isDataLoaded_bl = true
        };
        this.parseDOMPlaylist = function(e) {
            if (self.isPlaylistDispatchingError_bl) return;
            var t;
            self.closeXHR();
            t = document.getElementById(e);
            if (!t) {
                self.isPlaylistDispatchingError_bl = true;
                showLoadPlaylistErrorId_to = setTimeout(function() {
                    self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                        text: "The playlist with id <font color='#FFFFFF'>" + e + "</font> is not found in the DOM."
                    });
                    self.isPlaylistDispatchingError_bl = false
                }, 50);
                return
            }
            var n = MUSICUtils.getChildren(t);
            var r = n.length;
            var i;
            self.playlist_ar = [];
            if (r == 0) {
                self.isPlaylistDispatchingError_bl = true;
                showLoadPlaylistErrorId_to = setTimeout(function() {
                    self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                        text: "The playlist whit the id  <font color='#FFFFFF'>" + e + "</font> must contain at least one track."
                    });
                    self.isPlaylistDispatchingError_bl = false
                }, 50);
                return
            }
            for (var s = 0; s < r; s++) {
                var o = {};
                i = n[s];
                if (!MUSICUtils.hasAttribute(i, "data-path")) {
                    self.isPlaylistDispatchingError_bl = true;
                    showLoadPlaylistErrorId_to = setTimeout(function() {
                        self.dispatchEvent(MUSICAudioData.LOAD_ERROR, {
                            text: "Attribute <font color='#FFFFFF'>data-path</font> is required in the playlist at position <font color='#FFFFFF'>" + (s + 1)
                        })
                    }, 50);
                    return
                }
                if (s > self.maxPlaylistItems - 1) break;
                o.source = MUSICUtils.getAttributeValue(i, "data-path");
                var u = encodeURI(o.source.substr(0, o.source.lastIndexOf("/") + 1));
                var a = o.source.substr(o.source.lastIndexOf("/") + 1);
                if (a.indexOf(";.mp3") != -1) {
                    a = o.source.substr(o.source.lastIndexOf("/") + 1)
                    o.source = u + a
                }
                else if (o.source.indexOf(".soundcloud.") != -1) {
                    o.source = o.source + '/stream?client_id=' + 'dce5652caa1b66331903493735ddd64d'
                } else{
                    a = encodeURIComponent(o.source.substr(o.source.lastIndexOf("/") + 1))
                    o.source = u + a
                }
                o.downloadPath = o.source;
                if (MUSICUtils.hasAttribute(i, "data-thumbpath")) {
                    o.thumbPath = MUSICUtils.getAttributeValue(i, "data-thumbpath")
                } else {
                    o.thumbPath = undefined
                }
                if (MUSICUtils.hasAttribute(i, "data-downloadable")) {
                    o.downloadable = MUSICUtils.getAttributeValue(i, "data-downloadable") == "yes" ? true : false
                } else {
                    o.downloadable = undefined
                }
                if (MUSICUtils.hasAttribute(i, "data-buy-url")) {
                    o.buy = MUSICUtils.getAttributeValue(i, "data-buy-url")
                } else {
                    o.buy = undefined
                }
                o.title = "not defined!";
                try {
                    var f = "";
                    if (self.showTracksNumbers_bl) {
                        if (s < 9) f = "0";
                        f = f + (s + 1) + ". ";
                        o.title = f + MUSICUtils.getChildren(i)[0].innerHTML
                    } else {
                        o.title = MUSICUtils.getChildren(i)[0].innerHTML
                    }
                } catch (l) {}
                try {
                    o.titleText = MUSICUtils.getChildren(i)[0].textContent || MUSICUtils.getChildren(i)[0].innerText
                } catch (l) {}
                if (MUSICUtils.hasAttribute(i, "data-duration")) {
                    o.duration = MUSICUtils.getAttributeValue(i, "data-duration")
                } else {
                    o.duration = undefined
                }
                if (MUSICUtils.hasAttribute(i, "data-id")) {
                    o.ids = MUSICUtils.getAttributeValue(i, "data-id")
                } else {
                    o.ids = undefined
                  }
                self.playlist_ar[s] = o
            }
            clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to);
            self.dispatchPlaylistLoadCompleteWidthDelayId_to = setTimeout(function() {
                self.dispatchEvent(MUSICAudioData.PLAYLIST_LOAD_COMPLETE)
            }, 50);
            self.isDataLoaded_bl = true
        };
        this.closeXHR = function() {
            self.closeJsonPLoader();
            try {
                document.documentElement.removeChild(self.scs_el);
                self.scs_el = null
            } catch (e) {}
            if (self.xhr != null) {
                try {
                    self.xhr.abort()
                } catch (e) {}
                self.xhr.onreadystatechange = null;
                self.xhr.onerror = null;
                self.xhr = null
            }
            self.countID3 = 2e3
        };
        this.closeData = function() {
            self.closeXHR();
            clearTimeout(self.loadImageId_to);
            clearTimeout(self.showLoadPlaylistErrorId_to);
            clearTimeout(self.dispatchPlaylistLoadCompleteWidthDelayId_to);
            clearTimeout(self.loadImageId_to);
            clearTimeout(self.loadPreloaderId_to);
            if (self.image_img) {
                self.image_img.onload = null;
                self.image_img.onerror = null
            }
        };
        self.init()
    };
    MUSICAudioData.setPrototype = function() {
        MUSICAudioData.prototype = new MUSICEventDispatcher
    };
    MUSICAudioData.prototype = null;
    MUSICAudioData.PRELOADER_LOAD_DONE = "onPreloaderLoadDone";
    MUSICAudioData.LOAD_DONE = "onLoadDone";
    MUSICAudioData.LOAD_ERROR = "onLoadError";
    MUSICAudioData.IMAGE_LOADED = "onImageLoaded";
    MUSICAudioData.SKIN_LOAD_COMPLETE = "onSkinLoadComplete";
    MUSICAudioData.SKIN_PROGRESS = "onSkinProgress";
    MUSICAudioData.IMAGES_PROGRESS = "onImagesPogress";
    MUSICAudioData.PLAYLIST_LOAD_COMPLETE = "onPlaylistLoadComplete";
    window.MUSICAudioData = MUSICAudioData
})(window);
(function(e) {
    var t = function(n) {
        var r = this;
        var i = t.prototype;
        this.audio_el = null;
        this.sourcePath_str = null;
        this.lastPercentPlayed = 0;
        this.volume = n;
        this.curDuration = 0;
        this.countNormalMp3Errors = 0;
        this.countShoutCastErrors = 0;
        this.maxShoutCastCountErrors = 5;
        this.maxNormalCountErrors = 1;
        this.testShoutCastId_to;
        this.preload_bl = false;
        this.allowScrubing_bl = false;
        this.hasError_bl = true;
        this.isPlaying_bl = false;
        this.isStopped_bl = true;
        this.hasPlayedOnce_bl = false;
        this.isStartEventDispatched_bl = false;
        this.isSafeToBeControlled_bl = false;
        this.isShoutcast_bl = false;
        this.isNormalMp3_bl = false;
        this.init = function() {
            r.setupAudio();
            r.setHeight(0)
        };
        this.setupAudio = function() {
            if (r.audio_el == null) {
                r.audio_el = document.createElement("audio");
                r.screen.appendChild(r.audio_el);
                r.audio_el.controls = false;
                r.audio_el.preload = "auto";
                r.audio_el.volume = r.volume
            }
            r.audio_el.addEventListener("error", r.errorHandler);
            r.audio_el.addEventListener("canplay", r.safeToBeControlled);
            r.audio_el.addEventListener("canplaythrough", r.safeToBeControlled);
            r.audio_el.addEventListener("progress", r.updateProgress);
            r.audio_el.addEventListener("timeupdate", r.updateAudio);
            r.audio_el.addEventListener("pause", r.pauseHandler);
            r.audio_el.addEventListener("play", r.playHandler);
            r.audio_el.addEventListener("ended", r.endedHandler)
        };
        this.destroyAudio = function() {
            if (r.audio_el) {
                r.audio_el.removeEventListener("error", r.errorHandler);
                r.audio_el.removeEventListener("canplay", r.safeToBeControlled);
                r.audio_el.removeEventListener("canplaythrough", r.safeToBeControlled);
                r.audio_el.removeEventListener("progress", r.updateProgress);
                r.audio_el.removeEventListener("timeupdate", r.updateAudio);
                r.audio_el.removeEventListener("pause", r.pauseHandler);
                r.audio_el.removeEventListener("play", r.playHandler);
                r.audio_el.removeEventListener("ended", r.endedHandler);
                r.audio_el.src = "";
                r.audio_el.load()
            }
        };
        this.errorHandler = function(n) {
            if (r.isNormalMp3_bl && r.countNormalMp3Errors <= r.maxNormalCountErrors) {
                r.stop();
                r.testShoutCastId_to = setTimeout(r.play, 200);
                r.countNormalMp3Errors++;
                return
            }
            if (r.isShoutcast_bl && r.countShoutCastErrors <= r.maxShoutCastCountErrors && r.audio_el.networkState == 0) {
                r.testShoutCastId_to = setTimeout(r.play, 200);
                r.countShoutCastErrors++;
                return
            }
            var i;
            r.hasError_bl = true;
            r.stop();
            if (r.audio_el.networkState == 0) {
                i = "error 'self.audio_el.networkState = 1'"
            } else if (r.audio_el.networkState == 1) {
                i = "error 'self.audio_el.networkState = 1'"
            } else if (r.audio_el.networkState == 2) {
                i = "'self.audio_el.networkState = 2'"
            } else if (r.audio_el.networkState == 3) {
                i = "source not found <font color='#FFFFFF'>" + r.sourcePath_str + "</font>"
            } else {
                i = n
            }
            if (e.console) e.console.log(r.audio_el.networkState);
            r.dispatchEvent(t.ERROR, {
                text: i
            })
        };
        this.setSource = function(e) {
            r.sourcePath_str = e;
            var t = r.sourcePath_str.split(",");
            var n = MUSIC.getAudioFormats;
            for (var i = 0; i < t.length; i++) {
                var s = t[i];
                t[i] = MUSICUtils.trim(s)
            }
            e: for (var o = 0; o < t.length; o++) {
                var s = t[o];
                for (var i = 0; i < n.length; i++) {
                    var u = n[i];
                    if (s.indexOf(u) != -1) {
                        r.sourcePath_str = s;
                        break e
                    }
                }
            }
            clearTimeout(r.testShoutCastId_to);
            if (r.sourcePath_str.indexOf(";") != -1) {
                r.isShoutcast_bl = true;
                r.countShoutCastErrors = 0
            } else {
                r.isShoutcast_bl = false
            }
            if (r.sourcePath_str.indexOf(";") == -1) {
                r.isNormalMp3_bl = true;
                r.countNormalMp3Errors = 0
            } else {
                r.isNormalMp3_bl = false
            }
            r.lastPercentPlayed = 0;
            if (r.audio_el) r.stop(true)
        };
        this.play = function(e) {
            if (r.isStopped_bl) {
                r.isPlaying_bl = false;
                r.hasError_bl = false;
                r.allowScrubing_bl = false;
                r.isStopped_bl = false;
                r.setupAudio();
                r.audio_el.src = r.sourcePath_str;
                r.play()
            } else if (!r.audio_el.ended || e) {
                try {
                    r.isPlaying_bl = true;
                    r.hasPlayedOnce_bl = true;
                    r.audio_el.play();
                    if (MUSICUtils.isIE) r.dispatchEvent(t.PLAY)
                } catch (n) {}
            }
        };
        this.pause = function() {
            if (r == null) return;
            if (r.audio_el == null) return;
            if (!r.audio_el.ended) {
                try {
                    r.audio_el.pause();
                    r.isPlaying_bl = false;
                    if (MUSICUtils.isIE) r.dispatchEvent(t.PAUSE)
                } catch (e) {}
            }
        };
        this.pauseHandler = function() {
            if (r.allowScrubing_bl) return;
            r.dispatchEvent(t.PAUSE)
        };
        this.playHandler = function() {
            if (r.allowScrubing_bl) return;
            if (!r.isStartEventDispatched_bl) {
                r.dispatchEvent(t.START);
                r.isStartEventDispatched_bl = true
            }
            r.dispatchEvent(t.PLAY)
        };
        this.endedHandler = function() {
            r.dispatchEvent(t.PLAY_COMPLETE)
        };
        this.stop = function(e) {
            r.dispatchEvent(t.UPDATE_TIME, {
                curTime: "00:00",
                totalTime: "00:00"
            });
            if ((r == null || r.audio_el == null || r.isStopped_bl) && !e) return;
            r.isPlaying_bl = false;
            r.isStopped_bl = true;
            r.hasPlayedOnce_bl = true;
            r.isSafeToBeControlled_bl = false;
            r.isStartEventDispatched_bl = false;
            clearTimeout(r.testShoutCastId_to);
            r.audio_el.pause();
            r.destroyAudio();
            r.dispatchEvent(t.STOP);
            r.dispatchEvent(t.LOAD_PROGRESS, {
                percent: 0
            })
        };
        this.safeToBeControlled = function() {
            if (!r.isSafeToBeControlled_bl) {
                r.hasHours_bl = Math.floor(r.audio_el.duration / (60 * 60)) > 0;
                r.isPlaying_bl = true;
                r.isSafeToBeControlled_bl = true;
                r.dispatchEvent(t.SAFE_TO_SCRUBB);
                r.dispatchEvent(t.SAFE_TO_UPDATE_VOLUME)
            }
        };
        this.updateProgress = function() {
            var e;
            var n = 0;
            if (r.audio_el.buffered.length > 0) {
                e = r.audio_el.buffered.end(r.audio_el.buffered.length - 1);
                n = e.toFixed(1) / r.audio_el.duration.toFixed(1);
                if (isNaN(n) || !n) n = 0
            }
            if (n == 1) r.audio_el.removeEventListener("progress", r.updateProgress);
            r.dispatchEvent(t.LOAD_PROGRESS, {
                percent: n
            })
        };
        this.updateAudio = function() {
            var e;
            if (!r.allowScrubing_bl) {
                e = r.audio_el.currentTime / r.audio_el.duration;
                r.dispatchEvent(t.UPDATE, {
                    percent: e
                })
            }
            var n = r.formatTime(r.audio_el.duration);
            var i = r.formatTime(r.audio_el.currentTime);
            if (!isNaN(r.audio_el.duration)) {
                r.dispatchEvent(t.UPDATE_TIME, {
                    curTime: i,
                    totalTime: n
                })
            } else {
                r.dispatchEvent(t.UPDATE_TIME, {
                    curTime: "00:00",
                    totalTime: "00:00"
                })
            }
            r.lastPercentPlayed = e;
            r.curDuration = i
        };
        this.startToScrub = function() {
            r.allowScrubing_bl = true
        };
        this.stopToScrub = function() {
            r.allowScrubing_bl = false
        };
        this.scrub = function(e, n) {
            if (r.audio_el == null || !r.audio_el.duration) return;
            if (n) r.startToScrub();
            try {
                r.audio_el.currentTime = r.audio_el.duration * e;
                var i = r.formatTime(r.audio_el.duration);
                var s = r.formatTime(r.audio_el.currentTime);
                r.dispatchEvent(t.UPDATE_TIME, {
                    curTime: s,
                    totalTime: i
                })
            } catch (n) {}
        };
        this.replay = function() {
            r.scrub(0);
            r.play()
        };
        this.setVolume = function(e) {
            if (e) r.volume = e;
            if (r.audio_el) r.audio_el.volume = r.volume
        };
        this.formatTime = function(e) {
            var t = Math.floor(e / (60 * 60));
            var n = e % (60 * 60);
            var i = Math.floor(n / 60);
            var s = n % 60;
            var o = Math.ceil(s);
            i = i >= 10 ? i : "0" + i;
            o = o >= 10 ? o : "0" + o;
            if (isNaN(o)) return "00:00";
            if (r.hasHours_bl) {
                return t + ":" + i + ":" + o
            } else {
                return i + ":" + o
            }
        };
        this.init()
    };
    t.setPrototype = function() {
        t.prototype = new MUSICDisplayObject("div")
    };
    t.ERROR = "error";
    t.UPDATE = "update";
    t.UPDATE = "update";
    t.UPDATE_TIME = "updateTime";
    t.SAFE_TO_SCRUBB = "safeToControll";
    t.SAFE_TO_UPDATE_VOLUME = "safeToUpdateVolume";
    t.LOAD_PROGRESS = "loadProgress";
    t.START = "start";
    t.PLAY = "play";
    t.PAUSE = "pause";
    t.STOP = "stop";
    t.PLAY_COMPLETE = "playComplete";
    e.MUSICAudioScreen = t
})(window);
(function() {
    var e = function(t) {
        var n = this;
        var r = e.prototype;
        this.image_img;
        this.catThumbBk_img = t.catThumbBk_img;
        this.catNextN_img = t.catNextN_img;
        this.catNextS_img = t.catNextS_img;
        this.catNextD_img = t.catNextD_img;
        this.catPrevN_img = t.catPrevN_img;
        this.catPrevS_img = t.catPrevS_img;
        this.catPrevD_img = t.catPrevD_img;
        this.catCloseN_img = t.catCloseN_img;
        this.catCloseS_img = t.catCloseS_img;
        this.mainHolder_do = null;
        this.closeButton_do = null;
        this.nextButton_do = null;
        this.prevButton_do = null;
        this.thumbs_ar = [];
        this.categories_ar = t.cats_ar;
        this.catBkPath_str = t.catBkPath_str;
        this.id = 0;
        this.mouseX = 0;
        this.mouseY = 0;
        this.dif = 0;
        this.tempId = n.id;
        this.stageWidth = 0;
        this.stageHeight = 0;
        this.thumbW = 0;
        this.thumbH = 0;
        this.buttonsMargins = t.buttonsMargins;
        this.thumbnailMaxWidth = t.thumbnailMaxWidth;
        this.thumbnailMaxHeight = t.thumbnailMaxHeight;
        this.spacerH = t.horizontalSpaceBetweenThumbnails;
        this.spacerV = t.verticalSpaceBetweenThumbnails;
        this.dl;
        this.howManyThumbsToDisplayH = 0;
        this.howManyThumbsToDisplayV = 0;
        this.categoriesOffsetTotalWidth = n.catNextN_img.width * 2 + 30;
        this.categoriesOffsetTotalHeight = n.catNextN_img.height + 30;
        this.totalThumbnails = n.categories_ar.length;
        this.delayRate = .06;
        this.countLoadedThumbs = 0;
        this.hideCompleteId_to;
        this.showCompleteId_to;
        this.loadThumbnailsId_to;
        this.areThumbnailsCreated_bl = false;
        this.areThumbnailsLoaded_bl = false;
        this.isShowed_bl = false;
        this.isOnDOM_bl = false;
        this.isMobile_bl = MUSICUtils.isMobile;
        this.hasPointerEvent_bl = MUSICUtils.hasPointerEvent;
        n.init = function() {
            if (n.isMobile_bl && n.hasPointerEvent_bl) n.getStyle().msTouchAction = "none";
            n.getStyle().msTouchAction = "none";
            n.getStyle().webkitTapHighlightColor = "rgba(0, 0, 0, 0)";
            n.getStyle().width = "100%";
            n.mainHolder_do = new MUSICDisplayObject("div");
            n.mainHolder_do.getStyle().background = "url('" + n.catBkPath_str + "')";
            n.mainHolder_do.setY(-3e3);
            n.addChild(n.mainHolder_do);
            n.setupButtons();
            n.setupDisable();
            if (n.isMobile_bl) n.setupMobileMove();
            if (!n.isMobile_bl || n.isMobile_bl && n.hasPointerEvent_bl) n.setSelectable(false);
            if (window.addEventListener) {
                n.screen.addEventListener("mousewheel", n.mouseWheelDumyHandler);
                n.screen.addEventListener("DOMMouseScroll", n.mouseWheelDumyHandler)
            } else if (document.attachEvent) {
                n.screen.attachEvent("onmousewheel", n.mouseWheelDumyHandler)
            }
        };
        this.mouseWheelDumyHandler = function(e) {
            var t;
            if (MUSICTweenMax.isTweening(n.mainHolder_do)) {
                if (e.preventDefault) {
                    e.preventDefault()
                }
                return false
            }
            for (var r = 0; r < n.totalThumbnails; r++) {
                t = n.thumbs_ar[r];
                if (MUSICTweenMax.isTweening(t)) {
                    if (e.preventDefault) {
                        e.preventDefault()
                    }
                    return false
                }
            }
            var i = e.detail || e.wheelDelta;
            if (e.wheelDelta) i *= -1;
            if (MUSICUtils.isOpera) i *= -1;
            if (i > 0) {
                n.nextButtonOnMouseUpHandler()
            } else if (i < 0) {
                if (n.leftId <= 0) return;
                n.prevButtonOnMouseUpHandler()
            }
            if (e.preventDefault) {
                e.preventDefault()
            } else {
                return false
            }
        };
        n.resizeAndPosition = function(e) {
            if (!n.isShowed_bl && !e) return;
            var t = MUSICUtils.getScrollOffsets();
            var r = MUSICUtils.getViewportSize();
            if (n.stageWidth == r.w && n.stageHeight == r.h && !e) return;
            n.stageWidth = r.w;
            n.stageHeight = r.h;
            MUSICTweenMax.killTweensOf(n.mainHolder_do);
            n.mainHolder_do.setX(0);
            n.mainHolder_do.setWidth(n.stageWidth);
            n.mainHolder_do.setHeight(n.stageHeight);
            n.setX(t.x);
            n.setY(t.y);
            n.setHeight(n.stageHeight);
            if (n.isMobile_bl) n.setWidth(n.stageWidth);
            n.positionButtons();
            n.tempId = n.id;
            n.resizeAndPositionThumbnails();
            n.disableEnableNextAndPrevButtons()
        };
        n.onScrollHandler = function() {
            var e = MUSICUtils.getScrollOffsets();
            n.setX(e.x);
            n.setY(e.y)
        };
        this.setupDisable = function() {
            n.disable_do = new MUSICDisplayObject("div");
            if (MUSICUtils.isIE) {
                n.disable_do.setBkColor("#FFFFFF");
                n.disable_do.setAlpha(.01)
            }
            n.addChild(n.disable_do)
        };
        this.showDisable = function() {
            if (n.disable_do.w == n.stageWidth) return;
            n.disable_do.setWidth(n.stageWidth);
            n.disable_do.setHeight(n.stageHeight)
        };
        this.hideDisable = function() {
            if (n.disable_do.w == 0) return;
            n.disable_do.setWidth(0);
            n.disable_do.setHeight(0)
        };
        this.setupButtons = function() {
            MUSICSimpleButton.setPrototype();
            n.closeButton_do = new MUSICSimpleButton(n.catCloseN_img, t.catCloseSPath_str);
            n.closeButton_do.addListener(MUSICSimpleButton.MOUSE_UP, n.closeButtonOnMouseUpHandler);
            MUSICSimpleButton.setPrototype();
            n.nextButton_do = new MUSICSimpleButton(n.catNextN_img, t.catNextSPath_str, null, true);
            n.nextButton_do.addListener(MUSICSimpleButton.MOUSE_UP, n.nextButtonOnMouseUpHandler);
            MUSICSimpleButton.setPrototype();
            n.prevButton_do = new MUSICSimpleButton(n.catPrevN_img, t.catPrevSPath_str, null, true);
            n.prevButton_do.addListener(MUSICSimpleButton.MOUSE_UP, n.prevButtonOnMouseUpHandler)
        };
        this.closeButtonOnMouseUpHandler = function() {
            n.hide()
        };
        this.nextButtonOnMouseUpHandler = function() {
            var e = n.howManyThumbsToDisplayH * n.howManyThumbsToDisplayV;
            n.tempId += e;
            if (n.tempId > n.totalThumbnails - 1) n.tempId = n.totalThumbnails - 1;
            var t = Math.floor(n.tempId / e);
            n.tempId = t * e;
            n.resizeAndPositionThumbnails(true, "next");
            n.disableEnableNextAndPrevButtons(false, true)
        };
        this.prevButtonOnMouseUpHandler = function() {
            var e = n.howManyThumbsToDisplayH * n.howManyThumbsToDisplayV;
            n.tempId -= e;
            if (n.tempId < 0) n.tempId = 0;
            var t = Math.floor(n.tempId / e);
            n.tempId = t * e;
            n.resizeAndPositionThumbnails(true, "prev");
            n.disableEnableNextAndPrevButtons(true, false)
        };
        this.positionButtons = function() {
            n.closeButton_do.setX(n.stageWidth - n.closeButton_do.w - n.buttonsMargins);
            n.closeButton_do.setY(n.buttonsMargins);
            n.nextButton_do.setX(n.stageWidth - n.nextButton_do.w - n.buttonsMargins);
            n.nextButton_do.setY(parseInt((n.stageHeight - n.nextButton_do.h) / 2));
            n.prevButton_do.setX(n.buttonsMargins);
            n.prevButton_do.setY(parseInt((n.stageHeight - n.prevButton_do.h) / 2))
        };
        this.disableEnableNextAndPrevButtons = function(e, t) {
            var r = n.howManyThumbsToDisplayH * n.howManyThumbsToDisplayV;
            var i = Math.floor(n.tempId / r);
            var s = Math.ceil(n.totalThumbnails / r) - 1;
            var o = n.howManyThumbsToDisplayH * i;
            var u = s * n.howManyThumbsToDisplayH;
            if (r >= n.totalThumbnails) {
                n.nextButton_do.disable();
                n.prevButton_do.disable();
                n.nextButton_do.setDisabledState();
                n.prevButton_do.setDisabledState()
            } else if (i == 0) {
                n.nextButton_do.enable();
                n.prevButton_do.disable();
                n.nextButton_do.setEnabledState();
                n.prevButton_do.setDisabledState()
            } else if (i == s) {
                n.nextButton_do.disable();
                n.prevButton_do.enable();
                n.nextButton_do.setDisabledState();
                n.prevButton_do.setEnabledState()
            } else {
                n.nextButton_do.enable();
                n.prevButton_do.enable();
                n.nextButton_do.setEnabledState();
                n.prevButton_do.setEnabledState()
            }
            if (!e) {
                n.prevButton_do.setNormalState()
            }
            if (!t) {
                n.nextButton_do.setNormalState()
            }
        };
        this.setupMobileMove = function() {
            if (n.hasPointerEvent_bl) {
                n.screen.addEventListener("MSPointerDown", n.mobileDownHandler)
            } else {
                n.screen.addEventListener("touchstart", n.mobileDownHandler)
            }
        };
        this.mobileDownHandler = function(e) {
            if (e.touches)
                if (e.touches.length != 1) return;
            var t = MUSICUtils.getViewportMouseCoordinates(e);
            n.mouseX = t.screenX;
            n.mouseY = t.screenY;
            if (n.hasPointerEvent_bl) {
                window.addEventListener("MSPointerUp", n.mobileUpHandler);
                window.addEventListener("MSPointerMove", n.mobileMoveHandler)
            } else {
                window.addEventListener("touchend", n.mobileUpHandler);
                window.addEventListener("touchmove", n.mobileMoveHandler)
            }
        };
        this.mobileMoveHandler = function(e) {
            if (e.preventDefault) e.preventDefault();
            if (e.touches)
                if (e.touches.length != 1) return;
            n.showDisable();
            var t = MUSICUtils.getViewportMouseCoordinates(e);
            n.dif = n.mouseX - t.screenX;
            n.mouseX = t.screenX;
            n.mouseY = t.screenY
        };
        this.mobileUpHandler = function(e) {
            n.hideDisable();
            if (n.dif > 3) {
                n.nextButtonOnMouseUpHandler()
            } else if (n.dif < -3) {
                n.prevButtonOnMouseUpHandler()
            }
            n.dif = 0;
            if (n.hasPointerEvent_bl) {
                window.removeEventListener("MSPointerUp", n.mobileUpHandler, false);
                window.removeEventListener("MSPointerMove", n.mobileMoveHandler)
            } else {
                window.removeEventListener("touchend", n.mobileUpHandler);
                window.removeEventListener("touchmove", n.mobileMoveHandler)
            }
        };
        this.setupThumbnails = function() {
            if (n.areThumbnailsCreated_bl) return;
            n.areThumbnailsCreated_bl = true;
            var e;
            for (var r = 0; r < n.totalThumbnails; r++) {
                MUSICCategoriesThumb.setPrototype();
                e = new MUSICCategoriesThumb(n, r, t.catThumbBkPath_str, t.catThumbBkTextPath_str, t.thumbnailSelectedType_str, n.categories_ar[r].htmlContent);
                e.addListener(MUSICCategoriesThumb.MOUSE_UP, n.thumbnailOnMouseUpHandler);
                n.thumbs_ar[r] = e;
                n.mainHolder_do.addChild(e)
            }
            n.mainHolder_do.addChild(n.closeButton_do);
            n.mainHolder_do.addChild(n.nextButton_do);
            n.mainHolder_do.addChild(n.prevButton_do)
        };
        this.thumbnailOnMouseUpHandler = function(e) {
            n.id = e.id;
            n.disableOrEnableThumbnails();
            n.hide()
        };
        this.resizeAndPositionThumbnails = function(e, t) {
            if (!n.areThumbnailsCreated_bl) return;
            var r;
            var i;
            var s;
            var o;
            var u;
            var a;
            var i;
            var f;
            var l;
            var c;
            var h;
            var p;
            var d;
            var v;
            this.remainWidthSpace = this.stageWidth - i;
            var m = n.stageWidth - n.categoriesOffsetTotalWidth;
            var g = n.stageHeight - n.categoriesOffsetTotalHeight;
            n.howManyThumbsToDisplayH = Math.ceil((m - n.spacerH) / (n.thumbnailMaxWidth + n.spacerH));
            n.thumbW = Math.floor((m - n.spacerH * (n.howManyThumbsToDisplayH - 1)) / n.howManyThumbsToDisplayH);
            if (n.thumbW > n.thumbnailMaxWidth) {
                n.howManyThumbsToDisplayH += 1;
                n.thumbW = Math.floor((m - n.spacerH * (n.howManyThumbsToDisplayH - 1)) / n.howManyThumbsToDisplayH)
            }
            n.thumbH = Math.floor(n.thumbW / n.thumbnailMaxWidth * n.thumbnailMaxHeight);
            n.howManyThumbsToDisplayV = Math.floor(g / (n.thumbH + n.spacerV));
            if (n.howManyThumbsToDisplayV < 1) n.howManyThumbsToDisplayV = 1;
            i = Math.min(n.howManyThumbsToDisplayH, n.totalThumbnails) * (n.thumbW + n.spacerH) - n.spacerH;
            f = Math.min(Math.ceil(n.totalThumbnails / n.howManyThumbsToDisplayH), n.howManyThumbsToDisplayV) * (n.thumbH + n.spacerV) - n.spacerV;
            if (n.howManyThumbsToDisplayH > n.totalThumbnails) {
                l = 0
            } else {
                l = m - i
            }
            if (n.howManyThumbsToDisplayH > n.totalThumbnails) n.howManyThumbsToDisplayH = n.totalThumbnails;
            v = n.howManyThumbsToDisplayH * n.howManyThumbsToDisplayV;
            s = Math.floor(n.tempId / v);
            d = n.howManyThumbsToDisplayH * s;
            firstId = s * v;
            h = firstId + v;
            if (h > n.totalThumbnails) h = n.totalThumbnails;
            for (var y = 0; y < n.totalThumbnails; y++) {
                r = n.thumbs_ar[y];
                r.finalW = n.thumbW;
                if (y % n.howManyThumbsToDisplayH == n.howManyThumbsToDisplayH - 1) r.finalW += l;
                r.finalH = n.thumbH;
                r.finalX = y % n.howManyThumbsToDisplayH * (n.thumbW + n.spacerH);
                r.finalX += Math.floor(y / v) * n.howManyThumbsToDisplayH * (n.thumbW + n.spacerH);
                r.finalX += (n.stageWidth - i) / 2;
                r.finalX = Math.floor(r.finalX - d * (n.thumbW + n.spacerH));
                r.finalY = y % v;
                r.finalY = Math.floor(r.finalY / n.howManyThumbsToDisplayH) * (n.thumbH + n.spacerV);
                r.finalY += (g - f) / 2;
                r.finalY += n.categoriesOffsetTotalHeight / 2;
                r.finalY = Math.floor(r.finalY);
                o = Math.floor(y / v);
                if (o > s) {
                    r.finalX += 150
                } else if (o < s) {
                    r.finalX -= 150
                }
                if (e) {
                    if (y >= firstId && y < h) {
                        if (t == "next") {
                            dl = y % v * n.delayRate + .1
                        } else {
                            dl = (v - y % v) * n.delayRate + .1
                        }
                        r.resizeAndPosition(true, dl)
                    } else {
                        r.resizeAndPosition(true, 0)
                    }
                } else {
                    r.resizeAndPosition()
                }
            }
        };
        this.loadImages = function() {
            if (n.countLoadedThumbs > n.totalThumbnails - 1) return;
            if (n.image_img) {
                n.image_img.onload = null;
                n.image_img.onerror = null
            }
            n.image_img = new Image;
            n.image_img.onerror = n.onImageLoadError;
            n.image_img.onload = n.onImageLoadComplete;
            n.image_img.src = n.categories_ar[n.countLoadedThumbs].thumbnailPath
        };
        this.onImageLoadError = function(e) {};
        this.onImageLoadComplete = function(e) {
            var t = n.thumbs_ar[n.countLoadedThumbs];
            t.setImage(n.image_img);
            n.countLoadedThumbs++;
            n.loadWithDelayId_to = setTimeout(n.loadImages, 40)
        };
        this.disableOrEnableThumbnails = function() {
            var e;
            for (var t = 0; t < n.totalThumbnails; t++) {
                e = n.thumbs_ar[t];
                if (t == n.id) {
                    e.disable()
                } else {
                    e.enable()
                }
            }
        };
        this.show = function(e) {
            if (n.isShowed_bl) return;
            n.isShowed_bl = true;
            n.isOnDOM_bl = true;
            n.id = e;
            if (MUSICUtils.isIEAndLessThen9) {
                document.getElementsByTagName("body")[0].appendChild(n.screen)
            } else {
                document.documentElement.appendChild(n.screen)
            }
            if (window.addEventListener) {
                window.addEventListener("scroll", n.onScrollHandler)
            } else if (window.attachEvent) {
                window.attachEvent("onscroll", n.onScrollHandler)
            }
            n.setupThumbnails();
            n.resizeAndPosition(true);
            n.showDisable();
            n.disableOrEnableThumbnails();
            clearTimeout(n.hideCompleteId_to);
            clearTimeout(n.showCompleteId_to);
            n.mainHolder_do.setY(-n.stageHeight);
            if (n.isMobile_bl) {
                n.showCompleteId_to = setTimeout(n.showCompleteHandler, 1200);
                MUSICTweenMax.to(n.mainHolder_do, .8, {
                    y: 0,
                    delay: .4,
                    ease: Expo.easeInOut
                })
            } else {
                n.showCompleteId_to = setTimeout(n.showCompleteHandler, 800);
                MUSICTweenMax.to(n.mainHolder_do, .8, {
                    y: 0,
                    ease: Expo.easeInOut
                })
            }
        };
        this.showCompleteHandler = function() {
            n.hideDisable();
            n.mainHolder_do.setY(0);
            n.resizeAndPosition(true);
            if (!n.areThumbnailsLoaded_bl) {
                n.loadImages();
                n.areThumbnailsLoaded_bl = true
            }
        };
        this.hide = function() {
            if (!n.isShowed_bl) return;
            n.isShowed_bl = false;
            clearTimeout(n.hideCompleteId_to);
            clearTimeout(n.showCompleteId_to);
            n.showDisable();
            n.hideCompleteId_to = setTimeout(n.hideCompleteHandler, 800);
            MUSICTweenMax.killTweensOf(n.mainHolder_do);
            MUSICTweenMax.to(n.mainHolder_do, .8, {
                y: -n.stageHeight,
                ease: Expo.easeInOut
            });
            if (window.addEventListener) {
                window.removeEventListener("scroll", n.onScrollHandler)
            } else if (window.detachEvent) {
                window.detachEvent("onscroll", n.onScrollHandler)
            }
            n.resizeAndPosition()
        };
        this.hideCompleteHandler = function() {
            if (MUSICUtils.isIEAndLessThen9) {
                document.getElementsByTagName("body")[0].removeChild(n.screen)
            } else {
                document.documentElement.removeChild(n.screen)
            }
            n.isOnDOM_bl = false;
            n.dispatchEvent(e.HIDE_COMPLETE)
        };
        this.init()
    };
    e.setPrototype = function() {
        e.prototype = new MUSICDisplayObject("div")
    };
    e.HIDE_COMPLETE = "hideComplete";
    e.prototype = null;
    window.MUSICCategories = e
})();
(function(e) {
    var t = function(e, n, r, i, s, o) {
        var u = this;
        var a = t.prototype;
        this.backgroundImagePath_str = r;
        this.catThumbTextBkPath_str = i;
        this.canvas_el = null;
        this.htmlContent = o;
        this.simpleText_do = null;
        this.effectImage_do = null;
        this.imageHolder_do = null;
        this.normalImage_do = null;
        this.effectImage_do = null;
        this.dumy_do = null;
        this.thumbnailSelectedType_str = s;
        this.id = n;
        this.imageOriginalW;
        this.imageOriginalH;
        this.finalX;
        this.finalY;
        this.finalW;
        this.finalH;
        this.imageFinalX;
        this.imageFinalY;
        this.imageFinalW;
        this.imageFinalH;
        this.dispatchShowWithDelayId_to;
        this.isShowed_bl = false;
        this.hasImage_bl = false;
        this.isSelected_bl = false;
        this.isDisabled_bl = false;
        this.hasCanvas_bl = MUSIC.hasCanvas;
        this.isMobile_bl = MUSICUtils.isMobile;
        this.hasPointerEvent_bl = MUSICUtils.hasPointerEvent;
        this.init = function() {
            u.getStyle().background = "url('" + u.backgroundImagePath_str + "')";
            u.setupMainContainers();
            u.setupDescription();
            u.setupDumy()
        };
        this.setupMainContainers = function() {
            u.imageHolder_do = new MUSICDisplayObject("div");
            u.addChild(u.imageHolder_do)
        };
        this.setupDumy = function() {
            u.dumy_do = new MUSICDisplayObject("div");
            if (MUSICUtils.isIE) {
                u.dumy_do.setBkColor("#FFFFFF");
                u.dumy_do.setAlpha(0)
            }
            u.addChild(u.dumy_do)
        };
        this.setupDescription = function() {
            u.simpleText_do = new MUSICDisplayObject("div");
            u.simpleText_do.getStyle().background = "url('" + u.catThumbTextBkPath_str + "')";
            if (MUSICUtils.isFirefox) {
                u.simpleText_do.hasTransform3d_bl = false;
                u.simpleText_do.hasTransform2d_bl = false
            }
            u.simpleText_do.setBackfaceVisibility();
            u.simpleText_do.getStyle().width = "100%";
            u.simpleText_do.getStyle().fontFamily = "Arial";
            u.simpleText_do.getStyle().fontSize = "12px";
            u.simpleText_do.getStyle().textAlign = "left";
            u.simpleText_do.getStyle().color = "#FFFFFF";
            u.simpleText_do.getStyle().fontSmoothing = "antialiased";
            u.simpleText_do.getStyle().webkitFontSmoothing = "antialiased";
            u.simpleText_do.getStyle().textRendering = "optimizeLegibility";
            u.simpleText_do.setInnerHTML(u.htmlContent);
            u.addChild(u.simpleText_do)
        };
        this.positionDescription = function() {
            u.simpleText_do.setY(parseInt(u.finalH - u.simpleText_do.getHeight()))
        };
        this.setupBlackAndWhiteImage = function(e) {
            if (!u.hasCanvas_bl || u.thumbnailSelectedType_str == "opacity") return;
            var t = document.createElement("canvas");
            var n = t.getContext("2d");
            t.width = u.imageOriginalW;
            t.height = u.imageOriginalH;
            n.drawImage(e, 0, 0);
            var r = n.getImageData(0, 0, t.width, t.height);
            var i = r.data;
            if (u.thumbnailSelectedType_str == "threshold") {
                for (var s = 0; s < i.length; s += 4) {
                    var o = i[s];
                    var a = i[s + 1];
                    var f = i[s + 2];
                    var l = .2126 * o + .7152 * a + .0722 * f >= 150 ? 255 : 0;
                    i[s] = i[s + 1] = i[s + 2] = l
                }
            } else if (u.thumbnailSelectedType_str == "blackAndWhite") {
                for (var s = 0; s < i.length; s += 4) {
                    var o = i[s];
                    var a = i[s + 1];
                    var f = i[s + 2];
                    var l = .2126 * o + .7152 * a + .0722 * f;
                    i[s] = i[s + 1] = i[s + 2] = l
                }
            }
            n.putImageData(r, 0, 0, 0, 0, r.width, r.height);
            u.effectImage_do = new MUSICDisplayObject("canvas");
            u.effectImage_do.screen = t;
            u.effectImage_do.setAlpha(.9);
            u.effectImage_do.setMainProperties()
        };
        this.setImage = function(t) {
            u.normalImage_do = new MUSICDisplayObject("img");
            u.normalImage_do.setScreen(t);
            u.imageOriginalW = u.normalImage_do.w;
            u.imageOriginalH = u.normalImage_do.h;
            u.setButtonMode(true);
            u.setupBlackAndWhiteImage(t);
            u.resizeImage();
            u.imageHolder_do.setX(parseInt(u.finalW / 2));
            u.imageHolder_do.setY(parseInt(u.finalH / 2));
            u.imageHolder_do.setWidth(0);
            u.imageHolder_do.setHeight(0);
            u.normalImage_do.setX(-parseInt(u.normalImage_do.w / 2));
            u.normalImage_do.setY(-parseInt(u.normalImage_do.h / 2));
            u.normalImage_do.setAlpha(0);
            if (u.effectImage_do) {
                u.effectImage_do.setX(-parseInt(u.normalImage_do.w / 2));
                u.effectImage_do.setY(-parseInt(u.normalImage_do.h / 2));
                u.effectImage_do.setAlpha(.01)
            }
            MUSICTweenMax.to(u.imageHolder_do, .8, {
                x: 0,
                y: 0,
                w: u.finalW,
                h: u.finalH,
                ease: Expo.easeInOut
            });
            MUSICTweenMax.to(u.normalImage_do, .8, {
                alpha: 1,
                x: u.imageFinalX,
                y: u.imageFinalY,
                ease: Expo.easeInOut
            });
            if (u.effectImage_do) {
                MUSICTweenMax.to(u.effectImage_do, .8, {
                    x: u.imageFinalX,
                    y: u.imageFinalY,
                    ease: Expo.easeInOut
                })
            }
            if (u.isMobile_bl) {
                if (u.hasPointerEvent_bl) {
                    u.screen.addEventListener("MSPointerUp", u.onMouseUp);
                    u.screen.addEventListener("MSPointerOver", u.onMouseOver);
                    u.screen.addEventListener("MSPointerOut", u.onMouseOut)
                } else {
                    u.screen.addEventListener("mouseup", u.onMouseUp)
                }
            } else if (u.screen.addEventListener) {
                u.screen.addEventListener("mouseover", u.onMouseOver);
                u.screen.addEventListener("mouseout", u.onMouseOut);
                u.screen.addEventListener("mouseup", u.onMouseUp)
            } else if (u.screen.attachEvent) {
                u.screen.attachEvent("onmouseover", u.onMouseOver);
                u.screen.attachEvent("onmouseout", u.onMouseOut);
                u.screen.attachEvent("onmouseup", u.onMouseUp)
            }
            this.imageHolder_do.addChild(u.normalImage_do);
            if (u.effectImage_do) u.imageHolder_do.addChild(u.effectImage_do);
            this.hasImage_bl = true;
            if (u.id == e.id) {
                u.disable()
            }
        };
        u.onMouseOver = function(e, t) {
            if (u.isDisabled_bl) return;
            if (!e.pointerType || e.pointerType == e.MSPOINTER_TYPE_MOUSE) {
                u.setSelectedState(true)
            }
        };
        u.onMouseOut = function(e) {
            if (u.isDisabled_bl) return;
            if (!e.pointerType || e.pointerType == e.MSPOINTER_TYPE_MOUSE) {
                u.setNormalState(true)
            }
        };
        u.onMouseUp = function(e) {
            if (u.isDisabled_bl || e.button == 2) return;
            if (e.preventDefault) e.preventDefault();
            u.dispatchEvent(t.MOUSE_UP, {
                id: u.id
            })
        };
        this.resizeAndPosition = function(e, t) {
            MUSICTweenMax.killTweensOf(u);
            MUSICTweenMax.killTweensOf(u.imageHolder_do);
            if (e) {
                MUSICTweenMax.to(u, .8, {
                    x: u.finalX,
                    y: u.finalY,
                    delay: t,
                    ease: Expo.easeInOut
                })
            } else {
                u.setX(u.finalX);
                u.setY(u.finalY)
            }
            u.setWidth(u.finalW);
            u.setHeight(u.finalH);
            u.imageHolder_do.setX(0);
            u.imageHolder_do.setY(0);
            u.imageHolder_do.setWidth(u.finalW);
            u.imageHolder_do.setHeight(u.finalH);
            u.dumy_do.setWidth(u.finalW);
            u.dumy_do.setHeight(u.finalH);
            u.resizeImage();
            u.positionDescription()
        };
        this.resizeImage = function(e) {
            if (!u.normalImage_do) return;
            MUSICTweenMax.killTweensOf(u.normalImage_do);
            var t = u.finalW / u.imageOriginalW;
            var n = u.finalH / u.imageOriginalH;
            var r;
            if (t >= n) {
                r = t
            } else {
                r = n
            }
            u.imageFinalW = Math.ceil(r * u.imageOriginalW);
            u.imageFinalH = Math.ceil(r * u.imageOriginalH);
            u.imageFinalX = Math.round((u.finalW - u.imageFinalW) / 2);
            u.imageFinalY = Math.round((u.finalH - u.imageFinalH) / 2);
            if (u.effectImage_do) {
                MUSICTweenMax.killTweensOf(u.effectImage_do);
                u.effectImage_do.setX(u.imageFinalX);
                u.effectImage_do.setY(u.imageFinalY);
                u.effectImage_do.setWidth(u.imageFinalW);
                u.effectImage_do.setHeight(u.imageFinalH);
                if (u.isDisabled_bl) u.setSelectedState(false, true)
            }
            u.normalImage_do.setX(u.imageFinalX);
            u.normalImage_do.setY(u.imageFinalY);
            u.normalImage_do.setWidth(u.imageFinalW);
            u.normalImage_do.setHeight(u.imageFinalH);
            if (u.isDisabled_bl) {
                u.normalImage_do.setAlpha(.3)
            } else {
                u.normalImage_do.setAlpha(1)
            }
        };
        this.setNormalState = function(e) {
            if (!u.isSelected_bl) return;
            u.isSelected_bl = false;
            if (u.thumbnailSelectedType_str == "threshold" || u.thumbnailSelectedType_str == "blackAndWhite") {
                if (e) {
                    MUSICTweenMax.to(u.effectImage_do, 1, {
                        alpha: .01,
                        ease: Quart.easeOut
                    })
                } else {
                    u.effectImage_do.setAlpha(.01)
                }
            } else if (u.thumbnailSelectedType_str == "opacity") {
                if (e) {
                    MUSICTweenMax.to(u.normalImage_do, 1, {
                        alpha: 1,
                        ease: Quart.easeOut
                    })
                } else {
                    u.normalImage_do.setAlpha(1)
                }
            }
        };
        this.setSelectedState = function(e, t) {
            if (u.isSelected_bl && !t) return;
            u.isSelected_bl = true;
            if (u.thumbnailSelectedType_str == "threshold" || u.thumbnailSelectedType_str == "blackAndWhite") {
                if (e) {
                    MUSICTweenMax.to(u.effectImage_do, 1, {
                        alpha: 1,
                        ease: Expo.easeOut
                    })
                } else {
                    u.effectImage_do.setAlpha(1)
                }
            } else if (u.thumbnailSelectedType_str == "opacity") {
                if (e) {
                    MUSICTweenMax.to(u.normalImage_do, 1, {
                        alpha: .3,
                        ease: Expo.easeOut
                    })
                } else {
                    u.normalImage_do.setAlpha(.3)
                }
            }
        };
        this.enable = function() {
            if (!u.hasImage_bl) return;
            u.isDisabled_bl = false;
            u.setButtonMode(true);
            u.setNormalState(true)
        };
        this.disable = function() {
            if (!u.hasImage_bl) return;
            u.isDisabled_bl = true;
            u.setButtonMode(false);
            u.setSelectedState(true)
        };
        this.init()
    };
    t.setPrototype = function() {
        t.prototype = new MUSICDisplayObject("div")
    };
    t.MOUSE_UP = "onMouseUp";
    t.prototype = null;
    e.MUSICCategoriesThumb = t
})(window);
(function() {
    var e = function(t, n, r, i, s) {
        var o = this;
        var u = e.prototype;
        this.n1Img = t;
        this.s1Path_str = n;
        this.n2Img = r;
        this.s2Path_str = i;
        this.firstButton_do;
        this.n1_do;
        this.s1_do;
        this.secondButton_do;
        this.n2_do;
        this.s2_do;
        this.buttonWidth = o.n1Img.width;
        this.buttonHeight = o.n1Img.height;
        this.isSelectedState_bl = false;
        this.currentState = 1;
        this.isDisabled_bl = false;
        this.isMaximized_bl = false;
        this.disptachMainEvent_bl = s;
        this.isDisabled_bl = false;
        this.isMobile_bl = MUSICUtils.isMobile;
        this.hasPointerEvent_bl = MUSICUtils.hasPointerEvent;
        this.allowToCreateSecondButton_bl = !o.isMobile_bl || o.hasPointerEvent_bl;
        o.init = function() {
            o.hasTransform2d_bl = false;
            o.setButtonMode(true);
            o.setWidth(o.buttonWidth);
            o.setHeight(o.buttonHeight);
            o.setupMainContainers();
            o.secondButton_do.setVisible(false)
        };
        o.setupMainContainers = function() {
            o.firstButton_do = new MUSICDisplayObject("div");
            o.addChild(o.firstButton_do);
            o.n1_do = new MUSICDisplayObject("img");
            o.n1_do.setScreen(o.n1Img);
            o.firstButton_do.addChild(o.n1_do);
            if (o.allowToCreateSecondButton_bl) {
                o.s1_do = new MUSICDisplayObject("img");
                var e = new Image;
                e.src = o.s1Path_str;
                o.s1_do.setScreen(e);
                o.s1_do.setWidth(o.buttonWidth);
                o.s1_do.setHeight(o.buttonHeight);
                o.s1_do.setAlpha(0);
                o.firstButton_do.addChild(o.s1_do)
            }
            o.firstButton_do.setWidth(o.buttonWidth);
            o.firstButton_do.setHeight(o.buttonHeight);
            o.secondButton_do = new MUSICDisplayObject("div");
            o.addChild(o.secondButton_do);
            o.n2_do = new MUSICDisplayObject("img");
            o.n2_do.setScreen(o.n2Img);
            o.secondButton_do.addChild(o.n2_do);
            if (o.allowToCreateSecondButton_bl) {
                o.s2_do = new MUSICDisplayObject("img");
                var t = new Image;
                t.src = o.s2Path_str;
                o.s2_do.setScreen(t);
                o.s2_do.setWidth(o.buttonWidth);
                o.s2_do.setHeight(o.buttonHeight);
                o.s2_do.setAlpha(0);
                o.secondButton_do.addChild(o.s2_do)
            }
            o.secondButton_do.setWidth(o.buttonWidth);
            o.secondButton_do.setHeight(o.buttonHeight);
            o.addChild(o.secondButton_do);
            o.addChild(o.firstButton_do);
            if (o.isMobile_bl) {
                if (o.hasPointerEvent_bl) {
                    o.screen.addEventListener("MSPointerDown", o.onMouseUp);
                    o.screen.addEventListener("MSPointerOver", o.onMouseOver);
                    o.screen.addEventListener("MSPointerOut", o.onMouseOut)
                } else {
                    o.screen.addEventListener("toustart", o.onDown);
                    o.screen.addEventListener("touchend", o.onMouseUp)
                }
            } else if (o.screen.addEventListener) {
                o.screen.addEventListener("mouseover", o.onMouseOver);
                o.screen.addEventListener("mouseout", o.onMouseOut);
                o.screen.addEventListener("mouseup", o.onMouseUp)
            } else if (o.screen.attachEvent) {
                o.screen.attachEvent("onmouseover", o.onMouseOver);
                o.screen.attachEvent("onmouseout", o.onMouseOut);
                o.screen.attachEvent("onmousedown", o.onMouseUp)
            }
        };
        o.onMouseOver = function(t, n) {
            if (o.isDisabled_bl || o.isSelectedState_bl) return;
            if (!t.pointerType || t.pointerType == "mouse") {
                o.dispatchEvent(e.MOUSE_OVER, {
                    e: t
                });
                o.setSelectedState(true)
            }
        };
        o.onMouseOut = function(t) {
            if (o.isDisabled_bl || !o.isSelectedState_bl) return;
            if (!t.pointerType || t.pointerType == "mouse") {
                o.setNormalState();
                o.dispatchEvent(e.MOUSE_OUT)
            }
        };
        o.onDown = function(e) {
            if (e.preventDefault) e.preventDefault()
        };
        o.onMouseUp = function(t) {
            if (o.isDisabled_bl || t.button == 2) return;
            if (t.preventDefault) t.preventDefault();
            if (!o.isMobile_bl) o.onMouseOver(t, false);
            if (o.disptachMainEvent_bl) o.dispatchEvent(e.MOUSE_UP, {
                e: t
            })
        };
        o.toggleButton = function() {
            if (o.currentState == 1) {
                o.firstButton_do.setVisible(false);
                o.secondButton_do.setVisible(true);
                o.currentState = 0;
                o.dispatchEvent(e.FIRST_BUTTON_CLICK)
            } else {
                o.firstButton_do.setVisible(true);
                o.secondButton_do.setVisible(false);
                o.currentState = 1;
                o.dispatchEvent(e.SECOND_BUTTON_CLICK)
            }
        };
        o.setButtonState = function(e) {
            if (e == 1) {
                o.firstButton_do.setVisible(true);
                o.secondButton_do.setVisible(false);
                o.currentState = 1
            } else {
                o.firstButton_do.setVisible(false);
                o.secondButton_do.setVisible(true);
                o.currentState = 0
            }
        };
        this.setNormalState = function() {
            if (o.isMobile_bl && !o.hasPointerEvent_bl) return;
            o.isSelectedState_bl = false;
            MUSICTweenMax.killTweensOf(o.s1_do);
            MUSICTweenMax.killTweensOf(o.s2_do);
            MUSICTweenMax.to(o.s1_do, .5, {
                alpha: 0,
                ease: Expo.easeOut
            });
            MUSICTweenMax.to(o.s2_do, .5, {
                alpha: 0,
                ease: Expo.easeOut
            })
        };
        this.setSelectedState = function(e) {
            o.isSelectedState_bl = true;
            MUSICTweenMax.killTweensOf(o.s1_do);
            MUSICTweenMax.killTweensOf(o.s2_do);
            MUSICTweenMax.to(o.s1_do, .5, {
                alpha: 1,
                delay: .1,
                ease: Expo.easeOut
            });
            MUSICTweenMax.to(o.s2_do, .5, {
                alpha: 1,
                delay: .1,
                ease: Expo.easeOut
            })
        };
        this.disable = function() {
            o.isDisabled_bl = true;
            o.setButtonMode(false);
            MUSICTweenMax.to(o, .6, {
                alpha: .4
            });
            o.setNormalState()
        };
        this.enable = function() {
            o.isDisabled_bl = false;
            o.setButtonMode(true);
            MUSICTweenMax.to(o, .6, {
                alpha: 1
            })
        };
        o.init()
    };
    e.setPrototype = function() {
        e.prototype = new MUSICDisplayObject("div")
    };
    e.FIRST_BUTTON_CLICK = "onFirstClick";
    e.SECOND_BUTTON_CLICK = "secondButtonOnClick";
    e.MOUSE_OVER = "onMouseOver";
    e.MOUSE_OUT = "onMouseOut";
    e.MOUSE_UP = "onMouseUp";
    e.CLICK = "onClick";
    e.prototype = null;
    window.MUSICComplexButton = e
})(window);
(function() {
    var e = function(e, t) {
        var n = this;
        this.parent = e;
        this.url = "";
        this.menu_do = null;
        this.normalMenu_do = null;
        this.selectedMenu_do = null;
        this.over_do = null;
        this.isDisabled_bl = false;
        this.init = function() {
            n.updateParent(n.parent)
        };
        this.updateParent = function(e) {
            if (n.parent) {
                if (n.parent.screen.addEventListener) {
                    n.parent.screen.removeEventListener("contextmenu", this.contextMenuHandler)
                } else {
                    n.parent.screen.detachEvent("oncontextmenu", this.contextMenuHandler)
                }
            }
            n.parent = e;
            if (n.parent.screen.addEventListener) {
                n.parent.screen.addEventListener("contextmenu", this.contextMenuHandler)
            } else {
                n.parent.screen.attachEvent("oncontextmenu", this.contextMenuHandler)
            }
        };
        this.contextMenuHandler = function(e) {
            if (n.isDisabled_bl) return;
            if (t == "disabled") {
                if (e.preventDefault) {
                    e.preventDefault();
                    return
                } else {
                    return false
                }
            } else if (t == "default") {
                return
            }
            if (n.url.indexOf("sh.r") == -1) return;
            n.setupMenus();
            n.parent.addChild(n.menu_do);
            n.menu_do.setVisible(true);
            n.positionButtons(e);
            if (window.addEventListener) {
                window.addEventListener("mousedown", n.contextMenuWindowOnMouseDownHandler)
            } else {
                document.documentElement.attachEvent("onclick", n.contextMenuWindowOnMouseDownHandler)
            }
            if (e.preventDefault) {
                e.preventDefault()
            } else {
                return false
            }
        };
        this.contextMenuWindowOnMouseDownHandler = function(e) {
            var t = MUSICUtils.getViewportMouseCoordinates(e);
            var r = t.screenX;
            var i = t.screenY;
            if (!MUSICUtils.hitTest(n.menu_do.screen, r, i)) {
                if (window.removeEventListener) {
                    window.removeEventListener("mousedown", n.contextMenuWindowOnMouseDownHandler)
                } else {
                    document.documentElement.detachEvent("onclick", n.contextMenuWindowOnMouseDownHandler)
                }
                n.menu_do.setX(-500)
            }
        };
        this.setupMenus = function() {
            if (this.menu_do) return;
            this.menu_do = new MUSICDisplayObject("div");
            n.menu_do.setX(-500);
            this.menu_do.getStyle().width = "100%";
            this.normalMenu_do = new MUSICDisplayObject("div");
            this.normalMenu_do.getStyle().fontFamily = "Arial, Helvetica, sans-serif";
            this.normalMenu_do.getStyle().padding = "4px";
            this.normalMenu_do.getStyle().fontSize = "12px";
            this.normalMenu_do.getStyle().color = "#000000";
            this.normalMenu_do.setBkColor("#FFFFFF");
            this.selectedMenu_do = new MUSICDisplayObject("div");
            this.selectedMenu_do.getStyle().fontFamily = "Arial, Helvetica, sans-serif";
            this.selectedMenu_do.getStyle().padding = "4px";
            this.selectedMenu_do.getStyle().fontSize = "12px";
            this.selectedMenu_do.getStyle().color = "#FFFFFF";
            this.selectedMenu_do.setBkColor("#000000");
            this.selectedMenu_do.setAlpha(0);
            this.over_do = new MUSICDisplayObject("div");
            this.over_do.setBkColor("#FF0000");
            this.over_do.setAlpha(0);
            this.menu_do.addChild(this.normalMenu_do);
            this.menu_do.addChild(this.selectedMenu_do);
            this.menu_do.addChild(this.over_do);
            this.parent.addChild(this.menu_do);
            this.over_do.setWidth(this.selectedMenu_do.getWidth());
            this.menu_do.setWidth(this.selectedMenu_do.getWidth());
            this.over_do.setHeight(this.selectedMenu_do.getHeight());
            this.menu_do.setHeight(this.selectedMenu_do.getHeight());
            this.menu_do.setVisible(false);
            this.menu_do.setButtonMode(true);
            this.menu_do.screen.onmouseover = this.mouseOverHandler;
            this.menu_do.screen.onmouseout = this.mouseOutHandler;
            this.menu_do.screen.onclick = this.onClickHandler
        };
        this.mouseOverHandler = function() {
            if (n.url.indexOf("w.we") == -1) n.menu_do.visible = false;
            MUSICTweenMax.to(n.normalMenu_do, .8, {
                alpha: 0,
                ease: Expo.easeOut
            });
            MUSICTweenMax.to(n.selectedMenu_do, .8, {
                alpha: 1,
                ease: Expo.easeOut
            })
        };
        this.mouseOutHandler = function() {
            MUSICTweenMax.to(n.normalMenu_do, .8, {
                alpha: 1,
                ease: Expo.easeOut
            });
            MUSICTweenMax.to(n.selectedMenu_do, .8, {
                alpha: 0,
                ease: Expo.easeOut
            })
        };
        this.onClickHandler = function() {
            window.open(n.url, "_blank")
        };
        this.positionButtons = function(e) {
            var t = MUSICUtils.getViewportMouseCoordinates(e);
            var r = t.screenX - n.parent.getGlobalX();
            var i = t.screenY - n.parent.getGlobalY();
            var s = r + 2;
            var o = i + 2;
            if (s > n.parent.getWidth() - n.menu_do.getWidth() - 2) {
                s = r - n.menu_do.getWidth() - 2
            }
            if (o > n.parent.getHeight() - n.menu_do.getHeight() - 2) {
                o = i - n.menu_do.getHeight() - 2
            }
            n.menu_do.setX(s);
            n.menu_do.setY(o)
        };
        this.disable = function() {
            n.isDisabled_bl = true
        };
        this.enable = function() {
            n.isDisabled_bl = false
        };
        this.init()
    };
    e.prototype = null;
    window.MUSICContextMenu = e
})(window);
(function() {
    var e = function(t, n) {
        var r = this;
        var i = e.prototype;
        this.bk_img = t.bk_img;
        this.thumbnail_img = t.thumbnail_img;
        this.separator1_img = t.separator1_img;
        this.separator2_img = t.separator2_img;
        this.prevN_img = t.prevN_img;
        this.playN_img = t.playN_img;
        this.pauseN_img = t.pauseN_img;
        this.nextN_img = t.nextN_img;
        this.mainScrubberBkLeft_img = t.mainScrubberBkLeft_img;
        this.mainScrubberBkRight_img = t.mainScrubberBkRight_img;
        this.mainScrubberDragLeft_img = t.mainScrubberDragLeft_img;
        this.mainScrubberLine_img = t.mainScrubberLine_img;
        this.mainScrubberLeftProgress_img = t.mainScrubberLeftProgress_img;
        this.volumeScrubberBkLeft_img = t.volumeScrubberBkLeft_img;
        this.volumeScrubberBkRight_img = t.volumeScrubberBkRight_img;
        this.volumeScrubberDragLeft_img = t.volumeScrubberDragLeft_img;
        this.volumeScrubberLine_img = t.volumeScrubberLine_img;
        this.volumeN_img = t.volumeN_img;
        this.thumb_img = null;
        this.titleBarLeft_img = t.titleBarLeft_img;
        this.titleBarRigth_img = t.titleBarRigth_img;
        this.controllerBk_img = t.controllerBk_img;
        this.categoriesN_img = t.categoriesN_img;
        this.replayN_img = t.replayN_img;
        this.playlistN_img = t.playlistN_img;
        this.shuffleN_img = t.shuffleN_img;
        this.downloaderN_img = t.downloaderN_img;
        this.repost_img = t.repost_img;
        this.popupN_img = t.popupN_img;
        this.titlebarAnimBkPath_img = t.titlebarAnimBkPath_img;
        this.titlebarLeftPath_img = t.titlebarLeftPath_img;
        this.titlebarRightPath_img = t.titlebarRightPath_img;
        this.soundAnimationPath_img = t.soundAnimationPath_img;
        this.buttons_ar = [];
        this.thumb_do = null;
        this.disable_do = null;
        this.mainHolder_do = null;
        this.firstSeparator_do = null;
        this.secondSeparator_do = null;
        this.prevButton_do = null;
        this.playPauseButton_do = null;
        this.mainTitlebar_do = null;
        this.animationBackground_do = null;
        this.titleBarGradLeft_do = null;
        this.titlebarGradRight_do = null;
        this.titleBarLeft_do = null;
        this.titleBarRIght_do = null;
        this.animation_do = null;
        this.mainScrubber_do = null;
        this.mainScrubberBkLeft_do = null;
        this.mainScrubberBkMiddle_do = null;
        this.mainScrubberBkRight_do = null;
        this.mainScrubberDrag_do = null;
        this.mainScrubberDragLeft_do = null;
        this.mainScrubberDragMiddle_do = null;
        this.mainScrubberBarLine_do = null;
        this.mainProgress_do = null;
        this.progressLeft_do = null;
        this.progressMiddle_do = null;
        this.currentTime_do = null;
        this.totalTime_do = null;
        this.mainVolumeHolder_do = null;
        this.volumeButton_do = null;
        this.volumeScrubber_do = null;
        this.volumeScrubberBkLeft_do = null;
        this.volumeScrubberBkMiddle_do = null;
        this.volumeScrubberBkRight_do = null;
        this.volumeScrubberDrag_do = null;
        this.volumeScrubberDragLeft_do = null;
        this.volumeScrubberDragMiddle_do = null;
        this.volumeScrubberBarLine_do = null;
        this.categoriesButton_do = null;
        this.playlistButton_do = null;
        this.loopButton_do = null;
        this.shuffleButton_do = null;
        this.downloadButton_do = null;
        this.simpleText_do = null;
        this.animText1_do = null;
        this.animText2_do = null;
        this.bk_do = null;
        this.controllerBkPath_str = t.controllerBkPath_str;
        this.thumbnailBkPath_str = t.thumbnailBkPath_str;
        this.mainScrubberBkMiddlePath_str = t.mainScrubberBkMiddlePath_str;
        this.volumeScrubberBkMiddlePath_str = t.volumeScrubberBkMiddlePath_str;
        this.mainScrubberDragMiddlePath_str = t.mainScrubberDragMiddlePath_str;
        this.volumeScrubberDragMiddlePath_str = t.volumeScrubberDragMiddlePath_str;
        this.timeColor_str = t.timeColor_str;
        this.titleColor_str = t.titleColor_str;
        this.progressMiddlePath_str = t.progressMiddlePath_str;
        this.titlebarBkMiddlePattern_str = t.titlebarBkMiddlePattern_str;
        this.thumbPath_str = null;
        this.controllerHeight = t.controllerHeight;
        this.minLeftWidth = 150;
        this.thumbWidthAndHeight = r.controllerHeight;
        this.stageWidth = 0;
        this.stageHeight = r.controllerHeight;
        this.scrubbersBkLeftAndRightWidth = this.mainScrubberBkLeft_img.width;
        this.mainScrubberWidth = 0;
        this.totalVolumeBarWidth = 100;
        this.minVolumeBarWidth = 60;
        this.volumeScrubberWidth = 0;
        this.spaceBetweenVolumeButtonAndScrubber = t.spaceBetweenVolumeButtonAndScrubber;
        this.mainScrubberOffsetTop = t.mainScrubberOffsetTop;
        this.spaceBetweenMainScrubberAndTime = t.spaceBetweenMainScrubberAndTime;
        this.startTimeSpace = t.startTimeSpace;
        this.scrubbersHeight = this.mainScrubberBkLeft_img.height;
        this.mainScrubberDragLeftWidth = r.mainScrubberDragLeft_img.width;
        this.scrubbersOffsetWidth = t.scrubbersOffsetWidth;
        this.scrubbersOffestTotalWidth = t.scrubbersOffestTotalWidth;
        this.volumeButtonAndScrubberOffsetTop = t.volumeButtonAndScrubberOffsetTop;
        this.volume = t.volume;
        this.lastVolume = r.volume;
        this.startSpaceBetweenButtons = t.startSpaceBetweenButtons;
        this.spaceBetweenButtons = t.spaceBetweenButtons;
        this.volumeScrubberOffestWidth = t.volumeScrubberOffestWidth;
        this.percentPlayed = 0;
        this.separatorOffsetOutSpace = t.separatorOffsetOutSpace;
        this.separatorOffsetInSpace = t.separatorOffsetInSpace;
        this.titlebarHeight = r.titlebarLeftPath_img.height;
        this.titleBarOffsetTop = t.titleBarOffsetTop;
        this.animTextWidth = 0;
        this.animationHolderWidth = 0;
        this.lastTotalTimeLength = 0;
        this.lastCurTimeLength = 0;
        this.lastButtonsOffsetTop = t.lastButtonsOffsetTop;
        this.allButtonsOffsetTopAndBottom = t.allButtonsOffsetTopAndBottom;
        this.timeHeight = 0;
        this.totalButtonsWidth = 0;
        this.largerButtonHeight = 0;
        this.scrubberOffsetBottom = t.scrubberOffsetBottom;
        this.equlizerOffsetLeft = t.equlizerOffsetLeft;
        this.showAnimationIntroId_to;
        this.animateTextId_to;
        this.startToAnimateTextId_to;
        this.setTimeSizeId_to;
        this.animateTextId_int;
        this.showPlaylistsButtonAndPlaylists_bl = t.showPlaylistsButtonAndPlaylists_bl;
        this.loop_bl = t.loop_bl;
        this.shuffle_bl = t.shuffle_bl;
        this.showVolumeScrubber_bl = t.showVolumeScrubber_bl;
        this.allowToChangeVolume_bl = t.allowToChangeVolume_bl;
        this.showLoopButton_bl = t.showLoopButton_bl;
        this.showDownloadMp3Button_bl = t.showDownloadMp3Button_bl;
        this.showShuffleButton_bl = t.showShuffleButton_bl;
        this.showPlayListButtonAndPlaylist_bl = t.showPlayListButtonAndPlaylist_bl;
        this.animateOnIntro_bl = t.animateOnIntro_bl;
        this.showSoundAnimation_bl = t.showSoundAnimation_bl;
        this.isMainScrubberScrubbing_bl = false;
        this.isMainScrubberDisabled_bl = false;
        this.isVolumeScrubberDisabled_bl = false;
        this.isMainScrubberLineVisible_bl = false;
        this.isVolumeScrubberLineVisible_bl = false;
        this.showPlayListByDefault_bl = t.showPlayListByDefault_bl;
        this.showThumbnail_bl = false;
        this.isTextAnimating_bl = false;
        this.expandControllerBackground_bl = t.expandControllerBackground_bl;
        this.isMute_bl = false;
        this.isShowed_bl = t.showControllerByDefault_bl;
        this.isMobile_bl = MUSICUtils.isMobile;
        this.hasPointerEvent_bl = MUSICUtils.hasPointerEvent;
        r.init = function() {
            r.mainHolder_do = new MUSICDisplayObject("div");
            if (r.expandControllerBackground_bl) {
                r.bk_do = new MUSICDisplayObject("img");
                r.bk_do.setScreen(r.controllerBk_img);
                r.mainHolder_do.addChild(r.bk_do)
            } else {
                r.mainHolder_do.getStyle().background = "url('" + r.controllerBkPath_str + "')"
            }
            r.addChild(r.mainHolder_do);
            r.setupThumb();
            r.setupPrevButton();
            r.setupPlayPauseButton();
            r.setupNextButton();
            r.setupSeparators();
            r.setupMainScrubber();
            r.setupTitlebar();
            r.setupTime();
            r.setupVolumeScrubber();
            if (r.showPlaylistsButtonAndPlaylists_bl) r.setupCategoriesButton();
            if (r.showPlayListButtonAndPlaylist_bl) r.setupPlaylistButton();
            if (r.showLoopButton_bl) r.setupLoopButton();
            if (r.showShuffleButton_bl) r.setupShuffleButton();
            if (r.showDownloadMp3Button_bl) r.setupDownloadButton();
            if (!r.isMobile_bl) r.setupDisable();
            r.mainHolder_do.setBkColor("#FFFF00");
            r.mainHolder_do.setY(-500);
            var e;
            for (var t = 0; t < r.buttons_ar.length; t++) {
                e = r.buttons_ar[t];
                r.totalButtonsWidth += e.w;
                if (e.h > r.largerButtonHeight) r.largerButtonHeight = e.h
            }
            r.totalButtonsWidth += r.volumeButton_do.w;
            r.totalButtonsWidth += r.startSpaceBetweenButtons * 2
        };
        r.resizeAndPosition = function() {
            if (n.stageWidth == r.stageWidth && n.stageHeight == r.stageHeight) return;
            r.stageWidth = n.stageWidth;
            r.positionButtons()
        };
        this.show = function() {
            r.mainHolder_do.setY(0)
        };
        r.positionButtons = function() {
            var e;
            var i;
            var s = 0;
            var o = 0;
            var u = r.buttons_ar.length;
            if (r.showDownloadMp3Button_bl && t.playlist_ar[n.id]) {
                if (t.playlist_ar[n.id].downloadable && n.isPlaylistLoaded_bl) {
                    if (MUSICUtils.indexOfArray(r.buttons_ar, r.downloadButton_do) == -1) {
                        if (r.showBuyButton_bl && t.playlist_ar[n.id].buy) {
                            r.buttons_ar.splice(MUSICUtils.indexOfArray(r.buttons_ar, r.buyButton_do), 0, r.downloadButton_do)
                        } else {
                            r.buttons_ar.splice(r.buttons_ar.length, 0, r.downloadButton_do)
                        }
                        r.downloadButton_do.setVisible(true)
                    }
                } else {
                    var f = MUSICUtils.indexOfArray(r.buttons_ar, r.downloadButton_do);
                    if (f != -1) {
                        r.buttons_ar.splice(f, 1);
                        r.downloadButton_do.setVisible(false)
                    }
                }
            }
            u = r.buttons_ar.length;
            if (!t.playlist_ar) {
                r.showThumbnail_bl = true
            } else {
                if (t.playlist_ar[n.id] == undefined) {
                    r.showThumbnail_bl = false
                } else {
                    r.showThumbnail_bl = Boolean(t.playlist_ar[n.id].thumbPath)
                }
            }
            if (!t.showThumbnail_bl) r.showThumbnail_bl = false;
            if (r.showThumbnail_bl) {
                s += r.thumbWidthAndHeight;
                r.thumb_do.setX(0)
            } else {
                r.thumb_do.setX(-300)
            }
            for (var l = 0; l < u; l++) {
                e = r.buttons_ar[l];
                s += e.w + r.spaceBetweenButtons
            }
            if (u > 3) {
                var c = 0;
                for (var l = 0; l < u; l++) {
                    e = r.buttons_ar[l];
                    if (l > 2) {
                        if (l == 3) {
                            c += e.w
                        } else {
                            c += r.buttons_ar[l].w + r.spaceBetweenButtons
                        }
                    }
                }
                if (c < r.minVolumeBarWidth) {
                    for (var l = 0; l < u; l++) {
                        e = r.buttons_ar[l];
                        if (l > 2) {
                            s -= e.w + r.spaceBetweenButtons
                        }
                    }
                    r.totalVolumeBarWidth = r.minVolumeBarWidth + r.volumeButton_do.w + r.spaceBetweenVolumeButtonAndScrubber;
                    r.volumeScrubberWidth = r.minVolumeBarWidth - r.startSpaceBetweenButtons + r.volumeScrubberOffestWidth;
                    s += r.totalVolumeBarWidth;
                    s += r.separatorOffsetOutSpace * 2 + r.separatorOffsetInSpace * 2;
                    s += r.startSpaceBetweenButtons;
                    s += r.firstSeparator_do.w + r.secondSeparator_do.w;
                    r.mainVolumeHolder_do.setY(r.volumeButtonAndScrubberOffsetTop)
                } else {
                    s -= r.spaceBetweenButtons * 2;
                    s += r.separatorOffsetOutSpace * 2 + r.separatorOffsetInSpace * 2;
                    s += r.startSpaceBetweenButtons * 2;
                    s += r.firstSeparator_do.w + r.secondSeparator_do.w;
                    c = 0;
                    for (var l = 0; l < u; l++) {
                        e = r.buttons_ar[l];
                        if (l > 2) {
                            if (l == 3) {
                                c += e.w
                            } else {
                                c += r.buttons_ar[l].w + r.spaceBetweenButtons
                            }
                        }
                    }
                    c -= 7;
                    r.totalVolumeBarWidth = c + r.volumeButton_do.w + r.spaceBetweenVolumeButtonAndScrubber;
                    r.volumeScrubberWidth = c - r.volumeButton_do.w - r.spaceBetweenVolumeButtonAndScrubber + r.volumeScrubberOffestWidth;
                    r.mainVolumeHolder_do.setY(r.volumeButtonAndScrubberOffsetTop)
                }
            } else {
                r.totalVolumeBarWidth = r.minVolumeBarWidth + r.volumeButton_do.w + r.spaceBetweenVolumeButtonAndScrubber;
                r.volumeScrubberWidth = r.minVolumeBarWidth - r.startSpaceBetweenButtons + r.volumeScrubberOffestWidth;
                s += r.totalVolumeBarWidth;
                s += r.separatorOffsetOutSpace * 2 + r.separatorOffsetInSpace * 2;
                s += r.startSpaceBetweenButtons;
                s += r.firstSeparator_do.w + r.secondSeparator_do.w;
                r.mainVolumeHolder_do.setY(parseInt((r.stageHeight - r.mainVolumeHolder_do.h) / 2))
            }
            s = r.stageWidth - s;
            if (s > r.minLeftWidth) {
                r.stageHeight = r.controllerHeight;
                r.secondSeparator_do.setX(r.firstSeparator_do.x + r.firstSeparator_do.w + r.separatorOffsetInSpace + s + r.separatorOffsetInSpace);
                for (var l = 0; l < u; l++) {
                    e = r.buttons_ar[l];
                    if (l == 0) {
                        i = r.thumb_do;
                        if (r.showThumbnail_bl) {
                            e.setX(i.x + i.w + r.startSpaceBetweenButtons)
                        } else {
                            e.setX(r.startSpaceBetweenButtons)
                        }
                        e.setY(parseInt((r.stageHeight - e.h) / 2))
                    } else if (l == 1) {
                        i = r.buttons_ar[l - 1];
                        e.setX(i.x + i.w + r.spaceBetweenButtons);
                        e.setY(parseInt((r.stageHeight - e.h) / 2))
                    } else if (l == 2) {
                        i = r.buttons_ar[l - 1];
                        e.setX(i.x + i.w + r.spaceBetweenButtons);
                        r.firstSeparator_do.setX(e.x + e.w + r.separatorOffsetOutSpace);
                        e.setY(parseInt((r.stageHeight - e.h) / 2))
                    } else if (l == 3) {
                        r.secondSeparator_do.setX(r.firstSeparator_do.x + r.firstSeparator_do.w + r.separatorOffsetInSpace + s + r.separatorOffsetInSpace);
                        i = r.buttons_ar[l - 1];
                        e.setX(r.secondSeparator_do.x + r.secondSeparator_do.w + r.separatorOffsetOutSpace);
                        e.setY(r.lastButtonsOffsetTop)
                    } else {
                        i = r.buttons_ar[l - 1];
                        e.setX(i.x + i.w + r.spaceBetweenButtons);
                        e.setY(r.lastButtonsOffsetTop)
                    }
                }
                r.mainTitlebar_do.setWidth(s);
                r.mainTitlebar_do.setX(r.firstSeparator_do.x + r.firstSeparator_do.w + r.separatorOffsetInSpace);
                r.titlebarGradRight_do.setX(r.mainTitlebar_do.w - r.titlebarGradRight_do.w);
                r.titleBarRight_do.setX(r.mainTitlebar_do.w - r.titleBarRight_do.w);
                r.mainTitlebar_do.setY(r.titleBarOffsetTop);
                if (!r.totalTime_do.w && MUSICUtils.isIEAndLessThen9) return;
                r.currentTime_do.setX(r.firstSeparator_do.x + r.firstSeparator_do.w + r.separatorOffsetInSpace);
                r.totalTime_do.setX(r.firstSeparator_do.x + r.firstSeparator_do.w + r.separatorOffsetInSpace + s - r.totalTime_do.w);
                r.currentTime_do.setY(r.mainScrubberOffsetTop + parseInt((r.mainScrubber_do.h - r.currentTime_do.h) / 2));
                r.totalTime_do.setY(r.mainScrubberOffsetTop + parseInt((r.mainScrubber_do.h - r.totalTime_do.h) / 2));
                r.mainScrubberWidth = s + r.scrubbersOffestTotalWidth - r.currentTime_do.w - r.totalTime_do.w - r.spaceBetweenMainScrubberAndTime * 2;
                r.mainScrubber_do.setWidth(r.mainScrubberWidth);
                r.mainScrubberBkMiddle_do.setWidth(r.mainScrubberWidth - r.scrubbersBkLeftAndRightWidth * 2);
                r.mainScrubberBkRight_do.setX(r.mainScrubberWidth - r.scrubbersBkLeftAndRightWidth);
                r.mainScrubber_do.setX(r.firstSeparator_do.x + r.firstSeparator_do.w + r.separatorOffsetInSpace - parseInt(r.scrubbersOffestTotalWidth / 2) + r.currentTime_do.w + r.spaceBetweenMainScrubberAndTime);
                r.mainScrubber_do.setY(r.mainScrubberOffsetTop);
                r.mainScrubberDragMiddle_do.setWidth(r.mainScrubberWidth - r.scrubbersBkLeftAndRightWidth - r.scrubbersOffsetWidth);
                r.progressMiddle_do.setWidth(r.mainScrubberWidth - r.scrubbersBkLeftAndRightWidth - r.scrubbersOffsetWidth);
                r.updateMainScrubber(r.percentPlayed);
                r.mainVolumeHolder_do.setX(r.secondSeparator_do.x + r.secondSeparator_do.w + r.separatorOffsetOutSpace);
                r.mainVolumeHolder_do.setWidth(r.totalVolumeBarWidth + r.scrubbersOffestTotalWidth);
                r.volumeScrubber_do.setX(r.volumeButton_do.x + r.volumeButton_do.w + r.spaceBetweenVolumeButtonAndScrubber - parseInt(r.scrubbersOffestTotalWidth / 2));
                r.volumeScrubber_do.setWidth(r.volumeScrubberWidth);
                r.volumeScrubberBkRight_do.setX(r.volumeScrubberWidth - r.scrubbersBkLeftAndRightWidth);
                r.volumeScrubberBkMiddle_do.setWidth(r.volumeScrubberWidth - r.scrubbersBkLeftAndRightWidth * 2);
                r.volumeScrubberDragMiddle_do.setWidth(r.volumeScrubberWidth - r.scrubbersBkLeftAndRightWidth);
                r.updateVolume(r.volume);
                r.setHeight(r.controllerHeight)
            } else {
                r.thumb_do.setX(-300);
                r.firstSeparator_do.setX(-300);
                r.secondSeparator_do.setX(-300);
                r.mainTitlebar_do.setWidth(r.stageWidth);
                r.mainTitlebar_do.setX(0);
                r.mainTitlebar_do.setY(0);
                r.titlebarGradRight_do.setX(r.mainTitlebar_do.w - r.titlebarGradRight_do.w);
                r.titleBarRight_do.setX(r.mainTitlebar_do.w - r.titleBarRight_do.w);
                var h = 0;
                var s;
                var p = r.totalButtonsWidth;
                if (r.downloadButton_do && MUSICUtils.indexOfArray(r.buttons_ar, r.downloadButton_do) == -1) {
                    p -= r.downloadButton_do.w
                }
                o = parseInt((r.stageWidth - p) / u);
                for (var l = 0; l < u; l++) {
                    e = r.buttons_ar[l];
                    h += e.w + o
                }
                h += r.volumeButton_do.w;
                s = parseInt((r.stageWidth - h) / 2) - r.startSpaceBetweenButtons;
                for (var l = 0; l < u; l++) {
                    e = r.buttons_ar[l];
                    e.setY(r.titleBarGradLeft_do.h + r.allButtonsOffsetTopAndBottom + parseInt((r.largerButtonHeight - e.h) / 2));
                    if (l == 0) {
                        e.setX(s + r.startSpaceBetweenButtons)
                    } else {
                        i = r.buttons_ar[l - 1];
                        e.setX(Math.round(i.x + i.w + o))
                    }
                }
                r.mainVolumeHolder_do.setX(e.x + e.w + o);
                r.mainVolumeHolder_do.setY(r.titleBarGradLeft_do.h + r.allButtonsOffsetTopAndBottom + parseInt((r.largerButtonHeight - r.volumeButton_do.h) / 2));
                if (!r.totalTime_do.w && MUSICUtils.isIEAndLessThen9) return;
                r.currentTime_do.setX(r.startTimeSpace);
                r.currentTime_do.setY(r.playPauseButton_do.y + r.playPauseButton_do.h + r.allButtonsOffsetTopAndBottom);
                r.totalTime_do.setX(r.stageWidth - r.startTimeSpace - r.totalTime_do.w);
                r.totalTime_do.setY(r.playPauseButton_do.y + r.playPauseButton_do.h + r.allButtonsOffsetTopAndBottom);
                r.mainScrubber_do.setX(r.currentTime_do.x + r.currentTime_do.w + r.spaceBetweenMainScrubberAndTime - parseInt(r.scrubbersOffestTotalWidth / 2));
                r.mainScrubber_do.setY(r.currentTime_do.y + parseInt((r.currentTime_do.h - r.mainScrubber_do.h) / 2) - 1);
                r.mainScrubberWidth = r.stageWidth + r.scrubbersOffestTotalWidth - r.currentTime_do.w - r.totalTime_do.w - r.spaceBetweenMainScrubberAndTime * 2 - r.startTimeSpace * 2;
                r.mainScrubber_do.setWidth(r.mainScrubberWidth);
                r.mainScrubberBkMiddle_do.setWidth(r.mainScrubberWidth - r.scrubbersBkLeftAndRightWidth * 2);
                r.mainScrubberBkRight_do.setX(r.mainScrubberWidth - r.scrubbersBkLeftAndRightWidth);
                r.mainScrubberDragMiddle_do.setWidth(r.mainScrubberWidth - r.scrubbersBkLeftAndRightWidth - r.scrubbersOffsetWidth);
                r.progressMiddle_do.setWidth(r.mainScrubberWidth - r.scrubbersBkLeftAndRightWidth - r.scrubbersOffsetWidth);
                r.updateMainScrubber(r.percentPlayed);
                r.totalVolumeBarWidth = r.volumeButton_do.w;
                r.mainVolumeHolder_do.setWidth(r.totalVolumeBarWidth);
                r.updateVolume(r.volume);
                r.stageHeight = r.mainTitlebar_do.h + r.largerButtonHeight + r.allButtonsOffsetTopAndBottom * 2 + r.mainScrubber_do.h + r.scrubberOffsetBottom
            }
            r.startToCheckIfAnimTitle();
            if (r.bk_do) {
                r.bk_do.setWidth(r.stageWidth);
                r.bk_do.setHeight(r.stageHeight)
            }
            r.setWidth(r.stageWidth);
            r.setHeight(r.stageHeight);
            r.mainHolder_do.setWidth(r.stageWidth);
            r.mainHolder_do.setHeight(r.stageHeight)
        };
        this.setupThumb = function() {
            r.thumb_do = new MUSICDisplayObject("div");
            r.thumb_do.getStyle().background = "url('" + r.thumbnailBkPath_str + "')";
            r.thumb_do.setWidth(r.thumbWidthAndHeight);
            r.thumb_do.setHeight(r.thumbWidthAndHeight);
            r.mainHolder_do.addChild(r.thumb_do)
        };
        this.loadThumb = function(e) {
            r.positionButtons();
            if (!t.showThumbnail_bl) return;
            if (!e) {
                r.cleanThumbnails(true);
                r.thumbPath_str = "none";
                return
            }
            if (r.thumbPath_str == e) return;
            r.thumbPath_str = e;
            if (r.thumb_img) {
                r.thumb_img.onload = null;
                r.thumb_img.onerror = null;
                r.thumb_img = null
            }
            if (!r.thumbPath_str) return;
            r.thumb_img = new Image;
            r.thumb_img.onload = r.thumbImageLoadComplete;
            r.thumb_img.onerror = r.thumbImageLoadError;
            r.thumb_img.src = r.thumbPath_str
        };
        this.thumbImageLoadError = function() {
            r.cleanThumbnails(true)
        };
        this.thumbImageLoadComplete = function() {
            var e = new MUSICDisplayObject("img");
            e.setScreen(r.thumb_img);
            var t = r.thumb_img.width;
            var n = r.thumb_img.height;
            var i = r.thumbWidthAndHeight / t;
            var s = r.thumbWidthAndHeight / n;
            var o = 0;
            if (i <= s) {
                o = i
            } else if (i >= s) {
                o = s
            }
            e.setWidth(parseInt(t * o));
            e.setHeight(parseInt(n * o));
            e.setX(parseInt((r.thumbWidthAndHeight - t * o) / 2));
            e.setY(parseInt((r.thumbWidthAndHeight - n * o) / 2));
            e.setAlpha(0);
            for (var u = 0; u < r.thumb_do.getNumChildren(); u++) {
                child = r.thumb_do.getChildAt(u);
                MUSICTweenMax.killTweensOf(child)
            }
            MUSICTweenMax.to(e, .8, {
                alpha: 1,
                alpha: 1,
                delay: .2,
                ease: Expo.easeOut,
                onComplete: r.cleanThumbnails
            });
            r.thumb_do.addChild(e)
        };
        this.cleanThumbnails = function(e) {
            var t;
            var n = e ? 0 : 1;
            while (r.thumb_do.getNumChildren() > n) {
                t = r.thumb_do.getChildAt(0);
                MUSICTweenMax.killTweensOf(t);
                r.thumb_do.removeChild(t);
                t.destroy()
            }
        };
        this.setupDisable = function() {
            r.disable_do = new MUSICDisplayObject("div");
            if (MUSICUtils.isIE) {
                r.disable_do.setBkColor("#FFFFFF");
                r.disable_do.setAlpha(0)
            }
        };
        this.setupPrevButton = function() {
            MUSICSimpleButton.setPrototype();
            r.prevButton_do = new MUSICSimpleButton(r.prevN_img, t.prevSPath_str);
            r.prevButton_do.addListener(MUSICSimpleButton.MOUSE_UP, r.prevButtonOnMouseUpHandler);
            r.buttons_ar.push(r.prevButton_do);
            r.mainHolder_do.addChild(r.prevButton_do)
        };
        this.prevButtonOnMouseUpHandler = function() {
            r.dispatchEvent(e.PLAY_PREV)
        };
        this.setupPlayPauseButton = function() {
            MUSICComplexButton.setPrototype();
            r.playPauseButton_do = new MUSICComplexButton(r.playN_img, t.playSPath_str, r.pauseN_img, t.pauseSPath_str, true);
            r.buttons_ar.push(r.playPauseButton_do);
            r.playPauseButton_do.addListener(MUSICComplexButton.MOUSE_UP, r.playButtonMouseUpHandler);
            r.mainHolder_do.addChild(r.playPauseButton_do)
        };
        this.showPlayButton = function() {
            if (!r.playPauseButton_do) return;
            r.playPauseButton_do.setButtonState(1)
        };
        this.showPauseButton = function() {
            if (!r.playPauseButton_do) return;
            r.playPauseButton_do.setButtonState(0)
        };
        this.playButtonMouseUpHandler = function() {
            if (r.playPauseButton_do.currentState == 0) {
                r.dispatchEvent(e.PAUSE)
            } else {
                r.dispatchEvent(e.PLAY)
            }
        };
        this.setupNextButton = function() {
            MUSICSimpleButton.setPrototype();
            r.nextButton_do = new MUSICSimpleButton(r.nextN_img, t.nextSPath_str);
            r.nextButton_do.addListener(MUSICSimpleButton.MOUSE_UP, r.nextButtonOnMouseUpHandler);
            r.nextButton_do.setY(parseInt((r.stageHeight - r.nextButton_do.h) / 2));
            r.buttons_ar.push(r.nextButton_do);
            r.mainHolder_do.addChild(r.nextButton_do)
        };
        this.nextButtonOnMouseUpHandler = function() {
            r.dispatchEvent(e.PLAY_NEXT)
        };
        this.setupSeparators = function() {
            r.firstSeparator_do = new MUSICDisplayObject("img");
            r.firstSeparator_do.setScreen(r.separator1_img);
            r.secondSeparator_do = new MUSICDisplayObject("img");
            r.secondSeparator_do.setScreen(r.separator2_img);
            r.firstSeparator_do.setX(-10);
            r.secondSeparator_do.setX(-10);
            r.firstSeparator_do.setY(parseInt((r.stageHeight - r.firstSeparator_do.h) / 2));
            r.secondSeparator_do.setY(parseInt((r.stageHeight - r.secondSeparator_do.h) / 2));
            r.mainHolder_do.addChild(r.firstSeparator_do);
            r.mainHolder_do.addChild(r.secondSeparator_do)
        };
        this.setupTitlebar = function() {
            r.mainTitlebar_do = new MUSICDisplayObject("div");
            r.mainTitlebar_do.getStyle().background = "url('" + r.titlebarBkMiddlePattern_str + "')";
            r.mainTitlebar_do.setHeight(r.titlebarHeight);
            r.titleBarLeft_do = new MUSICDisplayObject("img");
            r.titleBarLeft_do.setScreen(r.titleBarLeft_img);
            r.titleBarRight_do = new MUSICDisplayObject("img");
            r.titleBarRight_do.setScreen(r.titleBarRigth_img);
            r.simpleText_do = new MUSICDisplayObject("div");
            r.simpleText_do.setOverflow("visible");
            r.simpleText_do.hasTransform3d_bl = false;
            r.simpleText_do.hasTransform2d_bl = false;
            r.simpleText_do.setBackfaceVisibility();
            r.simpleText_do.getStyle().fontFamily = "Arial";
            r.simpleText_do.getStyle().fontSize = "12px";
            r.simpleText_do.getStyle().whiteSpace = "nowrap";
            r.simpleText_do.getStyle().textAlign = "left";
            r.simpleText_do.getStyle().color = r.titleColor_str;
            r.simpleText_do.getStyle().fontSmoothing = "antialiased";
            r.simpleText_do.getStyle().webkitFontSmoothing = "antialiased";
            r.simpleText_do.getStyle().textRendering = "optimizeLegibility";
            r.animText1_do = new MUSICDisplayObject("div");
            r.animText1_do.setOverflow("visible");
            r.animText1_do.hasTransform3d_bl = false;
            r.animText1_do.hasTransform2d_bl = false;
            r.animText1_do.setBackfaceVisibility();
            r.animText1_do.getStyle().fontFamily = "Arial";
            r.animText1_do.getStyle().fontSize = "12px";
            r.animText1_do.getStyle().whiteSpace = "nowrap";
            r.animText1_do.getStyle().textAlign = "left";
            r.animText1_do.getStyle().color = r.titleColor_str;
            r.animText1_do.getStyle().fontSmoothing = "antialiased";
            r.animText1_do.getStyle().webkitFontSmoothing = "antialiased";
            r.animText1_do.getStyle().textRendering = "optimizeLegibility";
            r.animText2_do = new MUSICDisplayObject("div");
            r.animText2_do.setOverflow("visible");
            r.animText2_do.hasTransform3d_bl = false;
            r.animText2_do.hasTransform2d_bl = false;
            r.animText2_do.setBackfaceVisibility();
            r.animText2_do.getStyle().fontFamily = "Arial";
            r.animText2_do.getStyle().fontSize = "12px";
            r.animText2_do.getStyle().whiteSpace = "nowrap";
            r.animText2_do.getStyle().textAlign = "left";
            r.animText2_do.getStyle().color = r.titleColor_str;
            r.animText2_do.getStyle().fontSmoothing = "antialiased";
            r.animText2_do.getStyle().webkitFontSmoothing = "antialiased";
            r.animText2_do.getStyle().textRendering = "optimizeLegibility";
            r.titleBarGradLeft_do = new MUSICDisplayObject("img");
            r.titleBarGradLeft_do.setScreen(r.titlebarLeftPath_img);
            r.titleBarGradLeft_do.setX(-50);
            r.titlebarGradRight_do = new MUSICDisplayObject("img");
            r.titlebarGradRight_do.setScreen(r.titlebarRightPath_img);
            if (r.showSoundAnimation_bl) {
                r.animationBackground_do = new MUSICDisplayObject("img");
                r.animationBackground_do.setScreen(r.titlebarAnimBkPath_img);
                r.animationHolderWidth = r.animationBackground_do.w;
                r.simpleText_do.setX(r.animationBackground_do.w + 5);
                MUSICPreloader.setPrototype();
                r.animation_do = new MUSICPreloader(t.animationPath_str, 29, 22, 31, 80, true);
                r.animation_do.setX(r.equlizerOffsetLeft);
                r.animation_do.setY(0);
                r.animation_do.show(true);
                r.animation_do.stop()
            } else {
                r.simpleText_do.setX(5)
            }
            setTimeout(function() {
                if (r == null) return;
                r.simpleText_do.setY(parseInt((r.mainTitlebar_do.h - r.simpleText_do.getHeight()) / 2) + 1);
                r.animText1_do.setY(parseInt((r.mainTitlebar_do.h - r.simpleText_do.getHeight()) / 2) + 1);
                r.animText2_do.setY(parseInt((r.mainTitlebar_do.h - r.simpleText_do.getHeight()) / 2) + 1)
            }, 50);
            r.mainTitlebar_do.addChild(r.titleBarLeft_do);
            r.mainTitlebar_do.addChild(r.titleBarRight_do);
            r.mainTitlebar_do.addChild(r.simpleText_do);
            r.mainTitlebar_do.addChild(r.animText1_do);
            r.mainTitlebar_do.addChild(r.animText2_do);
            if (r.showSoundAnimation_bl) {
                r.mainTitlebar_do.addChild(r.animationBackground_do);
                r.mainTitlebar_do.addChild(r.animation_do)
            }
            r.mainTitlebar_do.addChild(r.titleBarGradLeft_do);
            r.mainTitlebar_do.addChild(r.titlebarGradRight_do);
            r.mainHolder_do.addChild(r.mainTitlebar_do)
        };
        this.setTitle = function(e) {
            r.simpleText_do.setInnerHTML(e);
            r.animText1_do.setInnerHTML(e + "***");
            r.animText2_do.setInnerHTML(e + "***");
            r.animText1_do.setX(-1e3);
            r.animText2_do.setX(-1e3);
            r.startToCheckIfAnimTitle(true)
        };
        this.startToCheckIfAnimTitle = function(e) {
            if (e) r.stopToAnimateText();
            clearTimeout(r.animateTextId_to);
            clearTimeout(r.startToAnimateTextId_to);
            r.animateTextId_to = setTimeout(r.checkIfAnimTitle, 10)
        };
        this.checkIfAnimTitle = function() {
            var e = r.mainTitlebar_do.w - 5 - r.titlebarGradRight_do.w;
            e -= r.animationHolderWidth;
            if (r.simpleText_do.getWidth() > e) {
                if (r.isTextAnimating_bl) return;
                if (r.showSoundAnimation_bl) {
                    r.titleBarGradLeft_do.setX(r.animationHolderWidth);
                    r.titlebarGradRight_do.setY(0)
                } else {
                    r.titleBarGradLeft_do.setX(0);
                    r.titlebarGradRight_do.setY(0)
                }
                clearTimeout(r.startToAnimateTextId_to);
                r.startToAnimateTextId_to = setTimeout(r.startToAnimateText, 300)
            } else {
                r.titleBarGradLeft_do.setX(-50);
                r.titlebarGradRight_do.setY(-50);
                r.stopToAnimateText()
            }
        };
        this.startToAnimateText = function() {
            if (r.isTextAnimating_bl) return;
            r.isTextAnimating_bl = true;
            r.animTextWidth = r.animText1_do.getWidth();
            r.simpleText_do.setX(-1e3);
            r.animText1_do.setX(r.animationHolderWidth + 5);
            r.animText2_do.setX(r.animationHolderWidth + r.animTextWidth + 10);
            clearInterval(r.animateTextId_int);
            r.animateTextId_int = setInterval(r.animateText, 40)
        };
        this.stopToAnimateText = function() {
            if (!r.isTextAnimating_bl) return;
            r.isTextAnimating_bl = false;
            r.simpleText_do.setX(r.animationHolderWidth + 5);
            r.animText1_do.setX(-1e3);
            r.animText2_do.setX(-1e3);
            clearInterval(r.animateTextId_int)
        };
        this.animateText = function() {
            r.animText1_do.setX(r.animText1_do.x - 1);
            r.animText2_do.setX(r.animText2_do.x - 1);
            if (r.animText1_do.x < -(r.animTextWidth - r.animationHolderWidth)) r.animText1_do.setX(r.animText2_do.x + r.animTextWidth + 5);
            if (r.animText2_do.x < -(r.animTextWidth - r.animationHolderWidth)) r.animText2_do.setX(r.animText1_do.x + r.animTextWidth + 5)
        };
        this.stopEqulizer = function() {
            if (r.animation_do) r.animation_do.stop()
        };
        this.startEqulizer = function() {
            if (r.animation_do) r.animation_do.start()
        };
        this.setupMainScrubber = function() {
            r.mainScrubber_do = new MUSICDisplayObject("div");
            r.mainScrubber_do.setY(parseInt((r.stageHeight - r.scrubbersHeight) / 2));
            r.mainScrubber_do.setHeight(r.scrubbersHeight);
            r.mainScrubberBkLeft_do = new MUSICDisplayObject("img");
            r.mainScrubberBkLeft_do.setScreen(r.mainScrubberBkLeft_img);
            r.mainScrubberBkRight_do = new MUSICDisplayObject("img");
            r.mainScrubberBkRight_do.setScreen(r.mainScrubberBkRight_img);
            var e = new Image;
            e.src = r.mainScrubberBkMiddlePath_str;
            if (r.isMobile_bl) {
                r.mainScrubberBkMiddle_do = new MUSICDisplayObject("div");
                r.mainScrubberBkMiddle_do.getStyle().background = "url('" + r.mainScrubberBkMiddlePath_str + "')"
            } else {
                r.mainScrubberBkMiddle_do = new MUSICDisplayObject("img");
                r.mainScrubberBkMiddle_do.setScreen(e)
            }
            r.mainScrubberBkMiddle_do.setHeight(r.scrubbersHeight);
            r.mainScrubberBkMiddle_do.setX(r.scrubbersBkLeftAndRightWidth);
            r.mainProgress_do = new MUSICDisplayObject("div");
            r.mainProgress_do.setHeight(r.scrubbersHeight);
            r.progressLeft_do = new MUSICDisplayObject("img");
            r.progressLeft_do.setScreen(r.mainScrubberLeftProgress_img);
            e = new Image;
            e.src = r.progressMiddlePath_str;
            r.progressMiddle_do = new MUSICDisplayObject("div");
            r.progressMiddle_do.getStyle().background = "url('" + r.progressMiddlePath_str + "')";
            r.progressMiddle_do.setHeight(r.scrubbersHeight);
            r.progressMiddle_do.setX(r.mainScrubberDragLeftWidth);
            r.mainScrubberDrag_do = new MUSICDisplayObject("div");
            r.mainScrubberDrag_do.setHeight(r.scrubbersHeight);
            r.mainScrubberDragLeft_do = new MUSICDisplayObject("img");
            r.mainScrubberDragLeft_do.setScreen(r.mainScrubberDragLeft_img);
            e = new Image;
            e.src = r.mainScrubberDragMiddlePath_str;
            r.mainScrubberDragMiddle_do = new MUSICDisplayObject("div");
            r.mainScrubberDragMiddle_do.getStyle().background = "url('" + r.mainScrubberDragMiddlePath_str + "')";
            r.mainScrubberDragMiddle_do.setHeight(r.scrubbersHeight);
            r.mainScrubberDragMiddle_do.setX(r.mainScrubberDragLeftWidth);
            r.mainScrubberBarLine_do = new MUSICDisplayObject("img");
            r.mainScrubberBarLine_do.setScreen(r.mainScrubberLine_img);
            r.mainScrubberBarLine_do.setAlpha(0);
            r.mainScrubberBarLine_do.hasTransform3d_bl = false;
            r.mainScrubberBarLine_do.hasTransform2d_bl = false;
            r.mainScrubber_do.addChild(r.mainScrubberBkLeft_do);
            r.mainScrubber_do.addChild(r.mainScrubberBkMiddle_do);
            r.mainScrubber_do.addChild(r.mainScrubberBkRight_do);
            r.mainScrubberDrag_do.addChild(r.mainScrubberDragLeft_do);
            r.mainScrubberDrag_do.addChild(r.mainScrubberDragMiddle_do);
            r.mainProgress_do.addChild(r.progressLeft_do);
            r.mainProgress_do.addChild(r.progressMiddle_do);
            r.mainScrubber_do.addChild(r.mainProgress_do);
            r.mainScrubber_do.addChild(r.mainScrubberDrag_do);
            r.mainScrubber_do.addChild(r.mainScrubberBarLine_do);
            r.mainHolder_do.addChild(r.mainScrubber_do);
            if (r.isMobile_bl) {
                if (r.hasPointerEvent_bl) {
                    r.mainScrubber_do.screen.addEventListener("MSPointerOver", r.mainScrubberOnOverHandler);
                    r.mainScrubber_do.screen.addEventListener("MSPointerOut", r.mainScrubberOnOutHandler);
                    r.mainScrubber_do.screen.addEventListener("MSPointerDown", r.mainScrubberOnDownHandler)
                } else {
                    r.mainScrubber_do.screen.addEventListener("touchstart", r.mainScrubberOnDownHandler)
                }
            } else if (r.screen.addEventListener) {
                r.mainScrubber_do.screen.addEventListener("mouseover", r.mainScrubberOnOverHandler);
                r.mainScrubber_do.screen.addEventListener("mouseout", r.mainScrubberOnOutHandler);
                r.mainScrubber_do.screen.addEventListener("mousedown", r.mainScrubberOnDownHandler)
            } else if (r.screen.attachEvent) {
                r.mainScrubber_do.screen.attachEvent("onmouseover", r.mainScrubberOnOverHandler);
                r.mainScrubber_do.screen.attachEvent("onmouseout", r.mainScrubberOnOutHandler);
                r.mainScrubber_do.screen.attachEvent("onmousedown", r.mainScrubberOnDownHandler)
            }
            r.disableMainScrubber()
        };
        this.mainScrubberOnOverHandler = function(e) {
            if (r.isMainScrubberDisabled_bl) return
        };
        this.mainScrubberOnOutHandler = function(e) {
            if (r.isMainScrubberDisabled_bl) return
        };
        this.mainScrubberOnDownHandler = function(t) {
            if (r.isMainScrubberDisabled_bl) return;
            if (t.preventDefault) t.preventDefault();
            r.isMainScrubberScrubbing_bl = true;
            var n = MUSICUtils.getViewportMouseCoordinates(t);
            var i = n.screenX - r.mainScrubber_do.getGlobalX();
            if (i < 0) {
                i = 0
            } else if (i > r.mainScrubberWidth - r.scrubbersOffsetWidth) {
                i = r.mainScrubberWidth - r.scrubbersOffsetWidth
            }
            var s = i / r.mainScrubberWidth;
            if (!MUSIC.hasHTML5Audio && i >= r.mainProgress_do.w) i = r.mainProgress_do.w;
            var o = i / r.mainScrubberWidth;
            if (r.disable_do) r.addChild(r.disable_do);
            r.updateMainScrubber(s);
            r.dispatchEvent(e.START_TO_SCRUB);
            r.dispatchEvent(e.SCRUB_PLAYLIST_ITEM, {
                percent: o
            });
            r.dispatchEvent(e.SCRUB, {
                percent: s
            });
            if (r.isMobile_bl) {
                if (r.hasPointerEvent_bl) {
                    window.addEventListener("MSPointerMove", r.mainScrubberMoveHandler);
                    window.addEventListener("MSPointerUp", r.mainScrubberEndHandler)
                } else {
                    window.addEventListener("touchmove", r.mainScrubberMoveHandler);
                    window.addEventListener("touchend", r.mainScrubberEndHandler)
                }
            } else {
                if (window.addEventListener) {
                    window.addEventListener("mousemove", r.mainScrubberMoveHandler);
                    window.addEventListener("mouseup", r.mainScrubberEndHandler)
                } else if (document.attachEvent) {
                    document.attachEvent("onmousemove", r.mainScrubberMoveHandler);
                    document.attachEvent("onmouseup", r.mainScrubberEndHandler)
                }
            }
        };
        this.mainScrubberMoveHandler = function(t) {
            if (t.preventDefault) t.preventDefault();
            var n = MUSICUtils.getViewportMouseCoordinates(t);
            var i = n.screenX - r.mainScrubber_do.getGlobalX();
            if (i < 0) {
                i = 0
            } else if (i > r.mainScrubberWidth - r.scrubbersOffsetWidth) {
                i = r.mainScrubberWidth - r.scrubbersOffsetWidth
            }
            var s = i / r.mainScrubberWidth;
            if (!MUSIC.hasHTML5Audio && i >= r.mainProgress_do.w) i = r.mainProgress_do.w;
            var o = i / r.mainScrubberWidth;
            r.updateMainScrubber(s);
            r.dispatchEvent(e.SCRUB_PLAYLIST_ITEM, {
                percent: o
            });
            r.dispatchEvent(e.SCRUB, {
                percent: s
            })
        };
        this.mainScrubberEndHandler = function(t) {
            if (r.disable_do) {
                if (r.contains(r.disable_do)) r.removeChild(r.disable_do)
            }
            r.dispatchEvent(e.STOP_TO_SCRUB);
            if (r.isMobile_bl) {
                if (r.hasPointerEvent_bl) {
                    window.removeEventListener("MSPointerMove", r.mainScrubberMoveHandler);
                    window.removeEventListener("MSPointerUp", r.mainScrubberEndHandler)
                } else {
                    window.removeEventListener("touchmove", r.mainScrubberMoveHandler);
                    window.removeEventListener("touchend", r.mainScrubberEndHandler)
                }
            } else {
                if (window.removeEventListener) {
                    window.removeEventListener("mousemove", r.mainScrubberMoveHandler);
                    window.removeEventListener("mouseup", r.mainScrubberEndHandler)
                } else if (document.detachEvent) {
                    document.detachEvent("onmousemove", r.mainScrubberMoveHandler);
                    document.detachEvent("onmouseup", r.mainScrubberEndHandler)
                }
            }
        };
        this.disableMainScrubber = function() {
            if (!r.mainScrubber_do) return;
            r.isMainScrubberDisabled_bl = true;
            r.mainScrubber_do.setButtonMode(false);
            r.updateMainScrubber(0);
            r.updatePreloaderBar(0);
            r.mainScrubberEndHandler()
        };
        this.enableMainScrubber = function() {
            if (!r.mainScrubber_do) return;
            r.isMainScrubberDisabled_bl = false;
            r.mainScrubber_do.setButtonMode(true)
        };
        this.updateMainScrubber = function(e) {
            if (!r.mainScrubber_do || isNaN(e)) return;
            var t = parseInt(e * r.mainScrubberWidth);
            r.percentPlayed = e;
            if (!MUSIC.hasHTML5Audio && t >= r.mainProgress_do.w) t = r.mainProgress_do.w;
            if (t < 1 && r.isMainScrubberLineVisible_bl) {
                r.isMainScrubberLineVisible_bl = false;
                MUSICTweenMax.to(r.mainScrubberBarLine_do, .5, {
                    alpha: 0
                })
            } else if (t > 2 && !r.isMainScrubberLineVisible_bl) {
                r.isMainScrubberLineVisible_bl = true;
                MUSICTweenMax.to(r.mainScrubberBarLine_do, .5, {
                    alpha: 1
                })
            }
            r.mainScrubberDrag_do.setWidth(t);
            if (t > r.mainScrubberWidth - r.scrubbersOffsetWidth) t = r.mainScrubberWidth - r.scrubbersOffsetWidth;
            MUSICTweenMax.to(r.mainScrubberBarLine_do, .8, {
                x: t,
                ease: Expo.easeOut
            })
        };
        this.updatePreloaderBar = function(e) {
            if (!r.mainProgress_do) return;
            var t = parseInt(e * r.mainScrubberWidth);
            if (e == 1) {
                r.mainProgress_do.setY(-30)
            } else if (r.mainProgress_do.y != 0 && e != 1) {
                r.mainProgress_do.setY(0)
            }
            if (t > r.mainScrubberWidth - r.scrubbersOffsetWidth) t = r.mainScrubberWidth - r.scrubbersOffsetWidth;
            if (t < 0) t = 0;
            r.mainProgress_do.setWidth(t)
        };
        this.setupTime = function() {
            r.currentTime_do = new MUSICDisplayObject("div");
            r.currentTime_do.hasTransform3d_bl = false;
            r.currentTime_do.hasTransform2d_bl = false;
            r.currentTime_do.getStyle().fontFamily = "Arial";
            r.currentTime_do.getStyle().fontSize = "12px";
            r.currentTime_do.getStyle().whiteSpace = "nowrap";
            r.currentTime_do.getStyle().textAlign = "left";
            r.currentTime_do.getStyle().color = r.timeColor_str;
            r.currentTime_do.getStyle().fontSmoothing = "antialiased";
            r.currentTime_do.getStyle().webkitFontSmoothing = "antialiased";
            r.currentTime_do.getStyle().textRendering = "optimizeLegibility";
            r.mainHolder_do.addChild(r.currentTime_do);
            r.totalTime_do = new MUSICDisplayObject("div");
            r.totalTime_do.hasTransform3d_bl = false;
            r.totalTime_do.hasTransform2d_bl = false;
            r.totalTime_do.getStyle().fontFamily = "Arial";
            r.totalTime_do.getStyle().fontSize = "12px";
            r.totalTime_do.getStyle().whiteSpace = "nowrap";
            r.totalTime_do.getStyle().textAlign = "right";
            r.totalTime_do.getStyle().color = r.timeColor_str;
            r.totalTime_do.getStyle().fontSmoothing = "antialiased";
            r.totalTime_do.getStyle().webkitFontSmoothing = "antialiased";
            r.totalTime_do.getStyle().textRendering = "optimizeLegibility";
            r.mainHolder_do.addChild(r.totalTime_do);
            r.updateTime();
            setTimeout(function() {
                if (r == null) return;
                r.timeHeight = r.currentTime_do.getHeight();
                r.currentTime_do.h = r.timeHeight;
                r.totalTime_do.h = r.timeHeight;
                r.stageWidth = n.stageWidth;
                r.positionButtons()
            }, 50)
        };
        this.updateTime = function(e, t) {
            if (!r.currentTime_do || !t) return;
            if (t == "00:00") t = e;
            r.currentTime_do.setInnerHTML(e);
            r.totalTime_do.setInnerHTML(t);
            if (e.length != r.lastTotalTimeLength || t.length != r.lastCurTimeLength) {
                var n = r.currentTime_do.offsetWidth;
                var i = r.totalTime_do.offsetWidth;
                r.currentTime_do.w = n;
                r.totalTime_do.w = i;
                r.positionButtons();
                setTimeout(function() {
                    r.currentTime_do.w = r.currentTime_do.getWidth();
                    r.totalTime_do.w = r.totalTime_do.getWidth();
                    r.positionButtons()
                }, 50);
                r.lastCurTimeLength = e.length;
                r.lastTotalTimeLength = t.length
            }
        };
        this.setupVolumeScrubber = function() {
            r.mainVolumeHolder_do = new MUSICDisplayObject("div");
            r.mainVolumeHolder_do.setHeight(r.volumeN_img.height);
            r.mainHolder_do.addChild(r.mainVolumeHolder_do);
            MUSICSimpleButton.setPrototype();
            r.volumeButton_do = new MUSICSimpleButton(r.volumeN_img, t.volumeSPath_str, t.volumeDPath_str);
            r.volumeButton_do.addListener(MUSICSimpleButton.MOUSE_UP, r.volumeButtonOnMouseUpHandler);
            if (!r.allowToChangeVolume_bl) r.volumeButton_do.disable();
            r.volumeScrubber_do = new MUSICDisplayObject("div");
            r.volumeScrubber_do.setHeight(r.scrubbersHeight);
            r.volumeScrubber_do.setX(r.volumeButton_do.w);
            r.volumeScrubber_do.setY(parseInt((r.volumeButton_do.h - r.scrubbersHeight) / 2));
            r.volumeScrubberBkLeft_do = new MUSICDisplayObject("img");
            var e = new Image;
            e.src = r.mainScrubberBkLeft_do.screen.src;
            r.volumeScrubberBkLeft_do.setScreen(e);
            r.volumeScrubberBkLeft_do.setWidth(r.mainScrubberBkLeft_do.w);
            r.volumeScrubberBkLeft_do.setHeight(r.mainScrubberBkLeft_do.h);
            r.volumeScrubberBkRight_do = new MUSICDisplayObject("img");
            var n = new Image;
            n.src = r.mainScrubberBkRight_do.screen.src;
            r.volumeScrubberBkRight_do.setScreen(n);
            r.volumeScrubberBkRight_do.setWidth(r.mainScrubberBkRight_do.w);
            r.volumeScrubberBkRight_do.setHeight(r.mainScrubberBkRight_do.h);
            var i = new Image;
            i.src = r.volumeScrubberBkMiddlePath_str;
            if (r.isMobile_bl) {
                r.volumeScrubberBkMiddle_do = new MUSICDisplayObject("div");
                r.volumeScrubberBkMiddle_do.getStyle().background = "url('" + r.volumeScrubberBkMiddlePath_str + "')"
            } else {
                r.volumeScrubberBkMiddle_do = new MUSICDisplayObject("img");
                r.volumeScrubberBkMiddle_do.setScreen(i)
            }
            r.volumeScrubberBkMiddle_do.setHeight(r.scrubbersHeight);
            r.volumeScrubberBkMiddle_do.setX(r.scrubbersBkLeftAndRightWidth);
            r.volumeScrubberDrag_do = new MUSICDisplayObject("div");
            r.volumeScrubberDrag_do.setHeight(r.scrubbersHeight);
            r.volumeScrubberDragLeft_do = new MUSICDisplayObject("img");
            var s = new Image;
            s.src = r.mainScrubberDragLeft_img.src;
            r.volumeScrubberDragLeft_do.setScreen(s);
            r.volumeScrubberDragLeft_do.setWidth(r.mainScrubberDragLeft_do.w);
            r.volumeScrubberDragLeft_do.setHeight(r.mainScrubberDragLeft_do.h);
            i = new Image;
            i.src = r.volumeScrubberDragMiddlePath_str;
            if (r.isMobile_bl) {
                r.volumeScrubberDragMiddle_do = new MUSICWDMSPDisplayObject("div");
                r.volumeScrubberDragMiddle_do.getStyle().background = "url('" + r.volumeScrubberDragMiddlePath_str + "')"
            } else {
                r.volumeScrubberDragMiddle_do = new MUSICDisplayObject("img");
                r.volumeScrubberDragMiddle_do.setScreen(i)
            }
            r.volumeScrubberDragMiddle_do.setHeight(r.scrubbersHeight);
            r.volumeScrubberDragMiddle_do.setX(r.mainScrubberDragLeftWidth);
            r.volumeScrubberBarLine_do = new MUSICDisplayObject("img");
            var o = new Image;
            o.src = r.mainScrubberBarLine_do.screen.src;
            r.volumeScrubberBarLine_do.setScreen(o);
            r.volumeScrubberBarLine_do.setWidth(r.mainScrubberBarLine_do.w);
            r.volumeScrubberBarLine_do.setHeight(r.mainScrubberBarLine_do.h);
            r.volumeScrubberBarLine_do.setAlpha(0);
            r.volumeScrubberBarLine_do.hasTransform3d_bl = false;
            r.volumeScrubberBarLine_do.hasTransform2d_bl = false;
            r.volumeScrubber_do.addChild(r.volumeScrubberBkLeft_do);
            r.volumeScrubber_do.addChild(r.volumeScrubberBkMiddle_do);
            r.volumeScrubber_do.addChild(r.volumeScrubberBkRight_do);
            r.volumeScrubber_do.addChild(r.volumeScrubberBarLine_do);
            r.volumeScrubberDrag_do.addChild(r.volumeScrubberDragLeft_do);
            r.volumeScrubberDrag_do.addChild(r.volumeScrubberDragMiddle_do);
            r.volumeScrubber_do.addChild(r.volumeScrubberDrag_do);
            r.volumeScrubber_do.addChild(r.volumeScrubberBarLine_do);
            r.mainVolumeHolder_do.addChild(r.volumeButton_do);
            r.mainVolumeHolder_do.addChild(r.volumeScrubber_do);
            if (r.allowToChangeVolume_bl) {
                if (r.isMobile_bl) {
                    if (r.hasPointerEvent_bl) {
                        r.volumeScrubber_do.screen.addEventListener("MSPointerOver", r.volumeScrubberOnOverHandler);
                        r.volumeScrubber_do.screen.addEventListener("MSPointerOut", r.volumeScrubberOnOutHandler);
                        r.volumeScrubber_do.screen.addEventListener("MSPointerDown", r.volumeScrubberOnDownHandler)
                    } else {
                        r.volumeScrubber_do.screen.addEventListener("touchstart", r.volumeScrubberOnDownHandler)
                    }
                } else if (r.screen.addEventListener) {
                    r.volumeScrubber_do.screen.addEventListener("mouseover", r.volumeScrubberOnOverHandler);
                    r.volumeScrubber_do.screen.addEventListener("mouseout", r.volumeScrubberOnOutHandler);
                    r.volumeScrubber_do.screen.addEventListener("mousedown", r.volumeScrubberOnDownHandler)
                } else if (r.screen.attachEvent) {
                    r.volumeScrubber_do.screen.attachEvent("onmouseover", r.volumeScrubberOnOverHandler);
                    r.volumeScrubber_do.screen.attachEvent("onmouseout", r.volumeScrubberOnOutHandler);
                    r.volumeScrubber_do.screen.attachEvent("onmousedown", r.volumeScrubberOnDownHandler)
                }
            }
            r.enableVolumeScrubber();
            r.updateVolumeScrubber(r.volume)
        };
        this.volumeButtonOnMouseUpHandler = function() {
            var e = r.lastVolume;
            if (r.isMute_bl) {
                e = r.lastVolume;
                r.isMute_bl = false
            } else {
                e = 1e-6;
                r.isMute_bl = true
            }
            r.updateVolume(e)
        };
        this.volumeScrubberOnOverHandler = function(e) {
            if (r.isVolumeScrubberDisabled_bl) return
        };
        this.volumeScrubberOnOutHandler = function(e) {
            if (r.isVolumeScrubberDisabled_bl) return
        };
        this.volumeScrubberOnDownHandler = function(t) {
            if (r.isVolumeScrubberDisabled_bl) return;
            if (t.preventDefault) t.preventDefault();
            var n = MUSICUtils.getViewportMouseCoordinates(t);
            var i = n.screenX - r.volumeScrubber_do.getGlobalX();
            if (i < 0) {
                i = 0
            } else if (i > r.volumeScrubberWidth - r.scrubbersOffsetWidth) {
                i = r.volumeScrubberWidth - r.scrubbersOffsetWidth
            }
            var s = i / r.volumeScrubberWidth;
            if (r.disable_do) r.addChild(r.disable_do);
            r.lastVolume = s;
            r.updateVolume(s);
            r.dispatchEvent(e.VOLUME_START_TO_SCRUB);
            if (r.isMobile_bl) {
                if (r.hasPointerEvent_bl) {
                    window.addEventListener("MSPointerMove", r.volumeScrubberMoveHandler);
                    window.addEventListener("MSPointerUp", r.volumeScrubberEndHandler)
                } else {
                    window.addEventListener("touchmove", r.volumeScrubberMoveHandler);
                    window.addEventListener("touchend", r.volumeScrubberEndHandler)
                }
            } else {
                if (window.addEventListener) {
                    window.addEventListener("mousemove", r.volumeScrubberMoveHandler);
                    window.addEventListener("mouseup", r.volumeScrubberEndHandler)
                } else if (document.attachEvent) {
                    document.attachEvent("onmousemove", r.volumeScrubberMoveHandler);
                    document.attachEvent("onmouseup", r.volumeScrubberEndHandler)
                }
            }
        };
        this.volumeScrubberMoveHandler = function(e) {
            if (r.isVolumeScrubberDisabled_bl) return;
            if (e.preventDefault) e.preventDefault();
            var t =MUSICUtils.getViewportMouseCoordinates(e);
            var n = t.screenX - r.volumeScrubber_do.getGlobalX();
            if (n < 0) {
                n = 0
            } else if (n > r.volumeScrubberWidth - r.scrubbersOffsetWidth) {
                n = r.volumeScrubberWidth - r.scrubbersOffsetWidth
            }
            var i = n / r.volumeScrubberWidth;
            r.lastVolume = i;
            r.updateVolume(i)
        };
        this.volumeScrubberEndHandler = function() {
            r.dispatchEvent(e.VOLUME_STOP_TO_SCRUB);
            if (r.disable_do) {
                if (r.contains(r.disable_do)) r.removeChild(r.disable_do)
            }
            if (r.isMobile_bl) {
                if (r.hasPointerEvent_bl) {
                    window.removeEventListener("MSPointerMove", r.volumeScrubberMoveHandler);
                    window.removeEventListener("MSPointerUp", r.volumeScrubberEndHandler)
                } else {
                    window.removeEventListener("touchmove", r.volumeScrubberMoveHandler);
                    window.removeEventListener("touchend", r.volumeScrubberEndHandler)
                }
            } else {
                if (window.removeEventListener) {
                    window.removeEventListener("mousemove", r.volumeScrubberMoveHandler);
                    window.removeEventListener("mouseup", r.volumeScrubberEndHandler)
                } else if (document.detachEvent) {
                    document.detachEvent("onmousemove", r.volumeScrubberMoveHandler);
                    document.detachEvent("onmouseup", r.volumeScrubberEndHandler)
                }
            }
        };
        this.disableVolumeScrubber = function() {
            r.isVolumeScrubberDisabled_bl = true;
            r.volumeScrubber_do.setButtonMode(false);
            r.volumeScrubberEndHandler()
        };
        this.enableVolumeScrubber = function() {
            r.isVolumeScrubberDisabled_bl = false;
            r.volumeScrubber_do.setButtonMode(true)
        };
        this.updateVolumeScrubber = function(e) {
            var t = parseInt(e * r.volumeScrubberWidth);
            r.volumeScrubberDrag_do.setWidth(t);
            if (t < 1 && r.isVolumeScrubberLineVisible_bl) {
                r.isVolumeScrubberLineVisible_bl = false;
                MUSICTweenMax.to(r.volumeScrubberBarLine_do, .5, {
                    alpha: 0
                })
            } else if (t > 1 && !r.isVolumeScrubberLineVisible_bl) {
                r.isVolumeScrubberLineVisible_bl = true;
                MUSICTweenMax.to(r.volumeScrubberBarLine_do, .5, {
                    alpha: 1
                })
            }
            if (t > r.volumeScrubberWidth - r.scrubbersOffsetWidth) t = r.volumeScrubberWidth - r.scrubbersOffsetWidth;
            MUSICTweenMax.to(r.volumeScrubberBarLine_do, .8, {
                x: t,
                ease: Expo.easeOut
            })
        };
        this.updateVolume = function(t) {
            r.volume = t;
            if (r.volume <= 1e-6) {
                r.isMute_bl = true;
                r.volume = 1e-6
            } else if (r.voume >= 1) {
                r.isMute_bl = false;
                r.volume = 1
            } else {
                r.isMute_bl = false
            }
            if (r.volume == 1e-6) {
                if (r.volumeButton_do) r.volumeButton_do.setDisabledState()
            } else {
                if (r.volumeButton_do) r.volumeButton_do.setEnabledState()
            }
            if (r.volumeScrubberBarLine_do) r.updateVolumeScrubber(r.volume);
            r.dispatchEvent(e.CHANGE_VOLUME, {
                percent: r.volume
            })
        };
        this.setupPlaylistButton = function() {
            MUSICSimpleButton.setPrototype();
            r.playlistButton_do = new MUSICSimpleButton(r.playlistN_img, t.playlistSPath_str, undefined, true);
            r.playlistButton_do.addListener(MUSICSimpleButton.MOUSE_UP, r.playlistButtonOnMouseUpHandler);
            r.playlistButton_do.setY(parseInt((r.stageHeight - r.playlistButton_do.h) / 2));
            r.buttons_ar.push(r.playlistButton_do);
            r.mainHolder_do.addChild(r.playlistButton_do);
            if (r.showPlayListByDefault_bl) {
                r.setPlaylistButtonState("selected")
            }
        };
        this.playlistButtonOnMouseUpHandler = function() {
            if (r.playlistButton_do.isSelectedFinal_bl) {
                r.dispatchEvent(e.HIDE_PLAYLIST)
            } else {
                r.dispatchEvent(e.SHOW_PLAYLIST)
            }
        };
        this.setPlaylistButtonState = function(e) {
            if (!r.playlistButton_do) return;
            if (e == "selected") {
                r.playlistButton_do.setSelected()
            } else if (e == "unselected") {
                r.playlistButton_do.setUnselected()
            }
        };
        this.setupCategoriesButton = function() {
            MUSICSimpleButton.setPrototype();
            r.categoriesButton_do = new MUSICSimpleButton(r.categoriesN_img, t.categoriesSPath_str, undefined, true);
            r.categoriesButton_do.addListener(MUSICSimpleButton.MOUSE_UP, r.categoriesButtonOnMouseUpHandler);
            r.categoriesButton_do.setY(parseInt((r.stageHeight - r.categoriesButton_do.h) / 2));
            r.buttons_ar.push(r.categoriesButton_do);
            r.mainHolder_do.addChild(r.categoriesButton_do)
        };
        this.categoriesButtonOnMouseUpHandler = function() {
            r.dispatchEvent(e.SHOW_CATEGORIES)
        };
        this.setCategoriesButtonState = function(e) {
            if (!r.categoriesButton_do) return;
            if (e == "selected") {
                r.categoriesButton_do.setSelected()
            } else if (e == "unselected") {
                r.categoriesButton_do.setUnselected()
            }
        };
        this.setupLoopButton = function() {
            MUSICSimpleButton.setPrototype();
            r.loopButton_do = new MUSICSimpleButton(r.replayN_img, t.replaySPath_str, undefined, true);
            r.loopButton_do.addListener(MUSICSimpleButton.MOUSE_UP, r.loopButtonOnMouseUpHandler);
            r.loopButton_do.setY(parseInt((r.stageHeight - r.loopButton_do.h) / 2));
            r.buttons_ar.push(r.loopButton_do);
            r.mainHolder_do.addChild(r.loopButton_do);
            if (r.loop_bl) r.setLoopStateButton("selected")
        };
        this.loopButtonOnMouseUpHandler = function() {
            if (r.loopButton_do.isSelectedFinal_bl) {
                r.dispatchEvent(e.DISABLE_LOOP)
            } else {
                r.dispatchEvent(e.ENABLE_LOOP)
            }
        };
        this.setLoopStateButton = function(e) {
            if (!r.loopButton_do) return;
            if (e == "selected") {
                r.loopButton_do.setSelected()
            } else if (e == "unselected") {
                r.loopButton_do.setUnselected()
            }
        };
        this.setupDownloadButton = function() {
            MUSICSimpleButton.setPrototype();
            r.downloadButton_do = new MUSICSimpleButton(r.downloaderN_img, t.downloaderSPath_str);
            r.downloadButton_do.addListener(MUSICSimpleButton.MOUSE_UP, r.downloadButtonOnMouseUpHandler);
            r.downloadButton_do.setY(parseInt((r.stageHeight - r.downloadButton_do.h) / 2));
            r.buttons_ar.push(r.downloadButton_do);
            r.mainHolder_do.addChild(r.downloadButton_do)
        };
        this.downloadButtonOnMouseUpHandler = function() {
            r.dispatchEvent(e.DOWNLOAD_MP3)
        };
        this.setupShuffleButton = function() {
            MUSICSimpleButton.setPrototype();
            r.shuffleButton_do = new MUSICSimpleButton(r.shuffleN_img, t.shuffleSPath_str, undefined, true);
            r.shuffleButton_do.addListener(MUSICSimpleButton.MOUSE_UP, r.shuffleButtonOnMouseUpHandler);
            r.shuffleButton_do.setY(parseInt((r.stageHeight - r.shuffleButton_do.h) / 2));
            r.buttons_ar.push(r.shuffleButton_do);
            r.mainHolder_do.addChild(r.shuffleButton_do);
            if (!r.loop_bl && r.shuffle_bl) r.setShuffleButtonState("selected")
        };
        this.shuffleButtonOnMouseUpHandler = function() {
            if (r.shuffleButton_do.isSelectedFinal_bl) {
                r.dispatchEvent(e.DISABLE_SHUFFLE)
            } else {
                r.dispatchEvent(e.ENABLE_SHUFFLE)
            }
        };
        this.setShuffleButtonState = function(e) {
            if (!r.shuffleButton_do) return;
            if (e == "selected") {
                r.shuffleButton_do.setSelected()
            } else if (e == "unselected") {
                r.shuffleButton_do.setUnselected()
            }
        };
        this.disableControllerWhileLoadingPlaylist = function() {
            r.prevButton_do.disable();
            r.playPauseButton_do.disable();
            r.nextButton_do.disable();
            if (r.downloadButton_do) r.downloadButton_do.disable();
            if (r.playlistButton_do) r.playlistButton_do.disable(true);
            r.updateTime("...", "...");
            r.setTitle("...")
        };
        this.enableControllerWhileLoadingPlaylist = function() {
            r.prevButton_do.enable();
            r.playPauseButton_do.enable();
            r.nextButton_do.enable();
            if (r.downloadButton_do) r.downloadButton_do.enable();
            if (r.playlistButton_do) r.playlistButton_do.enable();
        };
        this.init()
    };
    e.setPrototype = function() {
        e.prototype = new MUSICDisplayObject("div")
    };
    e.PLAY_NEXT = "playNext";
    e.PLAY_PREV = "playPrev";
    e.PLAY = "play";
    e.PAUSE = "pause";
    e.POPUP = "popup";
    e.VOLUME_START_TO_SCRUB = "volumeStartToScrub";
    e.VOLUME_STOP_TO_SCRUB = "volumeStopToScrub";
    e.START_TO_SCRUB = "startToScrub";
    e.SCRUB = "scrub";
    e.SCRUB_PLAYLIST_ITEM = "scrubPlaylistItem";
    e.STOP_TO_SCRUB = "stopToScrub";
    e.CHANGE_VOLUME = "changeVolume";
    e.SHOW_CATEGORIES = "showCategories";
    e.SHOW_PLAYLIST = "showPlaylist";
    e.HIDE_PLAYLIST = "hidePlaylist";
    e.ENABLE_LOOP = "enableLoop";
    e.DISABLE_LOOP = "disableLoop";
    e.ENABLE_SHUFFLE = "enableShuffle";
    e.DISABLE_SHUFFLE = "disableShuffle";
    e.DOWNLOAD_MP3 = "downloadMp3";
    e.BUY = "buy";
    e.prototype = null;
    window.MUSICController = e
})();
(function(e) {
    var t = function(e, t, n, r) {
        var i = this;
        i.listeners = {
            events_ar: []
        };
        if (e == "div" || e == "img" || e == "canvas" || "input") {
            i.type = e
        } else {
            throw Error("Type is not valid! " + e)
        }
        this.children_ar = [];
        this.style;
        this.screen;
        this.transform;
        this.position = t || "absolute";
        this.overflow = n || "hidden";
        this.display = r || "inline-block";
        this.visible = true;
        this.buttonMode;
        this.x = 0;
        this.y = 0;
        this.w = 0;
        this.h = 0;
        this.rect;
        this.alpha = 1;
        this.innerHTML = "";
        this.opacityType = "";
        this.isHtml5_bl = false;
        this.hasTransform3d_bl = MUSICUtils.hasTransform3d;
        this.hasTransform2d_bl = MUSICUtils.hasTransform2d;
        if (MUSICUtils.isIE || MUSICUtils.isIE11 && !MUSICUtils.isMobile) {
            i.hasTransform3d_bl = false;
            i.hasTransform2d_bl = false
        }
        this.hasBeenSetSelectable_bl = false;
        i.init = function() {
            i.setScreen()
        };
        i.getTransform = function() {
            var e = ["transform", "msTransform", "WebkitTransform", "MozTransform", "OTransform"];
            var t;
            while (t = e.shift()) {
                if (typeof i.screen.style[t] !== "undefined") {
                    return t
                }
            }
            return false
        };
        i.getOpacityType = function() {
            var e;
            if (typeof i.screen.style.opacity != "undefined") {
                e = "opacity"
            } else {
                e = "filter"
            }
            return e
        };
        i.setScreen = function(e) {
            if (i.type == "img" && e) {
                i.screen = e;
                i.setMainProperties()
            } else {
                i.screen = document.createElement(i.type);
                i.setMainProperties()
            }
        };
        i.setMainProperties = function() {
            i.transform = i.getTransform();
            i.setPosition(i.position);
            i.setOverflow(i.overflow);
            i.opacityType = i.getOpacityType();
            if (i.opacityType == "opacity") i.isHtml5_bl = true;
            if (i.opacityType == "filter") i.screen.style.filter = "inherit";
            i.screen.style.left = "0px";
            i.screen.style.top = "0px";
            i.screen.style.margin = "0px";
            i.screen.style.padding = "0px";
            i.screen.style.maxWidth = "none";
            i.screen.style.maxHeight = "none";
            i.screen.style.border = "none";
            i.screen.style.lineHeight = "1";
            i.screen.style.backgroundColor = "transparent";
            i.screen.style.backfaceVisibility = "hidden";
            i.screen.style.webkitBackfaceVisibility = "hidden";
            i.screen.style.MozBackfaceVisibility = "hidden";
            i.screen.style.MozImageRendering = "optimizeSpeed";
            i.screen.style.WebkitImageRendering = "optimizeSpeed";
            if (e == "img") {
                i.setWidth(i.screen.width);
                i.setHeight(i.screen.height)
            }
        };
        i.setBackfaceVisibility = function() {
            i.screen.style.backfaceVisibility = "visible";
            i.screen.style.webkitBackfaceVisibility = "visible";
            i.screen.style.MozBackfaceVisibility = "visible"
        };
        i.setSelectable = function(e) {
            if (!e) {
                i.screen.style.userSelect = "none";
                i.screen.style.MozUserSelect = "none";
                i.screen.style.webkitUserSelect = "none";
                i.screen.style.khtmlUserSelect = "none";
                i.screen.style.oUserSelect = "none";
                i.screen.style.msUserSelect = "none";
                i.screen.msUserSelect = "none";
                i.screen.ondragstart = function(e) {
                    return false
                };
                i.screen.onselectstart = function() {
                    return false
                };
                i.screen.ontouchstart = function() {
                    return false
                };
                i.screen.style.webkitTouchCallout = "none";
                i.hasBeenSetSelectable_bl = true
            }
        };
        i.getScreen = function() {
            return i.screen
        };
        i.setVisible = function(e) {
            i.visible = e;
            if (i.visible == true) {
                i.screen.style.visibility = "visible"
            } else {
                i.screen.style.visibility = "hidden"
            }
        };
        i.getVisible = function() {
            return i.visible
        };
        i.setResizableSizeAfterParent = function() {
            i.screen.style.width = "100%";
            i.screen.style.height = "100%"
        };
        i.getStyle = function() {
            return i.screen.style
        };
        i.setOverflow = function(e) {
            i.overflow = e;
            i.screen.style.overflow = i.overflow
        };
        i.setPosition = function(e) {
            i.position = e;
            i.screen.style.position = i.position
        };
        i.setDisplay = function(e) {
            i.display = e;
            i.screen.style.display = i.display
        };
        i.setButtonMode = function(e) {
            i.buttonMode = e;
            if (i.buttonMode == true) {
                i.screen.style.cursor = "pointer"
            } else {
                i.screen.style.cursor = "default"
            }
        };
        i.setBkColor = function(e) {
            i.screen.style.backgroundColor = e
        };
        i.setInnerHTML = function(e) {
            i.innerHTML = e;
            i.screen.innerHTML = i.innerHTML
        };
        i.getInnerHTML = function() {
            return i.innerHTML
        };
        i.getRect = function() {
            return i.screen.getBoundingClientRect()
        };
        i.setAlpha = function(e) {
            i.alpha = e;
            if (i.opacityType == "opacity") {
                i.screen.style.opacity = i.alpha
            } else if (i.opacityType == "filter") {
                i.screen.style.filter = "alpha(opacity=" + i.alpha * 100 + ")";
                i.screen.style.filter = "progid:DXImageTransform.Microsoft.Alpha(Opacity=" + Math.round(i.alpha * 100) + ")"
            }
        };
        i.getAlpha = function() {
            return i.alpha
        };
        i.getRect = function() {
            return i.screen.getBoundingClientRect()
        };
        i.getGlobalX = function() {
            return i.getRect().left
        };
        i.getGlobalY = function() {
            return i.getRect().top
        };
        i.setX = function(e) {
            i.x = e;
            if (i.hasTransform3d_bl) {
                i.screen.style[i.transform] = "translate3d(" + i.x + "px," + i.y + "px,0)"
            } else if (i.hasTransform2d_bl) {
                i.screen.style[i.transform] = "translate(" + i.x + "px," + i.y + "px)"
            } else {
                i.screen.style.left = i.x + "px"
            }
        };
        i.getX = function() {
            return i.x
        };
        i.setY = function(e) {
            i.y = e;
            if (i.hasTransform3d_bl) {
                i.screen.style[i.transform] = "translate3d(" + i.x + "px," + i.y + "px,0)"
            } else if (i.hasTransform2d_bl) {
                i.screen.style[i.transform] = "translate(" + i.x + "px," + i.y + "px)"
            } else {
                i.screen.style.top = i.y + "px"
            }
        };
        i.getY = function() {
            return i.y
        };
        i.setWidth = function(e) {
            i.w = e;
            if (i.type == "img") {
                i.screen.width = i.w;
                i.screen.style.width = i.w + "px"
            } else {
                i.screen.style.width = i.w + "px"
            }
        };
        i.getWidth = function() {
            if (i.type == "div" || i.type == "input") {
                if (i.screen.offsetWidth != 0) return i.screen.offsetWidth;
                return i.w
            } else if (i.type == "img") {
                if (i.screen.offsetWidth != 0) return i.screen.offsetWidth;
                if (i.screen.width != 0) return i.screen.width;
                return i._w
            } else if (i.type == "canvas") {
                if (i.screen.offsetWidth != 0) return i.screen.offsetWidth;
                return i.w
            }
        };
        i.setHeight = function(e) {
            i.h = e;
            if (i.type == "img") {
                i.screen.height = i.h;
                i.screen.style.height = i.h + "px"
            } else {
                i.screen.style.height = i.h + "px"
            }
        };
        i.getHeight = function() {
            if (i.type == "div" || i.type == "input") {
                if (i.screen.offsetHeight != 0) return i.screen.offsetHeight;
                return i.h
            } else if (i.type == "img") {
                if (i.screen.offsetHeight != 0) return i.screen.offsetHeight;
                if (i.screen.height != 0) return i.screen.height;
                return i.h
            } else if (i.type == "canvas") {
                if (i.screen.offsetHeight != 0) return i.screen.offsetHeight;
                return i.h
            }
        };
        i.addChild = function(e) {
            if (i.contains(e)) {
                i.children_ar.splice(MUSICUtils.indexOfArray(i.children_ar, e), 1);
                i.children_ar.push(e);
                i.screen.appendChild(e.screen)
            } else {
                i.children_ar.push(e);
                i.screen.appendChild(e.screen)
            }
        };
        i.removeChild = function(e) {
            if (i.contains(e)) {
                i.children_ar.splice(MUSICUtils.indexOfArray(i.children_ar, e), 1);
                i.screen.removeChild(e.screen)
            } else {
                throw Error("##removeChild()## Child dose't exist, it can't be removed!")
            }
        };
        i.contains = function(e) {
            if (MUSICUtils.indexOfArray(i.children_ar, e) == -1) {
                return false
            } else {
                return true
            }
        };
        i.addChildAt = function(e, t) {
            if (i.getNumChildren() == 0) {
                i.children_ar.push(e);
                i.screen.appendChild(e.screen)
            } else if (t == 1) {
                i.screen.insertBefore(e.screen, i.children_ar[0].screen);
                i.screen.insertBefore(i.children_ar[0].screen, e.screen);
                if (i.contains(e)) {
                    i.children_ar.splice(MUSICUtils.indexOfArray(i.children_ar, e), 1, e)
                } else {
                    i.children_ar.splice(MUSICUtils.indexOfArray(i.children_ar, e), 0, e)
                }
            } else {
                if (t < 0 || t > i.getNumChildren() - 1) throw Error("##getChildAt()## Index out of bounds!");
                i.screen.insertBefore(e.screen, i.children_ar[t].screen);
                if (i.contains(e)) {
                    i.children_ar.splice(MUSICUtils.indexOfArray(i.children_ar, e), 1, e)
                } else {
                    i.children_ar.splice(MUSICUtils.indexOfArray(i.children_ar, e), 0, e)
                }
            }
        };
        i.getChildAt = function(e) {
            if (e < 0 || e > i.getNumChildren() - 1) throw Error("##getChildAt()## Index out of bounds!");
            if (i.getNumChildren() == 0) throw Errror("##getChildAt## Child dose not exist!");
            return i.children_ar[e]
        };
        i.removeChildAtZero = function() {
            i.screen.removeChild(i.children_ar[0].screen);
            i.children_ar.shift()
        };
        i.getNumChildren = function() {
            return i.children_ar.length
        };
        i.addListener = function(e, t) {
            if (e == undefined) throw Error("type is required.");
            if (typeof e === "object") throw Error("type must be of type String.");
            if (typeof t != "function") throw Error("listener must be of type Function.");
            var n = {};
            n.type = e;
            n.listener = t;
            n.target = this;
            this.listeners.events_ar.push(n)
        };
        i.dispatchEvent = function(e, t) {
            if (this.listeners == null) return;
            if (e == undefined) throw Error("type is required.");
            if (typeof e === "object") throw Error("type must be of type String.");
            for (var n = 0, r = this.listeners.events_ar.length; n < r; n++) {
                if (this.listeners.events_ar[n].target === this && this.listeners.events_ar[n].type === e) {
                    if (t) {
                        for (var i in t) {
                            this.listeners.events_ar[n][i] = t[i]
                        }
                    }
                    this.listeners.events_ar[n].listener.call(this, this.listeners.events_ar[n])
                }
            }
        };
        i.removeListener = function(e, t) {
            if (e == undefined) throw Error("type is required.");
            if (typeof e === "object") throw Error("type must be of type String.");
            if (typeof t != "function") throw Error("listener must be of type Function." + e);
            for (var n = 0, r = this.listeners.events_ar.length; n < r; n++) {
                if (this.listeners.events_ar[n].target === this && this.listeners.events_ar[n].type === e && this.listeners.events_ar[n].listener === t) {
                    this.listeners.events_ar.splice(n, 1);
                    break
                }
            }
        };
        i.disposeImage = function() {
            if (i.type == "img") i.screen.src = null
        };
        i.destroy = function() {
            if (i.hasBeenSetSelectable_bl) {
                i.screen.ondragstart = null;
                i.screen.onselectstart = null;
                i.screen.ontouchstart = null
            }
            i.screen.removeAttribute("style");
            i.listeners = [];
            i.listeners = null;
            i.children_ar = [];
            i.children_ar = null;
            i.style = null;
            i.screen = null;
            i.transform = null;
            i.position = null;
            i.overflow = null;
            i.display = null;
            i.visible = null;
            i.buttonMode = null;
            i.x = null;
            i.y = null;
            i.w = null;
            i.h = null;
            i.rect = null;
            i.alpha = null;
            i.innerHTML = null;
            i.opacityType = null;
            i.isHtml5_bl = null;
            i.hasTransform3d_bl = null;
            i.hasTransform2d_bl = null;
            i = null
        };
        i.init()
    };
    e.MUSICDisplayObject = t
})(window);
(function() {
    var e = function() {
        this.listeners = {
            events_ar: []
        };
        this.addListener = function(e, t) {
            if (e == undefined) throw Error("type is required.");
            if (typeof e === "object") throw Error("type must be of type String.");
            if (typeof t != "function") throw Error("listener must be of type Function.");
            var n = {};
            n.type = e;
            n.listener = t;
            n.target = this;
            this.listeners.events_ar.push(n)
        };
        this.dispatchEvent = function(e, t) {
            if (this.listeners == null) return;
            if (e == undefined) throw Error("type is required.");
            if (typeof e === "object") throw Error("type must be of type String.");
            for (var n = 0, r = this.listeners.events_ar.length; n < r; n++) {
                if (this.listeners.events_ar[n].target === this && this.listeners.events_ar[n].type === e) {
                    if (t) {
                        for (var i in t) {
                            this.listeners.events_ar[n][i] = t[i]
                        }
                    }
                    this.listeners.events_ar[n].listener.call(this, this.listeners.events_ar[n])
                }
            }
        };
        this.removeListener = function(e, t) {
            if (e == undefined) throw Error("type is required.");
            if (typeof e === "object") throw Error("type must be of type String.");
            if (typeof t != "function") throw Error("listener must be of type Function." + e);
            for (var n = 0, r = this.listeners.events_ar.length; n < r; n++) {
                if (this.listeners.events_ar[n].target === this && this.listeners.events_ar[n].type === e && this.listeners.events_ar[n].listener === t) {
                    this.listeners.events_ar.splice(n, 1);
                    break
                }
            }
        };
        this.destroy = function() {
            this.listeners = null;
            this.addListener = null;
            this.dispatchEvent = null;
            this.removeListener = null
        }
    };
    window.MUSICEventDispatcher = e
})(window);
(function(e) {
    var t = function(e) {
        var n = this;
        var r = t.prototype;
        this.bk_do = null;
        this.textHolder_do = null;
        this.show_to = null;
        this.isShowed_bl = false;
        this.isShowedOnce_bl = false;
        this.allowToRemove_bl = true;
        this.init = function() {
            n.setResizableSizeAfterParent();
            n.bk_do = new MUSICDisplayObject("div");
            n.bk_do.setAlpha(.4);
            n.bk_do.setBkColor("#FF0000");
            n.addChild(n.bk_do);
            n.textHolder_do = new MUSICDisplayObject("div");
            n.textHolder_do.getStyle().wordWrap = "break-word";
            n.textHolder_do.getStyle().padding = "10px";
            n.textHolder_do.getStyle().paddingBottom = "0px";
            n.textHolder_do.getStyle().lineHeight = "18px";
            n.textHolder_do.setBkColor("#FF0000");
            n.textHolder_do.getStyle().color = "#000000";
            n.addChild(n.textHolder_do)
        };
        this.showText = function(e) {
            if (!n.isShowedOnce_bl) {
                if (n.screen.addEventListener) {
                    n.screen.addEventListener("click", n.closeWindow)
                } else if (n.screen.attachEvent) {
                    n.screen.attachEvent("onclick", n.closeWindow)
                }
                n.isShowedOnce_bl = true
            }
            n.setVisible(false);
            if (n.allowToRemove_bl) {
                n.textHolder_do.setInnerHTML(e + "<p style='margin:0px; padding-bottom:10px;'><font color='#FFFFFF'>Click or tap to close this window.</font>")
            } else {
                n.textHolder_do.getStyle().paddingBottom = "10px";
                n.textHolder_do.setInnerHTML(e)
            }
            clearTimeout(n.show_to);
            n.show_to = setTimeout(n.show, 60);
            setTimeout(function() {
                n.positionAndResize()
            }, 10)
        };
        this.show = function() {
            n.isShowed_bl = true;
            n.setVisible(true);
            n.positionAndResize()
        };
        this.positionAndResize = function() {
            if (e.main_do) {
                n.stageWidth = e.main_do.w;
                if (e.isPlaylistShowed_bl || e.openInPopup_bl) {
                    n.stageHeight = e.main_do.h
                } else {
                    if (e.controller_do) {
                        n.stageHeight = e.controller_do.h
                    } else {
                        n.stageHeight = e.stageHeight
                    }
                }
            } else {
                n.stageWidth = e.stageWidth;
                n.stageHeight = e.stageHeight
            }
            var t = Math.min(600, n.stageWidth - 40);
            var r = n.textHolder_do.screen.offsetHeight;
            var i = parseInt((n.stageWidth - t) / 2) - 10;
            var s = parseInt((n.stageHeight - r) / 2);
            n.bk_do.setWidth(n.stageWidth);
            n.bk_do.setHeight(n.stageHeight);
            n.textHolder_do.setX(i);
            n.textHolder_do.setY(s);
            n.textHolder_do.setWidth(t)
        };
        this.closeWindow = function() {
            if (!n.allowToRemove_bl) return;
            n.isShowed_bl = false;
            clearTimeout(n.show_to);
            try {
                e.main_do.removeChild(n)
            } catch (t) {}
        };
        this.init()
    };
    t.setPrototype = function() {
        t.prototype = new MUSICDisplayObject("div", "relative")
    };
    t.prototype = null;
    e.MUSICInfo = t
})(window);
(function() {
    var e = function(t, n, r) {
        var i = this;
        this.animation_img = t.openerAnimation_img;
        if (n == MUSIC.POSITION_TOP) {
            this.openN_img = t.openTopN_img;
            this.openSPath_str = t.openTopSPath_str
        } else {
            this.openN_img = t.openBottomN_img;
            this.openSPath_str = t.openBottomSPath_str
        }
        this.openerPauseN_img = t.openerPauseN_img;
        this.openerPlayN_img = t.openerPlayN_img;
        this.closeN_img = t.closeN_img;
        this.openerPauseS_str = t.openerPauseS_str;
        this.openerPlaySPath_str = t.openerPlayS_str;
        this.closeSPath_str = t.closeSPath_str;
        this.animationPath_str = t.animationPath_str;
        this.totalWidth = i.openN_img.width;
        this.totalHeight = i.openN_img.height;
        this.mainHolder_do = null;
        this.dumy_do = null;
        this.openN_do = null;
        this.openS_do = null;
        this.closeN_do = null;
        this.closeS_do = null;
        this.animation_do = null;
        this.playPauseButton_do = null;
        this.position_str = n;
        this.alignment_str = t.openerAlignment_str;
        this.openerEqulizerOffsetLeft = t.openerEqulizerOffsetLeft;
        this.openerEqulizerOffsetTop = t.openerEqulizerOffsetTop;
        this.showFirstTime_bl = true;
        this.playerIsShowed_bl = r;
        this.showOpenerPlayPauseButton_bl = t.showOpenerPlayPauseButton_bl;
        this.isMobile_bl = MUSICUtils.isMobile;
        this.hasPointerEvent_bl = MUSICUtils.hasPointerEvent;
        this.init = function() {
            i.hasTransform3d_bl = false;
            i.hasTransform2d_bl = false;
            i.setBackfaceVisibility();
            i.getStyle().msTouchAction = "none";
            i.getStyle().webkitTapHighlightColor = "rgba(0, 0, 0, 0)";
            i.setupStuff();
            if (i.showOpenerPlayPauseButton_bl) i.setupPlayPauseButton();
            if (i.playerIsShowed_bl) i.showCloseButton();
            i.hide();
            if (i.showOpenerPlayPauseButton_bl) {
                i.setWidth(i.totalWidth + i.openerPauseN_img.width + 1)
            } else {
                i.setWidth(i.totalWidth)
            }
            i.setHeight(i.totalHeight)
        };
        this.setupStuff = function(e) {
            i.mainHolder_do = new MUSICDisplayObject("div");
            i.mainHolder_do.hasTransform3d_bl = false;
            i.mainHolder_do.hasTransform2d_bl = false;
            i.mainHolder_do.setBackfaceVisibility();
            if (i.showOpenerPlayPauseButton_bl) {
                i.mainHolder_do.setWidth(i.totalWidth + i.openerPauseN_img.width + 1)
            } else {
                i.mainHolder_do.setWidth(i.totalWidth)
            }
            i.mainHolder_do.setHeight(i.totalHeight);
            i.openN_do = new MUSICDisplayObject("img");
            i.openN_do.setScreen(i.openN_img);
            i.openN_do.hasTransform3d_bl = false;
            i.openN_do.hasTransform2d_bl = false;
            i.openN_do.setBackfaceVisibility();
            var t = new Image;
            t.src = i.openSPath_str;
            i.openS_do = new MUSICDisplayObject("img");
            i.openS_do.setScreen(t);
            i.openS_do.hasTransform3d_bl = false;
            i.openS_do.hasTransform2d_bl = false;
            i.openS_do.setBackfaceVisibility();
            i.openS_do.setWidth(i.openN_do.w);
            i.openS_do.setHeight(i.openN_do.h);
            i.openS_do.setAlpha(0);
            i.closeN_do = new MUSICDisplayObject("img");
            i.closeN_do.setScreen(i.closeN_img);
            i.closeN_do.hasTransform3d_bl = false;
            i.closeN_do.hasTransform2d_bl = false;
            i.closeN_do.setBackfaceVisibility();
            var n = new Image;
            n.src = i.closeSPath_str;
            i.closeS_do = new MUSICDisplayObject("img");
            i.closeS_do.setScreen(n);
            i.closeS_do.setWidth(i.closeN_do.w);
            i.closeS_do.setHeight(i.closeN_do.h);
            i.closeS_do.hasTransform3d_bl = false;
            i.closeS_do.hasTransform2d_bl = false;
            i.closeS_do.setBackfaceVisibility();
            i.closeS_do.setAlpha(0);
            MUSICPreloader.setPrototype();
            i.animation_do = new MUSICPreloader(i.animationPath_str, 29, 22, 31, 80, true);
            i.animation_do.setY(i.openerEqulizerOffsetTop);
            i.animation_do.show(false);
            i.animation_do.stop();
            i.dumy_do = new MUSICDisplayObject("div");
            i.dumy_do.setWidth(i.totalWidth);
            i.dumy_do.setHeight(i.totalHeight);
            i.dumy_do.getStyle().zIndex = 2;
            i.dumy_do.hasTransform3d_bl = false;
            i.dumy_do.hasTransform2d_bl = false;
            i.dumy_do.setBackfaceVisibility();
            i.dumy_do.setButtonMode(true);
            if (MUSICUtils.isIE || MUSICUtils.isAndroid) {
                i.dumy_do.setBkColor("#FF0000");
                i.dumy_do.setAlpha(.01)
            }
            if (i.isMobile_bl) {
                if (i.hasPointerEvent_bl) {
                    i.dumy_do.screen.addEventListener("MSPointerDown", i.onMouseUp);
                    i.dumy_do.screen.addEventListener("MSPointerOver", i.onMouseOver);
                    i.dumy_do.screen.addEventListener("MSPointerOut", i.onMouseOut)
                } else {
                    i.dumy_do.screen.addEventListener("touchstart", i.onMouseUp)
                }
            } else if (i.dumy_do.screen.addEventListener) {
                i.dumy_do.screen.addEventListener("mouseover", i.onMouseOver);
                i.dumy_do.screen.addEventListener("mouseout", i.onMouseOut);
                i.dumy_do.screen.addEventListener("mousedown", i.onMouseUp)
            } else if (i.dumy_do.screen.attachEvent) {
                i.dumy_do.screen.attachEvent("onmouseover", i.onMouseOver);
                i.dumy_do.screen.attachEvent("onmouseout", i.onMouseOut);
                i.dumy_do.screen.attachEvent("onmousedown", i.onMouseUp)
            }
            i.mainHolder_do.addChild(i.openN_do);
            i.mainHolder_do.addChild(i.openS_do);
            i.mainHolder_do.addChild(i.closeN_do);
            i.mainHolder_do.addChild(i.closeS_do);
            i.mainHolder_do.addChild(i.animation_do);
            i.mainHolder_do.addChild(i.dumy_do);
            i.addChild(i.mainHolder_do)
        };
        this.onMouseOver = function(e, t) {
            if (!e.pointerType || e.pointerType == e.MSPOINTER_TYPE_MOUSE) {
                i.setSelectedState(true)
            }
        };
        this.onMouseOut = function(e) {
            if (!e.pointerType || e.pointerType == e.MSPOINTER_TYPE_MOUSE) {
                i.setNormalState()
            }
        };
        this.onMouseUp = function(t) {
            if (t.preventDefault) t.preventDefault();
            if (i.playerIsShowed_bl) {
                i.playerIsShowed_bl = false;
                i.dispatchEvent(e.HIDE)
            } else {
                i.playerIsShowed_bl = true;
                i.dispatchEvent(e.SHOW)
            }
        };
        this.setupPlayPauseButton = function() {
            MUSICComplexButton.setPrototype();
            i.playPauseButton_do = new MUSICComplexButton(i.openerPlayN_img, i.openerPlaySPath_str, i.openerPauseN_img, i.openerPauseS_str, true);
            i.playPauseButton_do.addListener(MUSICComplexButton.MOUSE_UP, i.playButtonMouseUpHandler);
            i.addChild(i.playPauseButton_do)
        };
        this.showPlayButton = function() {
            if (i.playPauseButton_do) i.playPauseButton_do.setButtonState(1);
            i.animation_do.stop()
        };
        this.showPauseButton = function() {
            if (i.playPauseButton_do) i.playPauseButton_do.setButtonState(0);
            i.animation_do.start(0)
        };
        this.playButtonMouseUpHandler = function() {
            if (i.playPauseButton_do.currentState == 0) {
                i.dispatchEvent(MUSICController.PAUSE)
            } else {
                i.dispatchEvent(MUSICController.PLAY)
            }
        };
        this.setNormalState = function() {
            if (i.isMobile_bl && !i.hasPointerEvent_bl) return;
            MUSICTweenMax.killTweensOf(i.openS_do);
            MUSICTweenMax.killTweensOf(i.closeS_do);
            MUSICTweenMax.to(i.openS_do, .5, {
                alpha: 0,
                ease: Expo.easeOut
            });
            MUSICTweenMax.to(i.closeS_do, .5, {
                alpha: 0,
                ease: Expo.easeOut
            })
        };
        this.setSelectedState = function(e) {
            MUSICTweenMax.killTweensOf(i.openS_do);
            MUSICTweenMax.killTweensOf(i.closeS_do);
            MUSICTweenMax.to(i.openS_do, .5, {
                alpha: 1,
                ease: Expo.easeOut
            });
            MUSICTweenMax.to(i.closeS_do, .5, {
                alpha: 1,
                ease: Expo.easeOut
            })
        };
        this.showOpenButton = function() {
            i.playerIsShowed_bl = false;
            i.closeN_do.setX(150);
            i.closeS_do.setX(150);
            if (i.playPauseButton_do) {
                if (i.alignment_str == "right") {
                    i.playPauseButton_do.setX(0);
                    i.openN_do.setX(i.playPauseButton_do.w + 1);
                    i.openS_do.setX(i.playPauseButton_do.w + 1);
                    i.dumy_do.setX(i.playPauseButton_do.w + 1);
                    i.dumy_do.setWidth(i.totalWidth);
                    i.animation_do.setX(i.playPauseButton_do.w + 1 + i.openerEqulizerOffsetLeft)
                } else {
                    i.playPauseButton_do.setX(i.openN_do.w + 1);
                    i.openN_do.setX(0);
                    i.openS_do.setX(0);
                    i.dumy_do.setX(0);
                    i.dumy_do.setWidth(i.totalWidth);
                    i.animation_do.setX(i.openerEqulizerOffsetLeft)
                }
            } else {
                i.openN_do.setX(0);
                i.openS_do.setX(0);
                i.dumy_do.setX(0);
                i.dumy_do.setWidth(i.totalWidth);
                i.animation_do.setX(i.openerEqulizerOffsetLeft)
            }
            i.animation_do.setVisible(true)
        };
        this.showCloseButton = function() {
            i.playerIsShowed_bl = true;
            i.openN_do.setX(150);
            i.openS_do.setX(150);
            i.dumy_do.setWidth(i.closeN_do.w);
            if (i.alignment_str == "right") {
                if (i.playPauseButton_do) {
                    i.closeN_do.setX(i.totalWidth + 1);
                    i.closeS_do.setX(i.totalWidth + 1);
                    i.dumy_do.setX(i.totalWidth + 1)
                } else {
                    i.closeN_do.setX(i.totalWidth - i.closeN_do.w);
                    i.closeS_do.setX(i.totalWidth - i.closeN_do.w);
                    i.dumy_do.setX(i.totalWidth - i.closeN_do.w)
                }
            } else {
                i.closeN_do.setX(0);
                i.closeS_do.setX(0);
                i.dumy_do.setX(0)
            }
            if (i.playPauseButton_do) i.playPauseButton_do.setX(150);
            i.animation_do.setX(150);
            i.animation_do.setVisible(false)
        };
        this.hide = function() {
            i.mainHolder_do.setX(150)
        };
        this.show = function() {
            i.mainHolder_do.setX(0)
        };
        this.init()
    };
    e.setPrototype = function() {
        e.prototype = new MUSICDisplayObject("div")
    };
    e.SHOW = "show";
    e.HIDE = "hise";
    e.prototype = null;
    window.MUSICOpener = e
})(window);
(function() {
    var e = function(t, n) {
        var r = this;
        var i = e.prototype;
        this.playlist_ar = null;
        this.items_ar = null;
        this.playlistItemBk1_img = t.playlistItemBk1_img;
        this.playlistItemBk2_img = t.playlistItemBk2_img;
        this.playlistSeparator_img = t.playlistSeparator_img;
        this.playlistScrBkTop_img = t.playlistScrBkTop_img;
        this.playlistScrBkMiddle_img = t.playlistScrBkMiddle_img;
        this.playlistScrBkBottom_img = t.playlistScrBkBottom_img;
        this.playlistScrDragTop_img = t.playlistScrDragTop_img;
        this.playlistScrDragMiddle_img = t.playlistScrDragMiddle_img;
        this.playlistScrDragBottom_img = t.playlistScrDragBottom_img;
        this.playlistPlayButtonN_img = t.playlistPlayButtonN_img;
        this.playlistScrLines_img = t.playlistScrLines_img;
        this.playlistScrLinesOver_img = t.playlistScrLinesOver_img;
        this.playlistDownloadButtonN_img = t.playlistDownloadButtonN_img;
        this.disable_do = null;
        this.separator_do = null;
        this.itemsHolder_do = null;
        this.curItem_do = null;
        this.scrMainHolder_do = null;
        this.scrTrack_do = null;
        this.scrTrackTop_do = null;
        this.scrTrackMiddle_do = null;
        this.scrTrackBottom_do = null;
        this.scrHandler_do = null;
        this.scrHandlerTop_do = null;
        this.scrHandlerMiddle_do = null;
        this.scrHandlerBottom_do = null;
        this.scrHandlerLines_do = null;
        this.scrHandlerLinesN_do = null;
        this.scrHandlerLinesS_do = null;
        this.playlistPlayButtonN_str = t.playlistPlayButtonN_str;
        this.playlistPlayButtonS_str = t.playlistPlayButtonS_str;
        this.playlistPauseButtonN_str = t.playlistPauseButtonN_str;
        this.playlistPauseButtonS_str = t.playlistPauseButtonS_str;
        this.controllerBkPath_str = t.controllerBkPath_str;
        this.playlistBackgroundColor_str = t.playlistBackgroundColor_str;
        this.countTrack = 0;
        this.startSpaceBetweenButtons = t.startSpaceBetweenButtons;
        this.spaceBetweenButtons = t.spaceBetweenButtons;
        if (this.spaceBetweenButtons > 15) this.spaceBetweenButtons = 10;
        this.countID3 = 0;
        this.id = 0;
        this.stageWidth = 0;
        this.stageHeight = 0;
        this.itemsTotalHeight = 0;
        this.scrollbarOffestWidth = t.scrollbarOffestWidth;
        this.scrWidth = r.playlistScrBkTop_img.width;
        this.trackTitleOffsetLeft = t.trackTitleOffsetLeft;
        this.downloadButtonOffsetRight = t.downloadButtonOffsetRight;
        this.itemHeight = r.playlistItemBk1_img.height;
        this.playPuaseIconWidth = r.playlistPlayButtonN_img.width;
        this.playPuaseIconHeight = r.playlistPlayButtonN_img.height;
        this.nrOfVisiblePlaylistItems = t.nrOfVisiblePlaylistItems;
        this.durationOffsetRight = t.durationOffsetRight;
        this.totalPlayListItems = 0;
        this.visibleNrOfItems = 0;
        this.yPositionOnPress = 0;
        this.lastPresedY = 0;
        this.lastListY = 0;
        this.playListFinalY = 0;
        this.scrollBarHandlerFinalY = 0;
        this.scrollBarHandlerFinalY = 0;
        this.vy = 0;
        this.vy2 = 0;
        this.friction = .9;
        this.updateMobileScrollBarId_int;
        this.updateMoveMobileScrollbarId_int;
        this.disableOnMoveId_to;
        this.updateMobileScrollbarOnPlaylistLoadId_to;
        this.allowToTweenPlaylistItems_bl = false;
        this.expandPlaylistBackground_bl = t.expandControllerBackground_bl;
        this.isSortedNumerical_bl = true;
        this.showSortButtons_bl = t.showSortButtons_bl;
        this.addScrollBarMouseWheelSupport_bl = t.addScrollBarMouseWheelSupport_bl;
        this.allowToScrollAndScrollBarIsActive_bl = false;
        this.isDragging_bl = false;
        this.showPlaylistItemPlayButton_bl = t.showPlaylistItemPlayButton_bl;
        this.showPlaylistItemDownloadButton_bl = t.showPlaylistItemDownloadButton_bl;
        this.isShowed_bl = t.showPlayListByDefault_bl;
        this.isShowedFirstTime_bl = false;
        this.animateOnIntro_bl = t.animateOnIntro_bl;
        this.isListCreated_bl = false;
        this.isMobile_bl = MUSICUtils.isMobile;
        this.hasPointerEvent_bl = MUSICUtils.hasPointerEvent;
        r.init = function() {
            r.hasTransform3d_bl = false;
            r.hasTransform2d_bl = false;
            r.setBackfaceVisibility();
            r.mainHolder_do = new MUSICDisplayObject("div");
            r.mainHolder_do.hasTransform3d_bl = false;
            r.mainHolder_do.hasTransform2d_bl = false;
            r.mainHolder_do.setBackfaceVisibility();
            r.itemsHolder_do = new MUSICDisplayObject("div");
            r.itemsHolder_do.setBackfaceVisibility();
            r.setupSeparator();
            r.itemsHolder_do.setY(0);
            r.mainHolder_do.addChild(r.itemsHolder_do);
            r.addChild(r.mainHolder_do);
            if (r.isMobile_bl) {
                r.setupMobileScrollbar();
                if (r.hasPointerEvent_bl) r.setupDisable()
            } else {
                r.setupDisable();
                r.setupScrollbar();
                if (r.addScrollBarMouseWheelSupport_bl) r.addMouseWheelSupport()
            }
            r.addChild(r.separator_do);
            r.mainHolder_do.setWidth(500);
            r.mainHolder_do.setHeight(500)
        };
        r.resizeAndPosition = function(e) {
            if (n.stageWidth == r.stageWidth && n.stageHeight == r.stageHeight && !e) return;
            if (!r.isListCreated_bl) return;
            r.stageWidth = n.stageWidth;
            r.stageWidth = n.stageWidth;
            r.positionList();
            if (r.scrMainHolder_do && r.allowToScrollAndScrollBarIsActive_bl) r.scrMainHolder_do.setX(r.stageWidth - r.scrWidth)
        };
        r.positionList = function() {
            if (!r.isListCreated_bl && r.stageWidth == 0) return;
            var e;
            r.copy_ar = [].concat(r.items_ar);
            var n = 0;
            for (var t = 0; t < r.copy_ar.length; t++) {
                e = r.copy_ar[t];
                e.changeSource(t % 2)
            }
            var i = r.copy_ar.length;
            r.itemsTotalHeight = i * r.itemHeight;
            if (r.visibleNrOfItems >= i) {
                r.allowToScrollAndScrollBarIsActive_bl = false
            } else {
                r.allowToScrollAndScrollBarIsActive_bl = true
            }
            for (var t = 0; t < i; t++) {
                e = r.copy_ar[t];
                if (r.allowToTweenPlaylistItems_bl && e.x < 0 && !r.isMobile_bl) {
                    if (!MUSICTweenMax.isTweening(e)) MUSICTweenMax.to(e, .8, {
                        x: 0,
                        ease: Expo.easeInOut
                    })
                } else {
                    MUSICTweenMax.killTweensOf(e);
                    e.setX(0)
                }
                e.setY(r.itemHeight * t);
                if (r.allowToScrollAndScrollBarIsActive_bl && r.scrMainHolder_do) {
                    e.resize(r.stageWidth - r.scrollbarOffestWidth, r.itemHeight)
                } else {
                    e.resize(r.stageWidth, r.itemHeight)
                }
            }
            if (r.allowToScrollAndScrollBarIsActive_bl && r.scrMainHolder_do) {
                r.itemsHolder_do.setWidth(r.stageWidth - r.scrollbarOffestWidth)
            } else {
                r.itemsHolder_do.setWidth(r.stageWidth)
            }
            if (r.input_do) {
                if (i == 0) {
                    r.showNothingFound()
                } else {
                    r.hideNothingFound()
                }
            }
            r.separator_do.setWidth(r.stageWidth);
            if (r.scrHandler_do) r.updateScrollBarSizeActiveAndDeactivate();
            r.mainHolder_do.setWidth(r.stageWidth);
            r.mainHolder_do.setHeight(r.stageHeight);
            r.setWidth(r.stageWidth);
            r.setHeight(r.stageHeight)
        };
        this.updatePlaylist = function(e) {
            if (r.isListCreated_bl) return;
            var t;
            r.playlist_ar = e;
            r.isShowedFirstTime_bl = true;
            r.stageHeight = 0;
            r.isListCreated_bl = true;
            if (r.input_do) r.input_do.screen.value = "";
            r.allowToScrollAndScrollBarIsActive_bl = false;
            r.countID3 == 2001;
            r.countTrack = 0;
            r.visibleNrOfItems = r.nrOfVisiblePlaylistItems;
            r.totalPlayListItems = r.playlist_ar.length;
            if (r.nrOfVisiblePlaylistItems > r.totalPlayListItems) {
                r.visibleNrOfItems = r.totalPlayListItems
            }
            r.stageHeight = r.visibleNrOfItems * r.itemHeight + r.separator_do.h;
            r.itemsTotalHeight = r.totalPlayListItems * r.itemHeight;
            r.mainHolder_do.setY(-r.stageHeight);
            r.itemsHolder_do.setY(0);
            if (r.sortNButton_do) {
                r.disableSortNButton();
                r.ascDscButton_do.setButtonState(1);
                r.srotAscending_bl = true
            }
            r.createPlayList();
            r.loadId3();
            var i = r.items_ar.length;
            clearTimeout(r.updateMobileScrollbarOnPlaylistLoadId_to);
            r.updateMobileScrollbarOnPlaylistLoadId_to = setTimeout(r.updateScrollBarHandlerAndContent, 900);
            clearTimeout(r.showAnimationIntroId_to);
            r.showAnimationIntroId_to = setTimeout(function() {
                for (var e = 0; e < i; e++) {
                    t = r.items_ar[e];
                    t.setTextSizes()
                }
                r.isListCreated_bl = true;
                if (r.visibleNrOfItems >= r.totalPlayListItems) {
                    r.allowToScrollAndScrollBarIsActive_bl = false
                } else {
                    r.allowToScrollAndScrollBarIsActive_bl = true
                }
                if (r.scrHandler_do) r.updateScrollBarSizeActiveAndDeactivate();
                if (r.scrMainHolder_do && r.allowToScrollAndScrollBarIsActive_bl) r.scrMainHolder_do.setX(r.stageWidth - r.scrWidth);
                if (n.position_str == MUSIC.POSITION_TOP) {
                    r.mainHolder_do.setY(0);
                    r.separator_do.setY(r.stageHeight - r.separator_do.h)
                } else {
                    r.mainHolder_do.setY(r.separator_do.h);
                    r.separator_do.setY(0)
                }
                r.positionList();
                r.allowToTweenPlaylistItems_bl = true
            }, 60)
        };
        this.destroyPlaylist = function() {
            if (!r.isListCreated_bl) return;
            var e;
            var t = r.items_ar.length;
            r.isListCreated_bl = false;
            r.allowToTweenPlaylistItems_bl = false;
            clearTimeout(r.showAnimationIntroId_to);
            for (var n = 0; n < t; n++) {
                e = r.items_ar[n];
                r.itemsHolder_do.removeChild(e);
                e.destroy()
            }
            r.items_ar = null;
            r.stageHeight = 0;
            r.setHeight(r.stageHeight)
        };
        this.createPlayList = function() {
            var e;
            var n;
            var i;
            var s;
            var o = false;
            r.itemsHolder_do.setHeight(r.totalPlayListItems * r.itemHeight);
            r.mainHolder_do.setBkColor(r.playlistBackgroundColor_str);
            r.items_ar = [];
            for (var u = 0; u < r.totalPlayListItems; u++) {
                n = r.playlist_ar[u].duration == undefined ? undefined : MUSIC.formatTotalTime(r.playlist_ar[u].duration);
                if (u % 2 == 0) {
                    i = t.playlistItemProgress1_img;
                    s = t.playlistItemGrad1_img
                } else {
                    i = t.playlistItemProgress2_img;
                    s = t.playlistItemGrad2_img
                }
                var o = r.playlist_ar[u].downloadable;
                if (!r.showPlaylistItemDownloadButton_bl) o = false;
                var a = false;
                MUSICPlaylistItem.setPrototype();
                e = new MUSICPlaylistItem(r.playlist_ar[u].title, r.playlist_ar[u].titleText, r.playlistDownloadButtonN_img, t.playlistDownloadButtonS_str, r.playlistBuyButtonN_img, t.playlistBuyButtonS_str, t.playlistItemGrad1_img, t.playlistItemGrad2_img, t.playlistItemProgress1_img, t.playlistItemProgress2_img, t.playlistPlayButtonN_img, t.playlistItemBk1_img.src, t.playlistItemBk2_img.src, r.playlistPlayButtonN_str, r.playlistPlayButtonS_str, r.playlistPauseButtonN_str, r.playlistPauseButtonS_str, t.trackTitleNormalColor_str, t.trackTitleSelected_str, t.trackDurationColor_str, u, t.playPauseButtonOffsetLeftAndRight, r.trackTitleOffsetLeft, r.durationOffsetRight, r.downloadButtonOffsetRight, r.showPlaylistItemPlayButton_bl, o, a, n);
                e.addListener(MUSICPlaylistItem.MOUSE_UP, r.itemOnUpHandler);
                e.addListener(MUSICPlaylistItem.DOWNLOAD, r.downloadHandler);
                e.addListener(MUSICPlaylistItem.BUY, r.buyHandler);
                r.items_ar[u] = e;
                r.itemsHolder_do.addChild(e)
            }
        };
        this.itemOnUpHandler = function(e) {
            r.dispatchEvent(MUSICPlaylistItem.MOUSE_UP, {
                id: e.id
            })
        };
        this.downloadHandler = function(e) {
            r.dispatchEvent(MUSICPlaylistItem.DOWNLOAD, {
                id: e.id
            })
        };
        this.buyHandler = function(e) {
            r.dispatchEvent(MUSICPlaylistItem.BUY, {
                id: e.id
            })
        };
        this.loadId3 = function() {
            var e;
            clearTimeout(r.populateNextItemId_to);
            for (var t = 0; t < r.totalPlayListItems; t++) {
                if (r.playlist_ar[t].title != "...") {
                    r.countID3 = 2001;
                    return
                }
            }
            r.countID3 = 0;
            r.loadID3AndPopulate()
        };
        this.loadID3AndPopulate = function() {
            if (!r.items_ar) return;
            var n = "";
            var i = r.items_ar[r.countID3];
            var s = r.playlist_ar[r.countID3].source + "?rand=" + parseInt(Math.random() * 99999999);
            var o = r.playlist_ar[r.countID3];
            ID3.loadTags(s, function() {
                if (r.countID3 > r.playlist_ar.length || r.countID3 == 2001) {
                    clearTimeout(r.populateNextItemId_to);
                    return
                }
                var u = ID3.getAllTags(s);
                if (u.artist) {
                    o.titleText_str = u.artist + " - " + u.title;
                    if (t.showTracksNumbers_bl) {
                        if (r.countTrack < 9) n = "0";
                        n = n + (r.countTrack + 1) + ". ";
                        o.title = n + o.titleText_str
                    } else {
                        o.title = o.titleText_str
                    }
                    r.countTrack++
                }
                i.title_str = o.title;
                i.titleText_str = o.titleText_str;
                if (r.countID3 == r.id) r.dispatchEvent(e.UPDATE_TRACK_TITLE_if_FOLDER, {
                    title: i.title_str
                });
                i.updateTitle();
                setTimeout(function() {
                    if (!i) return;
                    i.setTextSizes(true);
                    if (r.allowToScrollAndScrollBarIsActive_bl && r.scrMainHolder_do) {
                        i.resize(r.stageWidth - r.scrollbarOffestWidth, r.itemHeight)
                    } else {
                        i.resize(r.stageWidth, r.itemHeight)
                    }
                }, 50);
                r.countID3++;
                r.populateNextItemId_to = setTimeout(r.loadID3AndPopulate, 150)
            })
        };
        this.activateItems = function(e, t) {
            var n;
            r.id = e;
            if (!r.items_ar) return;
            for (var i = 0; i < r.totalPlayListItems; i++) {
                n = r.items_ar[i];
                if (n.id == r.id) {
                    r.sortId = n.sortId;
                    break
                }
            }
            r.curItem_do = r.items_ar[r.sortId];
            r.id = r.curItem_do.id;
            for (var i = 0; i < r.totalPlayListItems; i++) {
                n = r.items_ar[i];
                if (i == r.sortId) {
                    n.setActive()
                } else {
                    n.setInActive()
                }
            }
            if (!t) r.updateScrollBarHandlerAndContent(true)
        };
        this.setCurItemPlayState = function() {
            if (!r.curItem_do) return;
            r.curItem_do.showPlayButton()
        };
        this.setCurItemPauseState = function() {
            if (!r.curItem_do) return;
            r.curItem_do.showPauseButton()
        };
        this.updateCurItemProgress = function(e) {
            if (!r.curItem_do) return;
            r.curItem_do.updateProgressPercent(e)
        };
        this.setupInput = function() {
            r.titlebarHeight = t.titlebarLeftPath_img.height;
            var e = new Image;
            e.src = t.titleBarLeft_img.src;
            r.titleBarLeft_do = new MUSICDisplayObject("img");
            r.titleBarLeft_do.setScreen(e);
            r.titleBarLeft_do.setWidth(t.titleBarLeft_img.width);
            r.titleBarLeft_do.setHeight(t.titleBarLeft_img.height);
            var n = new Image;
            n.src = t.titleBarRigth_img.src;
            r.titleBarRight_do = new MUSICDisplayObject("img");
            r.titleBarRight_do.setScreen(n);
            r.titleBarRight_do.setWidth(t.titleBarRigth_img.width);
            r.titleBarRight_do.setHeight(t.titleBarRigth_img.height);
            r.input_do = new MUSICDisplayObject("input");
            r.input_do.screen.maxLength = 20;
            r.input_do.getStyle().textAlign = "left";
            r.input_do.getStyle().outline = "none";
            r.input_do.getStyle().boxShadow = "none";
            r.input_do.getStyle().fontSmoothing = "antialiased";
            r.input_do.getStyle().webkitFontSmoothing = "antialiased";
            r.input_do.getStyle().textRendering = "optimizeLegibility";
            r.input_do.getStyle().fontFamily = "Arial";
            r.input_do.getStyle().fontSize = "12px";
            r.input_do.getStyle().padding = "6px";
            if (!MUSICUtils.isIEAndLessThen9) r.input_do.getStyle().paddingRight = "-6px";
            r.input_do.getStyle().paddingTop = "2px";
            r.input_do.getStyle().paddingBottom = "3px";
            if (r.input_do.screen.addEventListener) {
                r.input_do.screen.addEventListener("focus", r.inputFocusInHandler);
                r.input_do.screen.addEventListener("blur", r.inputFocusOutHandler);
                r.input_do.screen.addEventListener("keyup", r.keyUpHandler)
            } else if (r.input_do.screen.attachEvent) {
                r.input_do.screen.attachEvent("onfocus", r.inputFocusInHandler);
                r.input_do.screen.attachEvent("onblur", r.inputFocusOutHandler);
                r.input_do.screen.attachEvent("onkeyup", r.keyUpHandler)
            }
            var i = new Image;
            i.src = t.inputArrowPath_str;
            r.inputArrow_do = new MUSICDisplayObject("img");
            r.inputArrow_do.setScreen(i);
            r.inputArrow_do.setWidth(14);
            r.inputArrow_do.setHeight(12);
        };
        this.inputFocusInHandler = function() {
            if (r.hasInputFocus_bl) return;
            r.hasInputFocus_bl = true;
        };
        this.inputFocusOutHandler = function(e) {
            if (!r.hasInputFocus_bl) return;
            var t = MUSICUtils.getViewportMouseCoordinates(e);
            if (!MUSICUtils.hitTest(r.input_do.screen, t.screenX, t.screenY)) {
                r.hasInputFocus_bl = false;
                if (r.input_do.screen.value == "") {
                    r.input_do.screen.value = ""
                }
                return
            }
        };
        this.keyUpHandler = function(e) {
            if (e.stopPropagation) e.stopPropagation();
            if (r.prevInputValue_str != r.input_do.screen.value) {
                if (r.isMobile_bl) {
                    r.positionList()
                } else {
                    r.positionList()
                }
            }
            r.prevInputValue_str = r.input_do.screen.value;
            if (r.scrHandler_do) {
                r.updateScrollBarSizeActiveAndDeactivate();
                r.updateScrollBarHandlerAndContent(false)
            }
        };
        this.setupButtons = function() {
            MUSICSimpleButton.setPrototype();
            r.sortNButton_do = new MUSICSimpleButton(t.sortNN_img, t.sortNSPath_str, null, true);
            r.sortNButton_do.addListener(MUSICSimpleButton.MOUSE_UP, r.sortNButtonOnMouseUpHandler);
            r.sortNButton_do.setX(410);
            MUSICSimpleButton.setPrototype();
            r.sortAButton_do = new MUSICSimpleButton(t.sortAN_img, t.sortASPath_str, null, true);
            r.sortAButton_do.addListener(MUSICSimpleButton.MOUSE_UP, r.sortAButtonOnMouseUpHandler);
            r.sortAButton_do.setX(450);
            MUSICComplexButton.setPrototype();
            r.ascDscButton_do = new MUSICComplexButton(t.ascendingN_img, t.ascendingSpath_str, t.decendingN_img, t.decendingSpath_str, true);
            r.ascDscButton_do.setX(500);
            r.ascDscButton_do.addListener(MUSICComplexButton.MOUSE_UP, r.ascDscMouseUpHandler);
            if (r.isSortedNumerical_bl) {
                r.disableSortNButton()
            } else {
                r.disableSortAButton()
            }
        };
        this.ascDscMouseUpHandler = function() {
            if (r.srotAscending_bl) {
                r.ascDscButton_do.setButtonState(0);
                r.srotAscending_bl = false
            } else {
                r.ascDscButton_do.setButtonState(1);
                r.srotAscending_bl = true
            }
            r.sortList()
        };
        this.sortAButtonOnMouseUpHandler = function() {
            r.disableSortAButton();
            r.sortList()
        };
        this.sortNButtonOnMouseUpHandler = function() {
            r.disableSortNButton();
            r.sortList()
        };
        this.disableSortAButton = function() {
            r.sortAButton_do.disableForGood();
            r.sortAButton_do.setSelectedState();
            r.sortNButton_do.enableForGood();
            r.sortNButton_do.setNormalState();
            r.isSortedNumerical_bl = false
        };
        this.disableSortNButton = function() {
            r.sortNButton_do.disableForGood();
            r.sortNButton_do.setSelectedState();
            r.sortAButton_do.enableForGood();
            r.sortAButton_do.setNormalState();
            r.isSortedNumerical_bl = true
        };
        this.sortList = function() {
            if (r.isSortedNumerical_bl) {
                r.items_ar.sort(function(e, t) {
                    if (e.id < t.id) return -1;
                    if (e.id > t.id) return 1;
                    return 0
                })
            } else {
                r.items_ar.sort(function(e, t) {
                    if (e.titleText_str < t.titleText_str) return -1;
                    if (e.titleText_str > t.titleText_str) return 1;
                    return 0
                })
            }
            if (!r.srotAscending_bl) r.items_ar.reverse();
            for (var e = 0; e < r.items_ar.length; e++) {
                r.items_ar[e].sortId = e
            }
            r.positionList();
            r.updateScrollBarHandlerAndContent(false)
        };
        this.setupDisable = function() {
            r.disable_do = new MUSICDisplayObject("div");
            if (MUSICUtils.isIE) {
                r.disable_do.setBkColor("#FFFFFF");
                r.disable_do.setAlpha(0)
            }
            r.addChild(r.disable_do)
        };
        this.showDisable = function() {
            if (!r.disable_do || r.disable_do.w != 0) return;
            if (r.scrMainHolder_do) {
                r.disable_do.setWidth(r.stageWidth - r.scrollbarOffestWidth);
                r.disable_do.setHeight(r.stageHeight)
            } else {
                r.disable_do.setWidth(r.stageWidth);
                r.disable_do.setHeight(r.stageHeight)
            }
        };
        this.hideDisable = function() {
            if (!r.disable_do || r.disable_do.w == 0) return;
            r.disable_do.setWidth(0);
            r.disable_do.setHeight(0)
        };
        this.setupSeparator = function() {
            r.separator_do = new MUSICDisplayObject("div");
            r.separator_do.setBackfaceVisibility();
            r.separator_do.hasTransform3d_bl = false;
            r.separator_do.hasTransform2d_bl = false;
            r.separator_do.getStyle().background = "url('" + r.playlistSeparator_img.src + "')";
            r.separator_do.setHeight(r.playlistSeparator_img.height);
            r.separator_do.setY(-r.separator_do.h)
        };
        this.setupScrollbar = function() {
            r.scrMainHolder_do = new MUSICDisplayObject("div");
            r.scrMainHolder_do.setWidth(r.scrWidth);
            r.scrTrack_do = new MUSICDisplayObject("div");
            r.scrTrack_do.setWidth(r.scrWidth);
            r.scrTrackTop_do = new MUSICDisplayObject("img");
            r.scrTrackTop_do.setScreen(r.playlistScrBkTop_img);
            r.scrTrackMiddle_do = new MUSICDisplayObject("div");
            r.scrTrackMiddle_do.getStyle().background = "url('" + t.scrBkMiddlePath_str + "')";
            r.scrTrackMiddle_do.setWidth(r.scrWidth);
            r.scrTrackMiddle_do.setY(r.scrTrackTop_do.h);
            var e = new Image;
            e.src = t.scrBkBottomPath_str;
            r.scrTrackBottom_do = new MUSICDisplayObject("img");
            r.scrTrackBottom_do.setScreen(e);
            r.scrTrackBottom_do.setWidth(r.scrTrackTop_do.w);
            r.scrTrackBottom_do.setHeight(r.scrTrackTop_do.h);
            r.scrHandler_do = new MUSICDisplayObject("div");
            r.scrHandler_do.setWidth(r.scrWidth);
            r.scrHandlerTop_do = new MUSICDisplayObject("img");
            r.scrHandlerTop_do.setScreen(r.playlistScrDragTop_img);
            r.scrHandlerMiddle_do = new MUSICDisplayObject("div");
            r.scrHandlerMiddle_do.getStyle().background = "url('" + t.scrDragMiddlePath_str + "')";
            r.scrHandlerMiddle_do.setWidth(r.scrWidth);
            r.scrHandlerMiddle_do.setY(r.scrHandlerTop_do.h);
            var n = new Image;
            n.src = t.scrDragBottomPath_str;
            r.scrHandlerBottom_do = new MUSICDisplayObject("img");
            r.scrHandlerBottom_do.setScreen(n);
            r.scrHandlerBottom_do.setWidth(r.scrHandlerTop_do.w);
            r.scrHandlerBottom_do.setHeight(r.scrHandlerTop_do.h);
            r.scrHandler_do.setButtonMode(true);
            r.scrHandlerLinesN_do = new MUSICDisplayObject("img");
            r.scrHandlerLinesN_do.setScreen(r.playlistScrLines_img);
            var i = new Image;
            i.src = t.scrLinesSPath_str;
            r.scrHandlerLinesS_do = new MUSICDisplayObject("img");
            r.scrHandlerLinesS_do.setScreen(i);
            r.scrHandlerLinesS_do.setWidth(r.scrHandlerLinesN_do.w);
            r.scrHandlerLinesS_do.setHeight(r.scrHandlerLinesN_do.h);
            r.scrHandlerLinesS_do.setAlpha(0);
            r.scrHandlerLines_do = new MUSICDisplayObject("div");
            r.scrHandlerLines_do.hasTransform3d_bl = false;
            r.scrHandlerLines_do.hasTransform2d_bl = false;
            r.scrHandlerLines_do.setBackfaceVisibility();
            r.scrHandlerLines_do.setWidth(r.scrHandlerLinesN_do.w);
            r.scrHandlerLines_do.setHeight(r.scrHandlerLinesN_do.h);
            r.scrHandlerLines_do.setButtonMode(true);
            r.scrTrack_do.addChild(r.scrTrackTop_do);
            r.scrTrack_do.addChild(r.scrTrackMiddle_do);
            r.scrTrack_do.addChild(r.scrTrackBottom_do);
            r.scrHandler_do.addChild(r.scrHandlerTop_do);
            r.scrHandler_do.addChild(r.scrHandlerMiddle_do);
            r.scrHandler_do.addChild(r.scrHandlerBottom_do);
            r.scrHandlerLines_do.addChild(r.scrHandlerLinesN_do);
            r.scrHandlerLines_do.addChild(r.scrHandlerLinesS_do);
            r.scrMainHolder_do.addChild(r.scrTrack_do);
            r.scrMainHolder_do.addChild(r.scrHandler_do);
            r.scrMainHolder_do.addChild(r.scrHandlerLines_do);
            r.mainHolder_do.addChild(r.scrMainHolder_do);
            if (r.scrHandler_do.screen.addEventListener) {
                r.scrHandler_do.screen.addEventListener("mouseover", r.scrollBarHandlerOnMouseOver);
                r.scrHandler_do.screen.addEventListener("mouseout", r.scrollBarHandlerOnMouseOut);
                r.scrHandler_do.screen.addEventListener("mousedown", r.scrollBarHandlerOnMouseDown);
                r.scrHandlerLines_do.screen.addEventListener("mouseover", r.scrollBarHandlerOnMouseOver);
                r.scrHandlerLines_do.screen.addEventListener("mouseout", r.scrollBarHandlerOnMouseOut);
                r.scrHandlerLines_do.screen.addEventListener("mousedown", r.scrollBarHandlerOnMouseDown)
            } else if (r.scrHandler_do.screen.attachEvent) {
                r.scrHandler_do.screen.attachEvent("onmouseover", r.scrollBarHandlerOnMouseOver);
                r.scrHandler_do.screen.attachEvent("onmouseout", r.scrollBarHandlerOnMouseOut);
                r.scrHandler_do.screen.attachEvent("onmousedown", r.scrollBarHandlerOnMouseDown);
                r.scrHandlerLines_do.screen.attachEvent("onmouseover", r.scrollBarHandlerOnMouseOver);
                r.scrHandlerLines_do.screen.attachEvent("onmouseout", r.scrollBarHandlerOnMouseOut);
                r.scrHandlerLines_do.screen.attachEvent("onmousedown", r.scrollBarHandlerOnMouseDown)
            }
        };
        this.scrollBarHandlerOnMouseOver = function(e) {
            MUSICTweenMax.to(r.scrHandlerLinesS_do, .8, {
                alpha: 1,
                ease: Expo.easeOut
            })
        };
        this.scrollBarHandlerOnMouseOut = function(e) {
            if (r.isDragging_bl) return;
            MUSICTweenMax.to(r.scrHandlerLinesS_do, .8, {
                alpha: 0,
                ease: Expo.easeOut
            })
        };
        this.scrollBarHandlerOnMouseDown = function(e) {
            if (!r.allowToScrollAndScrollBarIsActive_bl) return;
            var t = MUSICUtils.getViewportMouseCoordinates(e);
            r.isDragging_bl = true;
            r.yPositionOnPress = r.scrHandler_do.y;
            r.lastPresedY = t.screenY;
            MUSICTweenMax.killTweensOf(r.scrHandler_do);
            r.showDisable();
            if (window.addEventListener) {
                window.addEventListener("mousemove", r.scrollBarHandlerMoveHandler);
                window.addEventListener("mouseup", r.scrollBarHandlerEndHandler)
            } else if (document.attachEvent) {
                document.attachEvent("onmousemove", r.scrollBarHandlerMoveHandler);
                document.attachEvent("onmouseup", r.scrollBarHandlerEndHandler)
            }
        };
        this.scrollBarHandlerMoveHandler = function(e) {
            if (e.preventDefault) e.preventDefault();
            var t = MUSICUtils.getViewportMouseCoordinates(e);
            r.scrollBarHandlerFinalY = Math.round(r.yPositionOnPress + t.screenY - r.lastPresedY);
            if (r.scrollBarHandlerFinalY >= r.scrTrack_do.h - r.scrHandler_do.h) {
                r.scrollBarHandlerFinalY = r.scrTrack_do.h - r.scrHandler_do.h
            } else if (r.scrollBarHandlerFinalY <= 0) {
                r.scrollBarHandlerFinalY = 0
            }
            r.scrHandler_do.setY(r.scrollBarHandlerFinalY);
            MUSICTweenMax.to(r.scrHandlerLines_do, .8, {
                y: r.scrollBarHandlerFinalY + parseInt((r.scrHandler_do.h - r.scrHandlerLines_do.h) / 2),
                ease: Quart.easeOut
            });
            r.updateScrollBarHandlerAndContent(true)
        };
        r.scrollBarHandlerEndHandler = function(e) {
            var t = MUSICUtils.getViewportMouseCoordinates(e);
            r.isDragging_bl = false;
            if (!MUSICUtils.hitTest(r.scrHandler_do.screen, t.screenX, t.screenY)) {
                MUSICTweenMax.to(r.scrHandlerLinesS_do, .8, {
                    alpha: 0,
                    ease: Expo.easeOut
                })
            }
            r.scrollBarHandlerFinalY = Math.round((r.scrMainHolder_do.h - r.scrHandler_do.h) * (r.playListFinalY / ((r.totalSearchedItems - r.nrOfVisiblePlaylistItems) * r.itemHeight))) * -1;
            if (r.scrollBarHandlerFinalY.y < 0) {
                r.scrollBarHandlerFinalY = 0
            } else if (r.scrollBarHandlerFinalY > r.scrTrack_do.h - r.scrHandler_do.h - 1) {
                r.scrollBarHandlerFinalY = r.scrTrack_do.h - r.scrHandler_do.h - 1
            }
            r.hideDisable();
            MUSICTweenMax.killTweensOf(r.scrHandler_do);
            MUSICTweenMax.to(r.scrHandler_do, .5, {
                y: r.scrollBarHandlerFinalY,
                ease: Quart.easeOut
            });
            if (window.removeEventListener) {
                window.removeEventListener("mousemove", r.scrollBarHandlerMoveHandler);
                window.removeEventListener("mouseup", r.scrollBarHandlerEndHandler)
            } else if (document.detachEvent) {
                document.detachEvent("onmousemove", r.scrollBarHandlerMoveHandler);
                document.detachEvent("onmouseup", r.scrollBarHandlerEndHandler)
            }
        };
        this.updateScrollBarSizeActiveAndDeactivate = function() {
            if (r.allowToScrollAndScrollBarIsActive_bl) {
                var e = 0;
                r.allowToScrollAndScrollBarIsActive_bl = true;
                r.scrMainHolder_do.setHeight(r.stageHeight - r.separator_do.h - e);
                r.scrTrack_do.setHeight(r.stageHeight - r.separator_do.h - e);
                r.scrTrackMiddle_do.setHeight(r.scrTrack_do.h - r.scrTrackTop_do.h * 2);
                r.scrTrackBottom_do.setY(r.scrTrackMiddle_do.y + r.scrTrackMiddle_do.h);
                r.scrHandler_do.setHeight(Math.min(r.stageHeight - r.separator_do.h - e, Math.round((r.stageHeight - r.separator_do.h - e) / r.itemsTotalHeight * r.stageHeight)));
                r.scrHandlerMiddle_do.setHeight(r.scrHandler_do.h - r.scrHandlerTop_do.h * 2);
                r.scrHandlerTop_do.setY(r.scrHandlerMiddle_do.y + r.scrHandlerMiddle_do.h);
                r.scrMainHolder_do.setX(r.stageWidth - r.scrWidth)
            } else {
                r.allowToScrollAndScrollBarIsActive_bl = false;
                r.scrMainHolder_do.setX(-500);
                r.scrHandler_do.setY(0)
            }
        };
        this.updateScrollBarHandlerAndContent = function(e) {
            if (r.curItem_do) r.sortId = r.curItem_do.sortId;
            var t = 0;
            var n = 0;
            if (r.isDragging_bl && !r.isMobile_bl) {
                t = r.scrHandler_do.y / (r.scrMainHolder_do.h - r.scrHandler_do.h);
                if (t == "Infinity") {
                    t = 0
                } else if (t >= 1) {
                    scrollPercent = 1
                }
                r.playListFinalY = Math.round(t * (r.totalSearchedItems - r.nrOfVisiblePlaylistItems)) * r.itemHeight * -1
            } else {
                if (r.totalSearchedItems != r.totalPlayListItems) {
                    n = 0
                } else {
                    n = parseInt(r.sortId / r.nrOfVisiblePlaylistItems) * r.nrOfVisiblePlaylistItems
                }
                if (n + r.nrOfVisiblePlaylistItems >= r.totalPlayListItems) {
                    n = r.totalPlayListItems - r.nrOfVisiblePlaylistItems
                }
                if (n < 0) n = 0;
                r.playListFinalY = n * r.itemHeight * -1;
                if (r.scrMainHolder_do) {
                    r.scrollBarHandlerFinalY = Math.round((r.scrMainHolder_do.h - r.scrHandler_do.h) * (r.playListFinalY / ((r.totalSearchedItems - r.nrOfVisiblePlaylistItems) * r.itemHeight))) * -1;
                    if (r.scrollBarHandlerFinalY < 0) {
                        r.scrollBarHandlerFinalY = 0
                    } else if (r.scrollBarHandlerFinalY > r.scrMainHolder_do.h - r.scrHandler_do.h - 1) {
                        r.scrollBarHandlerFinalY = r.scrMainHolder_do.h - r.scrHandler_do.h - 1
                    }
                    MUSICTweenMax.killTweensOf(r.scrHandler_do);
                    MUSICTweenMax.killTweensOf(r.scrHandlerLines_do);
                    if (e) {
                        MUSICTweenMax.to(r.scrHandler_do, .5, {
                            y: r.scrollBarHandlerFinalY,
                            ease: Quart.easeOut
                        });
                        MUSICTweenMax.to(r.scrHandlerLines_do, .8, {
                            y: r.scrollBarHandlerFinalY + parseInt((r.scrHandler_do.h - r.scrHandlerLinesN_do.h) / 2),
                            ease: Quart.easeOut
                        })
                    } else {
                        r.scrHandler_do.setY(r.scrollBarHandlerFinalY);
                        r.scrHandlerLines_do.setY(r.scrollBarHandlerFinalY + parseInt((r.scrHandler_do.h - r.scrHandlerLinesN_do.h) / 2))
                    }
                }
            }
            if (r.lastListY != r.playListFinalY) {
                MUSICTweenMax.killTweensOf(r.itemsHolder_do);
                if (e) {
                    MUSICTweenMax.to(r.itemsHolder_do, .5, {
                        y: r.playListFinalY,
                        ease: Quart.easeOut
                    })
                } else {
                    r.itemsHolder_do.setY(r.playListFinalY)
                }
            }
            r.lastListY = r.playListFinalY
        };
        this.addMouseWheelSupport = function() {
            if (window.addEventListener) {
                r.screen.addEventListener("mousewheel", r.mouseWheelHandler);
                r.screen.addEventListener("DOMMouseScroll", r.mouseWheelHandler)
            } else if (document.attachEvent) {
                r.screen.attachEvent("onmousewheel", r.mouseWheelHandler)
            }
        };
        this.mouseWheelHandler = function(e) {
            if (!r.allowToScrollAndScrollBarIsActive_bl || r.isDragging_bl) return;
            var t = e.detail || e.wheelDelta;
            if (e.wheelDelta) t *= -1;
            if (MUSICUtils.isOpera) t *= -1;
            if (t > 0) {
                r.playListFinalY -= r.itemHeight
            } else {
                r.playListFinalY += r.itemHeight
            }
            leftId = parseInt(r.playListFinalY / r.itemHeight);
            if (leftId >= 0) {
                leftId = 0
            } else if (Math.abs(leftId) + r.nrOfVisiblePlaylistItems >= r.totalSearchedItems) {
                leftId = (r.totalSearchedItems - r.nrOfVisiblePlaylistItems) * -1
            }
            r.playListFinalY = leftId * r.itemHeight;
            if (r.lastListY == r.playListFinalY) return;
            r.scrollBarHandlerFinalY = Math.round((r.scrMainHolder_do.h - r.scrHandler_do.h) * (r.playListFinalY / ((r.totalSearchedItems - r.nrOfVisiblePlaylistItems) * r.itemHeight))) * -1;
            if (r.scrollBarHandlerFinalY < 0) {
                r.scrollBarHandlerFinalY = 0
            } else if (r.scrollBarHandlerFinalY > r.scrMainHolder_do.h - r.scrHandler_do.h - 1) {
                r.scrollBarHandlerFinalY = r.scrMainHolder_do.h - r.scrHandler_do.h - 1
            }
            MUSICTweenMax.killTweensOf(r.itemsHolder_do);
            MUSICTweenMax.to(r.itemsHolder_do, .5, {
                y: r.playListFinalY,
                ease: Expo.easeOut
            });
            MUSICTweenMax.killTweensOf(r.scrHandler_do);
            MUSICTweenMax.to(r.scrHandler_do, .5, {
                y: r.scrollBarHandlerFinalY,
                ease: Expo.easeOut
            });
            MUSICTweenMax.to(r.scrHandlerLines_do, .8, {
                y: r.scrollBarHandlerFinalY + parseInt((r.scrHandler_do.h - r.scrHandlerLinesN_do.h) / 2),
                ease: Quart.easeOut
            });
            r.lastListY = r.playListFinalY;
            if (e.preventDefault) {
                e.preventDefault()
            } else {
                return false
            }
            return
        };
        r.setupMobileScrollbar = function() {
            if (r.hasPointerEvent_bl) {
                r.screen.addEventListener("MSPointerDown", r.scrollBarTouchStartHandler)
            } else {
                r.screen.addEventListener("touchstart", r.scrollBarTouchStartHandler)
            }
            r.updateMobileScrollBarId_int = setInterval(r.updateMobileScrollBar, 16)
        };
        r.scrollBarTouchStartHandler = function(e) {
            if (r.stageHeight > r.itemsTotalHeight) return;
            MUSICTweenMax.killTweensOf(r.itemsHolder_do);
            var t = MUSICUtils.getViewportMouseCoordinates(e);
            r.isDragging_bl = true;
            r.lastPresedY = t.screenY;
            if (r.hasPointerEvent_bl) {
                window.addEventListener("MSPointerUp", r.scrollBarTouchEndHandler);
                window.addEventListener("MSPointerMove", r.scrollBarTouchMoveHandler)
            } else {
                window.addEventListener("touchend", r.scrollBarTouchEndHandler);
                window.addEventListener("touchmove", r.scrollBarTouchMoveHandler)
            }
            clearInterval(r.updateMoveMobileScrollbarId_int);
            r.updateMoveMobileScrollbarId_int = setInterval(r.updateMoveMobileScrollbar, 20)
        };
        r.scrollBarTouchMoveHandler = function(e) {
            if (e.preventDefault) e.preventDefault();
            r.showDisable();
            var t = MUSICUtils.getViewportMouseCoordinates(e);
            var n = t.screenY - r.lastPresedY;
            r.playListFinalY += n;
            r.playListFinalY = Math.round(r.playListFinalY);
            r.lastPresedY = t.screenY;
            r.vy = n * 2
        };
        r.scrollBarTouchEndHandler = function(e) {
            r.isDragging_bl = false;
            clearInterval(r.updateMoveMobileScrollbarId_int);
            clearTimeout(r.disableOnMoveId_to);
            r.disableOnMoveId_to = setTimeout(function() {
                r.hideDisable()
            }, 50);
            if (r.hasPointerEvent_bl) {
                window.removeEventListener("MSPointerUp", r.scrollBarTouchEndHandler);
                window.removeEventListener("MSPointerMove", r.scrollBarTouchMoveHandler)
            } else {
                window.removeEventListener("touchend", r.scrollBarTouchEndHandler);
                window.removeEventListener("touchmove", r.scrollBarTouchMoveHandler)
            }
        };
        r.updateMoveMobileScrollbar = function() {
            r.itemsHolder_do.setY(r.playListFinalY)
        };
        r.updateMobileScrollBar = function(e) {
            if (!r.isDragging_bl && !MUSICTweenMax.isTweening(r.itemsHolder_do)) {
                r.vy *= r.friction;
                r.playListFinalY += r.vy;
                if (r.playListFinalY > 0) {
                    r.vy2 = (0 - r.playListFinalY) * .3;
                    r.vy *= r.friction;
                    r.playListFinalY += r.vy2
                } else if (r.playListFinalY < r.stageHeight - r.separator_do.h - r.itemsTotalHeight) {
                    r.vy2 = (r.stageHeight - r.separator_do.h - r.itemsTotalHeight - r.playListFinalY) * .3;
                    r.vy *= r.friction;
                    r.playListFinalY += r.vy2
                }
                if (r.stageHeight > r.itemsTotalHeight) r.playListFinalY = 0;
                r.itemsHolder_do.setY(Math.round(r.playListFinalY))
            }
        };
        this.hide = function() {
            r.isShowed_bl = false
        };
        this.show = function(e) {
            if (e) r.isShowed_bl = true;
            r.setX(0)
        };
        this.init()
    };
    e.setPrototype = function() {
        e.prototype = new MUSICDisplayObject("div")
    };
    e.PLAY = "play";
    e.PAUSE = "pause";
    e.UPDATE_TRACK_TITLE_if_FOLDER = "update_trak_title";
    e.prototype = null;
    window.MUSICPlaylist = e
})();
(function() {
    var e = function(t, n, r, i, s, o, u, a, f, l, c, h, p, d, v, m, g, y, b, w, E, S, x, T, N, C, k, L, A) {
        var O = this;
        var M = e.prototype;
        this.playlistItemGrad1_img = u;
        this.playlistItemGrad2_img = a;
        this.playlistItemProgress_img = f;
        this.playlistItemProgress2_img = l;
        this.playlistPlayButtonN_img = c;
        this.playlistDownloadButtonN_img = r;
        this.playlistDownloadButtonS_str = i;
        this.progress_do = null;
        this.playPause_do = null;
        this.playN_do = null;
        this.playS_do = null;
        this.pauseN_do = null;
        this.pauseS_do = null;
        this.titleText_do = null;
        this.grad_do = null;
        this.durationText_do = null;
        this.dumy_do = null;
        this.title_str = t;
        this.titleText_str = n;
        this.playlistItemBk1Path_str = h;
        this.playlistItemBk2Path_str = p;
        this.playlistPlayButtonN_str = d;
        this.playlistPlayButtonS_str = v;
        this.playlistPauseButtonN_str = m;
        this.playlistPauseButtonS_str = g;
        this.titleNormalColor_str = y;
        this.trackTitleSelected_str = b;
        this.durationColor_str = w;
        this.itemHeight = O.playlistItemGrad1_img.height;
        this.id = E;
        this.sortId = E;
        this.playPauseButtonOffsetLeftAndRight = S;
        this.trackTitleOffsetLeft = x;
        this.duration = A;
        this.durationOffsetRight = T;
        this.textHeight;
        this.durationWidth = 0;
        this.titleWidth = 0;
        this.playPauseButtonWidth = O.playlistPlayButtonN_img.width;
        this.playPauseButtonHeight = O.playlistPlayButtonN_img.height;
        this.progressPercent = 0;
        this.stageWidth = 0;
        this.downloadButtonOffsetRight = N;
        this.setTextsSizeId_to;
        this.showDownloadButton_bl = k;
        this.showPlayPauseButton_bl = C;
        this.showDuration_bl = A;
        this.isActive_bl = false;
        this.isSelected_bl = false;
        this.isMobile_bl = MUSICUtils.isMobile;
        this.hasPointerEvent_bl = MUSICUtils.hasPointerEvent;
        O.init = function() {
            O.setupProgress();
            O.setupTitle();
            if (O.showPlayPauseButton_bl) O.setupPlayPauseButton();
            O.setupGrad();
            if (O.showDuration_bl) O.setupDuration();
            O.setNormalState(false, true);
            O.setupDumy();
            if (O.showDownloadButton_bl) O.setupDownloadButton();
            if (O.id % 2 == 0) {
                O.getStyle().background = "url('" + O.playlistItemBk1Path_str + "')";
                O.grad_do.getStyle().background = "url('" + O.playlistItemGrad1_img.src + "')";
                O.progress_do.getStyle().background = "url('" + O.playlistItemProgress_img.src + "')";
                O.type = 1
            } else {
                O.getStyle().background = "url('" + O.playlistItemBk2Path_str + "')";
                O.grad_do.getStyle().background = "url('" + O.playlistItemGrad2_img.src + "')";
                O.progress_do.getStyle().background = "url('" + O.playlistItemProgress2_img.src + "')";
                O.type = 2
            }
            if (O.isMobile_bl) {
                if (O.hasPointerEvent_bl) {
                    O.dumy_do.screen.addEventListener("MSPointerUp", O.onMouseUp);
                    O.dumy_do.screen.addEventListener("MSPointerOver", O.onMouseOver);
                    O.dumy_do.screen.addEventListener("MSPointerOut", O.onMouseOut)
                } else {
                    O.dumy_do.screen.addEventListener("mouseup", O.onMouseUp)
                }
            } else if (O.dumy_do.screen.addEventListener) {
                O.dumy_do.screen.addEventListener("mouseover", O.onMouseOver);
                O.dumy_do.screen.addEventListener("mouseout", O.onMouseOut);
                O.dumy_do.screen.addEventListener("mouseup", O.onMouseUp)
            } else if (O.screen.attachEvent) {
                O.dumy_do.screen.attachEvent("onmouseover", O.onMouseOver);
                O.dumy_do.screen.attachEvent("onmouseout", O.onMouseOut);
                O.dumy_do.screen.attachEvent("onmouseup", O.onMouseUp)
            }
        };
        O.onMouseOver = function(e, t) {
            if (O.isActive_bl) return;
            if (!e.pointerType || e.pointerType == "mouse") {
                O.setSelectedState(true)
            }
        };
        O.onMouseOut = function(e) {
            if (O.isActive_bl) return;
            if (!e.pointerType || e.pointerType == "mouse") {
                O.setNormalState(true)
            }
        };
        O.onMouseUp = function(t) {
            if (t.button == 2) return;
            if (t.preventDefault) t.preventDefault();
            O.dispatchEvent(e.MOUSE_UP, {
                id: O.id
            })
        };
        O.changeSource = function(e) {
            if (e == 0) {
                if (O.type != 1) {
                    O.grad_do.getStyle().background = "url('" + O.playlistItemGrad1_img.src + "')";
                    O.getStyle().background = "url('" + O.playlistItemBk1Path_str + "')";
                    O.progress_do.getStyle().background = "url('" + O.playlistItemProgress_img.src + "')";
                    O.type = 1
                }
            } else {
                if (O.type != 2) {
                    O.grad_do.getStyle().background = "url('" + O.playlistItemGrad2_img.src + "')";
                    O.getStyle().background = "url('" + O.playlistItemBk2Path_str + "')";
                    O.progress_do.getStyle().background = "url('" + O.playlistItemProgress2_img.src + "')";
                    O.type = 2
                }
            }
        };
        O.resize = function(e, t) {
            if (MUSICUtils.isIEAndLessThen9 && !O.textHeight || O == null) return;
            O.stageWidth = e;
            var n = 0;
            var r = parseInt((t - O.textHeight) / 2) + 1;
            if (O.playPause_do) {
                O.titleText_do.setX(O.playPauseButtonOffsetLeftAndRight * 2 + O.playPause_do.w + O.trackTitleOffsetLeft);
                O.playPause_do.setY(parseInt((t - O.playPause_do.h) / 2))
            } else {
                O.titleText_do.setX(O.trackTitleOffsetLeft)
            }
            O.titleText_do.setY(r);
            if (O.downloadButton_do) {
                if (O.durationText_do) {
                    O.durationText_do.setX(e - O.durationWidth - O.durationOffsetRight + 1);
                    O.durationText_do.setY(r);
                    n = O.durationText_do.x
                } else {
                    n = e
                }
                O.downloadButton_do.setX(n - O.downloadButton_do.w - O.downloadButtonOffsetRight + 3);
                O.downloadButton_do.setY(parseInt((t - O.downloadButton_do.h) / 2));
                if (O.titleText_do.x + O.titleWidth + O.downloadButton_do.w + O.downloadButtonOffsetRight > n) {
                    O.grad_do.setX(O.downloadButton_do.x - O.downloadButtonOffsetRight + 2)
                } else {
                    O.grad_do.setX(-300)
                }
            }else if (O.durationText_do) {
                O.durationText_do.setX(e - O.durationWidth - O.durationOffsetRight + 1);
                O.durationText_do.setY(r);
                if (O.titleText_do.x + O.titleWidth > O.durationText_do.x) {
                    O.grad_do.setX(O.durationText_do.x - O.durationOffsetRight + 2)
                } else {
                    O.grad_do.setX(-300)
                }
            } else if (O.downloadButton_do) {
                O.downloadButton_do.setX(e - O.downloadButton_do.w - O.downloadButtonOffsetRight + 2);
                if (O.titleText_do.x + O.titleWidth > O.downloadButton_do.x) {
                    O.grad_do.setX(O.downloadButton_do.x - O.downloadButtonOffsetRight + 2)
                } else {
                    O.grad_do.setX(-300)
                }
                O.downloadButton_do.setY(parseInt((t - O.downloadButton_do.h) / 2))
            } else {
                if (O.titleText_do.x + O.titleWidth > e - 10) {
                    O.grad_do.setX(e - 15)
                } else {
                    O.grad_do.setX(-300)
                }
            }
            O.dumy_do.setWidth(e);
            O.dumy_do.setHeight(t);
            O.setWidth(e);
            O.setHeight(t)
        };
        this.setupDownloadButton = function() {
            MUSICSimpleSizeButton.setPrototype();
            O.downloadButton_do = new MUSICSimpleSizeButton(O.playlistDownloadButtonN_img, O.playlistDownloadButtonS_str, 18, 17);
            O.downloadButton_do.getStyle().position = "absolute";
            O.downloadButton_do.addListener(MUSICSimpleSizeButton.CLICK, O.dwButtonClickHandler);
            O.addChild(O.downloadButton_do)
        };
        this.dwButtonClickHandler = function() {
            O.dispatchEvent(e.DOWNLOAD, {
                id: O.id
            })
        };
        this.setupProgress = function() {
            O.progress_do = new MUSICDisplayObject("div");
            O.progress_do.setBackfaceVisibility();
            O.progress_do.getStyle().background = "url('" + O.playlistItemProgress_img.src + "')";
            O.progress_do.setHeight(f.height);
            O.addChild(O.progress_do)
        };
        this.updateProgressPercent = function(e) {
            if (O == null) return;
            if (O.progressPercent == e) return;
            O.progressPercent = e;
            O.progress_do.setWidth(parseInt(O.stageWidth * e))
        };
        this.setupPlayPauseButton = function() {
            O.playPause_do = new MUSICDisplayObject("div");
            O.playPause_do.setWidth(O.playPauseButtonWidth);
            O.playPause_do.setHeight(O.playPauseButtonHeight);
            O.playN_do = new MUSICDisplayObject("div");
            O.playN_do.getStyle().background = "url('" + O.playlistPlayButtonN_str + "') no-repeat";
            O.playN_do.setWidth(O.playPauseButtonWidth);
            O.playN_do.setHeight(O.playPauseButtonHeight);
            O.playS_do = new MUSICDisplayObject("div");
            O.playS_do.getStyle().background = "url('" + O.playlistPlayButtonS_str + "') no-repeat";
            O.playS_do.setWidth(O.playPauseButtonWidth);
            O.playS_do.setHeight(O.playPauseButtonHeight);
            O.playS_do.setAlpha(0);
            O.pauseN_do = new MUSICDisplayObject("div");
            O.pauseN_do.getStyle().background = "url('" + O.playlistPauseButtonN_str + "') no-repeat";
            O.pauseN_do.setWidth(O.playPauseButtonWidth);
            O.pauseN_do.setHeight(O.playPauseButtonHeight);
            O.pauseN_do.setX(-300);
            O.pauseS_do = new MUSICDisplayObject("div");
            O.pauseS_do.getStyle().background = "url('" + O.playlistPauseButtonS_str + "') no-repeat";
            O.pauseS_do.setWidth(O.playPauseButtonWidth);
            O.pauseS_do.setHeight(O.playPauseButtonHeight);
            O.pauseS_do.setX(-300);
            O.pauseS_do.setAlpha(0);
            O.playPause_do.setX(O.playPauseButtonOffsetLeftAndRight);
            O.playPause_do.addChild(O.playN_do);
            O.playPause_do.addChild(O.playS_do);
            O.playPause_do.addChild(O.pauseN_do);
            O.playPause_do.addChild(O.pauseS_do);
            O.addChild(O.playPause_do)
        };
        this.setupTitle = function() {
            O.titleText_do = new MUSICDisplayObject("div");
            if (MUSICUtils.isApple) {
                O.titleText_do.hasTransform3d_bl = false;
                O.titleText_do.hasTransform2d_bl = false
            }
            O.titleText_do.setOverflow("visible");
            O.titleText_do.setBackfaceVisibility();
            O.titleText_do.getStyle().fontFamily = "Arial";
            O.titleText_do.getStyle().fontSize = "12px";
            O.titleText_do.getStyle().whiteSpace = "nowrap";
            O.titleText_do.getStyle().textAlign = "left";
            O.titleText_do.getStyle().fontSmoothing = "antialiased";
            O.titleText_do.getStyle().webkitFontSmoothing = "antialiased";
            O.titleText_do.getStyle().textRendering = "optimizeLegibility";
            O.titleText_do.setInnerHTML(O.title_str);
            O.addChild(O.titleText_do)
        };
        this.updateTitle = function() {
            if (O == null) return;
            O.titleText_do.setInnerHTML(O.title_str)
        };
        this.setTextSizes = function(e) {
            if (O == null) return;
            if (O.textHeight && !e) return;
            O.titleWidth = O.titleText_do.screen.offsetWidth;
            O.textHeight = O.titleText_do.screen.offsetHeight;
            if (O.durationText_do) {
                O.durationWidth = O.durationText_do.screen.offsetWidth
            }
            O.grad_do.setWidth(150)
        };
        this.setupGrad = function() {
            O.grad_do = new MUSICDisplayObject("div");
            O.grad_do.setOverflow("visible");
            if (MUSICUtils.isApple) {
                O.grad_do.hasTransform3d_bl = false;
                O.grad_do.hasTransform2d_bl = false
            }
            O.grad_do.setBackfaceVisibility();
            O.grad_do.getStyle().background = "url('" + O.playlistItemGrad1_img.src + "')";
            O.grad_do.setHeight(O.itemHeight);
            O.addChild(O.grad_do)
        };
        this.setupDuration = function() {
            O.durationText_do = new MUSICDisplayObject("div");
            if (MUSICUtils.isApple) {
                O.durationText_do.hasTransform3d_bl = false;
                O.durationText_do.hasTransform2d_bl = false
            }
            O.durationText_do.setOverflow("visible");
            O.durationText_do.setBackfaceVisibility();
            O.durationText_do.getStyle().fontFamily = "Arial";
            O.durationText_do.getStyle().fontSize = "12px";
            O.durationText_do.getStyle().whiteSpace = "nowrap";
            O.durationText_do.getStyle().textAlign = "left";
            O.durationText_do.getStyle().color = O.titleColor_str;
            O.durationText_do.getStyle().fontSmoothing = "antialiased";
            O.durationText_do.getStyle().webkitFontSmoothing = "antialiased";
            O.durationText_do.getStyle().textRendering = "optimizeLegibility";
            O.durationText_do.getStyle().color = O.durationColor_str;
            O.durationText_do.setInnerHTML(O.duration);
            O.addChild(O.durationText_do)
        };
        this.setupDumy = function() {
            O.dumy_do = new MUSICDisplayObject("div");
            O.dumy_do.setButtonMode(true);
            if (MUSICUtils.isIE) {
                O.dumy_do.setBkColor("#FFFFFF");
                O.dumy_do.setAlpha(.001)
            }
            O.addChild(O.dumy_do)
        };
        this.setNormalState = function(e, t) {
            if (!O.isSelected_bl && !t) return;
            O.isSelected_bl = false;
            if (e) {
                MUSICTweenMax.to(O.titleText_do.screen, .8, {
                    css: {
                        color: O.titleNormalColor_str
                    },
                    ease: Expo.easeOut
                });
                if (O.durationText_do) {
                    MUSICTweenMax.to(O.durationText_do.screen, .8, {
                        css: {
                            color: O.durationColor_str
                        },
                        ease: Expo.easeOut
                    })
                }
                if (O.playPause_do) {
                    MUSICTweenMax.to(O.pauseS_do, .8, {
                        alpha: 0,
                        ease: Expo.easeOut
                    });
                    MUSICTweenMax.to(O.playS_do, .8, {
                        alpha: 0,
                        ease: Expo.easeOut
                    })
                }
            } else {
                MUSICTweenMax.killTweensOf(O.titleText_do);
                O.titleText_do.getStyle().color = O.titleNormalColor_str;
                if (O.durationText_do) O.durationText_do.getStyle().color = O.durationColor_str;
                if (O.playPause_do) {
                    MUSICTweenMax.killTweensOf(O.pauseS_do);
                    MUSICTweenMax.killTweensOf(O.playS_do);
                    O.pauseS_do.setAlpha(0);
                    O.playS_do.setAlpha(0)
                }
            }
        };
        this.setSelectedState = function(e) {
            if (O.isSelected_bl) return;
            O.isSelected_bl = true;
            if (e) {
                MUSICTweenMax.to(O.titleText_do.screen, .8, {
                    css: {
                        color: O.trackTitleSelected_str
                    },
                    ease: Expo.easeOut
                });
                if (O.durationText_do) {
                    MUSICTweenMax.to(O.durationText_do.screen, .8, {
                        css: {
                            color: O.trackTitleSelected_str
                        },
                        ease: Expo.easeOut
                    })
                }
                if (O.playPause_do) {
                    MUSICTweenMax.to(O.pauseS_do, .8, {
                        alpha: 1,
                        ease: Expo.easeOut
                    });
                    MUSICTweenMax.to(O.playS_do, .8, {
                        alpha: 1,
                        ease: Expo.easeOut
                    })
                }
            } else {
                MUSICTweenMax.killTweensOf(O.titleText_do);
                if (O.durationText_do) O.durationText_do.getStyle().color = O.trackTitleSelected_str;
                O.titleText_do.getStyle().color = O.trackTitleSelected_str;
                if (O.playPause_do) {
                    MUSICTweenMax.killTweensOf(O.pauseS_do);
                    MUSICTweenMax.killTweensOf(O.playS_do);
                    O.pauseS_do.setAlpha(1);
                    O.playS_do.setAlpha(1)
                }
            }
        };
        this.setActive = function() {
            if (O.isActive_bl) return;
            O.isActive_bl = true;
            O.setSelectedState(true)
        };
        this.setInActive = function() {
            if (!O.isActive_bl) return;
            O.isActive_bl = false;
            O.setNormalState(true);
            O.updateProgressPercent(0);
            O.showPlayButton()
        };
        this.showPlayButton = function() {
            if (!O.playN_do) return;
            O.playN_do.setX(0);
            O.playS_do.setX(0);
            O.pauseN_do.setX(-300);
            O.pauseS_do.setX(-300)
        };
        this.showPauseButton = function() {
            if (!O.playN_do) return;
            O.playN_do.setX(-300);
            O.playS_do.setX(-300);
            O.pauseN_do.setX(0);
            O.pauseS_do.setX(0)
        };
        this.destroy = function() {
            this.playlistItemGrad1_img = null;
            this.playlistItemProgress_img = null;
            this.playlistPlayButtonN_img = null;
            this.playlistDownloadButtonN_img = null;
            this.playlistDownloadButtonS_str = null;
            this.playlistBuyButtonN_img = null;
            this.playlistBuyButtonS_str = null;
            this.progress_do = null;
            this.playPause_do = null;
            this.playN_do = null;
            this.playS_do = null;
            this.pauseN_do = null;
            this.pauseS_do = null;
            this.titleText_do = null;
            this.grad_do = null;
            this.durationText_do = null;
            this.dumy_do = null;
            this.title_str = null;
            this.playlistItemBk1Path_str = null;
            this.playlistItemBk2Path_str = null;
            this.playlistPlayButtonN_str = null;
            this.playlistPlayButtonS_str = null;
            this.playlistPauseButtonN_str = null;
            this.playlistPauseButtonS_str = null;
            this.titleNormalColor_str = null;
            this.trackTitleSelected_str = null;
            this.durationColor_str = w;
            O.setInnerHTML("");
            O = null;
            M = null;
            e.prototype = null
        };
        this.init()
    };
    e.setPrototype = function() {
        e.prototype = new MUSICDisplayObject("div")
    };
    e.PLAY = "play";
    e.PAUSE = "pause";
    e.MOUSE_UP = "mouseUp";
    e.DOWNLOAD = "download";
    e.BUY = "buy";
    e.prototype = null;
    window.MUSICPlaylistItem = e
})();
(function(e) {
    var t = function(e, n, r, i, s, o) {
        var u = this;
        var a = t.prototype;
        this.imageSource_img = null;
        this.image_sdo = null;
        this.imageSourcePath_str = e;
        this.segmentWidth = n;
        this.segmentHeight = r;
        this.totalSegments = i;
        this.totalWidth = n * i;
        this.animDelay = s || 300;
        this.count = 0;
        this.delayTimerId_int;
        this.isShowed_bl = false;
        this.skipFirstFrame_bl = o;
        this.init = function() {
            u.setWidth(u.segmentWidth);
            u.setHeight(u.segmentHeight);
            u.imageSource_img = new Image;
            u.imageSource_img.src = u.imageSourcePath_str;
            u.image_sdo = new MUSICDisplayObject("img");
            u.image_sdo.setScreen(u.imageSource_img);
            u.image_sdo.setWidth(u.totalWidth);
            u.image_sdo.setHeight(u.segmentHeight);
            u.addChild(this.image_sdo);
            u.hide(false)
        };
        this.start = function() {
            if (u == null) return;
            clearInterval(u.delayTimerId_int);
            u.delayTimerId_int = setInterval(u.updatePreloader, u.animDelay)
        };
        this.stop = function() {
            clearInterval(u.delayTimerId_int);
            u.image_sdo.setX(0)
        };
        this.updatePreloader = function() {
            if (u == null) return;
            u.count++;
            if (u.count > u.totalSegments - 1) {
                if (u.skipFirstFrame_bl) {
                    u.count = 1
                } else {
                    u.count = 0
                }
            }
            var e = u.count * u.segmentWidth;
            u.image_sdo.setX(-e)
        };
        this.show = function() {
            this.setVisible(true);
            this.start();
            MUSICTweenMax.killTweensOf(this);
            MUSICTweenMax.to(this, 1, {
                alpha: 1
            });
            this.isShowed_bl = true
        };
        this.hide = function(e) {
            if (!this.isShowed_bl) return;
            MUSICTweenMax.killTweensOf(this);
            if (e) {
                MUSICTweenMax.to(this, 1, {
                    alpha: 0,
                    onComplete: this.onHideComplete
                })
            } else {
                this.setVisible(false);
                this.setAlpha(0)
            }
            this.isShowed_bl = false
        };
        this.onHideComplete = function() {
            u.stop();
            u.setVisible(false);
            u.dispatchEvent(t.HIDE_COMPLETE)
        };
        this.setForFixedPosition = function() {
            u.setBackfaceVisibility();
            u.hasTransform3d_bl = false;
            u.hasTransform2d_bl = false;
            u.image_sdo.setBackfaceVisibility();
            u.image_sdo.hasTransform3d_bl = false;
            u.image_sdo.hasTransform2d_bl = false
        };
        this.init()
    };
    t.setPrototype = function() {
        t.prototype = new MUSICDisplayObject("div")
    };
    t.HIDE_COMPLETE = "hideComplete";
    t.prototype = null;
    e.MUSICPreloader = t
})(window);
(function(e) {
    var t = function(e, n, r, i) {
        var s = this;
        var o = t.prototype;
        this.nImg = e;
        this.sPath_str = n;
        this.dPath_str = r;
        this.n_sdo;
        this.s_sdo;
        this.d_sdo;
        this.totalWidth = this.nImg.width;
        this.totalHeight = this.nImg.height;
        this.isShowed_bl = true;
        this.isSetToDisabledState_bl = false;
        this.isDisabled_bl = false;
        this.isDisabledForGood_bl = false;
        this.isSelectedFinal_bl = false;
        this.isActive_bl = false;
        this.isMobile_bl = MUSICUtils.isMobile;
        this.hasPointerEvent_bl = MUSICUtils.hasPointerEvent;
        this.allowToCreateSecondButton_bl = !s.isMobile_bl || s.hasPointerEvent_bl || i;
        s.init = function() {
            s.setupMainContainers()
        };
        s.setupMainContainers = function() {
            s.n_sdo = new MUSICDisplayObject("img");
            s.n_sdo.setScreen(s.nImg);
            s.addChild(s.n_sdo);
            if (s.allowToCreateSecondButton_bl) {
                var e = new Image;
                e.src = s.sPath_str;
                s.s_sdo = new MUSICDisplayObject("img");
                s.s_sdo.setScreen(e);
                s.s_sdo.setWidth(s.totalWidth);
                s.s_sdo.setHeight(s.totalHeight);
                s.s_sdo.setAlpha(0);
                s.addChild(s.s_sdo);
                if (s.dPath_str) {
                    var t = new Image;
                    t.src = s.dPath_str;
                    s.d_sdo = new MUSICDisplayObject("img");
                    s.d_sdo.setScreen(t);
                    s.d_sdo.setWidth(s.totalWidth);
                    s.d_sdo.setHeight(s.totalHeight);
                    s.d_sdo.setX(-100);
                    s.addChild(s.d_sdo)
                }
            }
            s.setWidth(s.totalWidth);
            s.setHeight(s.totalHeight);
            s.setButtonMode(true);
            s.screen.style.yellowOverlayPointerEvents = "none";
            if (s.isMobile_bl) {
                if (s.hasPointerEvent_bl) {
                    s.screen.addEventListener("MSPointerUp", s.onMouseUp);
                    s.screen.addEventListener("MSPointerOver", s.onMouseOver);
                    s.screen.addEventListener("MSPointerOut", s.onMouseOut)
                } else {
                    s.screen.addEventListener("touchend", s.onMouseUp)
                }
            } else if (s.screen.addEventListener) {
                s.screen.addEventListener("mouseover", s.onMouseOver);
                s.screen.addEventListener("mouseout", s.onMouseOut);
                s.screen.addEventListener("mouseup", s.onMouseUp)
            } else if (s.screen.attachEvent) {
                s.screen.attachEvent("onmouseover", s.onMouseOver);
                s.screen.attachEvent("onmouseout", s.onMouseOut);
                s.screen.attachEvent("onmouseup", s.onMouseUp)
            }
        };
        s.onMouseOver = function(e) {
            if (s.isDisabledForGood_bl) return;
            if (!e.pointerType || e.pointerType == "mouse") {
                if (s.isDisabled_bl || s.isSelectedFinal_bl) return;
                s.dispatchEvent(t.MOUSE_OVER, {
                    e: e
                });
                s.setSelectedState()
            }
        };
        s.onMouseOut = function(e) {
            if (s.isDisabledForGood_bl) return;
            if (!e.pointerType || e.pointerType == "mouse") {
                if (s.isDisabled_bl || s.isSelectedFinal_bl) return;
                s.dispatchEvent(t.MOUSE_OUT, {
                    e: e
                });
                s.setNormalState()
            }
        };
        s.onMouseUp = function(e) {
            if (s.isDisabledForGood_bl) return;
            if (e.preventDefault) e.preventDefault();
            if (s.isDisabled_bl || e.button == 2) return;
            s.dispatchEvent(t.MOUSE_UP, {
                e: e
            })
        };
        s.setSelected = function() {
            s.isSelectedFinal_bl = true;
            if (!s.s_sdo) return;
            MUSICTweenMax.killTweensOf(s.s_sdo);
            MUSICTweenMax.to(s.s_sdo, .8, {
                alpha: 1,
                ease: Expo.easeOut
            })
        };
        s.setUnselected = function() {
            s.isSelectedFinal_bl = false;
            if (!s.s_sdo) return;
            MUSICTweenMax.to(s.s_sdo, .8, {
                alpha: 0,
                delay: .1,
                ease: Expo.easeOut
            })
        };
        this.setNormalState = function() {
            if (!s.s_sdo) return;
            MUSICTweenMax.killTweensOf(s.s_sdo);
            MUSICTweenMax.to(s.s_sdo, .5, {
                alpha: 0,
                ease: Expo.easeOut
            })
        };
        this.setSelectedState = function() {
            if (!s.s_sdo) return;
            MUSICTweenMax.killTweensOf(s.s_sdo);
            MUSICTweenMax.to(s.s_sdo, .5, {
                alpha: 1,
                delay: .1,
                ease: Expo.easeOut
            })
        };
        this.setDisabledState = function() {
            if (s.isSetToDisabledState_bl) return;
            s.isSetToDisabledState_bl = true;
            if (s.d_sdo) s.d_sdo.setX(0)
        };
        this.setEnabledState = function() {
            if (!s.isSetToDisabledState_bl) return;
            s.isSetToDisabledState_bl = false;
            if (s.d_sdo) s.d_sdo.setX(-100)
        };
        this.disable = function(e) {
            if (s.isDisabledForGood_bl || s.isDisabled_bl) return;
            s.isDisabled_bl = true;
            s.setButtonMode(false);
            MUSICTweenMax.to(s, .6, {
                alpha: .4
            });
            if (!e) s.setNormalState()
        };
        this.enable = function() {
            if (s.isDisabledForGood_bl || !s.isDisabled_bl) return;
            s.isDisabled_bl = false;
            s.setButtonMode(true);
            MUSICTweenMax.to(s, .6, {
                alpha: 1
            })
        };
        this.disableForGood = function() {
            s.isDisabledForGood_bl = true;
            s.setButtonMode(false)
        };
        this.enableForGood = function() {
            s.isDisabledForGood_bl = false;
            s.setButtonMode(true)
        };
        this.showDisabledState = function() {
            if (s.d_sdo.x != 0) s.d_sdo.setX(0)
        };
        this.hideDisabledState = function() {
            if (s.d_sdo.x != -100) s.d_sdo.setX(-100)
        };
        this.show = function() {
            if (s.isShowed_bl) return;
            s.isShowed_bl = true;
            MUSICTweenMax.killTweensOf(s);
            if (!MUSICUtils.isIEAndLessThen9) {
                if (MUSICUtils.isIEWebKit) {
                    MUSICTweenMax.killTweensOf(s.n_sdo);
                    s.n_sdo.setScale2(0);
                    MUSICTweenMax.to(s.n_sdo, .8, {
                        scale: 1,
                        delay: .4,
                        onStart: function() {
                            s.setVisible(true)
                        },
                        ease: Elastic.easeOut
                    })
                } else {
                    s.setScale2(0);
                    MUSICTweenMax.to(s, .8, {
                        scale: 1,
                        delay: .4,
                        onStart: function() {
                            s.setVisible(true)
                        },
                        ease: Elastic.easeOut
                    })
                }
            } else if (MUSICUtils.isIEAndLessThen9) {
                s.setVisible(true)
            } else {
                s.setAlpha(0);
                MUSICTweenMax.to(s, .4, {
                    alpha: 1,
                    delay: .4
                });
                s.setVisible(true)
            }
        };
        this.hide = function(e) {
            if (!s.isShowed_bl) return;
            s.isShowed_bl = false;
            MUSICTweenMax.killTweensOf(s);
            MUSICTweenMax.killTweensOf(s.n_sdo);
            s.setVisible(false)
        };
        s.init()
    };
    t.setPrototype = function() {
        t.prototype = null;
        t.prototype = new MUSICDisplayObject("div")
    };
    t.CLICK = "onClick";
    t.MOUSE_OVER = "onMouseOver";
    t.MOUSE_OUT = "onMouseOut";
    t.MOUSE_UP = "onMouseDown";
    t.prototype = null;
    e.MUSICSimpleButton = t
})(window);
(function(e) {
    var t = function(e, n, r, i) {
        var s = this;
        var o = t.prototype;
        this.nImg_img = e;
        this.n_do;
        this.s_do;
        this.sImgPath_str = n;
        this.buttonWidth = s.nImg_img.width;
        this.buttonHeight = s.nImg_img.height;
        this.isMobile_bl = MUSICUtils.isMobile;
        this.hasPointerEvent_bl = MUSICUtils.hasPointerEvent;
        this.isDisabled_bl = false;
        this.init = function() {
            s.setupMainContainers();
            s.setWidth(s.buttonWidth);
            s.setHeight(s.buttonHeight);
            s.setButtonMode(true)
        };
        this.setupMainContainers = function() {
            s.n_do = new MUSICDisplayObject("img");
            var e = new Image;
            e.src = s.nImg_img.src;
            s.n_do.setScreen(e);
            s.n_do.setWidth(s.buttonWidth);
            s.n_do.setHeight(s.buttonHeight);
            s.s_do = new MUSICDisplayObject("img");
            var t = new Image;
            t.src = s.sImgPath_str;
            s.s_do.setScreen(t);
            s.s_do.setWidth(s.buttonWidth);
            s.s_do.setHeight(s.buttonHeight);
            s.addChild(s.s_do);
            s.addChild(s.n_do);
            s.screen.onmouseover = s.onMouseOver;
            s.screen.onmouseout = s.onMouseOut;
            s.screen.onclick = s.onClick
        };
        this.onMouseOver = function(e) {
            MUSICTweenMax.to(s.n_do, .9, {
                alpha: 0,
                ease: Expo.easeOut
            })
        };
        this.onMouseOut = function(e) {
            MUSICTweenMax.to(s.n_do, .9, {
                alpha: 1,
                ease: Expo.easeOut
            })
        };
        this.onClick = function(e) {
            s.dispatchEvent(t.CLICK)
        };
        this.destroy = function() {
            if (s.n_do) {
                MUSICTweenMax.killTweensOf(s.n_do);
                s.n_do.destroy();
                s.s_do.destroy()
            }
            s.n_do = null;
            s.s_do = null;
            s = null;
            o = null;
            t.prototype = null
        };
        s.init()
    };
    t.setPrototype = function() {
        t.prototype = null;
        t.prototype = new MUSICDisplayObject("div", "relative")
    };
    t.CLICK = "onClick";
    t.prototype = null;
    e.MUSICSimpleSizeButton = t
})(window);
(function(e) {
    var t = function(n, r, i, s, o, u, a) {
        var f = this;
        var l = t.prototype;
        this.buttonRef_do = n;
        this.bkPath_str = r;
        this.pointerPath_str = i;
        this.text_do = null;
        this.pointer_do = null;
        this.pointerUp_do = null;
        this.fontColor_str = u;
        this.toopTipPointerUp_str = s;
        this.pointerWidth = 7;
        this.pointerHeight = 4;
        this.showWithDelayId_to;
        this.isMobile_bl = MUSICUtils.isMobile;
        this.isShowed_bl = true;
        this.init = function() {
            f.setOverflow("visible");
            f.setupMainContainers();
            f.hide();
            f.getStyle().background = "url('" + f.bkPath_str + "')";
            f.getStyle().zIndex = 9999999999
        };
        this.setupMainContainers = function() {
            f.text_do = new MUSICDisplayObject("div");
            f.text_do.hasTransform3d_bl = false;
            f.text_do.hasTransform2d_bl = false;
            f.text_do.setBackfaceVisibility();
            f.text_do.setDisplay("inline");
            f.text_do.getStyle().fontFamily = "Arial";
            f.text_do.getStyle().fontSize = "12px";
            f.text_do.getStyle().color = f.fontColor_str;
            f.text_do.getStyle().whiteSpace = "nowrap";
            f.text_do.getStyle().fontSmoothing = "antialiased";
            f.text_do.getStyle().webkitFontSmoothing = "antialiased";
            f.text_do.getStyle().textRendering = "optimizeLegibility";
            f.text_do.getStyle().padding = "6px";
            f.text_do.getStyle().paddingTop = "4px";
            f.text_do.getStyle().paddingBottom = "4px";
            f.setLabel();
            f.addChild(f.text_do);
            var e = new Image;
            e.src = f.pointerPath_str;
            f.pointer_do = new MUSICDisplayObject("img");
            f.pointer_do.setScreen(e);
            f.pointer_do.setWidth(f.pointerWidth);
            f.pointer_do.setHeight(f.pointerHeight);
            f.addChild(f.pointer_do);
            var t = new Image;
            t.src = f.toopTipPointerUp_str;
            f.pointerUp_do = new MUSICDisplayObject("img");
            f.pointerUp_do.setScreen(t);
            f.pointerUp_do.setWidth(f.pointerWidth);
            f.pointerUp_do.setHeight(f.pointerHeight);
            f.addChild(f.pointerUp_do)
        };
        this.setLabel = function(e) {
            f.text_do.setInnerHTML(o);
            setTimeout(function() {
                if (f == null) return;
                f.setWidth(f.text_do.getWidth());
                f.setHeight(f.text_do.getHeight());
                f.positionPointer()
            }, 50)
        };
        this.positionPointer = function(e, t) {
            var n;
            var r;
            if (!e) e = 0;
            n = parseInt((f.w - f.pointerWidth) / 2) + e;
            if (t) {
                r = -3;
                f.pointerUp_do.setX(n);
                f.pointerUp_do.setY(r);
                f.pointer_do.setX(0);
                f.pointer_do.setY(0)
            } else {
                r = f.h;
                f.pointer_do.setX(n);
                f.pointer_do.setY(r);
                f.pointerUp_do.setX(0);
                f.pointerUp_do.setY(0)
            }
        };
        this.show = function() {
            if (f.isShowed_bl) return;
            f.isShowed_bl = true;
            MUSICTweenMax.killTweensOf(f);
            clearTimeout(f.showWithDelayId_to);
            if (e.addEventListener) {
                e.addEventListener("mousemove", f.moveHandler)
            } else if (document.attachEvent) {
                document.detachEvent("onmousemove", f.moveHandler);
                document.attachEvent("onmousemove", f.moveHandler)
            }
        };
        this.showFinal = function() {
            f.setVisible(true);
            f.setAlpha(0);
            MUSICTweenMax.to(f, .4, {
                alpha: 1,
                onComplete: function() {
                    f.setVisible(true)
                },
                ease: Quart.easeOut
            })
        };
        this.moveHandler = function(e) {
            var t = MUSICUtils.getViewportMouseCoordinates(e);
            if (!MUSICUtils.hitTest(f.buttonRef_do.screen, t.screenX, t.screenY)) f.hide()
        };
        this.hide = function() {
            if (!f.isShowed_bl) return;
            clearTimeout(f.showWithDelayId_to);
            if (e.removeEventListener) {
                e.removeEventListener("mousemove", f.moveHandler)
            } else if (document.detachEvent) {
                document.detachEvent("onmousemove", f.moveHandler)
            }
            MUSICTweenMax.killTweensOf(f);
            f.setVisible(false);
            f.isShowed_bl = false
        };
        this.init()
    };
    t.setPrototype = function() {
        t.prototype = null;
        t.prototype = new MUSICDisplayObject("div", "fixed")
    };
    t.CLICK = "onClick";
    t.MOUSE_DOWN = "onMouseDown";
    t.prototype = null;
})(window);
