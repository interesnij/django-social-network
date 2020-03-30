 !window.FWDAnimation) {
    var _fwd_gsScope = "undefined" != typeof fwd_module && fwd_module.exports && "undefined" != typeof fwd_global ? fwd_global : this || window;
    (_fwd_gsScope._fwd_gsQueue || (_fwd_gsScope._fwd_gsQueue = [])).push(function() {
            "use strict";

            function g(e, t, s, o) {
                s === o && (s = o - (o - t) / 1e6), e === t && (t = e + (s - e) / 1e6), this.a = e, this.b = t, this.c = s, this.d = o, this.da = o - e, this.ca = s - e, this.ba = t - e
            }

            function S(e, t, s, o) {
                var i = {
                        a: e
                    },
                    l = {},
                    n = {},
                    a = {
                        c: o
                    },
                    r = (e + t) / 2,
                    d = (t + s) / 2,
                    u = (s + o) / 2,
                    h = (r + d) / 2,
                    c = (d + u) / 2,
                    _ = (c - h) / 8;
                return i.b = r + (e - r) / 4, l.b = h + _, i.c = l.a = (i.b + l.b) / 2, l.c = n.a = (h + c) / 2, n.b = c - _, a.b = u + (o - u) / 4, n.c = a.a = (n.b + a.b) / 2, [i, l, n, a]
            }

            function b(e, t, s, o, i) {
                var l, n, a, r, d, u, h, c, _, f, p, m, b, g = e.length - 1,
                    y = 0,
                    v = e[0].a;
                for (l = 0; l < g; l++) n = (d = e[y]).a, a = d.d, r = e[y + 1].d, c = i ? (p = P[l], b = ((m = T[l]) + p) * t * .25 / (o ? .5 : B[l] || .5), a - ((u = a - (a - n) * (o ? .5 * t : 0 !== p ? b / p : 0)) + (((h = a + (r - a) * (o ? .5 * t : 0 !== m ? b / m : 0)) - u) * (3 * p / (p + m) + .5) / 4 || 0))) : a - ((u = a - (a - n) * t * .5) + (h = a + (r - a) * t * .5)) / 2, u += c, h += c, d.c = _ = u, d.b = 0 !== l ? v : v = d.a + .6 * (d.c - d.a), d.da = a - n, d.ca = _ - n, d.ba = v - n, s ? (f = S(n, v, _, a), e.splice(y, 1, f[0], f[1], f[2], f[3]), y += 4) : y++, v = h;
                (d = e[y]).b = v, d.c = v + .4 * (d.d - v), d.da = d.d - d.a, d.ca = d.c - d.a, d.ba = v - d.a, s && (f = S(d.a, v, d.c, d.d), e.splice(y, 1, f[0], f[1], f[2], f[3]))
            }

            function y(e, t, s, o) {
                var i, l, n, a, r, d, u = [];
                if (o)
                    for (l = (e = [o].concat(e)).length; - 1 < --l;) "string" == typeof(d = e[l][t]) && "=" === d.charAt(1) && (e[l][t] = o[t] + Number(d.charAt(0) + d.substr(2)));
                if ((i = e.length - 2) < 0) return u[0] = new g(e[0][t], 0, 0, e[i < -1 ? 0 : 1][t]), u;
                for (l = 0; l < i; l++) n = e[l][t], a = e[l + 1][t], u[l] = new g(n, 0, 0, a), s && (r = e[l + 2][t], P[l] = (P[l] || 0) + (a - n) * (a - n), T[l] = (T[l] || 0) + (r - a) * (r - a));
                return u[l] = new g(e[l][t], 0, 0, e[l + 1][t]), u
            }

            function _(e, t, s, o, i, l) {
                var n, a, r, d, u, h, c, _, f = {},
                    p = [],
                    m = l || e[0];
                for (a in i = "string" == typeof i ? "," + i + "," : ",x,y,z,left,top,right,bottom,marginTop,marginLeft,marginRight,marginBottom,paddingLeft,paddingTop,paddingRight,paddingBottom,backgroundPosition,backgroundPosition_y,", null == t && (t = 1), e[0]) p.push(a);
                if (1 < e.length) {
                    for (_ = e[e.length - 1], c = !0, n = p.length; - 1 < --n;)
                        if (a = p[n], .05 < Math.abs(m[a] - _[a])) {
                            c = !1;
                            break
                        } c && (e = e.concat(), l && e.unshift(l), e.push(e[1]), l = e[e.length - 3])
                }
                for (P.length = T.length = B.length = 0, n = p.length; - 1 < --n;) a = p[n], v[a] = -1 !== i.indexOf("," + a + ","), f[a] = y(e, a, v[a], l);
                for (n = P.length; - 1 < --n;) P[n] = Math.sqrt(P[n]), T[n] = Math.sqrt(T[n]);
                if (!o) {
                    for (n = p.length; - 1 < --n;)
                        if (v[a])
                            for (h = (r = f[p[n]]).length - 1, d = 0; d < h; d++) u = r[d + 1].da / T[d] + r[d].da / P[d] || 0, B[d] = (B[d] || 0) + u * u;
                    for (n = B.length; - 1 < --n;) B[n] = Math.sqrt(B[n])
                }
                for (n = p.length, d = s ? 4 : 1; - 1 < --n;) r = f[a = p[n]], b(r, t, s, o, v[a]), c && (r.splice(0, d), r.splice(r.length - d, d));
                return f
            }

            function f(e, t, s) {
                for (var o, i, l, n, a, r, d, u, h, c, _, f = 1 / s, p = e.length; - 1 < --p;)
                    for (l = (c = e[p]).a, n = c.d - l, a = c.c - l, r = c.b - l, o = i = 0, u = 1; u <= s; u++) o = i - (i = ((d = f * u) * d * n + 3 * (h = 1 - d) * (d * a + h * r)) * d), t[_ = p * s + u - 1] = (t[_] || 0) + o * o
            }
            var w, P, T, B, v, s, m, e, t, o;

            function r(e) {
                for (; e;) e.f || e.blob || (e.m = Math.round), e = e._next
            }
            _fwd_gsScope.FWDFWD_gsDefine("FWDAnimation", ["core.FWDAnimation", "core.FWDSimpleTimeline", "FWDTweenLite"], function(m, u, b) {
                function g(e) {
                    var t, s = [],
                        o = e.length;
                    for (t = 0; t !== o; s.push(e[t++]));
                    return s
                }

                function y(e, t, s) {
                    var o, i, l = e.cycle;
                    for (o in l) i = l[o], e[o] = "function" == typeof i ? i(s, t[s]) : i[s % i.length];
                    delete e.cycle
                }
                m = function(e, t, s) {
                    b.call(this, e, t, s), this._cycle = 0, this._yoyo = !0 === this.vars.yoyo, this._repeat = this.vars.repeat || 0, this._repeatDelay = this.vars.repeatDelay || 0, this._dirty = !0, this.render = m.prototype.render
                };
                var v = 1e-10,
                    S = b._internals,
                    P = S.isSelector,
                    w = S.isArray,
                    e = m.prototype = b.to({}, .1, {}),
                    T = [];
                m.version = "1.19.0", e.constructor = m, e.kill()._gc = !1, m.killTweensOf = m.killDelayedCallsTo = b.killTweensOf, m.getTweensOf = b.getTweensOf, m.lagSmoothing = b.lagSmoothing, m.ticker = b.ticker, m.render = b.render, e.invalidate = function() {
                    return this._yoyo = !0 === this.vars.yoyo, this._repeat = this.vars.repeat || 0, this._repeatDelay = this.vars.repeatDelay || 0, this._uncache(!0), b.prototype.invalidate.call(this)
                }, e.updateTo = function(e, t) {
                    var s, o = this.ratio,
                        i = this.vars.immediateRender || e.immediateRender;
                    for (s in t && this._startTime < this._timeline._time && (this._startTime = this._timeline._time, this._uncache(!1), this._gc ? this._enabled(!0, !1) : this._timeline.insert(this, this._startTime - this._delay)), e) this.vars[s] = e[s];
                    if (this._initted || i)
                        if (t) this._initted = !1, i && this.render(0, !0, !0);
                        else if (this._gc && this._enabled(!0, !1), this._notifyPluginsOfEnabled && this._firstPT && b._onPluginEvent("_onDisable", this), .998 < this._time / this._duration) {
                        var l = this._totalTime;
                        this.render(0, !0, !1), this._initted = !1, this.render(l, !0, !1)
                    } else if (this._initted = !1, this._init(), 0 < this._time || i)
                        for (var n, a = 1 / (1 - o), r = this._firstPT; r;) n = r.s + r.c, r.c *= a, r.s = n - r.c, r = r._next;
                    return this
                }, e.render = function(e, t, s) {
                    this._initted || 0 === this._duration && this.vars.repeat && this.invalidate();
                    var o, i, l, n, a, r, d, u, h = this._dirty ? this.totalDuration() : this._totalDuration,
                        c = this._time,
                        _ = this._totalTime,
                        f = this._cycle,
                        p = this._duration,
                        m = this._rawPrevTime;
                    if (h - 1e-7 <= e ? (this._totalTime = h, this._cycle = this._repeat, this._yoyo && 0 != (1 & this._cycle) ? (this._time = 0, this.ratio = this._ease._calcEnd ? this._ease.getRatio(0) : 0) : (this._time = p, this.ratio = this._ease._calcEnd ? this._ease.getRatio(1) : 1), this._reversed || (o = !0, i = "onComplete", s = s || this._timeline.autoRemoveChildren), 0 === p && (!this._initted && this.vars.lazy && !s || (this._startTime === this._timeline._duration && (e = 0), (m < 0 || e <= 0 && -1e-7 <= e || m === v && "isPause" !== this.data) && m !== e && (s = !0, v < m && (i = "onReverseComplete")), this._rawPrevTime = u = !t || e || m === e ? e : v))) : e < 1e-7 ? (this._totalTime = this._time = this._cycle = 0, this.ratio = this._ease._calcEnd ? this._ease.getRatio(0) : 0, (0 !== _ || 0 === p && 0 < m) && (i = "onReverseComplete", o = this._reversed), e < 0 && (this._active = !1, 0 === p && (!this._initted && this.vars.lazy && !s || (0 <= m && (s = !0), this._rawPrevTime = u = !t || e || m === e ? e : v))), this._initted || (s = !0)) : (this._totalTime = this._time = e, 0 !== this._repeat && (n = p + this._repeatDelay, this._cycle = this._totalTime / n >> 0, 0 !== this._cycle && this._cycle === this._totalTime / n && _ <= e && this._cycle--, this._time = this._totalTime - this._cycle * n, this._yoyo && 0 != (1 & this._cycle) && (this._time = p - this._time), this._time > p ? this._time = p : this._time < 0 && (this._time = 0)), this._easeType ? (a = this._time / p, (1 === (r = this._easeType) || 3 === r && .5 <= a) && (a = 1 - a), 3 === r && (a *= 2), 1 === (d = this._easePower) ? a *= a : 2 === d ? a *= a * a : 3 === d ? a *= a * a * a : 4 === d && (a *= a * a * a * a), 1 === r ? this.ratio = 1 - a : 2 === r ? this.ratio = a : this._time / p < .5 ? this.ratio = a / 2 : this.ratio = 1 - a / 2) : this.ratio = this._ease.getRatio(this._time / p)), c !== this._time || s || f !== this._cycle) {
                        if (!this._initted) {
                            if (this._init(), !this._initted || this._gc) return;
                            if (!s && this._firstPT && (!1 !== this.vars.lazy && this._duration || this.vars.lazy && !this._duration)) return this._time = c, this._totalTime = _, this._rawPrevTime = m, this._cycle = f, S.lazyTweens.push(this), void(this._lazy = [e, t]);
                            this._time && !o ? this.ratio = this._ease.getRatio(this._time / p) : o && this._ease._calcEnd && (this.ratio = this._ease.getRatio(0 === this._time ? 0 : 1))
                        }
                        for (!1 !== this._lazy && (this._lazy = !1), this._active || !this._paused && this._time !== c && 0 <= e && (this._active = !0), 0 === _ && (2 === this._initted && 0 < e && this._init(), this._startAt && (0 <= e ? this._startAt.render(e, t, s) : i = i || "_dummyGS"), this.vars.onStart && (0 === this._totalTime && 0 !== p || t || this._callback("onStart"))), l = this._firstPT; l;) {
                            if (l.f) l.t[l.p](l.c * this.ratio + l.s);
                            else {
                                var b = l.c * this.ratio + l.s;
                                "x" == l.p ? l.t.setX(b) : "y" == l.p ? l.t.setY(b) : "z" == l.p ? l.t.setZ(b) : "angleX" == l.p ? l.t.setAngleX(b) : "angleY" == l.p ? l.t.setAngleY(b) : "angleZ" == l.p ? l.t.setAngleZ(b) : "w" == l.p ? l.t.setWidth(b) : "h" == l.p ? l.t.setHeight(b) : "alpha" == l.p ? l.t.setAlpha(b) : "scale" == l.p ? l.t.setScale2(b) : l.t[l.p] = b
                            }
                            l = l._next
                        }
                        this._onUpdate && (e < 0 && this._startAt && this._startTime && this._startAt.render(e, t, s), t || this._totalTime === _ && !i || this._callback("onUpdate")), this._cycle !== f && (t || this._gc || this.vars.onRepeat && this._callback("onRepeat")), i && (this._gc && !s || (e < 0 && this._startAt && !this._onUpdate && this._startTime && this._startAt.render(e, t, s), o && (this._timeline.autoRemoveChildren && this._enabled(!1, !1), this._active = !1), !t && this.vars[i] && this._callback(i), 0 === p && this._rawPrevTime === v && u !== v && (this._rawPrevTime = 0)))
                    } else _ !== this._totalTime && this._onUpdate && (t || this._callback("onUpdate"))
                }, m.to = function(e, t, s) {
                    return new m(e, t, s)
                }, m.from = function(e, t, s) {
                    return s.runBackwards = !0, s.immediateRender = 0 != s.immediateRender, new m(e, t, s)
                }, m.fromTo = function(e, t, s, o) {
                    return o.startAt = s, o.immediateRender = 0 != o.immediateRender && 0 != s.immediateRender, new m(e, t, o)
                }, m.staggerTo = m.allTo = function(e, t, s, o, i, l, n) {
                    o = o || 0;

                    function a() {
                        s.onComplete && s.onComplete.apply(s.onCompleteScope || this, arguments), i.apply(n || s.callbackScope || this, l || T)
                    }
                    var r, d, u, h, c = 0,
                        _ = [],
                        f = s.cycle,
                        p = s.startAt && s.startAt.cycle;
                    for (w(e) || ("string" == typeof e && (e = b.selector(e) || e), P(e) && (e = g(e))), e = e || [], o < 0 && ((e = g(e)).reverse(), o *= -1), r = e.length - 1, u = 0; u <= r; u++) {
                        for (h in d = {}, s) d[h] = s[h];
                        if (f && (y(d, e, u), null != d.duration && (t = d.duration, delete d.duration)), p) {
                            for (h in p = d.startAt = {}, s.startAt) p[h] = s.startAt[h];
                            y(d.startAt, e, u)
                        }
                        d.delay = c + (d.delay || 0), u === r && i && (d.onComplete = a), _[u] = new m(e[u], t, d), c += o
                    }
                    return _
                }, m.staggerFrom = m.allFrom = function(e, t, s, o, i, l, n) {
                    return s.runBackwards = !0, s.immediateRender = 0 != s.immediateRender, m.staggerTo(e, t, s, o, i, l, n)
                }, m.staggerFromTo = m.allFromTo = function(e, t, s, o, i, l, n, a) {
                    return o.startAt = s, o.immediateRender = 0 != o.immediateRender && 0 != s.immediateRender, m.staggerTo(e, t, o, i, l, n, a)
                }, m.delayedCall = function(e, t, s, o, i) {
                    return new m(t, 0, {
                        delay: e,
                        onComplete: t,
                        onCompleteParams: s,
                        callbackScope: o,
                        onReverseComplete: t,
                        onReverseCompleteParams: s,
                        immediateRender: !1,
                        useFrames: i,
                        overwrite: 0
                    })
                }, m.set = function(e, t) {
                    return new m(e, 0, t)
                }, m.isTweening = function(e) {
                    return 0 < b.getTweensOf(e, !0).length
                };
                var l = function(e, t) {
                        for (var s = [], o = 0, i = e._first; i;) i instanceof b ? s[o++] = i : (t && (s[o++] = i), o = (s = s.concat(l(i, t))).length), i = i._next;
                        return s
                    },
                    h = m.getAllTweens = function(e) {
                        return l(m._rootTimeline, e).concat(l(m._rootFramesTimeline, e))
                    };
                m.killAll = function(e, t, s, o) {
                    null == t && (t = !0), null == s && (s = !0);
                    var i, l, n, a = h(0 != o),
                        r = a.length,
                        d = t && s && o;
                    for (n = 0; n < r; n++) l = a[n], (d || l instanceof u || (i = l.target === l.vars.onComplete) && s || t && !i) && (e ? l.totalTime(l._reversed ? 0 : l.totalDuration()) : l._enabled(!1, !1))
                }, m.killChildTweensOf = function(e, t) {
                    if (null != e) {
                        var s, o, i, l, n, a = S.tweenLookup;
                        if ("string" == typeof e && (e = b.selector(e) || e), P(e) && (e = g(e)), w(e))
                            for (l = e.length; - 1 < --l;) m.killChildTweensOf(e[l], t);
                        else {
                            for (i in s = [], a)
                                for (o = a[i].target.parentNode; o;) o === e && (s = s.concat(a[i].tweens)), o = o.parentNode;
                            for (n = s.length, l = 0; l < n; l++) t && s[l].totalTime(s[l].totalDuration()), s[l]._enabled(!1, !1)
                        }
                    }
                };

                function o(e, t, s, o) {
                    t = !1 !== t, s = !1 !== s;
                    for (var i, l, n = h(o = !1 !== o), a = t && s && o, r = n.length; - 1 < --r;) l = n[r], (a || l instanceof u || (i = l.target === l.vars.onComplete) && s || t && !i) && l.paused(e)
                }
                return m.pauseAll = function(e, t, s) {
                    o(!0, e, t, s)
                }, m.resumeAll = function(e, t, s) {
                    o(!1, e, t, s)
                }, m.globalTimeScale = function(e) {
                    var t = m._rootTimeline,
                        s = b.ticker.time;
                    return arguments.length ? (e = e || v, t._startTime = s - (s - t._startTime) * t._timeScale / e, t = m._rootFramesTimeline, s = b.ticker.frame, t._startTime = s - (s - t._startTime) * t._timeScale / e, t._timeScale = m._rootTimeline._timeScale = e, e) : t._timeScale
                }, e.progress = function(e, t) {
                    return arguments.length ? this.totalTime(this.duration() * (this._yoyo && 0 != (1 & this._cycle) ? 1 - e : e) + this._cycle * (this._duration + this._repeatDelay), t) : this._time / this.duration()
                }, e.totalProgress = function(e, t) {
                    return arguments.length ? this.totalTime(this.totalDuration() * e, t) : this._totalTime / this.totalDuration()
                }, e.time = function(e, t) {
                    return arguments.length ? (this._dirty && this.totalDuration(), e > this._duration && (e = this._duration), this._yoyo && 0 != (1 & this._cycle) ? e = this._duration - e + this._cycle * (this._duration + this._repeatDelay) : 0 !== this._repeat && (e += this._cycle * (this._duration + this._repeatDelay)), this.totalTime(e, t)) : this._time
                }, e.duration = function(e) {
                    return arguments.length ? m.prototype.duration.call(this, e) : this._duration
                }, e.totalDuration = function(e) {
                    return arguments.length ? -1 === this._repeat ? this : this.duration((e - this._repeat * this._repeatDelay) / (this._repeat + 1)) : (this._dirty && (this._totalDuration = -1 === this._repeat ? 999999999999 : this._duration * (this._repeat + 1) + this._repeatDelay * this._repeat, this._dirty = !1), this._totalDuration)
                }, e.repeat = function(e) {
                    return arguments.length ? (this._repeat = e, this._uncache(!0)) : this._repeat
                }, e.repeatDelay = function(e) {
                    return arguments.length ? (this._repeatDelay = e, this._uncache(!0)) : this._repeatDelay
                }, e.yoyo = function(e) {
                    return arguments.length ? (this._yoyo = e, this) : this._yoyo
                }, m
            }, !0), _fwd_gsScope.FWDFWD_gsDefine("FWDTimelineLite", ["core.FWDAnimation", "core.FWDSimpleTimeline", "FWDTweenLite"], function(u, h, c) {
                function _(e) {
                    h.call(this, e), this._labels = {}, this.autoRemoveChildren = !0 === this.vars.autoRemoveChildren, this.smoothChildTiming = !0 === this.vars.smoothChildTiming, this._sortChildren = !0, this._onUpdate = this.vars.onUpdate;
                    var t, s, o = this.vars;
                    for (s in o) t = o[s], y(t) && -1 !== t.join("").indexOf("{self}") && (o[s] = this._swapSelfInParams(t));
                    y(o.tweens) && this.add(o.tweens, 0, o.align, o.stagger)
                }

                function f(e) {
                    var t, s = {};
                    for (t in e) s[t] = e[t];
                    return s
                }

                function p(e, t, s) {
                    var o, i, l = e.cycle;
                    for (o in l) i = l[o], e[o] = "function" == typeof i ? i.call(t[s], s) : i[s % i.length];
                    delete e.cycle
                }

                function m(e) {
                    var t, s = [],
                        o = e.length;
                    for (t = 0; t !== o; s.push(e[t++]));
                    return s
                }
                var b = 1e-10,
                    e = c._internals,
                    t = _._internals = {},
                    g = e.isSelector,
                    y = e.isArray,
                    v = e.lazyTweens,
                    S = e.lazyRender,
                    n = _fwd_gsScope.FWDFWD_gsDefine.globals,
                    l = t.pauseCallback = function() {},
                    s = _.prototype = new h;
                return _.version = "1.19.0", s.constructor = _, s.kill()._gc = s._forcingPlayhead = s._hasPause = !1, s.to = function(e, t, s, o) {
                    var i = s.repeat && n.FWDAnimation || c;
                    return t ? this.add(new i(e, t, s), o) : this.set(e, s, o)
                }, s.from = function(e, t, s, o) {
                    return this.add((s.repeat && n.FWDAnimation || c).from(e, t, s), o)
                }, s.fromTo = function(e, t, s, o, i) {
                    var l = o.repeat && n.FWDAnimation || c;
                    return t ? this.add(l.fromTo(e, t, s, o), i) : this.set(e, o, i)
                }, s.staggerTo = function(e, t, s, o, i, l, n, a) {
                    var r, d, u = new _({
                            onComplete: l,
                            onCompleteParams: n,
                            callbackScope: a,
                            smoothChildTiming: this.smoothChildTiming
                        }),
                        h = s.cycle;
                    for ("string" == typeof e && (e = c.selector(e) || e), g(e = e || []) && (e = m(e)), (o = o || 0) < 0 && ((e = m(e)).reverse(), o *= -1), d = 0; d < e.length; d++)(r = f(s)).startAt && (r.startAt = f(r.startAt), r.startAt.cycle && p(r.startAt, e, d)), h && (p(r, e, d), null != r.duration && (t = r.duration, delete r.duration)), u.to(e[d], t, r, d * o);
                    return this.add(u, i)
                }, s.staggerFrom = function(e, t, s, o, i, l, n, a) {
                    return s.immediateRender = 0 != s.immediateRender, s.runBackwards = !0, this.staggerTo(e, t, s, o, i, l, n, a)
                }, s.staggerFromTo = function(e, t, s, o, i, l, n, a, r) {
                    return o.startAt = s, o.immediateRender = 0 != o.immediateRender && 0 != s.immediateRender, this.staggerTo(e, t, o, i, l, n, a, r)
                }, s.call = function(e, t, s, o) {
                    return this.add(c.delayedCall(0, e, t, s), o)
                }, s.set = function(e, t, s) {
                    return s = this._parseTimeOrLabel(s, 0, !0), null == t.immediateRender && (t.immediateRender = s === this._time && !this._paused), this.add(new c(e, 0, t), s)
                }, _.exportRoot = function(e, t) {
                    null == (e = e || {}).smoothChildTiming && (e.smoothChildTiming = !0);
                    var s, o, i = new _(e),
                        l = i._timeline;
                    for (null == t && (t = !0), l._remove(i, !0), i._startTime = 0, i._rawPrevTime = i._time = i._totalTime = l._time, s = l._first; s;) o = s._next, t && s instanceof c && s.target === s.vars.onComplete || i.add(s, s._startTime - s._delay), s = o;
                    return l.add(i, 0), i
                }, s.add = function(e, t, s, o) {
                    var i, l, n, a, r, d;
                    if ("number" != typeof t && (t = this._parseTimeOrLabel(t, 0, !0, e)), !(e instanceof u)) {
                        if (e instanceof Array || e && e.push && y(e)) {
                            for (s = s || "normal", o = o || 0, i = t, l = e.length, n = 0; n < l; n++) y(a = e[n]) && (a = new _({
                                tweens: a
                            })), this.add(a, i), "string" != typeof a && "function" != typeof a && ("sequence" === s ? i = a._startTime + a.totalDuration() / a._timeScale : "start" === s && (a._startTime -= a.delay())), i += o;
                            return this._uncache(!0)
                        }
                        if ("string" == typeof e) return this.addLabel(e, t);
                        if ("function" != typeof e) throw "Cannot add " + e + " into the timeline; it is not a tween, timeline, function, or string.";
                        e = c.delayedCall(0, e)
                    }
                    if (h.prototype.add.call(this, e, t), (this._gc || this._time === this._duration) && !this._paused && this._duration < this.duration())
                        for (d = (r = this).rawTime() > e._startTime; r._timeline;) d && r._timeline.smoothChildTiming ? r.totalTime(r._totalTime, !0) : r._gc && r._enabled(!0, !1), r = r._timeline;
                    return this
                }, s.remove = function(e) {
                    if (e instanceof u) {
                        this._remove(e, !1);
                        var t = e._timeline = e.vars.useFrames ? u._rootFramesTimeline : u._rootTimeline;
                        return e._startTime = (e._paused ? e._pauseTime : t._time) - (e._reversed ? e.totalDuration() - e._totalTime : e._totalTime) / e._timeScale, this
                    }
                    if (e instanceof Array || e && e.push && y(e)) {
                        for (var s = e.length; - 1 < --s;) this.remove(e[s]);
                        return this
                    }
                    return "string" == typeof e ? this.removeLabel(e) : this.kill(null, e)
                }, s._remove = function(e, t) {
                    h.prototype._remove.call(this, e, t);
                    var s = this._last;
                    return s ? this._time > s._startTime + s._totalDuration / s._timeScale && (this._time = this.duration(), this._totalTime = this._totalDuration) : this._time = this._totalTime = this._duration = this._totalDuration = 0, this
                }, s.append = function(e, t) {
                    return this.add(e, this._parseTimeOrLabel(null, t, !0, e))
                }, s.insert = s.insertMultiple = function(e, t, s, o) {
                    return this.add(e, t || 0, s, o)
                }, s.appendMultiple = function(e, t, s, o) {
                    return this.add(e, this._parseTimeOrLabel(null, t, !0, e), s, o)
                }, s.addLabel = function(e, t) {
                    return this._labels[e] = this._parseTimeOrLabel(t), this
                }, s.addPause = function(e, t, s, o) {
                    var i = c.delayedCall(0, l, s, o || this);
                    return i.vars.onComplete = i.vars.onReverseComplete = t, i.data = "isPause", this._hasPause = !0, this.add(i, e)
                }, s.removeLabel = function(e) {
                    return delete this._labels[e], this
                }, s.getLabelTime = function(e) {
                    return null != this._labels[e] ? this._labels[e] : -1
                }, s._parseTimeOrLabel = function(e, t, s, o) {
                    var i;
                    if (o instanceof u && o.timeline === this) this.remove(o);
                    else if (o && (o instanceof Array || o.push && y(o)))
                        for (i = o.length; - 1 < --i;) o[i] instanceof u && o[i].timeline === this && this.remove(o[i]);
                    if ("string" == typeof t) return this._parseTimeOrLabel(t, s && "number" == typeof e && null == this._labels[t] ? e - this.duration() : 0, s);
                    if (t = t || 0, "string" != typeof e || !isNaN(e) && null == this._labels[e]) null == e && (e = this.duration());
                    else {
                        if (-1 === (i = e.indexOf("="))) return null == this._labels[e] ? s ? this._labels[e] = this.duration() + t : t : this._labels[e] + t;
                        t = parseInt(e.charAt(i - 1) + "1", 10) * Number(e.substr(i + 1)), e = 1 < i ? this._parseTimeOrLabel(e.substr(0, i - 1), 0, s) : this.duration()
                    }
                    return Number(e) + t
                }, s.seek = function(e, t) {
                    return this.totalTime("number" == typeof e ? e : this._parseTimeOrLabel(e), !1 !== t)
                }, s.stop = function() {
                    return this.paused(!0)
                }, s.gotoAndPlay = function(e, t) {
                    return this.play(e, t)
                }, s.gotoAndStop = function(e, t) {
                    return this.pause(e, t)
                }, s.render = function(e, t, s) {
                    this._gc && this._enabled(!0, !1);
                    var o, i, l, n, a, r, d, u = this._dirty ? this.totalDuration() : this._totalDuration,
                        h = this._time,
                        c = this._startTime,
                        _ = this._timeScale,
                        f = this._paused;
                    if (u - 1e-7 <= e) this._totalTime = this._time = u, this._reversed || this._hasPausedChild() || (i = !0, n = "onComplete", a = !!this._timeline.autoRemoveChildren, 0 === this._duration && (e <= 0 && -1e-7 <= e || this._rawPrevTime < 0 || this._rawPrevTime === b) && this._rawPrevTime !== e && this._first && (a = !0, this._rawPrevTime > b && (n = "onReverseComplete"))), this._rawPrevTime = this._duration || !t || e || this._rawPrevTime === e ? e : b, e = u + 1e-4;
                    else if (e < 1e-7)
                        if (this._totalTime = this._time = 0, (0 !== h || 0 === this._duration && this._rawPrevTime !== b && (0 < this._rawPrevTime || e < 0 && 0 <= this._rawPrevTime)) && (n = "onReverseComplete", i = this._reversed), e < 0) this._active = !1, this._timeline.autoRemoveChildren && this._reversed ? (a = i = !0, n = "onReverseComplete") : 0 <= this._rawPrevTime && this._first && (a = !0), this._rawPrevTime = e;
                        else {
                            if (this._rawPrevTime = this._duration || !t || e || this._rawPrevTime === e ? e : b, 0 === e && i)
                                for (o = this._first; o && 0 === o._startTime;) o._duration || (i = !1), o = o._next;
                            e = 0, this._initted || (a = !0)
                        }
                    else {
                        if (this._hasPause && !this._forcingPlayhead && !t) {
                            if (h <= e)
                                for (o = this._first; o && o._startTime <= e && !r;) o._duration || "isPause" !== o.data || o.ratio || 0 === o._startTime && 0 === this._rawPrevTime || (r = o), o = o._next;
                            else
                                for (o = this._last; o && o._startTime >= e && !r;) o._duration || "isPause" === o.data && 0 < o._rawPrevTime && (r = o), o = o._prev;
                            r && (this._time = e = r._startTime, this._totalTime = e + this._cycle * (this._totalDuration + this._repeatDelay))
                        }
                        this._totalTime = this._time = this._rawPrevTime = e
                    }
                    if (this._time !== h && this._first || s || a || r) {
                        if (this._initted || (this._initted = !0), this._active || !this._paused && this._time !== h && 0 < e && (this._active = !0), 0 === h && this.vars.onStart && (0 === this._time && this._duration || t || this._callback("onStart")), h <= (d = this._time))
                            for (o = this._first; o && (l = o._next, d === this._time && (!this._paused || f));)(o._active || o._startTime <= d && !o._paused && !o._gc) && (r === o && this.pause(), o._reversed ? o.render((o._dirty ? o.totalDuration() : o._totalDuration) - (e - o._startTime) * o._timeScale, t, s) : o.render((e - o._startTime) * o._timeScale, t, s)), o = l;
                        else
                            for (o = this._last; o && (l = o._prev, d === this._time && (!this._paused || f));) {
                                if (o._active || o._startTime <= h && !o._paused && !o._gc) {
                                    if (r === o) {
                                        for (r = o._prev; r && r.endTime() > this._time;) r.render(r._reversed ? r.totalDuration() - (e - r._startTime) * r._timeScale : (e - r._startTime) * r._timeScale, t, s), r = r._prev;
                                        r = null, this.pause()
                                    }
                                    o._reversed ? o.render((o._dirty ? o.totalDuration() : o._totalDuration) - (e - o._startTime) * o._timeScale, t, s) : o.render((e - o._startTime) * o._timeScale, t, s)
                                }
                                o = l
                            }
                        this._onUpdate && (t || (v.length && S(), this._callback("onUpdate"))), n && (this._gc || c !== this._startTime && _ === this._timeScale || (0 === this._time || u >= this.totalDuration()) && (i && (v.length && S(), this._timeline.autoRemoveChildren && this._enabled(!1, !1), this._active = !1), !t && this.vars[n] && this._callback(n)))
                    }
                }, s._hasPausedChild = function() {
                    for (var e = this._first; e;) {
                        if (e._paused || e instanceof _ && e._hasPausedChild()) return !0;
                        e = e._next
                    }
                    return !1
                }, s.getChildren = function(e, t, s, o) {
                    o = o || -9999999999;
                    for (var i = [], l = this._first, n = 0; l;) l._startTime < o || (l instanceof c ? !1 !== t && (i[n++] = l) : (!1 !== s && (i[n++] = l), !1 !== e && (n = (i = i.concat(l.getChildren(!0, t, s))).length))), l = l._next;
                    return i
                }, s.getTweensOf = function(e, t) {
                    var s, o, i = this._gc,
                        l = [],
                        n = 0;
                    for (i && this._enabled(!0, !0), o = (s = c.getTweensOf(e)).length; - 1 < --o;)(s[o].timeline === this || t && this._contains(s[o])) && (l[n++] = s[o]);
                    return i && this._enabled(!1, !0), l
                }, s.recent = function() {
                    return this._recent
                }, s._contains = function(e) {
                    for (var t = e.timeline; t;) {
                        if (t === this) return !0;
                        t = t.timeline
                    }
                    return !1
                }, s.shiftChildren = function(e, t, s) {
                    s = s || 0;
                    for (var o, i = this._first, l = this._labels; i;) i._startTime >= s && (i._startTime += e), i = i._next;
                    if (t)
                        for (o in l) l[o] >= s && (l[o] += e);
                    return this._uncache(!0)
                }, s._kill = function(e, t) {
                    if (!e && !t) return this._enabled(!1, !1);
                    for (var s = t ? this.getTweensOf(t) : this.getChildren(!0, !0, !1), o = s.length, i = !1; - 1 < --o;) s[o]._kill(e, t) && (i = !0);
                    return i
                }, s.clear = function(e) {
                    var t = this.getChildren(!1, !0, !0),
                        s = t.length;
                    for (this._time = this._totalTime = 0; - 1 < --s;) t[s]._enabled(!1, !1);
                    return !1 !== e && (this._labels = {}), this._uncache(!0)
                }, s.invalidate = function() {
                    for (var e = this._first; e;) e.invalidate(), e = e._next;
                    return u.prototype.invalidate.call(this)
                }, s._enabled = function(e, t) {
                    if (e === this._gc)
                        for (var s = this._first; s;) s._enabled(e, !0), s = s._next;
                    return h.prototype._enabled.call(this, e, t)
                }, s.totalTime = function(e, t, s) {
                    this._forcingPlayhead = !0;
                    var o = u.prototype.totalTime.apply(this, arguments);
                    return this._forcingPlayhead = !1, o
                }, s.duration = function(e) {
                    return arguments.length ? (0 !== this.duration() && 0 !== e && this.timeScale(this._duration / e), this) : (this._dirty && this.totalDuration(), this._duration)
                }, s.totalDuration = function(e) {
                    if (arguments.length) return e && this.totalDuration() ? this.timeScale(this._totalDuration / e) : this;
                    if (this._dirty) {
                        for (var t, s, o = 0, i = this._last, l = 999999999999; i;) t = i._prev, i._dirty && i.totalDuration(), i._startTime > l && this._sortChildren && !i._paused ? this.add(i, i._startTime - i._delay) : l = i._startTime, i._startTime < 0 && !i._paused && (o -= i._startTime, this._timeline.smoothChildTiming && (this._startTime += i._startTime / this._timeScale), this.shiftChildren(-i._startTime, !1, -9999999999), l = 0), o < (s = i._startTime + i._totalDuration / i._timeScale) && (o = s), i = t;
                        this._duration = this._totalDuration = o, this._dirty = !1
                    }
                    return this._totalDuration
                }, s.paused = function(e) {
                    if (!e)
                        for (var t = this._first, s = this._time; t;) t._startTime === s && "isPause" === t.data && (t._rawPrevTime = 0), t = t._next;
                    return u.prototype.paused.apply(this, arguments)
                }, s.usesFrames = function() {
                    for (var e = this._timeline; e._timeline;) e = e._timeline;
                    return e === u._rootFramesTimeline
                }, s.rawTime = function() {
                    return this._paused ? this._totalTime : (this._timeline.rawTime() - this._startTime) * this._timeScale
                }, _
            }, !0), _fwd_gsScope.FWDFWD_gsDefine("TimelineMax", ["FWDTimelineLite", "FWDTweenLite", "easing.Ease"], function(t, a, e) {
                function s(e) {
                    t.call(this, e), this._repeat = this.vars.repeat || 0, this._repeatDelay = this.vars.repeatDelay || 0, this._cycle = 0, this._yoyo = !0 === this.vars.yoyo, this._dirty = !0
                }
                var D = 1e-10,
                    o = a._internals,
                    W = o.lazyTweens,
                    F = o.lazyRender,
                    r = _fwd_gsScope.FWDFWD_gsDefine.globals,
                    d = new e(null, null, 1, 0),
                    i = s.prototype = new t;
                return i.constructor = s, i.kill()._gc = !1, s.version = "1.19.0", i.invalidate = function() {
                    return this._yoyo = !0 === this.vars.yoyo, this._repeat = this.vars.repeat || 0, this._repeatDelay = this.vars.repeatDelay || 0, this._uncache(!0), t.prototype.invalidate.call(this)
                }, i.addCallback = function(e, t, s, o) {
                    return this.add(a.delayedCall(0, e, s, o), t)
                }, i.removeCallback = function(e, t) {
                    if (e)
                        if (null == t) this._kill(null, e);
                        else
                            for (var s = this.getTweensOf(e, !1), o = s.length, i = this._parseTimeOrLabel(t); - 1 < --o;) s[o]._startTime === i && s[o]._enabled(!1, !1);
                    return this
                }, i.removePause = function(e) {
                    return this.removeCallback(t._internals.pauseCallback, e)
                }, i.tweenTo = function(e, t) {
                    t = t || {};
                    var s, o, i, l = {
                            ease: d,
                            useFrames: this.usesFrames(),
                            immediateRender: !1
                        },
                        n = t.repeat && r.FWDAnimation || a;
                    for (o in t) l[o] = t[o];
                    return l.time = this._parseTimeOrLabel(e), s = Math.abs(Number(l.time) - this._time) / this._timeScale || .001, i = new n(this, s, l), l.onStart = function() {
                        i.target.paused(!0), i.vars.time !== i.target.time() && s === i.duration() && i.duration(Math.abs(i.vars.time - i.target.time()) / i.target._timeScale), t.onStart && i._callback("onStart")
                    }, i
                }, i.tweenFromTo = function(e, t, s) {
                    s = s || {}, e = this._parseTimeOrLabel(e), s.startAt = {
                        onComplete: this.seek,
                        onCompleteParams: [e],
                        callbackScope: this
                    }, s.immediateRender = !1 !== s.immediateRender;
                    var o = this.tweenTo(t, s);
                    return o.duration(Math.abs(o.vars.time - e) / this._timeScale || .001)
                }, i.render = function(e, t, s) {
                    this._gc && this._enabled(!0, !1);
                    var o, i, l, n, a, r, d, u, h = this._dirty ? this.totalDuration() : this._totalDuration,
                        c = this._duration,
                        _ = this._time,
                        f = this._totalTime,
                        p = this._startTime,
                        m = this._timeScale,
                        b = this._rawPrevTime,
                        g = this._paused,
                        y = this._cycle;
                    if (h - 1e-7 <= e) this._locked || (this._totalTime = h, this._cycle = this._repeat), this._reversed || this._hasPausedChild() || (i = !0, n = "onComplete", a = !!this._timeline.autoRemoveChildren, 0 === this._duration && (e <= 0 && -1e-7 <= e || b < 0 || b === D) && b !== e && this._first && (a = !0, D < b && (n = "onReverseComplete"))), this._rawPrevTime = this._duration || !t || e || this._rawPrevTime === e ? e : D, this._yoyo && 0 != (1 & this._cycle) ? this._time = e = 0 : e = (this._time = c) + 1e-4;
                    else if (e < 1e-7)
                        if (this._locked || (this._totalTime = this._cycle = 0), ((this._time = 0) !== _ || 0 === c && b !== D && (0 < b || e < 0 && 0 <= b) && !this._locked) && (n = "onReverseComplete", i = this._reversed), e < 0) this._active = !1, this._timeline.autoRemoveChildren && this._reversed ? (a = i = !0, n = "onReverseComplete") : 0 <= b && this._first && (a = !0), this._rawPrevTime = e;
                        else {
                            if (this._rawPrevTime = c || !t || e || this._rawPrevTime === e ? e : D, 0 === e && i)
                                for (o = this._first; o && 0 === o._startTime;) o._duration || (i = !1), o = o._next;
                            e = 0, this._initted || (a = !0)
                        }
                    else if (0 === c && b < 0 && (a = !0), this._time = this._rawPrevTime = e, this._locked || (this._totalTime = e, 0 !== this._repeat && (r = c + this._repeatDelay, this._cycle = this._totalTime / r >> 0, 0 !== this._cycle && this._cycle === this._totalTime / r && f <= e && this._cycle--, this._time = this._totalTime - this._cycle * r, this._yoyo && 0 != (1 & this._cycle) && (this._time = c - this._time), this._time > c ? e = (this._time = c) + 1e-4 : this._time < 0 ? this._time = e = 0 : e = this._time)), this._hasPause && !this._forcingPlayhead && !t) {
                        if (_ <= (e = this._time))
                            for (o = this._first; o && o._startTime <= e && !d;) o._duration || "isPause" !== o.data || o.ratio || 0 === o._startTime && 0 === this._rawPrevTime || (d = o), o = o._next;
                        else
                            for (o = this._last; o && o._startTime >= e && !d;) o._duration || "isPause" === o.data && 0 < o._rawPrevTime && (d = o), o = o._prev;
                        d && (this._time = e = d._startTime, this._totalTime = e + this._cycle * (this._totalDuration + this._repeatDelay))
                    }
                    if (this._cycle !== y && !this._locked) {
                        var v = this._yoyo && 0 != (1 & y),
                            S = v === (this._yoyo && 0 != (1 & this._cycle)),
                            P = this._totalTime,
                            w = this._cycle,
                            T = this._rawPrevTime,
                            B = this._time;
                        if (this._totalTime = y * c, this._cycle < y ? v = !v : this._totalTime += c, this._time = _, this._rawPrevTime = 0 === c ? b - 1e-4 : b, this._cycle = y, this._locked = !0, _ = v ? 0 : c, this.render(_, t, 0 === c), t || this._gc || this.vars.onRepeat && this._callback("onRepeat"), _ !== this._time) return;
                        if (S && (_ = v ? c + 1e-4 : -1e-4, this.render(_, !0, !1)), this._locked = !1, this._paused && !g) return;
                        this._time = B, this._totalTime = P, this._cycle = w, this._rawPrevTime = T
                    }
                    if (this._time !== _ && this._first || s || a || d) {
                        if (this._initted || (this._initted = !0), this._active || !this._paused && this._totalTime !== f && 0 < e && (this._active = !0), 0 === f && this.vars.onStart && (0 === this._totalTime && this._totalDuration || t || this._callback("onStart")), _ <= (u = this._time))
                            for (o = this._first; o && (l = o._next, u === this._time && (!this._paused || g));)(o._active || o._startTime <= this._time && !o._paused && !o._gc) && (d === o && this.pause(), o._reversed ? o.render((o._dirty ? o.totalDuration() : o._totalDuration) - (e - o._startTime) * o._timeScale, t, s) : o.render((e - o._startTime) * o._timeScale, t, s)), o = l;
                        else
                            for (o = this._last; o && (l = o._prev, u === this._time && (!this._paused || g));) {
                                if (o._active || o._startTime <= _ && !o._paused && !o._gc) {
                                    if (d === o) {
                                        for (d = o._prev; d && d.endTime() > this._time;) d.render(d._reversed ? d.totalDuration() - (e - d._startTime) * d._timeScale : (e - d._startTime) * d._timeScale, t, s), d = d._prev;
                                        d = null, this.pause()
                                    }
                                    o._reversed ? o.render((o._dirty ? o.totalDuration() : o._totalDuration) - (e - o._startTime) * o._timeScale, t, s) : o.render((e - o._startTime) * o._timeScale, t, s)
                                }
                                o = l
                            }
                        this._onUpdate && (t || (W.length && F(), this._callback("onUpdate"))), n && (this._locked || this._gc || p !== this._startTime && m === this._timeScale || (0 === this._time || h >= this.totalDuration()) && (i && (W.length && F(), this._timeline.autoRemoveChildren && this._enabled(!1, !1), this._active = !1), !t && this.vars[n] && this._callback(n)))
                    } else f !== this._totalTime && this._onUpdate && (t || this._callback("onUpdate"))
                }, i.getActive = function(e, t, s) {
                    null == e && (e = !0), null == t && (t = !0), null == s && (s = !1);
                    var o, i, l = [],
                        n = this.getChildren(e, t, s),
                        a = 0,
                        r = n.length;
                    for (o = 0; o < r; o++)(i = n[o]).isActive() && (l[a++] = i);
                    return l
                }, i.getLabelAfter = function(e) {
                    e || 0 !== e && (e = this._time);
                    var t, s = this.getLabelsArray(),
                        o = s.length;
                    for (t = 0; t < o; t++)
                        if (s[t].time > e) return s[t].name;
                    return null
                }, i.getLabelBefore = function(e) {
                    null == e && (e = this._time);
                    for (var t = this.getLabelsArray(), s = t.length; - 1 < --s;)
                        if (t[s].time < e) return t[s].name;
                    return null
                }, i.getLabelsArray = function() {
                    var e, t = [],
                        s = 0;
                    for (e in this._labels) t[s++] = {
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
                }, s
            }, !0), w = 180 / Math.PI, P = [], T = [], B = [], v = {}, s = _fwd_gsScope.FWDFWD_gsDefine.globals, m = _fwd_gsScope.FWDFWD_gsDefine.plugin({
                propName: "bezier",
                priority: -1,
                version: "1.3.7",
                API: 2,
                fwd_global: !0,
                init: function(e, t, s) {
                    this._target = e, t instanceof Array && (t = {
                        values: t
                    }), this._func = {}, this._mod = {}, this._props = [], this._timeRes = null == t.timeResolution ? 6 : parseInt(t.timeResolution, 10);
                    var o, i, l, n, a, r = t.values || [],
                        d = {},
                        u = r[0],
                        h = t.autoRotate || s.vars.orientToBezier;
                    for (o in this._autoRotate = h ? h instanceof Array ? h : [
                            ["x", "y", "rotation", !0 === h ? 0 : Number(h) || 0]
                        ] : null, u) this._props.push(o);
                    for (l = this._props.length; - 1 < --l;) o = this._props[l], this._overwriteProps.push(o), i = this._func[o] = "function" == typeof e[o], d[o] = i ? e[o.indexOf("set") || "function" != typeof e["get" + o.substr(3)] ? o : "get" + o.substr(3)]() : parseFloat(e[o]), a || d[o] !== r[0][o] && (a = d);
                    if (this._beziers = "cubic" !== t.type && "quadratic" !== t.type && "soft" !== t.type ? _(r, isNaN(t.curviness) ? 1 : t.curviness, !1, "thruBasic" === t.type, t.correlate, a) : function(e, t, s) {
                            var o, i, l, n, a, r, d, u, h, c, _, f = {},
                                p = "cubic" === (t = t || "soft") ? 3 : 2,
                                m = "soft" === t,
                                b = [];
                            if (m && s && (e = [s].concat(e)), null == e || e.length < 1 + p) throw "invalid Bezier data";
                            for (h in e[0]) b.push(h);
                            for (r = b.length; - 1 < --r;) {
                                for (f[h = b[r]] = a = [], c = 0, u = e.length, d = 0; d < u; d++) o = null == s ? e[d][h] : "string" == typeof(_ = e[d][h]) && "=" === _.charAt(1) ? s[h] + Number(_.charAt(0) + _.substr(2)) : Number(_), m && 1 < d && d < u - 1 && (a[c++] = (o + a[c - 2]) / 2), a[c++] = o;
                                for (u = c - p + 1, d = c = 0; d < u; d += p) o = a[d], i = a[d + 1], l = a[d + 2], n = 2 == p ? 0 : a[d + 3], a[c++] = _ = 3 == p ? new g(o, i, l, n) : new g(o, (2 * i + o) / 3, (2 * i + l) / 3, l);
                                a.length = c
                            }
                            return f
                        }(r, t.type, d), this._segCount = this._beziers[o].length, this._timeRes) {
                        var c = function(e, t) {
                            var s, o, i, l, n = [],
                                a = [],
                                r = 0,
                                d = 0,
                                u = (t = t >> 0 || 6) - 1,
                                h = [],
                                c = [];
                            for (s in e) f(e[s], n, t);
                            for (i = n.length, o = 0; o < i; o++) r += Math.sqrt(n[o]), c[l = o % t] = r, l === u && (d += r, h[l = o / t >> 0] = c, a[l] = d, r = 0, c = []);
                            return {
                                length: d,
                                lengths: a,
                                segments: h
                            }
                        }(this._beziers, this._timeRes);
                        this._length = c.length, this._lengths = c.lengths, this._segments = c.segments, this._l1 = this._li = this._s1 = this._si = 0, this._l2 = this._lengths[0], this._curSeg = this._segments[0], this._s2 = this._curSeg[0], this._prec = 1 / this._curSeg.length
                    }
                    if (h = this._autoRotate)
                        for (this._initialRotations = [], h[0] instanceof Array || (this._autoRotate = h = [h]), l = h.length; - 1 < --l;) {
                            for (n = 0; n < 3; n++) o = h[l][n], this._func[o] = "function" == typeof e[o] && e[o.indexOf("set") || "function" != typeof e["get" + o.substr(3)] ? o : "get" + o.substr(3)];
                            o = h[l][2], this._initialRotations[l] = (this._func[o] ? this._func[o].call(this._target) : this._target[o]) || 0, this._overwriteProps.push(o)
                        }
                    return this._startRatio = s.vars.runBackwards ? 1 : 0, !0
                },
                set: function(e) {
                    var t, s, o, i, l, n, a, r, d, u, h = this._segCount,
                        c = this._func,
                        _ = this._target,
                        f = e !== this._startRatio;
                    if (this._timeRes) {
                        if (d = this._lengths, u = this._curSeg, e *= this._length, o = this._li, e > this._l2 && o < h - 1) {
                            for (r = h - 1; o < r && (this._l2 = d[++o]) <= e;);
                            this._l1 = d[o - 1], this._li = o, this._curSeg = u = this._segments[o], this._s2 = u[this._s1 = this._si = 0]
                        } else if (e < this._l1 && 0 < o) {
                            for (; 0 < o && (this._l1 = d[--o]) >= e;);
                            0 === o && e < this._l1 ? this._l1 = 0 : o++, this._l2 = d[o], this._li = o, this._curSeg = u = this._segments[o], this._s1 = u[(this._si = u.length - 1) - 1] || 0, this._s2 = u[this._si]
                        }
                        if (t = o, e -= this._l1, o = this._si, e > this._s2 && o < u.length - 1) {
                            for (r = u.length - 1; o < r && (this._s2 = u[++o]) <= e;);
                            this._s1 = u[o - 1], this._si = o
                        } else if (e < this._s1 && 0 < o) {
                            for (; 0 < o && (this._s1 = u[--o]) >= e;);
                            0 === o && e < this._s1 ? this._s1 = 0 : o++, this._s2 = u[o], this._si = o
                        }
                        n = (o + (e - this._s1) / (this._s2 - this._s1)) * this._prec || 0
                    } else n = (e - (t = e < 0 ? 0 : 1 <= e ? h - 1 : h * e >> 0) * (1 / h)) * h;
                    for (s = 1 - n, o = this._props.length; - 1 < --o;) i = this._props[o], a = (n * n * (l = this._beziers[i][t]).da + 3 * s * (n * l.ca + s * l.ba)) * n + l.a, this._mod[i] && (a = this._mod[i](a, _)), c[i] ? _[i](a) : "x" == i ? _.setX(a) : "y" == i ? _.setY(a) : "z" == i ? _.setZ(a) : "angleX" == i ? _.setAngleX(a) : "angleY" == i ? _.setAngleY(a) : "angleZ" == i ? _.setAngleZ(a) : "w" == i ? _.setWidth(a) : "h" == i ? _.setHeight(a) : "alpha" == i ? _.setAlpha(a) : "scale" == i ? _.setScale2(a) : _[i] = a;
                    if (this._autoRotate) {
                        var p, m, b, g, y, v, S, P = this._autoRotate;
                        for (o = P.length; - 1 < --o;) i = P[o][2], v = P[o][3] || 0, S = !0 === P[o][4] ? 1 : w, l = this._beziers[P[o][0]], p = this._beziers[P[o][1]], l && p && (l = l[t], p = p[t], m = l.a + (l.b - l.a) * n, m += ((g = l.b + (l.c - l.b) * n) - m) * n, g += (l.c + (l.d - l.c) * n - g) * n, b = p.a + (p.b - p.a) * n, b += ((y = p.b + (p.c - p.b) * n) - b) * n, y += (p.c + (p.d - p.c) * n - y) * n, a = f ? Math.atan2(y - b, g - m) * S + v : this._initialRotations[o], this._mod[i] && (a = this._mod[i](a, _)), c[i] ? _[i](a) : _[i] = a)
                    }
                }
            }), e = m.prototype, m.bezierThrough = _, m.cubicToQuadratic = S, m._autoCSS = !0, m.quadraticToCubic = function(e, t, s) {
                return new g(e, (2 * t + e) / 3, (2 * t + s) / 3, s)
            }, m._cssRegister = function() {
                var e = s.CSSPlugin;
                if (e) {
                    var t = e._internals,
                        _ = t._parseToProxy,
                        f = t._setPluginRatio,
                        p = t.CSSPropTween;
                    t._registerComplexSpecialProp("bezier", {
                        parser: function(e, t, s, o, i, l) {
                            t instanceof Array && (t = {
                                values: t
                            }), l = new m;
                            var n, a, r, d = t.values,
                                u = d.length - 1,
                                h = [],
                                c = {};
                            if (u < 0) return i;
                            for (n = 0; n <= u; n++) r = _(e, d[n], o, i, l, u !== n), h[n] = r.end;
                            for (a in t) c[a] = t[a];
                            return c.values = h, (i = new p(e, "bezier", 0, 0, r.pt, 2)).data = r, i.plugin = l, i.setRatio = f, 0 === c.autoRotate && (c.autoRotate = !0), !c.autoRotate || c.autoRotate instanceof Array || (n = !0 === c.autoRotate ? 0 : Number(c.autoRotate), c.autoRotate = null != r.end.left ? [
                                ["left", "top", "rotation", n, !1]
                            ] : null != r.end.x && [
                                ["x", "y", "rotation", n, !1]
                            ]), c.autoRotate && (o._transform || o._enableTransforms(!1), r.autoRotate = o._target._gsTransform, r.proxy.rotation = r.autoRotate.rotation || 0, o._overwriteProps.push("rotation")), l._onInitTween(r.proxy, c, o._tween), i
                        }
                    })
                }
            }, e._mod = function(e) {
                for (var t, s = this._overwriteProps, o = s.length; - 1 < --o;)(t = e[s[o]]) && "function" == typeof t && (this._mod[s[o]] = t)
            }, e._kill = function(e) {
                var t, s, o = this._props;
                for (t in this._beziers)
                    if (t in e)
                        for (delete this._beziers[t], delete this._func[t], s = o.length; - 1 < --s;) o[s] === t && o.splice(s, 1);
                if (o = this._autoRotate)
                    for (s = o.length; - 1 < --s;) e[o[s][2]] && o.splice(s, 1);
                return this._super._kill.call(this, e)
            }, _fwd_gsScope.FWDFWD_gsDefine("plugins.CSSPlugin", ["plugins.TweenPlugin", "FWDTweenLite"], function(l, L) {
                var f, T, B, p, R = function() {
                        l.call(this, "css"), this._overwriteProps.length = 0, this.setRatio = R.prototype.setRatio
                    },
                    d = _fwd_gsScope.FWDFWD_gsDefine.globals,
                    m = {},
                    e = R.prototype = new l("css");
                (e.constructor = R).version = "1.19.0", R.API = 2, R.defaultTransformPerspective = 0, R.defaultSkewType = "compensated", R.defaultSmoothOrigin = !0, e = "px", R.suffixMap = {
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

                function n(e, t) {
                    return t.toUpperCase()
                }

                function t(e) {
                    return $.createElementNS ? $.createElementNS("http://www.w3.org/1999/xhtml", e) : $.createElement(e)
                }

                function a(e) {
                    return M.test("string" == typeof e ? e : (e.currentStyle ? e.currentStyle.filter : e.style.filter) || "") ? parseFloat(RegExp.$1) / 100 : 1
                }

                function b(e) {
                    window.console && console.log(e)
                }

                function D(e, t) {
                    var s, o, i = (t = t || ee).style;
                    if (void 0 !== i[e]) return e;
                    for (e = e.charAt(0).toUpperCase() + e.substr(1), s = ["O", "Moz", "ms", "Ms", "Webkit"], o = 5; - 1 < --o && void 0 === i[s[o] + e];);
                    return 0 <= o ? (le = "-" + (ne = 3 === o ? "ms" : s[o]).toLowerCase() + "-", ne + e) : null
                }

                function g(e, t) {
                    var s, o, i, l = {};
                    if (t = t || ae(e, null))
                        if (s = t.length)
                            for (; - 1 < --s;) - 1 !== (i = t[s]).indexOf("-transform") && Ae !== i || (l[i.replace(c, n)] = t.getPropertyValue(i));
                        else
                            for (s in t) - 1 !== s.indexOf("Transform") && xe !== s || (l[s] = t[s]);
                    else if (t = e.currentStyle || e.style)
                        for (s in t) "string" == typeof s && void 0 === l[s] && (l[s.replace(c, n)] = t[s]);
                    return ie || (l.opacity = a(e)), o = Qe(e, t, !1), l.rotation = o.rotation, l.skewX = o.skewX, l.scaleX = o.scaleX, l.scaleY = o.scaleY, l.x = o.x, l.y = o.y, Me && (l.z = o.z, l.rotationX = o.rotationX, l.rotationY = o.rotationY, l.scaleZ = o.scaleZ), l.filters && delete l.filters, l
                }

                function y(e, t, s, o, i) {
                    var l, n, a, r = {},
                        d = e.style;
                    for (n in s) "cssText" !== n && "length" !== n && isNaN(n) && (t[n] !== (l = s[n]) || i && i[n]) && -1 === n.indexOf("Origin") && ("number" != typeof l && "string" != typeof l || (r[n] = "auto" !== l || "left" !== n && "top" !== n ? "" !== l && "auto" !== l && "none" !== l || "string" != typeof t[n] || "" === t[n].replace(u, "") ? l : 0 : ue(e, n), void 0 !== d[n] && (a = new ve(d, n, d[n], a))));
                    if (o)
                        for (n in o) "className" !== n && (r[n] = o[n]);
                    return {
                        difs: r,
                        firstMPT: a
                    }
                }

                function v(e, t, s) {
                    if ("svg" === (e.nodeName + "").toLowerCase()) return (s || ae(e))[t] || 0;
                    if (e.getBBox && Ye(e)) return e.getBBox()[t] || 0;
                    var o = parseFloat("width" === t ? e.offsetWidth : e.offsetHeight),
                        i = he[t],
                        l = i.length;
                    for (s = s || ae(e, null); - 1 < --l;) o -= parseFloat(re(e, "padding" + i[l], s, !0)) || 0, o -= parseFloat(re(e, "border" + i[l] + "Width", s, !0)) || 0;
                    return o
                }

                function W(e, t) {
                    return "function" == typeof e && (e = e(E, V)), "string" == typeof e && "=" === e.charAt(1) ? parseInt(e.charAt(0) + "1", 10) * parseFloat(e.substr(2)) : parseFloat(e) - parseFloat(t) || 0
                }

                function F(e, t) {
                    return "function" == typeof e && (e = e(E, V)), null == e ? t : "string" == typeof e && "=" === e.charAt(1) ? parseInt(e.charAt(0) + "1", 10) * parseFloat(e.substr(2)) + t : parseFloat(e) || 0
                }

                function H(e, t, s, o) {
                    var i, l, n, a, r;
                    return "function" == typeof e && (e = e(E, V)), (a = null == e ? t : "number" == typeof e ? e : (i = 360, l = e.split("_"), n = ((r = "=" === e.charAt(1)) ? parseInt(e.charAt(0) + "1", 10) * parseFloat(l[0].substr(2)) : parseFloat(l[0])) * (-1 === e.indexOf("rad") ? 1 : J) - (r ? 0 : t), l.length && (o && (o[s] = t + n), -1 !== e.indexOf("short") && (n %= i) !== n % 180 && (n = n < 0 ? n + i : n - i), -1 !== e.indexOf("_cw") && n < 0 ? n = (n + 3599999999640) % i - (n / i | 0) * i : -1 !== e.indexOf("ccw") && 0 < n && (n = (n - 3599999999640) % i - (n / i | 0) * i)), t + n)) < 1e-6 && -1e-6 < a && (a = 0), a
                }

                function _(e, t, s) {
                    return 255 * (6 * (e = e < 0 ? e + 1 : 1 < e ? e - 1 : e) < 1 ? t + (s - t) * e * 6 : e < .5 ? s : 3 * e < 2 ? t + (s - t) * (2 / 3 - e) * 6 : t) + .5 | 0
                }

                function o(e, t) {
                    var s, o, i, l = e.match(me) || [],
                        n = 0,
                        a = l.length ? "" : e;
                    for (s = 0; s < l.length; s++) o = l[s], n += (i = e.substr(n, e.indexOf(o, n) - n)).length + o.length, 3 === (o = pe(o, t)).length && o.push(1), a += i + (t ? "hsla(" + o[0] + "," + o[1] + "%," + o[2] + "%," + o[3] : "rgba(" + o.join(",")) + ")";
                    return a + e.substr(n)
                }
                var U, S, P, k, w, C, V, E, s, i, O = /(?:\-|\.|\b)(\d|\.|e\-)+/g,
                    I = /(?:\d|\-\d|\.\d|\-\.\d|\+=\d|\-=\d|\+=.\d|\-=\.\d)+/g,
                    x = /(?:\+=|\-=|\-|\b)[\d\-\.]+[a-zA-Z0-9]*(?:%|\b)/gi,
                    u = /(?![+-]?\d*\.?\d+|[+-]|e[+-]\d+)[^0-9]/g,
                    A = /(?:\d|\-|\+|=|#|\.)*/g,
                    M = /opacity *= *([^)]*)/i,
                    N = /opacity:([^;]*)/i,
                    r = /alpha\(opacity *=.+?\)/i,
                    j = /^(rgb|hsl)/,
                    h = /([A-Z])/g,
                    c = /-([a-z])/gi,
                    Y = /(^(?:url\(\"|url\())|(?:(\"\))$|\)$)/gi,
                    X = /(?:Left|Right|Width)/i,
                    z = /(M11|M12|M21|M22)=[\d\-\.e]+/gi,
                    Q = /progid\:DXImageTransform\.Microsoft\.Matrix\(.+?\)/i,
                    G = /,(?=[^\)]*(?:\(|$))/gi,
                    q = /[\s,\(]/i,
                    K = Math.PI / 180,
                    J = 180 / Math.PI,
                    Z = {},
                    $ = document,
                    ee = t("div"),
                    te = t("img"),
                    se = R._internals = {
                        _specialProps: m
                    },
                    oe = navigator.userAgent,
                    ie = (s = oe.indexOf("Android"), i = t("a"), P = -1 !== oe.indexOf("Safari") && -1 === oe.indexOf("Chrome") && (-1 === s || 3 < Number(oe.substr(s + 8, 1))), w = P && Number(oe.substr(oe.indexOf("Version/") + 8, 1)) < 6, k = -1 !== oe.indexOf("Firefox"), (/MSIE ([0-9]{1,}[\.0-9]{0,})/.exec(oe) || /Trident\/.*rv:([0-9]{1,}[\.0-9]{0,})/.exec(oe)) && (C = parseFloat(RegExp.$1)), !!i && (i.style.cssText = "top:1px;opacity:.55;", /^0.55/.test(i.style.opacity))),
                    le = "",
                    ne = "",
                    ae = $.defaultView ? $.defaultView.getComputedStyle : function() {},
                    re = R.getStyle = function(e, t, s, o, i) {
                        var l;
                        return ie || "opacity" !== t ? (!o && e.style[t] ? l = e.style[t] : (s = s || ae(e)) ? l = s[t] || s.getPropertyValue(t) || s.getPropertyValue(t.replace(h, "-$1").toLowerCase()) : e.currentStyle && (l = e.currentStyle[t]), null == i || l && "none" !== l && "auto" !== l && "auto auto" !== l ? l : i) : a(e)
                    },
                    de = se.convertToPixels = function(e, t, s, o, i) {
                        if ("px" === o || !o) return s;
                        if ("auto" === o || !s) return 0;
                        var l, n, a, r = X.test(t),
                            d = e,
                            u = ee.style,
                            h = s < 0,
                            c = 1 === s;
                        if (h && (s = -s), c && (s *= 100), "%" === o && -1 !== t.indexOf("border")) l = s / 100 * (r ? e.clientWidth : e.clientHeight);
                        else {
                            if (u.cssText = "border:0 solid red;position:" + re(e, "position") + ";line-height:0;", "%" !== o && d.appendChild && "v" !== o.charAt(0) && "rem" !== o) u[r ? "borderLeftWidth" : "borderTopWidth"] = s + o;
                            else {
                                if (n = (d = e.parentNode || $.body)._gsCache, a = L.ticker.frame, n && r && n.time === a) return n.width * s / 100;
                                u[r ? "width" : "height"] = s + o
                            }
                            d.appendChild(ee), l = parseFloat(ee[r ? "offsetWidth" : "offsetHeight"]), d.removeChild(ee), r && "%" === o && !1 !== R.cacheWidths && ((n = d._gsCache = d._gsCache || {}).time = a, n.width = l / s * 100), 0 !== l || i || (l = de(e, t, s, o, !0))
                        }
                        return c && (l /= 100), h ? -l : l
                    },
                    ue = se.calculateOffset = function(e, t, s) {
                        if ("absolute" !== re(e, "position", s)) return 0;
                        var o = "left" === t ? "Left" : "Top",
                            i = re(e, "margin" + o, s);
                        return e["offset" + o] - (de(e, t, parseFloat(i), i.replace(A, "")) || 0)
                    },
                    he = {
                        width: ["Left", "Right"],
                        height: ["Top", "Bottom"]
                    },
                    ce = ["marginLeft", "marginRight", "marginTop", "marginBottom"],
                    _e = function(e, t) {
                        if ("contain" === e || "auto" === e || "auto auto" === e) return e + " ";
                        null != e && "" !== e || (e = "0 0");
                        var s, o = e.split(" "),
                            i = -1 !== e.indexOf("left") ? "0%" : -1 !== e.indexOf("right") ? "100%" : o[0],
                            l = -1 !== e.indexOf("top") ? "0%" : -1 !== e.indexOf("bottom") ? "100%" : o[1];
                        if (3 < o.length && !t) {
                            for (o = e.split(", ").join(",").split(","), e = [], s = 0; s < o.length; s++) e.push(_e(o[s]));
                            return e.join(",")
                        }
                        return null == l ? l = "center" === i ? "50%" : "0" : "center" === l && (l = "50%"), ("center" === i || isNaN(parseFloat(i)) && -1 === (i + "").indexOf("=")) && (i = "50%"), e = i + " " + l + (2 < o.length ? " " + o[2] : ""), t && (t.oxp = -1 !== i.indexOf("%"), t.oyp = -1 !== l.indexOf("%"), t.oxr = "=" === i.charAt(1), t.oyr = "=" === l.charAt(1), t.ox = parseFloat(i.replace(u, "")), t.oy = parseFloat(l.replace(u, "")), t.v = e), t || e
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
                    pe = R.parseColor = function(e, t) {
                        var s, o, i, l, n, a, r, d, u, h, c;
                        if (e)
                            if ("number" == typeof e) s = [e >> 16, e >> 8 & 255, 255 & e];
                            else {
                                if ("," === e.charAt(e.length - 1) && (e = e.substr(0, e.length - 1)), fe[e]) s = fe[e];
                                else if ("#" === e.charAt(0)) 4 === e.length && (e = "#" + (o = e.charAt(1)) + o + (i = e.charAt(2)) + i + (l = e.charAt(3)) + l), s = [(e = parseInt(e.substr(1), 16)) >> 16, e >> 8 & 255, 255 & e];
                                else if ("hsl" === e.substr(0, 3))
                                    if (s = c = e.match(O), t) {
                                        if (-1 !== e.indexOf("=")) return e.match(I)
                                    } else n = Number(s[0]) % 360 / 360, a = Number(s[1]) / 100, o = 2 * (r = Number(s[2]) / 100) - (i = r <= .5 ? r * (a + 1) : r + a - r * a), 3 < s.length && (s[3] = Number(e[3])), s[0] = _(n + 1 / 3, o, i), s[1] = _(n, o, i), s[2] = _(n - 1 / 3, o, i);
                                else s = e.match(O) || fe.transparent;
                                s[0] = Number(s[0]), s[1] = Number(s[1]), s[2] = Number(s[2]), 3 < s.length && (s[3] = Number(s[3]))
                            }
                        else s = fe.black;
                        return t && !c && (o = s[0] / 255, i = s[1] / 255, l = s[2] / 255, r = ((d = Math.max(o, i, l)) + (u = Math.min(o, i, l))) / 2, d === u ? n = a = 0 : (h = d - u, a = .5 < r ? h / (2 - d - u) : h / (d + u), n = d === o ? (i - l) / h + (i < l ? 6 : 0) : d === i ? (l - o) / h + 2 : (o - i) / h + 4, n *= 60), s[0] = n + .5 | 0, s[1] = 100 * a + .5 | 0, s[2] = 100 * r + .5 | 0), s
                    },
                    me = "(?:\\b(?:(?:rgb|rgba|hsl|hsla)\\(.+?\\))|\\B#(?:[0-9a-f]{3}){1,2}\\b";
                for (e in fe) me += "|" + e + "\\b";
                me = new RegExp(me + ")", "gi"), R.colorStringFilter = function(e) {
                    var t, s = e[0] + e[1];
                    me.test(s) && (t = -1 !== s.indexOf("hsl(") || -1 !== s.indexOf("hsla("), e[0] = o(e[0], t), e[1] = o(e[1], t)), me.lastIndex = 0
                }, L.defaultStringFilter || (L.defaultStringFilter = R.colorStringFilter);

                function be(e, t, l, n) {
                    if (null == e) return function(e) {
                        return e
                    };
                    var a, r = t ? (e.match(me) || [""])[0] : "",
                        d = e.split(r).join("").match(x) || [],
                        u = e.substr(0, e.indexOf(d[0])),
                        h = ")" === e.charAt(e.length - 1) ? ")" : "",
                        c = -1 !== e.indexOf(" ") ? " " : ",",
                        _ = d.length,
                        f = 0 < _ ? d[0].replace(O, "") : "";
                    return _ ? a = t ? function(e) {
                        var t, s, o, i;
                        if ("number" == typeof e) e += f;
                        else if (n && G.test(e)) {
                            for (i = e.replace(G, "|").split("|"), o = 0; o < i.length; o++) i[o] = a(i[o]);
                            return i.join(",")
                        }
                        if (t = (e.match(me) || [r])[0], o = (s = e.split(t).join("").match(x) || []).length, _ > o--)
                            for (; ++o < _;) s[o] = l ? s[(o - 1) / 2 | 0] : d[o];
                        return u + s.join(c) + c + t + h + (-1 !== e.indexOf("inset") ? " inset" : "")
                    } : function(e) {
                        var t, s, o;
                        if ("number" == typeof e) e += f;
                        else if (n && G.test(e)) {
                            for (s = e.replace(G, "|").split("|"), o = 0; o < s.length; o++) s[o] = a(s[o]);
                            return s.join(",")
                        }
                        if (o = (t = e.match(x) || []).length, _ > o--)
                            for (; ++o < _;) t[o] = l ? t[(o - 1) / 2 | 0] : d[o];
                        return u + t.join(c) + h
                    } : function(e) {
                        return e
                    }
                }

                function ge(d) {
                    return d = d.split(","),
                        function(e, t, s, o, i, l, n) {
                            var a, r = (t + "").split(" ");
                            for (n = {}, a = 0; a < 4; a++) n[d[a]] = r[a] = r[a] || r[(a - 1) / 2 >> 0];
                            return o.parse(e, n, i, l)
                        }
                }
                se._setPluginRatio = function(e) {
                    this.plugin.setRatio(e);
                    for (var t, s, o, i, l, n = this.data, a = n.proxy, r = n.firstMPT; r;) t = a[r.v], r.r ? t = Math.round(t) : t < 1e-6 && -1e-6 < t && (t = 0), r.t[r.p] = t, r = r._next;
                    if (n.autoRotate && (n.autoRotate.rotation = n.mod ? n.mod(a.rotation, this.t) : a.rotation), 1 === e || 0 === e)
                        for (r = n.firstMPT, l = 1 === e ? "e" : "b"; r;) {
                            if ((s = r.t).type) {
                                if (1 === s.type) {
                                    for (i = s.xs0 + s.s + s.xs1, o = 1; o < s.l; o++) i += s["xn" + o] + s["xs" + (o + 1)];
                                    s[l] = i
                                }
                            } else s[l] = s.s + s.xs0;
                            r = r._next
                        }
                };

                function ye(e, t, s, o, i, l) {
                    var n = new Se(e, t, s, o - s, i, -1, l);
                    return n.b = s, n.e = n.xs0 = o, n
                }
                var ve = function(e, t, s, o, i) {
                        this.t = e, this.p = t, this.v = s, this.r = i, o && ((o._prev = this)._next = o)
                    },
                    Se = (se._parseToProxy = function(e, t, s, o, i, l) {
                        var n, a, r, d, u, h = o,
                            c = {},
                            _ = {},
                            f = s._transform,
                            p = Z;
                        for (s._transform = null, Z = t, o = u = s.parse(e, t, o, i), Z = p, l && (s._transform = f, h && (h._prev = null, h._prev && (h._prev._next = null))); o && o !== h;) {
                            if (o.type <= 1 && (_[a = o.p] = o.s + o.c, c[a] = o.s, l || (d = new ve(o, "s", a, d, o.r), o.c = 0), 1 === o.type))
                                for (n = o.l; 0 < --n;) r = "xn" + n, _[a = o.p + "_" + r] = o.data[r], c[a] = o[r], l || (d = new ve(o, r, a, d, o.rxp[r]));
                            o = o._next
                        }
                        return {
                            proxy: c,
                            end: _,
                            firstMPT: d,
                            pt: u
                        }
                    }, se.CSSPropTween = function(e, t, s, o, i, l, n, a, r, d, u) {
                        this.t = e, this.p = t, this.s = s, this.c = o, this.n = n || t, e instanceof Se || p.push(this.n), this.r = a, this.type = l || 0, r && (this.pr = r, f = !0), this.b = void 0 === d ? s : d, this.e = void 0 === u ? s + o : u, i && ((this._next = i)._prev = this)
                    }),
                    Pe = R.parseComplex = function(e, t, s, o, i, l, n, a, r, d) {
                        s = s || l || "", "function" == typeof o && (o = o(E, V)), n = new Se(e, t, 0, 0, n, d ? 2 : 1, null, !1, a, s, o), o += "", i && me.test(o + s) && (o = [s, o], R.colorStringFilter(o), s = o[0], o = o[1]);
                        var u, h, c, _, f, p, m, b, g, y, v, S, P, w = s.split(", ").join(",").split(" "),
                            T = o.split(", ").join(",").split(" "),
                            B = w.length,
                            D = !1 !== U;
                        for (-1 === o.indexOf(",") && -1 === s.indexOf(",") || (w = w.join(" ").replace(G, ", ").split(" "), T = T.join(" ").replace(G, ", ").split(" "), B = w.length), B !== T.length && (B = (w = (l || "").split(" ")).length), n.plugin = r, n.setRatio = d, u = me.lastIndex = 0; u < B; u++)
                            if (_ = w[u], f = T[u], (b = parseFloat(_)) || 0 === b) n.appendXtra("", b, W(f, b), f.replace(I, ""), D && -1 !== f.indexOf("px"), !0);
                            else if (i && me.test(_)) S = ")" + ((S = f.indexOf(")") + 1) ? f.substr(S) : ""), P = -1 !== f.indexOf("hsl") && ie, _ = pe(_, P), f = pe(f, P), (g = 6 < _.length + f.length) && !ie && 0 === f[3] ? (n["xs" + n.l] += n.l ? " transparent" : "transparent", n.e = n.e.split(T[u]).join("transparent")) : (ie || (g = !1), P ? n.appendXtra(g ? "hsla(" : "hsl(", _[0], W(f[0], _[0]), ",", !1, !0).appendXtra("", _[1], W(f[1], _[1]), "%,", !1).appendXtra("", _[2], W(f[2], _[2]), g ? "%," : "%" + S, !1) : n.appendXtra(g ? "rgba(" : "rgb(", _[0], f[0] - _[0], ",", !0, !0).appendXtra("", _[1], f[1] - _[1], ",", !0).appendXtra("", _[2], f[2] - _[2], g ? "," : S, !0), g && (_ = _.length < 4 ? 1 : _[3], n.appendXtra("", _, (f.length < 4 ? 1 : f[3]) - _, S, !1))), me.lastIndex = 0;
                        else if (p = _.match(O)) {
                            if (!(m = f.match(I)) || m.length !== p.length) return n;
                            for (h = c = 0; h < p.length; h++) v = p[h], y = _.indexOf(v, c), n.appendXtra(_.substr(c, y - c), Number(v), W(m[h], v), "", D && "px" === _.substr(y + v.length, 2), 0 === h), c = y + v.length;
                            n["xs" + n.l] += _.substr(c)
                        } else n["xs" + n.l] += n.l || n["xs" + n.l] ? " " + f : f;
                        if (-1 !== o.indexOf("=") && n.data) {
                            for (S = n.xs0 + n.data.s, u = 1; u < n.l; u++) S += n["xs" + u] + n.data["xn" + u];
                            n.e = S + n["xs" + u]
                        }
                        return n.l || (n.type = -1, n.xs0 = n.e), n.xfirst || n
                    },
                    we = 9;
                for ((e = Se.prototype).l = e.pr = 0; 0 < --we;) e["xn" + we] = 0, e["xs" + we] = "";
                e.xs0 = "", e._next = e._prev = e.xfirst = e.data = e.plugin = e.setRatio = e.rxp = null, e.appendXtra = function(e, t, s, o, i, l) {
                    var n = this,
                        a = n.l;
                    return n["xs" + a] += l && (a || n["xs" + a]) ? " " + e : e || "", s || 0 === a || n.plugin ? (n.l++, n.type = n.setRatio ? 2 : 1, n["xs" + n.l] = o || "", 0 < a ? (n.data["xn" + a] = t + s, n.rxp["xn" + a] = i, n["xn" + a] = t, n.plugin || (n.xfirst = new Se(n, "xn" + a, t, s, n.xfirst || n, 0, n.n, i, n.pr), n.xfirst.xs0 = 0)) : (n.data = {
                        s: t + s
                    }, n.rxp = {}, n.s = t, n.c = s, n.r = i), n) : (n["xs" + a] += t + (o || ""), n)
                };

                function Te(e, t) {
                    t = t || {}, this.p = t.prefix && D(e) || e, m[e] = m[this.p] = this, this.format = t.formatter || be(t.defaultValue, t.color, t.collapsible, t.multi), t.parser && (this.parse = t.parser), this.clrs = t.color, this.multi = t.multi, this.keyword = t.keyword, this.dflt = t.defaultValue, this.pr = t.priority || 0
                }
                var Be = se._registerComplexSpecialProp = function(e, t, s) {
                        "object" != typeof t && (t = {
                            parser: s
                        });
                        var o, i = e.split(","),
                            l = t.defaultValue;
                        for (s = s || [l], o = 0; o < i.length; o++) t.prefix = 0 === o && t.prefix, t.defaultValue = s[o] || l, new Te(i[o], t)
                    },
                    De = se._registerPluginProp = function(e) {
                        if (!m[e]) {
                            var r = e.charAt(0).toUpperCase() + e.substr(1) + "Plugin";
                            Be(e, {
                                parser: function(e, t, s, o, i, l, n) {
                                    var a = d.com.greensock.plugins[r];
                                    return a ? (a._cssRegister(), m[s].parse(e, t, s, o, i, l, n)) : (b("Error: " + r + " js file not loaded."), i)
                                }
                            })
                        }
                    };
                (e = Te.prototype).parseComplex = function(e, t, s, o, i, l) {
                    var n, a, r, d, u, h, c = this.keyword;
                    if (this.multi && (G.test(s) || G.test(t) ? (a = t.replace(G, "|").split("|"), r = s.replace(G, "|").split("|")) : c && (a = [t], r = [s])), r) {
                        for (d = r.length > a.length ? r.length : a.length, n = 0; n < d; n++) t = a[n] = a[n] || this.dflt, s = r[n] = r[n] || this.dflt, c && (u = t.indexOf(c)) !== (h = s.indexOf(c)) && (-1 === h ? a[n] = a[n].split(c).join("") : -1 === u && (a[n] += " " + c));
                        t = a.join(", "), s = r.join(", ")
                    }
                    return Pe(e, this.p, t, s, this.clrs, this.dflt, o, this.pr, i, l)
                }, e.parse = function(e, t, s, o, i, l, n) {
                    return this.parseComplex(e.style, this.format(re(e, this.p, B, !1, this.dflt)), this.format(t), i, l)
                }, R.registerSpecialProp = function(e, r, d) {
                    Be(e, {
                        parser: function(e, t, s, o, i, l, n) {
                            var a = new Se(e, s, 0, 0, i, 2, s, !1, d);
                            return a.plugin = l, a.setRatio = r(e, t, o._tween, s), a
                        },
                        priority: d
                    })
                }, R.useSVGTransformAttr = P || k;

                function We(e, t, s) {
                    var o, i = $.createElementNS("http://www.w3.org/2000/svg", e),
                        l = /([a-z])([A-Z])/g;
                    for (o in s) i.setAttributeNS(null, o.replace(l, "$1-$2").toLowerCase(), s[o]);
                    return t.appendChild(i), i
                }

                function Fe(e, t, s, o, i, l) {
                    var n, a, r, d, u, h, c, _, f, p, m, b, g, y, v = e._gsTransform,
                        S = ze(e, !0);
                    v && (g = v.xOrigin, y = v.yOrigin), (!o || (n = o.split(" ")).length < 2) && (c = e.getBBox(), n = [(-1 !== (t = _e(t).split(" "))[0].indexOf("%") ? parseFloat(t[0]) / 100 * c.width : parseFloat(t[0])) + c.x, (-1 !== t[1].indexOf("%") ? parseFloat(t[1]) / 100 * c.height : parseFloat(t[1])) + c.y]), s.xOrigin = d = parseFloat(n[0]), s.yOrigin = u = parseFloat(n[1]), o && S !== Xe && (h = S[0], c = S[1], _ = S[2], f = S[3], p = S[4], a = d * (f / (b = h * f - c * _)) + u * (-_ / b) + (_ * (m = S[5]) - f * p) / b, r = d * (-c / b) + u * (h / b) - (h * m - c * p) / b, d = s.xOrigin = n[0] = a, u = s.yOrigin = n[1] = r), v && (l && (s.xOffset = v.xOffset, s.yOffset = v.yOffset, v = s), i || !1 !== i && !1 !== R.defaultSmoothOrigin ? (a = d - g, r = u - y, v.xOffset += a * S[0] + r * S[2] - a, v.yOffset += a * S[1] + r * S[3] - r) : v.xOffset = v.yOffset = 0), l || e.setAttribute("data-svg-origin", n.join(" "))
                }

                function He(e) {
                    var t, s, o = this.data,
                        i = -o.rotation * K,
                        l = i + o.skewX * K,
                        n = 1e5,
                        a = (Math.cos(i) * o.scaleX * n | 0) / n,
                        r = (Math.sin(i) * o.scaleX * n | 0) / n,
                        d = (Math.sin(l) * -o.scaleY * n | 0) / n,
                        u = (Math.cos(l) * o.scaleY * n | 0) / n,
                        h = this.t.style,
                        c = this.t.currentStyle;
                    if (c) {
                        s = r, r = -d, d = -s, t = c.filter, h.filter = "";
                        var _, f, p = this.t.offsetWidth,
                            m = this.t.offsetHeight,
                            b = "absolute" !== c.position,
                            g = "progid:DXImageTransform.Microsoft.Matrix(M11=" + a + ", M12=" + r + ", M21=" + d + ", M22=" + u,
                            y = o.x + p * o.xPercent / 100,
                            v = o.y + m * o.yPercent / 100;
                        if (null != o.ox && (y += (_ = (o.oxp ? p * o.ox * .01 : o.ox) - p / 2) - (_ * a + (f = (o.oyp ? m * o.oy * .01 : o.oy) - m / 2) * r), v += f - (_ * d + f * u)), g += b ? ", Dx=" + ((_ = p / 2) - (_ * a + (f = m / 2) * r) + y) + ", Dy=" + (f - (_ * d + f * u) + v) + ")" : ", sizingMethod='auto expand')", -1 !== t.indexOf("DXImageTransform.Microsoft.Matrix(") ? h.filter = t.replace(Q, g) : h.filter = g + " " + t, 0 !== e && 1 !== e || 1 == a && 0 === r && 0 === d && 1 == u && (b && -1 === g.indexOf("Dx=0, Dy=0") || M.test(t) && 100 !== parseFloat(RegExp.$1) || -1 === t.indexOf(t.indexOf("Alpha")) && h.removeAttribute("filter")), !b) {
                            var S, P, w, T = C < 8 ? 1 : -1;
                            for (_ = o.ieOffsetX || 0, f = o.ieOffsetY || 0, o.ieOffsetX = Math.round((p - ((a < 0 ? -a : a) * p + (r < 0 ? -r : r) * m)) / 2 + y), o.ieOffsetY = Math.round((m - ((u < 0 ? -u : u) * m + (d < 0 ? -d : d) * p)) / 2 + v), we = 0; we < 4; we++) w = (s = -1 !== (S = c[P = ce[we]]).indexOf("px") ? parseFloat(S) : de(this.t, P, parseFloat(S), S.replace(A, "")) || 0) !== o[P] ? we < 2 ? -o.ieOffsetX : -o.ieOffsetY : we < 2 ? _ - o.ieOffsetX : f - o.ieOffsetY, h[P] = (o[P] = Math.round(s - w * (0 === we || 2 === we ? 1 : T))) + "px"
                        }
                    }
                }
                var Ue, Ce, Ve, Ee, Oe, Ie = "scaleX,scaleY,scaleZ,x,y,z,skewX,skewY,rotation,rotationX,rotationY,perspective,xPercent,yPercent".split(","),
                    xe = D("transform"),
                    Ae = le + "transform",
                    ke = D("transformOrigin"),
                    Me = null !== D("perspective"),
                    Le = se.Transform = function() {
                        this.perspective = parseFloat(R.defaultTransformPerspective) || 0, this.force3D = !(!1 === R.defaultForce3D || !Me) && (R.defaultForce3D || "auto")
                    },
                    Re = window.SVGElement,
                    Ne = $.documentElement,
                    je = (Oe = C || /Android/i.test(oe) && !window.chrome, $.createElementNS && !Oe && (Ce = We("svg", Ne), Ee = (Ve = We("rect", Ce, {
                        width: 100,
                        height: 50,
                        x: 100
                    })).getBoundingClientRect().width, Ve.style[ke] = "50% 50%", Ve.style[xe] = "scaleX(0.5)", Oe = Ee === Ve.getBoundingClientRect().width && !(k && Me), Ne.removeChild(Ce)), Oe),
                    Ye = function(e) {
                        return !!(Re && e.getBBox && e.getCTM && function(e) {
                            try {
                                return e.getBBox()
                            } catch (e) {}
                        }(e) && (!e.parentNode || e.parentNode.getBBox && e.parentNode.getCTM))
                    },
                    Xe = [1, 0, 0, 1, 0, 0],
                    ze = function(e, t) {
                        var s, o, i, l, n, a, r = e._gsTransform || new Le,
                            d = e.style;
                        if (xe ? o = re(e, Ae, null, !0) : e.currentStyle && (o = (o = e.currentStyle.filter.match(z)) && 4 === o.length ? [o[0].substr(4), Number(o[2].substr(4)), Number(o[1].substr(4)), o[3].substr(4), r.x || 0, r.y || 0].join(",") : ""), (s = !o || "none" === o || "matrix(1, 0, 0, 1, 0, 0)" === o) && xe && ((a = "none" === ae(e).display) || !e.parentNode) && (a && (l = d.display, d.display = "block"), e.parentNode || (n = 1, Ne.appendChild(e)), s = !(o = re(e, Ae, null, !0)) || "none" === o || "matrix(1, 0, 0, 1, 0, 0)" === o, l ? d.display = l : a && Je(d, "display"), n && Ne.removeChild(e)), (r.svg || e.getBBox && Ye(e)) && (s && -1 !== (d[xe] + "").indexOf("matrix") && (o = d[xe], s = 0), i = e.getAttribute("transform"), s && i && (-1 !== i.indexOf("matrix") ? (o = i, s = 0) : -1 !== i.indexOf("translate") && (o = "matrix(1,0,0,1," + i.match(/(?:\-|\b)[\d\-\.e]+\b/gi).join(",") + ")", s = 0))), s) return Xe;
                        for (i = (o || "").match(O) || [], we = i.length; - 1 < --we;) l = Number(i[we]), i[we] = (n = l - (l |= 0)) ? (1e5 * n + (n < 0 ? -.5 : .5) | 0) / 1e5 + l : l;
                        return t && 6 < i.length ? [i[0], i[1], i[4], i[5], i[12], i[13]] : i
                    },
                    Qe = se.getTransform = function(e, t, s, o) {
                        if (e._gsTransform && s && !o) return e._gsTransform;
                        var i, l, n, a, r, d, u = s && e._gsTransform || new Le,
                            h = u.scaleX < 0,
                            c = Me && (parseFloat(re(e, ke, t, !1, "0 0 0").split(" ")[2]) || u.zOrigin) || 0,
                            _ = parseFloat(R.defaultTransformPerspective) || 0;
                        if (u.svg = !(!e.getBBox || !Ye(e)), u.svg && (Fe(e, re(e, ke, t, !1, "50% 50%") + "", u, e.getAttribute("data-svg-origin")), Ue = R.useSVGTransformAttr || je), (i = ze(e)) !== Xe) {
                            if (16 === i.length) {
                                var f, p, m, b, g, y = i[0],
                                    v = i[1],
                                    S = i[2],
                                    P = i[3],
                                    w = i[4],
                                    T = i[5],
                                    B = i[6],
                                    D = i[7],
                                    W = i[8],
                                    F = i[9],
                                    H = i[10],
                                    U = i[12],
                                    C = i[13],
                                    V = i[14],
                                    E = i[11],
                                    O = Math.atan2(B, H);
                                u.zOrigin && (U = W * (V = -u.zOrigin) - i[12], C = F * V - i[13], V = H * V + u.zOrigin - i[14]), u.rotationX = O * J, O && (f = w * (b = Math.cos(-O)) + W * (g = Math.sin(-O)), p = T * b + F * g, m = B * b + H * g, W = w * -g + W * b, F = T * -g + F * b, H = B * -g + H * b, E = D * -g + E * b, w = f, T = p, B = m), O = Math.atan2(-S, H), u.rotationY = O * J, O && (p = v * (b = Math.cos(-O)) - F * (g = Math.sin(-O)), m = S * b - H * g, F = v * g + F * b, H = S * g + H * b, E = P * g + E * b, y = f = y * b - W * g, v = p, S = m), O = Math.atan2(v, y), u.rotation = O * J, O && (y = y * (b = Math.cos(-O)) + w * (g = Math.sin(-O)), p = v * b + T * g, T = v * -g + T * b, B = S * -g + B * b, v = p), u.rotationX && 359.9 < Math.abs(u.rotationX) + Math.abs(u.rotation) && (u.rotationX = u.rotation = 0, u.rotationY = 180 - u.rotationY), u.scaleX = (1e5 * Math.sqrt(y * y + v * v) + .5 | 0) / 1e5, u.scaleY = (1e5 * Math.sqrt(T * T + F * F) + .5 | 0) / 1e5, u.scaleZ = (1e5 * Math.sqrt(B * B + H * H) + .5 | 0) / 1e5, u.rotationX || u.rotationY ? u.skewX = 0 : (u.skewX = w || T ? Math.atan2(w, T) * J + u.rotation : u.skewX || 0, 90 < Math.abs(u.skewX) && Math.abs(u.skewX) < 270 && (h ? (u.scaleX *= -1, u.skewX += u.rotation <= 0 ? 180 : -180, u.rotation += u.rotation <= 0 ? 180 : -180) : (u.scaleY *= -1, u.skewX += u.skewX <= 0 ? 180 : -180))), u.perspective = E ? 1 / (E < 0 ? -E : E) : 0, u.x = U, u.y = C, u.z = V, u.svg && (u.x -= u.xOrigin - (u.xOrigin * y - u.yOrigin * w), u.y -= u.yOrigin - (u.yOrigin * v - u.xOrigin * T))
                            } else if (!Me || o || !i.length || u.x !== i[4] || u.y !== i[5] || !u.rotationX && !u.rotationY) {
                                var I = 6 <= i.length,
                                    x = I ? i[0] : 1,
                                    A = i[1] || 0,
                                    k = i[2] || 0,
                                    M = I ? i[3] : 1;
                                u.x = i[4] || 0, u.y = i[5] || 0, n = Math.sqrt(x * x + A * A), a = Math.sqrt(M * M + k * k), r = x || A ? Math.atan2(A, x) * J : u.rotation || 0, d = k || M ? Math.atan2(k, M) * J + r : u.skewX || 0, 90 < Math.abs(d) && Math.abs(d) < 270 && (h ? (n *= -1, d += r <= 0 ? 180 : -180, r += r <= 0 ? 180 : -180) : (a *= -1, d += d <= 0 ? 180 : -180)), u.scaleX = n, u.scaleY = a, u.rotation = r, u.skewX = d, Me && (u.rotationX = u.rotationY = u.z = 0, u.perspective = _, u.scaleZ = 1), u.svg && (u.x -= u.xOrigin - (u.xOrigin * x + u.yOrigin * k), u.y -= u.yOrigin - (u.xOrigin * A + u.yOrigin * M))
                            }
                            for (l in u.zOrigin = c, u) u[l] < 2e-5 && -2e-5 < u[l] && (u[l] = 0)
                        }
                        return s && (e._gsTransform = u).svg && (Ue && e.style[xe] ? L.delayedCall(.001, function() {
                            Je(e.style, xe)
                        }) : !Ue && e.getAttribute("transform") && L.delayedCall(.001, function() {
                            e.removeAttribute("transform")
                        })), u
                    },
                    Ge = se.set3DTransformRatio = se.setTransformRatio = function(e) {
                        var t, s, o, i, l, n, a, r, d, u, h, c, _, f, p, m, b, g, y, v, S, P, w, T = this.data,
                            B = this.t.style,
                            D = T.rotation,
                            W = T.rotationX,
                            F = T.rotationY,
                            H = T.scaleX,
                            U = T.scaleY,
                            C = T.scaleZ,
                            V = T.x,
                            E = T.y,
                            O = T.z,
                            I = T.svg,
                            x = T.perspective,
                            A = T.force3D;
                        if (!((1 !== e && 0 !== e || "auto" !== A || this.tween._totalTime !== this.tween._totalDuration && this.tween._totalTime) && A || O || x || F || W || 1 !== C) || Ue && I || !Me) D || T.skewX || I ? (D *= K, P = T.skewX * K, w = 1e5, t = Math.cos(D) * H, i = Math.sin(D) * H, s = Math.sin(D - P) * -U, l = Math.cos(D - P) * U, P && "simple" === T.skewType && (b = Math.tan(P - T.skewY * K), s *= b = Math.sqrt(1 + b * b), l *= b, T.skewY && (b = Math.tan(T.skewY * K), t *= b = Math.sqrt(1 + b * b), i *= b)), I && (V += T.xOrigin - (T.xOrigin * t + T.yOrigin * s) + T.xOffset, E += T.yOrigin - (T.xOrigin * i + T.yOrigin * l) + T.yOffset, Ue && (T.xPercent || T.yPercent) && (f = this.t.getBBox(), V += .01 * T.xPercent * f.width, E += .01 * T.yPercent * f.height), V < (f = 1e-6) && -f < V && (V = 0), E < f && -f < E && (E = 0)), y = (t * w | 0) / w + "," + (i * w | 0) / w + "," + (s * w | 0) / w + "," + (l * w | 0) / w + "," + V + "," + E + ")", I && Ue ? this.t.setAttribute("transform", "matrix(" + y) : B[xe] = (T.xPercent || T.yPercent ? "translate(" + T.xPercent + "%," + T.yPercent + "%) matrix(" : "matrix(") + y) : B[xe] = (T.xPercent || T.yPercent ? "translate(" + T.xPercent + "%," + T.yPercent + "%) matrix(" : "matrix(") + H + ",0,0," + U + "," + V + "," + E + ")";
                        else {
                            if (k && (H < (f = 1e-4) && -f < H && (H = C = 2e-5), U < f && -f < U && (U = C = 2e-5), !x || T.z || T.rotationX || T.rotationY || (x = 0)), D || T.skewX) D *= K, p = t = Math.cos(D), m = i = Math.sin(D), T.skewX && (D -= T.skewX * K, p = Math.cos(D), m = Math.sin(D), "simple" === T.skewType && (b = Math.tan((T.skewX - T.skewY) * K), p *= b = Math.sqrt(1 + b * b), m *= b, T.skewY && (b = Math.tan(T.skewY * K), t *= b = Math.sqrt(1 + b * b), i *= b))), s = -m, l = p;
                            else {
                                if (!(F || W || 1 !== C || x || I)) return void(B[xe] = (T.xPercent || T.yPercent ? "translate(" + T.xPercent + "%," + T.yPercent + "%) translate3d(" : "translate3d(") + V + "px," + E + "px," + O + "px)" + (1 !== H || 1 !== U ? " scale(" + H + "," + U + ")" : ""));
                                t = l = 1, s = i = 0
                            }
                            d = 1, o = n = a = r = u = h = 0, c = x ? -1 / x : 0, _ = T.zOrigin, f = 1e-6, v = ",", S = "0", (D = F * K) && (p = Math.cos(D), u = c * (a = -(m = Math.sin(D))), o = t * m, n = i * m, c *= d = p, t *= p, i *= p), (D = W * K) && (b = s * (p = Math.cos(D)) + o * (m = Math.sin(D)), g = l * p + n * m, r = d * m, h = c * m, o = s * -m + o * p, n = l * -m + n * p, d *= p, c *= p, s = b, l = g), 1 !== C && (o *= C, n *= C, d *= C, c *= C), 1 !== U && (s *= U, l *= U, r *= U, h *= U), 1 !== H && (t *= H, i *= H, a *= H, u *= H), (_ || I) && (_ && (V += o * -_, E += n * -_, O += d * -_ + _), I && (V += T.xOrigin - (T.xOrigin * t + T.yOrigin * s) + T.xOffset, E += T.yOrigin - (T.xOrigin * i + T.yOrigin * l) + T.yOffset), V < f && -f < V && (V = S), E < f && -f < E && (E = S), O < f && -f < O && (O = 0)), y = T.xPercent || T.yPercent ? "translate(" + T.xPercent + "%," + T.yPercent + "%) matrix3d(" : "matrix3d(", y += (t < f && -f < t ? S : t) + v + (i < f && -f < i ? S : i) + v + (a < f && -f < a ? S : a), y += v + (u < f && -f < u ? S : u) + v + (s < f && -f < s ? S : s) + v + (l < f && -f < l ? S : l), W || F || 1 !== C ? (y += v + (r < f && -f < r ? S : r) + v + (h < f && -f < h ? S : h) + v + (o < f && -f < o ? S : o), y += v + (n < f && -f < n ? S : n) + v + (d < f && -f < d ? S : d) + v + (c < f && -f < c ? S : c) + v) : y += ",0,0,0,0,1,0,", y += V + v + E + v + O + v + (x ? 1 + -O / x : 1) + ")", B[xe] = y
                        }
                    };
                (e = Le.prototype).x = e.y = e.z = e.skewX = e.skewY = e.rotation = e.rotationX = e.rotationY = e.zOrigin = e.xPercent = e.yPercent = e.xOffset = e.yOffset = 0, e.scaleX = e.scaleY = e.scaleZ = 1, Be("transform,scale,scaleX,scaleY,scaleZ,x,y,z,rotation,rotationX,rotationY,rotationZ,skewX,skewY,shortRotation,shortRotationX,shortRotationY,shortRotationZ,transformOrigin,svgOrigin,transformPerspective,directionalRotation,parseTransform,force3D,skewType,xPercent,yPercent,smoothOrigin", {
                    parser: function(e, t, s, o, i, l, n) {
                        if (o._lastParsedTransform === n) return i;
                        var a;
                        "function" == typeof(o._lastParsedTransform = n)[s] && (a = n[s], n[s] = t);
                        var r, d, u, h, c, _, f, p, m, b = e._gsTransform,
                            g = e.style,
                            y = Ie.length,
                            v = n,
                            S = {},
                            P = "transformOrigin",
                            w = Qe(e, B, !0, v.parseTransform),
                            T = v.transform && ("function" == typeof v.transform ? v.transform(E, V) : v.transform);
                        if (o._transform = w, T && "string" == typeof T && xe)(d = ee.style)[xe] = T, d.display = "block", d.position = "absolute", $.body.appendChild(ee), r = Qe(ee, null, !1), w.svg && (_ = w.xOrigin, f = w.yOrigin, r.x -= w.xOffset, r.y -= w.yOffset, (v.transformOrigin || v.svgOrigin) && (T = {}, Fe(e, _e(v.transformOrigin), T, v.svgOrigin, v.smoothOrigin, !0), _ = T.xOrigin, f = T.yOrigin, r.x -= T.xOffset - w.xOffset, r.y -= T.yOffset - w.yOffset), (_ || f) && (p = ze(ee, !0), r.x -= _ - (_ * p[0] + f * p[2]), r.y -= f - (_ * p[1] + f * p[3]))), $.body.removeChild(ee), r.perspective || (r.perspective = w.perspective), null != v.xPercent && (r.xPercent = F(v.xPercent, w.xPercent)), null != v.yPercent && (r.yPercent = F(v.yPercent, w.yPercent));
                        else if ("object" == typeof v) {
                            if (r = {
                                    scaleX: F(null != v.scaleX ? v.scaleX : v.scale, w.scaleX),
                                    scaleY: F(null != v.scaleY ? v.scaleY : v.scale, w.scaleY),
                                    scaleZ: F(v.scaleZ, w.scaleZ),
                                    x: F(v.x, w.x),
                                    y: F(v.y, w.y),
                                    z: F(v.z, w.z),
                                    xPercent: F(v.xPercent, w.xPercent),
                                    yPercent: F(v.yPercent, w.yPercent),
                                    perspective: F(v.transformPerspective, w.perspective)
                                }, null != (c = v.directionalRotation))
                                if ("object" == typeof c)
                                    for (d in c) v[d] = c[d];
                                else v.rotation = c;
                            "string" == typeof v.x && -1 !== v.x.indexOf("%") && (r.x = 0, r.xPercent = F(v.x, w.xPercent)), "string" == typeof v.y && -1 !== v.y.indexOf("%") && (r.y = 0, r.yPercent = F(v.y, w.yPercent)), r.rotation = H("rotation" in v ? v.rotation : "shortRotation" in v ? v.shortRotation + "_short" : "rotationZ" in v ? v.rotationZ : w.rotation - w.skewY, w.rotation - w.skewY, "rotation", S), Me && (r.rotationX = H("rotationX" in v ? v.rotationX : "shortRotationX" in v ? v.shortRotationX + "_short" : w.rotationX || 0, w.rotationX, "rotationX", S), r.rotationY = H("rotationY" in v ? v.rotationY : "shortRotationY" in v ? v.shortRotationY + "_short" : w.rotationY || 0, w.rotationY, "rotationY", S)), r.skewX = H(v.skewX, w.skewX - w.skewY), (r.skewY = H(v.skewY, w.skewY)) && (r.skewX += r.skewY, r.rotation += r.skewY)
                        }
                        for (Me && null != v.force3D && (w.force3D = v.force3D, h = !0), w.skewType = v.skewType || w.skewType || R.defaultSkewType, (u = w.force3D || w.z || w.rotationX || w.rotationY || r.z || r.rotationX || r.rotationY || r.perspective) || null == v.scale || (r.scaleZ = 1); - 1 < --y;)(1e-6 < (T = r[m = Ie[y]] - w[m]) || T < -1e-6 || null != v[m] || null != Z[m]) && (h = !0, i = new Se(w, m, w[m], T, i), m in S && (i.e = S[m]), i.xs0 = 0, i.plugin = l, o._overwriteProps.push(i.n));
                        return T = v.transformOrigin, w.svg && (T || v.svgOrigin) && (_ = w.xOffset, f = w.yOffset, Fe(e, _e(T), r, v.svgOrigin, v.smoothOrigin), i = ye(w, "xOrigin", (b ? w : r).xOrigin, r.xOrigin, i, P), i = ye(w, "yOrigin", (b ? w : r).yOrigin, r.yOrigin, i, P), _ === w.xOffset && f === w.yOffset || (i = ye(w, "xOffset", b ? _ : w.xOffset, w.xOffset, i, P), i = ye(w, "yOffset", b ? f : w.yOffset, w.yOffset, i, P)), T = Ue ? null : "0px 0px"), (T || Me && u && w.zOrigin) && (xe ? (h = !0, m = ke, T = (T || re(e, m, B, !1, "50% 50%")) + "", (i = new Se(g, m, 0, 0, i, -1, P)).b = g[m], i.plugin = l, Me ? (d = w.zOrigin, T = T.split(" "), w.zOrigin = (2 < T.length && (0 === d || "0px" !== T[2]) ? parseFloat(T[2]) : d) || 0, i.xs0 = i.e = T[0] + " " + (T[1] || "50%") + " 0px", (i = new Se(w, "zOrigin", 0, 0, i, -1, i.n)).b = d, i.xs0 = i.e = w.zOrigin) : i.xs0 = i.e = T) : _e(T + "", w)), h && (o._transformType = w.svg && Ue || !u && 3 !== this._transformType ? 2 : 3), a && (n[s] = a), i
                    },
                    prefix: !0
                }), Be("boxShadow", {
                    defaultValue: "0px 0px 0px 0px #999",
                    prefix: !0,
                    color: !0,
                    multi: !0,
                    keyword: "inset"
                }), Be("borderRadius", {
                    defaultValue: "0px",
                    parser: function(e, t, s, o, i, l) {
                        t = this.format(t);
                        var n, a, r, d, u, h, c, _, f, p, m, b, g, y, v, S, P = ["borderTopLeftRadius", "borderTopRightRadius", "borderBottomRightRadius", "borderBottomLeftRadius"],
                            w = e.style;
                        for (f = parseFloat(e.offsetWidth), p = parseFloat(e.offsetHeight), n = t.split(" "), a = 0; a < P.length; a++) this.p.indexOf("border") && (P[a] = D(P[a])), -1 !== (u = d = re(e, P[a], B, !1, "0px")).indexOf(" ") && (u = (d = u.split(" "))[0], d = d[1]), h = r = n[a], c = parseFloat(u), b = u.substr((c + "").length), "" === (m = (g = "=" === h.charAt(1)) ? (_ = parseInt(h.charAt(0) + "1", 10), h = h.substr(2), _ *= parseFloat(h), h.substr((_ + "").length - (_ < 0 ? 1 : 0)) || "") : (_ = parseFloat(h), h.substr((_ + "").length))) && (m = T[s] || b), m !== b && (y = de(e, "borderLeft", c, b), v = de(e, "borderTop", c, b), d = "%" === m ? (u = y / f * 100 + "%", v / p * 100 + "%") : "em" === m ? (u = y / (S = de(e, "borderLeft", 1, "em")) + "em", v / S + "em") : (u = y + "px", v + "px"), g && (h = parseFloat(u) + _ + m, r = parseFloat(d) + _ + m)), i = Pe(w, P[a], u + " " + d, h + " " + r, !1, "0px", i);
                        return i
                    },
                    prefix: !0,
                    formatter: be("0px 0px 0px 0px", !1, !0)
                }), Be("borderBottomLeftRadius,borderBottomRightRadius,borderTopLeftRadius,borderTopRightRadius", {
                    defaultValue: "0px",
                    parser: function(e, t, s, o, i, l) {
                        return Pe(e.style, s, this.format(re(e, s, B, !1, "0px 0px")), this.format(t), !1, "0px", i)
                    },
                    prefix: !0,
                    formatter: be("0px 0px", !1, !0)
                }), Be("backgroundPosition", {
                    defaultValue: "0 0",
                    parser: function(e, t, s, o, i, l) {
                        var n, a, r, d, u, h, c = "background-position",
                            _ = B || ae(e, null),
                            f = this.format((_ ? C ? _.getPropertyValue(c + "-x") + " " + _.getPropertyValue(c + "-y") : _.getPropertyValue(c) : e.currentStyle.backgroundPositionX + " " + e.currentStyle.backgroundPositionY) || "0 0"),
                            p = this.format(t);
                        if (-1 !== f.indexOf("%") != (-1 !== p.indexOf("%")) && p.split(",").length < 2 && (h = re(e, "backgroundImage").replace(Y, "")) && "none" !== h) {
                            for (n = f.split(" "), a = p.split(" "), te.setAttribute("src", h), r = 2; - 1 < --r;)(d = -1 !== (f = n[r]).indexOf("%")) != (-1 !== a[r].indexOf("%")) && (u = 0 === r ? e.offsetWidth - te.width : e.offsetHeight - te.height, n[r] = d ? parseFloat(f) / 100 * u + "px" : parseFloat(f) / u * 100 + "%");
                            f = n.join(" ")
                        }
                        return this.parseComplex(e.style, f, p, i, l)
                    },
                    formatter: _e
                }), Be("backgroundSize", {
                    defaultValue: "0 0",
                    formatter: function(e) {
                        return _e(-1 === (e += "").indexOf(" ") ? e + " " + e : e)
                    }
                }), Be("perspective", {
                    defaultValue: "0px",
                    prefix: !0
                }), Be("perspectiveOrigin", {
                    defaultValue: "50% 50%",
                    prefix: !0
                }), Be("transformStyle", {
                    prefix: !0
                }), Be("backfaceVisibility", {
                    prefix: !0
                }), Be("userSelect", {
                    prefix: !0
                }), Be("margin", {
                    parser: ge("marginTop,marginRight,marginBottom,marginLeft")
                }), Be("padding", {
                    parser: ge("paddingTop,paddingRight,paddingBottom,paddingLeft")
                }), Be("clip", {
                    defaultValue: "rect(0px,0px,0px,0px)",
                    parser: function(e, t, s, o, i, l) {
                        var n, a, r;
                        return t = C < 9 ? (a = e.currentStyle, r = C < 8 ? " " : ",", n = "rect(" + a.clipTop + r + a.clipRight + r + a.clipBottom + r + a.clipLeft + ")", this.format(t).split(",").join(r)) : (n = this.format(re(e, this.p, B, !1, this.dflt)), this.format(t)), this.parseComplex(e.style, n, t, i, l)
                    }
                }), Be("textShadow", {
                    defaultValue: "0px 0px 0px #999",
                    color: !0,
                    multi: !0
                }), Be("autoRound,strictUnits", {
                    parser: function(e, t, s, o, i) {
                        return i
                    }
                }), Be("border", {
                    defaultValue: "0px solid #000",
                    parser: function(e, t, s, o, i, l) {
                        var n = re(e, "borderTopWidth", B, !1, "0px"),
                            a = this.format(t).split(" "),
                            r = a[0].replace(A, "");
                        return "px" !== r && (n = parseFloat(n) / de(e, "borderTopWidth", 1, r) + r), this.parseComplex(e.style, this.format(n + " " + re(e, "borderTopStyle", B, !1, "solid") + " " + re(e, "borderTopColor", B, !1, "#000")), a.join(" "), i, l)
                    },
                    color: !0,
                    formatter: function(e) {
                        var t = e.split(" ");
                        return t[0] + " " + (t[1] || "solid") + " " + (e.match(me) || ["#000"])[0]
                    }
                }), Be("borderWidth", {
                    parser: ge("borderTopWidth,borderRightWidth,borderBottomWidth,borderLeftWidth")
                }), Be("float,cssFloat,styleFloat", {
                    parser: function(e, t, s, o, i, l) {
                        var n = e.style,
                            a = "cssFloat" in n ? "cssFloat" : "styleFloat";
                        return new Se(n, a, 0, 0, i, -1, s, !1, 0, n[a], t)
                    }
                });

                function qe(e) {
                    var t, s = this.t,
                        o = s.filter || re(this.data, "filter") || "",
                        i = this.s + this.c * e | 0;
                    100 == i && (t = -1 === o.indexOf("atrix(") && -1 === o.indexOf("radient(") && -1 === o.indexOf("oader(") ? (s.removeAttribute("filter"), !re(this.data, "filter")) : (s.filter = o.replace(r, ""), !0)), t || (this.xn1 && (s.filter = o = o || "alpha(opacity=" + i + ")"), -1 === o.indexOf("pacity") ? 0 == i && this.xn1 || (s.filter = o + " alpha(opacity=" + i + ")") : s.filter = o.replace(M, "opacity=" + i))
                }
                Be("opacity,alpha,autoAlpha", {
                    defaultValue: "1",
                    parser: function(e, t, s, o, i, l) {
                        var n = parseFloat(re(e, "opacity", B, !1, "1")),
                            a = e.style,
                            r = "autoAlpha" === s;
                        return "string" == typeof t && "=" === t.charAt(1) && (t = ("-" === t.charAt(0) ? -1 : 1) * parseFloat(t.substr(2)) + n), r && 1 === n && "hidden" === re(e, "visibility", B) && 0 !== t && (n = 0), ie ? i = new Se(a, "opacity", n, t - n, i) : ((i = new Se(a, "opacity", 100 * n, 100 * (t - n), i)).xn1 = r ? 1 : 0, a.zoom = 1, i.type = 2, i.b = "alpha(opacity=" + i.s + ")", i.e = "alpha(opacity=" + (i.s + i.c) + ")", i.data = e, i.plugin = l, i.setRatio = qe), r && ((i = new Se(a, "visibility", 0, 0, i, -1, null, !1, 0, 0 !== n ? "inherit" : "hidden", 0 === t ? "hidden" : "inherit")).xs0 = "inherit", o._overwriteProps.push(i.n), o._overwriteProps.push(s)), i
                    }
                });

                function Ke(e) {
                    if (this.t._gsClassPT = this, 1 === e || 0 === e) {
                        this.t.setAttribute("class", 0 === e ? this.b : this.e);
                        for (var t = this.data, s = this.t.style; t;) t.v ? s[t.p] = t.v : Je(s, t.p), t = t._next;
                        1 === e && this.t._gsClassPT === this && (this.t._gsClassPT = null)
                    } else this.t.getAttribute("class") !== this.e && this.t.setAttribute("class", this.e)
                }
                var Je = function(e, t) {
                    t && (e.removeProperty ? ("ms" !== t.substr(0, 2) && "webkit" !== t.substr(0, 6) || (t = "-" + t), e.removeProperty(t.replace(h, "-$1").toLowerCase())) : e.removeAttribute(t))
                };
                Be("className", {
                    parser: function(e, t, s, o, i, l, n) {
                        var a, r, d, u, h, c = e.getAttribute("class") || "",
                            _ = e.style.cssText;
                        if ((i = o._classNamePT = new Se(e, s, 0, 0, i, 2)).setRatio = Ke, i.pr = -11, f = !0, i.b = c, r = g(e, B), d = e._gsClassPT) {
                            for (u = {}, h = d.data; h;) u[h.p] = 1, h = h._next;
                            d.setRatio(1)
                        }
                        return (e._gsClassPT = i).e = "=" !== t.charAt(1) ? t : c.replace(new RegExp("(?:\\s|^)" + t.substr(2) + "(?![\\w-])"), "") + ("+" === t.charAt(0) ? " " + t.substr(2) : ""), e.setAttribute("class", i.e), a = y(e, r, g(e), n, u), e.setAttribute("class", c), i.data = a.firstMPT, e.style.cssText = _, i = i.xfirst = o.parse(e, a.difs, i, l)
                    }
                });

                function Ze(e) {
                    if ((1 === e || 0 === e) && this.data._totalTime === this.data._totalDuration && "isFromStart" !== this.data.data) {
                        var t, s, o, i, l, n = this.t.style,
                            a = m.transform.parse;
                        if ("all" === this.e) i = !(n.cssText = "");
                        else
                            for (o = (t = this.e.split(" ").join("").split(",")).length; - 1 < --o;) s = t[o], m[s] && (m[s].parse === a ? i = !0 : s = "transformOrigin" === s ? ke : m[s].p), Je(n, s);
                        i && (Je(n, xe), (l = this.t._gsTransform) && (l.svg && (this.t.removeAttribute("data-svg-origin"), this.t.removeAttribute("transform")), delete this.t._gsTransform))
                    }
                }
                for (Be("clearProps", {
                        parser: function(e, t, s, o, i) {
                            return (i = new Se(e, s, 0, 0, i, 2)).setRatio = Ze, i.e = t, i.pr = -10, i.data = o._tween, f = !0, i
                        }
                    }), e = "bezier,throwProps,physicsProps,physics2D".split(","), we = e.length; we--;) De(e[we]);
                (e = R.prototype)._firstPT = e._lastParsedTransform = e._transform = null, e._onInitTween = function(e, t, s, o) {
                    if (!e.nodeType) return !1;
                    this._target = V = e, this._tween = s, this._vars = t, E = o, U = t.autoRound, f = !1, T = t.suffixMap || R.suffixMap, B = ae(e, ""), p = this._overwriteProps;
                    var i, l, n, a, r, d, u, h, c, _ = e.style;
                    if (S && "" === _.zIndex && ("auto" !== (i = re(e, "zIndex", B)) && "" !== i || this._addLazySet(_, "zIndex", 0)), "string" == typeof t && (a = _.cssText, i = g(e, B), _.cssText = a + ";" + t, i = y(e, i, g(e)).difs, !ie && N.test(t) && (i.opacity = parseFloat(RegExp.$1)), t = i, _.cssText = a), t.className ? this._firstPT = l = m.className.parse(e, t.className, "className", this, null, null, t) : this._firstPT = l = this.parse(e, t, null), this._transformType) {
                        for (c = 3 === this._transformType, xe ? P && (S = !0, "" === _.zIndex && ("auto" !== (u = re(e, "zIndex", B)) && "" !== u || this._addLazySet(_, "zIndex", 0)), w && this._addLazySet(_, "WebkitBackfaceVisibility", this._vars.WebkitBackfaceVisibility || (c ? "visible" : "hidden"))) : _.zoom = 1, n = l; n && n._next;) n = n._next;
                        h = new Se(e, "transform", 0, 0, null, 2), this._linkCSSP(h, null, n), h.setRatio = xe ? Ge : He, h.data = this._transform || Qe(e, B, !0), h.tween = s, h.pr = -1, p.pop()
                    }
                    if (f) {
                        for (; l;) {
                            for (d = l._next, n = a; n && n.pr > l.pr;) n = n._next;
                            (l._prev = n ? n._prev : r) ? l._prev._next = l: a = l, (l._next = n) ? n._prev = l : r = l, l = d
                        }
                        this._firstPT = a
                    }
                    return !0
                }, e.parse = function(e, t, s, o) {
                    var i, l, n, a, r, d, u, h, c, _, f = e.style;
                    for (i in t) "function" == typeof(d = t[i]) && (d = d(E, V)), (l = m[i]) ? s = l.parse(e, d, i, this, s, o, t) : (r = re(e, i, B) + "", c = "string" == typeof d, "color" === i || "fill" === i || "stroke" === i || -1 !== i.indexOf("Color") || c && j.test(d) ? (c || (d = (3 < (d = pe(d)).length ? "rgba(" : "rgb(") + d.join(",") + ")"), s = Pe(f, i, r, d, !0, "transparent", s, 0, o)) : c && q.test(d) ? s = Pe(f, i, r, d, !0, null, s, 0, o) : (u = (n = parseFloat(r)) || 0 === n ? r.substr((n + "").length) : "", "" !== r && "auto" !== r || (u = "width" === i || "height" === i ? (n = v(e, i, B), "px") : "left" === i || "top" === i ? (n = ue(e, i, B), "px") : (n = "opacity" !== i ? 0 : 1, "")), "" === (h = (_ = c && "=" === d.charAt(1)) ? (a = parseInt(d.charAt(0) + "1", 10), d = d.substr(2), a *= parseFloat(d), d.replace(A, "")) : (a = parseFloat(d), c ? d.replace(A, "") : "")) && (h = i in T ? T[i] : u), d = a || 0 === a ? (_ ? a + n : a) + h : t[i], u !== h && "" !== h && (a || 0 === a) && n && (n = de(e, i, n, u), "%" === h ? (n /= de(e, i, 100, "%") / 100, !0 !== t.strictUnits && (r = n + "%")) : "em" === h || "rem" === h || "vw" === h || "vh" === h ? n /= de(e, i, 1, h) : "px" !== h && (a = de(e, i, a, h), h = "px"), _ && (!a && 0 !== a || (d = a + n + h))), _ && (a += n), !n && 0 !== n || !a && 0 !== a ? void 0 !== f[i] && (d || d + "" != "NaN" && null != d) ? (s = new Se(f, i, a || n || 0, 0, s, -1, i, !1, 0, r, d)).xs0 = "none" !== d || "display" !== i && -1 === i.indexOf("Style") ? d : r : b("invalid " + i + " tween value: " + t[i]) : (s = new Se(f, i, n, a - n, s, 0, i, !1 !== U && ("px" === h || "zIndex" === i), 0, r, d)).xs0 = h)), o && s && !s.plugin && (s.plugin = o);
                    return s
                }, e.setRatio = function(e) {
                    var t, s, o, i = this._firstPT;
                    if (1 !== e || this._tween._time !== this._tween._duration && 0 !== this._tween._time)
                        if (e || this._tween._time !== this._tween._duration && 0 !== this._tween._time || -1e-6 === this._tween._rawPrevTime)
                            for (; i;) {
                                if (t = i.c * e + i.s, i.r ? t = Math.round(t) : t < 1e-6 && -1e-6 < t && (t = 0), i.type)
                                    if (1 === i.type)
                                        if (2 === (o = i.l)) i.t[i.p] = i.xs0 + t + i.xs1 + i.xn1 + i.xs2;
                                        else if (3 === o) i.t[i.p] = i.xs0 + t + i.xs1 + i.xn1 + i.xs2 + i.xn2 + i.xs3;
                                else if (4 === o) i.t[i.p] = i.xs0 + t + i.xs1 + i.xn1 + i.xs2 + i.xn2 + i.xs3 + i.xn3 + i.xs4;
                                else if (5 === o) i.t[i.p] = i.xs0 + t + i.xs1 + i.xn1 + i.xs2 + i.xn2 + i.xs3 + i.xn3 + i.xs4 + i.xn4 + i.xs5;
                                else {
                                    for (s = i.xs0 + t + i.xs1, o = 1; o < i.l; o++) s += i["xn" + o] + i["xs" + (o + 1)];
                                    i.t[i.p] = s
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
                                                for (o = i.l, s = i.xs0 + t + i.xs1, o = 1; o < i.l; o++) s += i["xn" + o] + i["xs" + (o + 1)];
                                                i.t[i.p] = s
                                            }
                                        } else i.t[i.p] = t + i.xs0;
                                else i.t[i.p] = i.e;
                                else i.setRatio(e);
                                i = i._next
                            }
                }, e._enableTransforms = function(e) {
                    this._transform = this._transform || Qe(this._target, B, !0), this._transformType = this._transform.svg && Ue || !e && 3 !== this._transformType ? 2 : 3
                };

                function $e(e) {
                    this.t[this.p] = this.e, this.data._linkCSSP(this, this._next, null, !0)
                }
                e._addLazySet = function(e, t, s) {
                    var o = this._firstPT = new Se(e, t, 0, 0, this._firstPT, 2);
                    o.e = s, o.setRatio = $e, o.data = this
                }, e._linkCSSP = function(e, t, s, o) {
                    return e && (t && (t._prev = e), e._next && (e._next._prev = e._prev), e._prev ? e._prev._next = e._next : this._firstPT === e && (this._firstPT = e._next, o = !0), s ? s._next = e : o || null !== this._firstPT || (this._firstPT = e), e._next = t, e._prev = s), e
                }, e._mod = function(e) {
                    for (var t = this._firstPT; t;) "function" == typeof e[t.p] && e[t.p] === Math.round && (t.r = 1), t = t._next
                }, e._kill = function(e) {
                    var t, s, o, i = e;
                    if (e.autoAlpha || e.alpha) {
                        for (s in i = {}, e) i[s] = e[s];
                        i.opacity = 1, i.autoAlpha && (i.visibility = 1)
                    }
                    for (e.className && (t = this._classNamePT) && ((o = t.xfirst) && o._prev ? this._linkCSSP(o._prev, t._next, o._prev._prev) : o === this._firstPT && (this._firstPT = t._next), t._next && this._linkCSSP(t._next, t._next._next, o._prev), this._classNamePT = null), t = this._firstPT; t;) t.plugin && t.plugin !== s && t.plugin._kill && (t.plugin._kill(e), s = t.plugin), t = t._next;
                    return l.prototype._kill.call(this, i)
                };
                var et = function(e, t, s) {
                    var o, i, l, n;
                    if (e.slice)
                        for (i = e.length; - 1 < --i;) et(e[i], t, s);
                    else
                        for (i = (o = e.childNodes).length; - 1 < --i;) n = (l = o[i]).type, l.style && (t.push(g(l)), s && s.push(l)), 1 !== n && 9 !== n && 11 !== n || !l.childNodes.length || et(l, t, s)
                };
                return R.cascadeTo = function(e, t, s) {
                    var o, i, l, n, a = L.to(e, t, s),
                        r = [a],
                        d = [],
                        u = [],
                        h = [],
                        c = L._internals.reservedProps;
                    for (e = a._targets || a.target, et(e, d, h), a.render(t, !0, !0), et(e, u), a.render(0, !0, !0), a._enabled(!0), o = h.length; - 1 < --o;)
                        if ((i = y(h[o], d[o], u[o])).firstMPT) {
                            for (l in i = i.difs, s) c[l] && (i[l] = s[l]);
                            for (l in n = {}, i) n[l] = d[o][l];
                            r.push(L.fromTo(h[o], t, n, i))
                        } return r
                }, l.activate([R]), R
            }, !0), t = _fwd_gsScope.FWDFWD_gsDefine.plugin({
                propName: "roundProps",
                version: "1.6.0",
                priority: -1,
                API: 2,
                init: function(e, t, s) {
                    return this._tween = s, !0
                }
            }), (o = t.prototype)._onInitAllProps = function() {
                for (var e, t, s, o = this._tween, i = o.vars.roundProps.join ? o.vars.roundProps : o.vars.roundProps.split(","), l = i.length, n = {}, a = o._propLookup.roundProps; - 1 < --l;) n[i[l]] = Math.round;
                for (l = i.length; - 1 < --l;)
                    for (e = i[l], t = o._firstPT; t;) s = t._next, t.pg ? t.t._mod(n) : t.n === e && (2 === t.f && t.t ? r(t.t._firstPT) : (this._add(t.t, e, t.s, t.c), s && (s._prev = t._prev), t._prev ? t._prev._next = s : o._firstPT === t && (o._firstPT = s), t._next = t._prev = null, o._propLookup[e] = a)), t = s;
                return !1
            }, o._add = function(e, t, s, o) {
                this._addTween(e, t, s, s + o, t, Math.round), this._overwriteProps.push(t)
            }, _fwd_gsScope.FWDFWD_gsDefine.plugin({
                propName: "attr",
                API: 2,
                version: "0.6.0",
                init: function(e, t, s, o) {
                    var i, l;
                    if ("function" != typeof e.setAttribute) return !1;
                    for (i in t) "function" == typeof(l = t[i]) && (l = l(o, e)), this._addTween(e, "setAttribute", e.getAttribute(i) + "", l + "", i, !1, i), this._overwriteProps.push(i);
                    return !0
                }
            }), _fwd_gsScope.FWDFWD_gsDefine.plugin({
                propName: "directionalRotation",
                version: "0.3.0",
                API: 2,
                init: function(e, t, s, o) {
                    "object" != typeof t && (t = {
                        rotation: t
                    }), this.finals = {};
                    var i, l, n, a, r, d, u = !0 === t.useRadians ? 2 * Math.PI : 360;
                    for (i in t) "useRadians" !== i && ("function" == typeof(a = t[i]) && (a = a(o, e)), l = (d = (a + "").split("_"))[0], n = parseFloat("function" != typeof e[i] ? e[i] : e[i.indexOf("set") || "function" != typeof e["get" + i.substr(3)] ? i : "get" + i.substr(3)]()), r = (a = this.finals[i] = "string" == typeof l && "=" === l.charAt(1) ? n + parseInt(l.charAt(0) + "1", 10) * Number(l.substr(2)) : Number(l) || 0) - n, d.length && (-1 !== (l = d.join("_")).indexOf("short") && (r %= u) !== r % (u / 2) && (r = r < 0 ? r + u : r - u), -1 !== l.indexOf("_cw") && r < 0 ? r = (r + 9999999999 * u) % u - (r / u | 0) * u : -1 !== l.indexOf("ccw") && 0 < r && (r = (r - 9999999999 * u) % u - (r / u | 0) * u)), (1e-6 < r || r < -1e-6) && (this._addTween(e, i, n, n + r, i), this._overwriteProps.push(i)));
                    return !0
                },
                set: function(e) {
                    var t;
                    if (1 !== e) this._super.setRatio.call(this, e);
                    else
                        for (t = this._firstPT; t;) t.f ? t.t[t.p](this.finals[t.p]) : t.t[t.p] = this.finals[t.p], t = t._next
                }
            })._autoCSS = !0, _fwd_gsScope.FWDFWD_gsDefine("easing.Back", ["easing.Ease"], function(m) {
                function e(e, t) {
                    var s = u("easing." + e, function() {}, !0),
                        o = s.prototype = new m;
                    return o.constructor = s, o.getRatio = t, s
                }

                function t(e, t, s, o, i) {
                    var l = u("easing." + e, {
                        easeOut: new t,
                        easeIn: new s,
                        easeInOut: new o
                    }, !0);
                    return h(l, e), l
                }

                function b(e, t, s) {
                    this.t = e, this.v = t, s && (((this.next = s).prev = this).c = s.v - t, this.gap = s.t - e)
                }

                function s(e, t) {
                    var s = u("easing." + e, function(e) {
                            this._p1 = e || 0 === e ? e : 1.70158, this._p2 = 1.525 * this._p1
                        }, !0),
                        o = s.prototype = new m;
                    return o.constructor = s, o.getRatio = t, o.config = function(e) {
                        return new s(e)
                    }, s
                }
                var o, i, l, n = _fwd_gsScope.FWDGreenSockGlobals || _fwd_gsScope,
                    a = n.com.greensock,
                    r = 2 * Math.PI,
                    d = Math.PI / 2,
                    u = a._class,
                    h = m.register || function() {},
                    c = t("Back", s("BackOut", function(e) {
                        return --e * e * ((this._p1 + 1) * e + this._p1) + 1
                    }), s("BackIn", function(e) {
                        return e * e * ((this._p1 + 1) * e - this._p1)
                    }), s("BackInOut", function(e) {
                        return (e *= 2) < 1 ? .5 * e * e * ((this._p2 + 1) * e - this._p2) : .5 * ((e -= 2) * e * ((this._p2 + 1) * e + this._p2) + 2)
                    })),
                    _ = u("easing.SlowMo", function(e, t, s) {
                        t = t || 0 === t ? t : .7, null == e ? e = .7 : 1 < e && (e = 1), this._p = 1 !== e ? t : 0, this._p1 = (1 - e) / 2, this._p2 = e, this._p3 = this._p1 + this._p2, this._calcEnd = !0 === s
                    }, !0),
                    f = _.prototype = new m;
                return f.constructor = _, f.getRatio = function(e) {
                    var t = e + (.5 - e) * this._p;
                    return e < this._p1 ? this._calcEnd ? 1 - (e = 1 - e / this._p1) * e : t - (e = 1 - e / this._p1) * e * e * e * t : e > this._p3 ? this._calcEnd ? 1 - (e = (e - this._p3) / this._p1) * e : t + (e - t) * (e = (e - this._p3) / this._p1) * e * e * e : this._calcEnd ? 1 : t
                }, _.ease = new _(.7, .7), f.config = _.config = function(e, t, s) {
                    return new _(e, t, s)
                }, (f = (o = u("easing.SteppedEase", function(e) {
                    e = e || 1, this._p1 = 1 / e, this._p2 = e + 1
                }, !0)).prototype = new m).constructor = o, f.getRatio = function(e) {
                    return e < 0 ? e = 0 : 1 <= e && (e = .999999999), (this._p2 * e >> 0) * this._p1
                }, f.config = o.config = function(e) {
                    return new o(e)
                }, (f = (i = u("easing.RoughEase", function(e) {
                    for (var t, s, o, i, l, n, a = (e = e || {}).taper || "none", r = [], d = 0, u = 0 | (e.points || 20), h = u, c = !1 !== e.randomize, _ = !0 === e.clamp, f = e.template instanceof m ? e.template : null, p = "number" == typeof e.strength ? .4 * e.strength : .4; - 1 < --h;) t = c ? Math.random() : 1 / u * h, s = f ? f.getRatio(t) : t, o = "none" === a ? p : "out" === a ? (i = 1 - t) * i * p : "in" === a ? t * t * p : t < .5 ? (i = 2 * t) * i * .5 * p : (i = 2 * (1 - t)) * i * .5 * p, c ? s += Math.random() * o - .5 * o : h % 2 ? s += .5 * o : s -= .5 * o, _ && (1 < s ? s = 1 : s < 0 && (s = 0)), r[d++] = {
                        x: t,
                        y: s
                    };
                    for (r.sort(function(e, t) {
                            return e.x - t.x
                        }), n = new b(1, 1, null), h = u; - 1 < --h;) l = r[h], n = new b(l.x, l.y, n);
                    this._prev = new b(0, 0, 0 !== n.t ? n : n.next)
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
                })), t("Elastic", (l = function(e, t, s) {
                    var o = u("easing." + e, function(e, t) {
                            this._p1 = 1 <= e ? e : 1, this._p2 = (t || s) / (e < 1 ? e : 1), this._p3 = this._p2 / r * (Math.asin(1 / this._p1) || 0), this._p2 = r / this._p2
                        }, !0),
                        i = o.prototype = new m;
                    return i.constructor = o, i.getRatio = t, i.config = function(e, t) {
                        return new o(e, t)
                    }, o
                })("ElasticOut", function(e) {
                    return this._p1 * Math.pow(2, -10 * e) * Math.sin((e - this._p3) * this._p2) + 1
                }, .3), l("ElasticIn", function(e) {
                    return -this._p1 * Math.pow(2, 10 * --e) * Math.sin((e - this._p3) * this._p2)
                }, .3), l("ElasticInOut", function(e) {
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
                }, !0), h(n.SlowMo, "SlowMo", "ease,"), h(i, "RoughEase", "ease,"), h(o, "SteppedEase", "ease,"), c
            }, !0)
        }), _fwd_gsScope.FWDFWD_gsDefine && _fwd_gsScope._fwd_gsQueue.pop()(),

        function(_, f) {
            "use strict";
            var p = {},
                m = _.FWDGreenSockGlobals = _.FWDGreenSockGlobals || _;
            if (!m.FWDTweenLite) {
                var e, t, s, b, g, o, i, y = function(e) {
                        var t, s = e.split("."),
                            o = m;
                        for (t = 0; t < s.length; t++) o[s[t]] = o = o[s[t]] || {};
                        return o
                    },
                    h = y("com.greensock"),
                    v = 1e-10,
                    r = function(e) {
                        var t, s = [],
                            o = e.length;
                        for (t = 0; t !== o; s.push(e[t++]));
                        return s
                    },
                    S = function() {},
                    P = (o = Object.prototype.toString, i = o.call([]), function(e) {
                        return null != e && (e instanceof Array || "object" == typeof e && !!e.push && o.call(e) === i)
                    }),
                    w = {},
                    T = function(r, d, u, h) {
                        this.sc = w[r] ? w[r].sc : [], (w[r] = this).gsClass = null, this.func = u;
                        var c = [];
                        this.check = function(e) {
                            for (var t, s, o, i, l, n = d.length, a = n; - 1 < --n;)(t = w[d[n]] || new T(d[n], [])).gsClass ? (c[n] = t.gsClass, a--) : e && t.sc.push(this);
                            if (0 === a && u) {
                                if (o = (s = ("com.greensock." + r).split(".")).pop(), i = y(s.join("."))[o] = this.gsClass = u.apply(u, c), h)
                                    if (m[o] = p[o] = i, !(l = "undefined" != typeof fwd_module && fwd_module.exports) && "function" == typeof define && define.amd) define((_.FWDGreenSockAMDPath ? _.FWDGreenSockAMDPath + "/" : "") + r.split(".").pop(), [], function() {
                                        return i
                                    });
                                    else if (l)
                                    if (r === f)
                                        for (n in fwd_module.exports = p[f] = i, p) i[n] = p[n];
                                    else p[f] && (p[f][o] = i);
                                for (n = 0; n < this.sc.length; n++) this.sc[n].check()
                            }
                        }, this.check(!0)
                    },
                    l = _.FWDFWD_gsDefine = function(e, t, s, o) {
                        return new T(e, t, s, o)
                    },
                    c = h._class = function(e, t, s) {
                        return t = t || function() {}, l(e, [], function() {
                            return t
                        }, s), t
                    };
                l.globals = m;
                var n = [0, 0, 1, 1],
                    B = c("easing.Ease", function(e, t, s, o) {
                        this._func = e, this._type = s || 0, this._power = o || 0, this._params = t ? n.concat(t) : n
                    }, !0),
                    D = B.map = {},
                    a = B.register = function(e, t, s, o) {
                        for (var i, l, n, a, r = t.split(","), d = r.length, u = (s || "easeIn,easeOut,easeInOut").split(","); - 1 < --d;)
                            for (l = r[d], i = o ? c("easing." + l, null, !0) : h.easing[l] || {}, n = u.length; - 1 < --n;) a = u[n], D[l + "." + a] = D[a + l] = i[a] = e.getRatio ? e : e[a] || new e
                    };
                for ((s = B.prototype)._calcEnd = !1, s.getRatio = function(e) {
                        if (this._func) return this._params[0] = e, this._func.apply(null, this._params);
                        var t = this._type,
                            s = this._power,
                            o = 1 === t ? 1 - e : 2 === t ? e : e < .5 ? 2 * e : 2 * (1 - e);
                        return 1 === s ? o *= o : 2 === s ? o *= o * o : 3 === s ? o *= o * o * o : 4 === s && (o *= o * o * o * o), 1 === t ? 1 - o : 2 === t ? o : e < .5 ? o / 2 : 1 - o / 2
                    }, t = (e = ["Linear", "Quad", "Cubic", "Quart", "Quint,Strong"]).length; - 1 < --t;) s = e[t] + ",Power" + t, a(new B(null, null, 1, t), s, "easeOut", !0), a(new B(null, null, 2, t), s, "easeIn" + (0 === t ? ",easeNone" : "")), a(new B(null, null, 3, t), s, "easeInOut");
                D.linear = h.easing.Linear.easeIn, D.swing = h.easing.Quad.easeInOut;
                var W = c("events.EventDispatcher", function(e) {
                    this._listeners = {}, this._eventTarget = e || this
                });
                (s = W.prototype).addEventListener = function(e, t, s, o, i) {
                    i = i || 0;
                    var l, n, a = this._listeners[e],
                        r = 0;
                    for (this !== b || g || b.wake(), null == a && (this._listeners[e] = a = []), n = a.length; - 1 < --n;)(l = a[n]).c === t && l.s === s ? a.splice(n, 1) : 0 === r && l.pr < i && (r = n + 1);
                    a.splice(r, 0, {
                        c: t,
                        s: s,
                        up: o,
                        pr: i
                    })
                }, s.removeEventListener = function(e, t) {
                    var s, o = this._listeners[e];
                    if (o)
                        for (s = o.length; - 1 < --s;)
                            if (o[s].c === t) return void o.splice(s, 1)
                }, s.dispatchEvent = function(e) {
                    var t, s, o, i = this._listeners[e];
                    if (i)
                        for (1 < (t = i.length) && (i = i.slice(0)), s = this._eventTarget; - 1 < --t;)(o = i[t]) && (o.up ? o.c.call(o.s || s, {
                            type: e,
                            target: s
                        }) : o.c.call(o.s || s))
                };
                var F = _.requestAnimationFrame,
                    H = _.cancelAnimationFrame,
                    U = Date.now || function() {
                        return (new Date).getTime()
                    },
                    C = U();
                for (t = (e = ["ms", "moz", "webkit", "o"]).length; - 1 < --t && !F;) F = _[e[t] + "RequestAnimationFrame"], H = _[e[t] + "CancelAnimationFrame"] || _[e[t] + "CancelRequestAnimationFrame"];
                c("Ticker", function(e, t) {
                    var i, l, n, a, r, d = this,
                        u = U(),
                        s = !(!1 === t || !F) && "auto",
                        h = 500,
                        c = 33,
                        _ = function(e) {
                            var t, s, o = U() - C;
                            h < o && (u += o - c), C += o, d.time = (C - u) / 1e3, t = d.time - r, (!i || 0 < t || !0 === e) && (d.frame++, r += t + (a <= t ? .004 : a - t), s = !0), !0 !== e && (n = l(_)), s && d.dispatchEvent("tick")
                        };
                    W.call(d), d.time = d.frame = 0, d.tick = function() {
                        _(!0)
                    }, d.lagSmoothing = function(e, t) {
                        h = e || 1e10, c = Math.min(t, h, 0)
                    }, d.sleep = function() {
                        null != n && ((s && H ? H : clearTimeout)(n), l = S, n = null, d === b && (g = !1))
                    }, d.wake = function(e) {
                        null !== n ? d.sleep() : e ? u += -C + (C = U()) : 10 < d.frame && (C = U() - h + 5), l = 0 === i ? S : s && F ? F : function(e) {
                            return setTimeout(e, 1e3 * (r - d.time) + 1 | 0)
                        }, d === b && (g = !0), _(2)
                    }, d.fps = function(e) {
                        if (!arguments.length) return i;
                        a = 1 / ((i = e) || 60), r = this.time + a, d.wake()
                    }, d.useRAF = function(e) {
                        if (!arguments.length) return s;
                        d.sleep(), s = e, d.fps(i)
                    }, d.fps(e), setTimeout(function() {
                        "auto" === s && d.frame < 5 && "hidden" !== document.visibilityState && d.useRAF(!1)
                    }, 1500)
                }), (s = h.Ticker.prototype = new h.events.EventDispatcher).constructor = h.Ticker;
                var d = c("core.FWDAnimation", function(e, t) {
                    if (this.vars = t = t || {}, this._duration = this._totalDuration = e || 0, this._delay = Number(t.delay) || 0, this._timeScale = 1, this._active = !0 === t.immediateRender, this.data = t.data, this._reversed = !0 === t.reversed, G) {
                        g || b.wake();
                        var s = this.vars.useFrames ? Q : G;
                        s.add(this, s._time), this.vars.paused && this.paused(!0)
                    }
                });
                b = d.ticker = new h.Ticker, (s = d.prototype)._dirty = s._gc = s._initted = s._paused = !1, s._totalTime = s._time = 0, s._rawPrevTime = -1, s._next = s._last = s._onUpdate = s._timeline = s.timeline = null, s._paused = !1;
                var u = function() {
                    g && 2e3 < U() - C && b.wake(), setTimeout(u, 2e3)
                };
                u(), s.play = function(e, t) {
                    return null != e && this.seek(e, t), this.reversed(!1).paused(!1)
                }, s.pause = function(e, t) {
                    return null != e && this.seek(e, t), this.paused(!0)
                }, s.resume = function(e, t) {
                    return null != e && this.seek(e, t), this.paused(!1)
                }, s.seek = function(e, t) {
                    return this.totalTime(Number(e), !1 !== t)
                }, s.restart = function(e, t) {
                    return this.reversed(!1).paused(!1).totalTime(e ? -this._delay : 0, !1 !== t, !0)
                }, s.reverse = function(e, t) {
                    return null != e && this.seek(e || this.totalDuration(), t), this.reversed(!0).paused(!1)
                }, s.render = function(e, t, s) {}, s.invalidate = function() {
                    return this._time = this._totalTime = 0, this._initted = this._gc = !1, this._rawPrevTime = -1, !this._gc && this.timeline || this._enabled(!0), this
                }, s.isActive = function() {
                    var e, t = this._timeline,
                        s = this._startTime;
                    return !t || !this._gc && !this._paused && t.isActive() && (e = t.rawTime()) >= s && e < s + this.totalDuration() / this._timeScale
                }, s._enabled = function(e, t) {
                    return g || b.wake(), this._gc = !e, this._active = this.isActive(), !0 !== t && (e && !this.timeline ? this._timeline.add(this, this._startTime - this._delay) : !e && this.timeline && this._timeline._remove(this, !0)), !1
                }, s._kill = function(e, t) {
                    return this._enabled(!1, !1)
                }, s.kill = function(e, t) {
                    return this._kill(e, t), this
                }, s._uncache = function(e) {
                    for (var t = e ? this : this.timeline; t;) t._dirty = !0, t = t.timeline;
                    return this
                }, s._swapSelfInParams = function(e) {
                    for (var t = e.length, s = e.concat(); - 1 < --t;) "{self}" === e[t] && (s[t] = this);
                    return s
                }, s._callback = function(e) {
                    var t = this.vars,
                        s = t[e],
                        o = t[e + "Params"],
                        i = t[e + "Scope"] || t.callbackScope || this;
                    switch (o ? o.length : 0) {
                        case 0:
                            s.call(i);
                            break;
                        case 1:
                            s.call(i, o[0]);
                            break;
                        case 2:
                            s.call(i, o[0], o[1]);
                            break;
                        default:
                            s.apply(i, o)
                    }
                }, s.eventCallback = function(e, t, s, o) {
                    if ("on" === (e || "").substr(0, 2)) {
                        var i = this.vars;
                        if (1 === arguments.length) return i[e];
                        null == t ? delete i[e] : (i[e] = t, i[e + "Params"] = P(s) && -1 !== s.join("").indexOf("{self}") ? this._swapSelfInParams(s) : s, i[e + "Scope"] = o), "onUpdate" === e && (this._onUpdate = t)
                    }
                    return this
                }, s.delay = function(e) {
                    return arguments.length ? (this._timeline.smoothChildTiming && this.startTime(this._startTime + e - this._delay), this._delay = e, this) : this._delay
                }, s.duration = function(e) {
                    return arguments.length ? (this._duration = this._totalDuration = e, this._uncache(!0), this._timeline.smoothChildTiming && 0 < this._time && this._time < this._duration && 0 !== e && this.totalTime(this._totalTime * (e / this._duration), !0), this) : (this._dirty = !1, this._duration)
                }, s.totalDuration = function(e) {
                    return this._dirty = !1, arguments.length ? this.duration(e) : this._totalDuration
                }, s.time = function(e, t) {
                    return arguments.length ? (this._dirty && this.totalDuration(), this.totalTime(e > this._duration ? this._duration : e, t)) : this._time
                }, s.totalTime = function(e, t, s) {
                    if (g || b.wake(), !arguments.length) return this._totalTime;
                    if (this._timeline) {
                        if (e < 0 && !s && (e += this.totalDuration()), this._timeline.smoothChildTiming) {
                            this._dirty && this.totalDuration();
                            var o = this._totalDuration,
                                i = this._timeline;
                            if (o < e && !s && (e = o), this._startTime = (this._paused ? this._pauseTime : i._time) - (this._reversed ? o - e : e) / this._timeScale, i._dirty || this._uncache(!1), i._timeline)
                                for (; i._timeline;) i._timeline._time !== (i._startTime + i._totalTime) / i._timeScale && i.totalTime(i._totalTime, !0), i = i._timeline
                        }
                        this._gc && this._enabled(!0, !1), this._totalTime === e && 0 !== this._duration || (I.length && K(), this.render(e, t, !1), I.length && K())
                    }
                    return this
                }, s.progress = s.totalProgress = function(e, t) {
                    var s = this.duration();
                    return arguments.length ? this.totalTime(s * e, t) : s ? this._time / s : this.ratio
                }, s.startTime = function(e) {
                    return arguments.length ? (e !== this._startTime && (this._startTime = e, this.timeline && this.timeline._sortChildren && this.timeline.add(this, e - this._delay)), this) : this._startTime
                }, s.endTime = function(e) {
                    return this._startTime + (0 != e ? this.totalDuration() : this.duration()) / this._timeScale
                }, s.timeScale = function(e) {
                    if (!arguments.length) return this._timeScale;
                    if (e = e || v, this._timeline && this._timeline.smoothChildTiming) {
                        var t = this._pauseTime,
                            s = t || 0 === t ? t : this._timeline.totalTime();
                        this._startTime = s - (s - this._startTime) * this._timeScale / e
                    }
                    return this._timeScale = e, this._uncache(!1)
                }, s.reversed = function(e) {
                    return arguments.length ? (e != this._reversed && (this._reversed = e, this.totalTime(this._timeline && !this._timeline.smoothChildTiming ? this.totalDuration() - this._totalTime : this._totalTime, !0)), this) : this._reversed
                }, s.paused = function(e) {
                    if (!arguments.length) return this._paused;
                    var t, s, o = this._timeline;
                    return e != this._paused && o && (g || e || b.wake(), s = (t = o.rawTime()) - this._pauseTime, !e && o.smoothChildTiming && (this._startTime += s, this._uncache(!1)), this._pauseTime = e ? t : null, this._paused = e, this._active = this.isActive(), !e && 0 != s && this._initted && this.duration() && (t = o.smoothChildTiming ? this._totalTime : (t - this._startTime) / this._timeScale, this.render(t, t === this._totalTime, !0))), this._gc && !e && this._enabled(!0, !1), this
                };
                var V = c("core.FWDSimpleTimeline", function(e) {
                    d.call(this, 0, e), this.autoRemoveChildren = this.smoothChildTiming = !0
                });
                (s = V.prototype = new d).constructor = V, s.kill()._gc = !1, s._first = s._last = s._recent = null, s._sortChildren = !1, s.add = s.insert = function(e, t, s, o) {
                    var i, l;
                    if (e._startTime = Number(t || 0) + e._delay, e._paused && this !== e._timeline && (e._pauseTime = e._startTime + (this.rawTime() - e._startTime) / e._timeScale), e.timeline && e.timeline._remove(e, !0), e.timeline = e._timeline = this, e._gc && e._enabled(!0, !0), i = this._last, this._sortChildren)
                        for (l = e._startTime; i && i._startTime > l;) i = i._prev;
                    return i ? (e._next = i._next, i._next = e) : (e._next = this._first, this._first = e), e._next ? e._next._prev = e : this._last = e, e._prev = i, this._recent = e, this._timeline && this._uncache(!0), this
                }, s._remove = function(e, t) {
                    return e.timeline === this && (t || e._enabled(!1, !0), e._prev ? e._prev._next = e._next : this._first === e && (this._first = e._next), e._next ? e._next._prev = e._prev : this._last === e && (this._last = e._prev), e._next = e._prev = e.timeline = null, e === this._recent && (this._recent = this._last), this._timeline && this._uncache(!0)), this
                }, s.render = function(e, t, s) {
                    var o, i = this._first;
                    for (this._totalTime = this._time = this._rawPrevTime = e; i;) o = i._next, (i._active || e >= i._startTime && !i._paused) && (i._reversed ? i.render((i._dirty ? i.totalDuration() : i._totalDuration) - (e - i._startTime) * i._timeScale, t, s) : i.render((e - i._startTime) * i._timeScale, t, s)), i = o
                }, s.rawTime = function() {
                    return g || b.wake(), this._totalTime
                };
                var E = c("FWDTweenLite", function(e, t, s) {
                        if (d.call(this, t, s), this.render = E.prototype.render, null == e) throw "Cannot tween a null target.";
                        this.target = e = "string" != typeof e ? e : E.selector(e) || e;
                        var o, i, l, n = e.jquery || e.length && e !== _ && e[0] && (e[0] === _ || e[0].nodeType && e[0].style && !e.nodeType),
                            a = this.vars.overwrite;
                        if (this._overwrite = a = null == a ? z[E.defaultOverwrite] : "number" == typeof a ? a >> 0 : z[a], (n || e instanceof Array || e.push && P(e)) && "number" != typeof e[0])
                            for (this._targets = l = r(e), this._propLookup = [], this._siblings = [], o = 0; o < l.length; o++)(i = l[o]) ? "string" != typeof i ? i.length && i !== _ && i[0] && (i[0] === _ || i[0].nodeType && i[0].style && !i.nodeType) ? (l.splice(o--, 1), this._targets = l = l.concat(r(i))) : (this._siblings[o] = J(i, this, !1), 1 === a && 1 < this._siblings[o].length && $(i, this, null, 1, this._siblings[o])) : "string" == typeof(i = l[o--] = E.selector(i)) && l.splice(o + 1, 1) : l.splice(o--, 1);
                        else this._propLookup = {}, this._siblings = J(e, this, !1), 1 === a && 1 < this._siblings.length && $(e, this, null, 1, this._siblings);
                        (this.vars.immediateRender || 0 === t && 0 === this._delay && !1 !== this.vars.immediateRender) && (this._time = -v, this.render(Math.min(0, -this._delay)))
                    }, !0),
                    O = function(e) {
                        return e && e.length && e !== _ && e[0] && (e[0] === _ || e[0].nodeType && e[0].style && !e.nodeType)
                    };
                (s = E.prototype = new d).constructor = E, s.kill()._gc = !1, s.ratio = 0, s._firstPT = s._targets = s._overwrittenProps = s._startAt = null, s._notifyPluginsOfEnabled = s._lazy = !1, E.version = "1.19.0", E.defaultEase = s._ease = new B(null, null, 1, 1), E.defaultOverwrite = "auto", E.ticker = b, E.autoSleep = 120, E.lagSmoothing = function(e, t) {
                    b.lagSmoothing(e, t)
                }, E.selector = _.$ || _.jQuery || function(e) {
                    var t = _.$ || _.jQuery;
                    return t ? (E.selector = t)(e) : "undefined" == typeof document ? e : document.querySelectorAll ? document.querySelectorAll(e) : document.getElementById("#" === e.charAt(0) ? e.substr(1) : e)
                };
                var I = [],
                    x = {},
                    A = /(?:(-|-=|\+=)?\d*\.?\d*(?:e[\-+]?\d+)?)[0-9]/gi,
                    k = function(e) {
                        for (var t, s = this._firstPT; s;) t = s.blob ? e ? this.join("") : this.start : s.c * e + s.s, s.m ? t = s.m(t, this._target || s.t) : t < 1e-6 && -1e-6 < t && (t = 0), s.f ? s.fp ? s.t[s.p](s.fp, t) : s.t[s.p](t) : s.t[s.p] = t, s = s._next
                    },
                    M = function(e, t, s, o) {
                        var i, l, n, a, r, d, u, h = [e, t],
                            c = 0,
                            _ = "",
                            f = 0;
                        for (h.start = e, s && (s(h), e = h[0], t = h[1]), h.length = 0, i = e.match(A) || [], l = t.match(A) || [], o && (o._next = null, o.blob = 1, h._firstPT = h._applyPT = o), r = l.length, a = 0; a < r; a++) u = l[a], _ += (d = t.substr(c, t.indexOf(u, c) - c)) || !a ? d : ",", c += d.length, f ? f = (f + 1) % 5 : "rgba(" === d.substr(-5) && (f = 1), u === i[a] || i.length <= a ? _ += u : (_ && (h.push(_), _ = ""), n = parseFloat(i[a]), h.push(n), h._firstPT = {
                            _next: h._firstPT,
                            t: h,
                            p: h.length - 1,
                            s: n,
                            c: ("=" === u.charAt(1) ? parseInt(u.charAt(0) + "1", 10) * parseFloat(u.substr(2)) : parseFloat(u) - n) || 0,
                            f: 0,
                            m: f && f < 4 ? Math.round : 0
                        }), c += u.length;
                        return (_ += t.substr(c)) && h.push(_), h.setRatio = k, h
                    },
                    L = function(e, t, s, o, i, l, n, a, r) {
                        "function" == typeof o && (o = o(r || 0, e));
                        var d, u = "get" === s ? e[t] : s,
                            h = typeof e[t],
                            c = "string" == typeof o && "=" === o.charAt(1),
                            _ = {
                                t: e,
                                p: t,
                                s: u,
                                f: "function" == h,
                                pg: 0,
                                n: i || t,
                                m: l ? "function" == typeof l ? l : Math.round : 0,
                                pr: 0,
                                c: c ? parseInt(o.charAt(0) + "1", 10) * parseFloat(o.substr(2)) : parseFloat(o) - u || 0
                            };
                        if ("number" != h && ("function" == h && "get" === s && (d = t.indexOf("set") || "function" != typeof e["get" + t.substr(3)] ? t : "get" + t.substr(3), _.s = u = n ? e[d](n) : e[d]()), "string" == typeof u && (n || isNaN(u)) ? (_.fp = n, _ = {
                                t: M(u, o, a || E.defaultStringFilter, _),
                                p: "setRatio",
                                s: 0,
                                c: 1,
                                f: 2,
                                pg: 0,
                                n: i || t,
                                pr: 0,
                                m: 0
                            }) : c || (_.s = parseFloat(u), _.c = parseFloat(o) - _.s || 0)), _.c) return (_._next = this._firstPT) && (_._next._prev = _), this._firstPT = _
                    },
                    R = E._internals = {
                        isArray: P,
                        isSelector: O,
                        lazyTweens: I,
                        blobDif: M
                    },
                    N = E._plugins = {},
                    j = R.tweenLookup = {},
                    Y = 0,
                    X = R.reservedProps = {
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
                    Q = d._rootFramesTimeline = new V,
                    G = d._rootTimeline = new V,
                    q = 30,
                    K = R.lazyRender = function() {
                        var e, t = I.length;
                        for (x = {}; - 1 < --t;)(e = I[t]) && !1 !== e._lazy && (e.render(e._lazy[0], e._lazy[1], !0), e._lazy = !1);
                        I.length = 0
                    };
                G._startTime = b.time, Q._startTime = b.frame, G._active = Q._active = !0, setTimeout(K, 1), d._updateRoot = E.render = function() {
                    var e, t, s;
                    if (I.length && K(), G.render((b.time - G._startTime) * G._timeScale, !1, !1), Q.render((b.frame - Q._startTime) * Q._timeScale, !1, !1), I.length && K(), b.frame >= q) {
                        for (s in q = b.frame + (parseInt(E.autoSleep, 10) || 120), j) {
                            for (e = (t = j[s].tweens).length; - 1 < --e;) t[e]._gc && t.splice(e, 1);
                            0 === t.length && delete j[s]
                        }
                        if ((!(s = G._first) || s._paused) && E.autoSleep && !Q._first && 1 === b._listeners.tick.length) {
                            for (; s && s._paused;) s = s._next;
                            s || b.sleep()
                        }
                    }
                }, b.addEventListener("tick", d._updateRoot);
                var J = function(e, t, s) {
                        var o, i, l = e._gsTweenID;
                        if (j[l || (e._gsTweenID = l = "t" + Y++)] || (j[l] = {
                                target: e,
                                tweens: []
                            }), t && ((o = j[l].tweens)[i = o.length] = t, s))
                            for (; - 1 < --i;) o[i] === t && o.splice(i, 1);
                        return j[l].tweens
                    },
                    Z = function(e, t, s, o) {
                        var i, l, n = e.vars.onOverwrite;
                        return n && (i = n(e, t, s, o)), (n = E.onOverwrite) && (l = n(e, t, s, o)), !1 !== i && !1 !== l
                    },
                    $ = function(e, t, s, o, i) {
                        var l, n, a, r;
                        if (1 === o || 4 <= o) {
                            for (r = i.length, l = 0; l < r; l++)
                                if ((a = i[l]) !== t) a._gc || a._kill(null, e, t) && (n = !0);
                                else if (5 === o) break;
                            return n
                        }
                        var d, u = t._startTime + v,
                            h = [],
                            c = 0,
                            _ = 0 === t._duration;
                        for (l = i.length; - 1 < --l;)(a = i[l]) === t || a._gc || a._paused || (a._timeline !== t._timeline ? (d = d || ee(t, 0, _), 0 === ee(a, d, _) && (h[c++] = a)) : a._startTime <= u && a._startTime + a.totalDuration() / a._timeScale > u && ((_ || !a._initted) && u - a._startTime <= 2e-10 || (h[c++] = a)));
                        for (l = c; - 1 < --l;)
                            if (a = h[l], 2 === o && a._kill(s, e, t) && (n = !0), 2 !== o || !a._firstPT && a._initted) {
                                if (2 !== o && !Z(a, t)) continue;
                                a._enabled(!1, !1) && (n = !0)
                            } return n
                    },
                    ee = function(e, t, s) {
                        for (var o = e._timeline, i = o._timeScale, l = e._startTime; o._timeline;) {
                            if (l += o._startTime, i *= o._timeScale, o._paused) return -100;
                            o = o._timeline
                        }
                        return t < (l /= i) ? l - t : s && l === t || !e._initted && l - t < 2 * v ? v : (l += e.totalDuration() / e._timeScale / i) > t + v ? 0 : l - t - v
                    };
                s._init = function() {
                    var e, t, s, o, i, l, n = this.vars,
                        a = this._overwrittenProps,
                        r = this._duration,
                        d = !!n.immediateRender,
                        u = n.ease;
                    if (n.startAt) {
                        for (o in this._startAt && (this._startAt.render(-1, !0), this._startAt.kill()), i = {}, n.startAt) i[o] = n.startAt[o];
                        if (i.overwrite = !1, i.immediateRender = !0, i.lazy = d && !1 !== n.lazy, i.startAt = i.delay = null, this._startAt = E.to(this.target, 0, i), d)
                            if (0 < this._time) this._startAt = null;
                            else if (0 !== r) return
                    } else if (n.runBackwards && 0 !== r)
                        if (this._startAt) this._startAt.render(-1, !0), this._startAt.kill(), this._startAt = null;
                        else {
                            for (o in 0 !== this._time && (d = !1), s = {}, n) X[o] && "autoCSS" !== o || (s[o] = n[o]);
                            if (s.overwrite = 0, s.data = "isFromStart", s.lazy = d && !1 !== n.lazy, s.immediateRender = d, this._startAt = E.to(this.target, 0, s), d) {
                                if (0 === this._time) return
                            } else this._startAt._init(), this._startAt._enabled(!1), this.vars.immediateRender && (this._startAt = null)
                        } if (this._ease = u = u ? u instanceof B ? u : "function" == typeof u ? new B(u, n.easeParams) : D[u] || E.defaultEase : E.defaultEase, n.easeParams instanceof Array && u.config && (this._ease = u.config.apply(u, n.easeParams)), this._easeType = this._ease._type, this._easePower = this._ease._power, this._firstPT = null, this._targets)
                        for (l = this._targets.length, e = 0; e < l; e++) this._initProps(this._targets[e], this._propLookup[e] = {}, this._siblings[e], a ? a[e] : null, e) && (t = !0);
                    else t = this._initProps(this.target, this._propLookup, this._siblings, a, 0);
                    if (t && E._onPluginEvent("_onInitAllProps", this), a && (this._firstPT || "function" != typeof this.target && this._enabled(!1, !1)), n.runBackwards)
                        for (s = this._firstPT; s;) s.s += s.c, s.c = -s.c, s = s._next;
                    this._onUpdate = n.onUpdate, this._initted = !0
                }, s._initProps = function(e, t, s, o, i) {
                    var l, n, a, r, d, u;
                    if (null == e) return !1;
                    for (l in x[e._gsTweenID] && K(), this.vars.css || e.style && e !== _ && e.nodeType && N.css && !1 !== this.vars.autoCSS && function(e, t) {
                            var s, o = {};
                            for (s in e) X[s] || s in t && "transform" !== s && "x" !== s && "y" !== s && "width" !== s && "height" !== s && "className" !== s && "border" !== s || !(!N[s] || N[s] && N[s]._autoCSS) || (o[s] = e[s], delete e[s]);
                            e.css = o
                        }(this.vars, e), this.vars)
                        if (u = this.vars[l], X[l]) u && (u instanceof Array || u.push && P(u)) && -1 !== u.join("").indexOf("{self}") && (this.vars[l] = u = this._swapSelfInParams(u, this));
                        else if (N[l] && (r = new N[l])._onInitTween(e, this.vars[l], this, i)) {
                        for (this._firstPT = d = {
                                _next: this._firstPT,
                                t: r,
                                p: "setRatio",
                                s: 0,
                                c: 1,
                                f: 1,
                                n: l,
                                pg: 1,
                                pr: r._priority,
                                m: 0
                            }, n = r._overwriteProps.length; - 1 < --n;) t[r._overwriteProps[n]] = this._firstPT;
                        (r._priority || r._onInitAllProps) && (a = !0), (r._onDisable || r._onEnable) && (this._notifyPluginsOfEnabled = !0), d._next && (d._next._prev = d)
                    } else t[l] = L.call(this, e, l, "get", u, l, 0, null, this.vars.stringFilter, i);
                    return o && this._kill(o, e) ? this._initProps(e, t, s, o, i) : 1 < this._overwrite && this._firstPT && 1 < s.length && $(e, this, t, this._overwrite, s) ? (this._kill(t, e), this._initProps(e, t, s, o, i)) : (this._firstPT && (!1 !== this.vars.lazy && this._duration || this.vars.lazy && !this._duration) && (x[e._gsTweenID] = !0), a)
                }, s.render = function(e, t, s) {
                    var o, i, l, n, a = this._time,
                        r = this._duration,
                        d = this._rawPrevTime;
                    if (r - 1e-7 <= e) this._totalTime = this._time = r, this.ratio = this._ease._calcEnd ? this._ease.getRatio(1) : 1, this._reversed || (o = !0, i = "onComplete", s = s || this._timeline.autoRemoveChildren), 0 === r && (!this._initted && this.vars.lazy && !s || (this._startTime === this._timeline._duration && (e = 0), (d < 0 || e <= 0 && -1e-7 <= e || d === v && "isPause" !== this.data) && d !== e && (s = !0, v < d && (i = "onReverseComplete")), this._rawPrevTime = n = !t || e || d === e ? e : v));
                    else if (e < 1e-7) this._totalTime = this._time = 0, this.ratio = this._ease._calcEnd ? this._ease.getRatio(0) : 0, (0 !== a || 0 === r && 0 < d) && (i = "onReverseComplete", o = this._reversed), e < 0 && (this._active = !1, 0 === r && (!this._initted && this.vars.lazy && !s || (0 <= d && (d !== v || "isPause" !== this.data) && (s = !0), this._rawPrevTime = n = !t || e || d === e ? e : v))), this._initted || (s = !0);
                    else if (this._totalTime = this._time = e, this._easeType) {
                        var u = e / r,
                            h = this._easeType,
                            c = this._easePower;
                        (1 === h || 3 === h && .5 <= u) && (u = 1 - u), 3 === h && (u *= 2), 1 === c ? u *= u : 2 === c ? u *= u * u : 3 === c ? u *= u * u * u : 4 === c && (u *= u * u * u * u), this.ratio = 1 === h ? 1 - u : 2 === h ? u : e / r < .5 ? u / 2 : 1 - u / 2
                    } else this.ratio = this._ease.getRatio(e / r);
                    if (this._time !== a || s) {
                        if (!this._initted) {
                            if (this._init(), !this._initted || this._gc) return;
                            if (!s && this._firstPT && (!1 !== this.vars.lazy && this._duration || this.vars.lazy && !this._duration)) return this._time = this._totalTime = a, this._rawPrevTime = d, I.push(this), void(this._lazy = [e, t]);
                            this._time && !o ? this.ratio = this._ease.getRatio(this._time / r) : o && this._ease._calcEnd && (this.ratio = this._ease.getRatio(0 === this._time ? 0 : 1))
                        }
                        for (!1 !== this._lazy && (this._lazy = !1), this._active || !this._paused && this._time !== a && 0 <= e && (this._active = !0), 0 === a && (this._startAt && (0 <= e ? this._startAt.render(e, t, s) : i = i || "_dummyGS"), this.vars.onStart && (0 === this._time && 0 !== r || t || this._callback("onStart"))), l = this._firstPT; l;) l.f ? l.t[l.p](l.c * this.ratio + l.s) : l.t[l.p] = l.c * this.ratio + l.s, l = l._next;
                        this._onUpdate && (e < 0 && this._startAt && -1e-4 !== e && this._startAt.render(e, t, s), t || (this._time !== a || o || s) && this._callback("onUpdate")), i && (this._gc && !s || (e < 0 && this._startAt && !this._onUpdate && -1e-4 !== e && this._startAt.render(e, t, s), o && (this._timeline.autoRemoveChildren && this._enabled(!1, !1), this._active = !1), !t && this.vars[i] && this._callback(i), 0 === r && this._rawPrevTime === v && n !== v && (this._rawPrevTime = 0)))
                    }
                }, s._kill = function(e, t, s) {
                    if ("all" === e && (e = null), null == e && (null == t || t === this.target)) return this._lazy = !1, this._enabled(!1, !1);
                    t = "string" != typeof t ? t || this._targets || this.target : E.selector(t) || t;
                    var o, i, l, n, a, r, d, u, h, c = s && this._time && s._startTime === this._startTime && this._timeline === s._timeline;
                    if ((P(t) || O(t)) && "number" != typeof t[0])
                        for (o = t.length; - 1 < --o;) this._kill(e, t[o], s) && (r = !0);
                    else {
                        if (this._targets) {
                            for (o = this._targets.length; - 1 < --o;)
                                if (t === this._targets[o]) {
                                    a = this._propLookup[o] || {}, this._overwrittenProps = this._overwrittenProps || [], i = this._overwrittenProps[o] = e ? this._overwrittenProps[o] || {} : "all";
                                    break
                                }
                        } else {
                            if (t !== this.target) return !1;
                            a = this._propLookup, i = this._overwrittenProps = e ? this._overwrittenProps || {} : "all"
                        }
                        if (a) {
                            if (d = e || a, u = e !== i && "all" !== i && e !== a && ("object" != typeof e || !e._tempKill), s && (E.onOverwrite || this.vars.onOverwrite)) {
                                for (l in d) a[l] && (h = h || []).push(l);
                                if ((h || !e) && !Z(this, s, t, h)) return !1
                            }
                            for (l in d)(n = a[l]) && (c && (n.f ? n.t[n.p](n.s) : n.t[n.p] = n.s, r = !0), n.pg && n.t._kill(d) && (r = !0), n.pg && 0 !== n.t._overwriteProps.length || (n._prev ? n._prev._next = n._next : n === this._firstPT && (this._firstPT = n._next), n._next && (n._next._prev = n._prev), n._next = n._prev = null), delete a[l]), u && (i[l] = 1);
                            !this._firstPT && this._initted && this._enabled(!1, !1)
                        }
                    }
                    return r
                }, s.invalidate = function() {
                    return this._notifyPluginsOfEnabled && E._onPluginEvent("_onDisable", this), this._firstPT = this._overwrittenProps = this._startAt = this._onUpdate = null, this._notifyPluginsOfEnabled = this._active = this._lazy = !1, this._propLookup = this._targets ? {} : [], d.prototype.invalidate.call(this), this.vars.immediateRender && (this._time = -v, this.render(Math.min(0, -this._delay))), this
                }, s._enabled = function(e, t) {
                    if (g || b.wake(), e && this._gc) {
                        var s, o = this._targets;
                        if (o)
                            for (s = o.length; - 1 < --s;) this._siblings[s] = J(o[s], this, !0);
                        else this._siblings = J(this.target, this, !0)
                    }
                    return d.prototype._enabled.call(this, e, t), !(!this._notifyPluginsOfEnabled || !this._firstPT) && E._onPluginEvent(e ? "_onEnable" : "_onDisable", this)
                }, E.to = function(e, t, s) {
                    return new E(e, t, s)
                }, E.from = function(e, t, s) {
                    return s.runBackwards = !0, s.immediateRender = 0 != s.immediateRender, new E(e, t, s)
                }, E.fromTo = function(e, t, s, o) {
                    return o.startAt = s, o.immediateRender = 0 != o.immediateRender && 0 != s.immediateRender, new E(e, t, o)
                }, E.delayedCall = function(e, t, s, o, i) {
                    return new E(t, 0, {
                        delay: e,
                        onComplete: t,
                        onCompleteParams: s,
                        callbackScope: o,
                        onReverseComplete: t,
                        onReverseCompleteParams: s,
                        immediateRender: !1,
                        lazy: !1,
                        useFrames: i,
                        overwrite: 0
                    })
                }, E.set = function(e, t) {
                    return new E(e, 0, t)
                }, E.getTweensOf = function(e, t) {
                    if (null == e) return [];
                    var s, o, i, l;
                    if (e = "string" != typeof e ? e : E.selector(e) || e, (P(e) || O(e)) && "number" != typeof e[0]) {
                        for (s = e.length, o = []; - 1 < --s;) o = o.concat(E.getTweensOf(e[s], t));
                        for (s = o.length; - 1 < --s;)
                            for (l = o[s], i = s; - 1 < --i;) l === o[i] && o.splice(s, 1)
                    } else
                        for (s = (o = J(e).concat()).length; - 1 < --s;)(o[s]._gc || t && !o[s].isActive()) && o.splice(s, 1);
                    return o
                }, E.killTweensOf = E.killDelayedCallsTo = function(e, t, s) {
                    "object" == typeof t && (s = t, t = !1);
                    for (var o = E.getTweensOf(e, t), i = o.length; - 1 < --i;) o[i]._kill(s, e)
                };
                var te = c("plugins.TweenPlugin", function(e, t) {
                    this._overwriteProps = (e || "").split(","), this._propName = this._overwriteProps[0], this._priority = t || 0, this._super = te.prototype
                }, !0);
                if (s = te.prototype, te.version = "1.19.0", te.API = 2, s._firstPT = null, s._addTween = L, s.setRatio = k, s._kill = function(e) {
                        var t, s = this._overwriteProps,
                            o = this._firstPT;
                        if (null != e[this._propName]) this._overwriteProps = [];
                        else
                            for (t = s.length; - 1 < --t;) null != e[s[t]] && s.splice(t, 1);
                        for (; o;) null != e[o.n] && (o._next && (o._next._prev = o._prev), o._prev ? (o._prev._next = o._next, o._prev = null) : this._firstPT === o && (this._firstPT = o._next)), o = o._next;
                        return !1
                    }, s._mod = s._roundProps = function(e) {
                        for (var t, s = this._firstPT; s;)(t = e[this._propName] || null != s.n && e[s.n.split(this._propName + "_").join("")]) && "function" == typeof t && (2 === s.f ? s.t._applyPT.m = t : s.m = t), s = s._next
                    }, E._onPluginEvent = function(e, t) {
                        var s, o, i, l, n, a = t._firstPT;
                        if ("_onInitAllProps" === e) {
                            for (; a;) {
                                for (n = a._next, o = i; o && o.pr > a.pr;) o = o._next;
                                (a._prev = o ? o._prev : l) ? a._prev._next = a: i = a, (a._next = o) ? o._prev = a : l = a, a = n
                            }
                            a = t._firstPT = i
                        }
                        for (; a;) a.pg && "function" == typeof a.t[e] && a.t[e]() && (s = !0), a = a._next;
                        return s
                    }, te.activate = function(e) {
                        for (var t = e.length; - 1 < --t;) e[t].API === te.API && (N[(new e[t])._propName] = e[t]);
                        return !0
                    }, l.plugin = function(e) {
                        if (!(e && e.propName && e.init && e.API)) throw "illegal plugin definition.";
                        var t, s = e.propName,
                            o = e.priority || 0,
                            i = e.overwriteProps,
                            l = {
                                init: "_onInitTween",
                                set: "setRatio",
                                kill: "_kill",
                                round: "_mod",
                                mod: "_mod",
                                initAll: "_onInitAllProps"
                            },
                            n = c("plugins." + s.charAt(0).toUpperCase() + s.substr(1) + "Plugin", function() {
                                te.call(this, s, o), this._overwriteProps = i || []
                            }, !0 === e.fwd_global),
                            a = n.prototype = new te(s);
                        for (t in (a.constructor = n).API = e.API, l) "function" == typeof e[t] && (a[l[t]] = e[t]);
                        return n.version = e.version, te.activate([n]), n
                    }, e = _._fwd_gsQueue) {
                    for (t = 0; t < e.length; t++) e[t]();
                    for (s in w) w[s].func || _.console.log("GSAP encountered missing dependency: " + s)
                }
                g = !1
            }
        }("undefined" != typeof fwd_module && fwd_module.exports && "undefined" != typeof fwd_global ? fwd_global : this || window, "FWDAnimation")
  }
