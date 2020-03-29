(window._gsQueue || (window._gsQueue = [])).push(function() {
    "use strict";
    window._gsDefine("MUSICTweenMax", ["core.Animation", "core.SimpleTimeline", "TweenLite"], function(e, t, n) {
        var r = [].slice,
            i = function(e, t, r) {
                n.call(this, e, t, r);
                this._cycle = 0;
                this._yoyo = this.vars.yoyo === true;
                this._repeat = this.vars.repeat || 0;
                this._repeatDelay = this.vars.repeatDelay || 0;
                this._dirty = true
            },
            s = function(e) {
                return e.jquery || e.length && e[0] && e[0].nodeType && e[0].style
            },
            o = i.prototype = n.to({}, .1, {}),
            u = [];
        i.version = "1.9.7";
        o.constructor = i;
        o.kill()._gc = false;
        i.killTweensOf = i.killDelayedCallsTo = n.killTweensOf;
        i.getTweensOf = n.getTweensOf;
        i.ticker = n.ticker;
        o.invalidate = function() {
            this._yoyo = this.vars.yoyo === true;
            this._repeat = this.vars.repeat || 0;
            this._repeatDelay = this.vars.repeatDelay || 0;
            this._uncache(true);
            return n.prototype.invalidate.call(this)
        };
        o.updateTo = function(e, t) {
            var r = this.ratio,
                i;
            if (t && this.timeline && this._startTime < this._timeline._time) {
                this._startTime = this._timeline._time;
                this._uncache(false);
                if (this._gc) {
                    this._enabled(true, false)
                } else {
                    this._timeline.insert(this, this._startTime - this._delay)
                }
            }
            for (i in e) {
                this.vars[i] = e[i]
            }
            if (this._initted) {
                if (t) {
                    this._initted = false
                } else {
                    if (this._notifyPluginsOfEnabled && this._firstPT) {
                        n._onPluginEvent("_onDisable", this)
                    }
                    if (this._time / this._duration > .998) {
                        var s = this._time;
                        this.render(0, true, false);
                        this._initted = false;
                        this.render(s, true, false)
                    } else if (this._time > 0) {
                        this._initted = false;
                        this._init();
                        var o = 1 / (1 - r),
                            u = this._firstPT,
                            a;
                        while (u) {
                            a = u.s + u.c;
                            u.c *= o;
                            u.s = a - u.c;
                            u = u._next
                        }
                    }
                }
            }
            return this
        };
        o.render = function(e, t, n) {
            var r = !this._dirty ? this._totalDuration : this.totalDuration(),
                i = this._time,
                s = this._totalTime,
                o = this._cycle,
                a, f, l, c, h, p, d;
            if (e >= r) {
                this._totalTime = r;
                this._cycle = this._repeat;
                if (this._yoyo && (this._cycle & 1) !== 0) {
                    this._time = 0;
                    this.ratio = this._ease._calcEnd ? this._ease.getRatio(0) : 0
                } else {
                    this._time = this._duration;
                    this.ratio = this._ease._calcEnd ? this._ease.getRatio(1) : 1
                }
                if (!this._reversed) {
                    a = true;
                    f = "onComplete"
                }
                if (this._duration === 0) {
                    if (e === 0 || this._rawPrevTime < 0)
                        if (this._rawPrevTime !== e) {
                            n = true;
                            if (this._rawPrevTime > 0) {
                                f = "onReverseComplete";
                                if (t) {
                                    e = -1
                                }
                            }
                        } this._rawPrevTime = e
                }
            } else if (e < 1e-7) {
                this._totalTime = this._time = this._cycle = 0;
                this.ratio = this._ease._calcEnd ? this._ease.getRatio(0) : 0;
                if (s !== 0 || this._duration === 0 && this._rawPrevTime > 0) {
                    f = "onReverseComplete";
                    a = this._reversed
                }
                if (e < 0) {
                    this._active = false;
                    if (this._duration === 0) {
                        if (this._rawPrevTime >= 0) {
                            n = true
                        }
                        this._rawPrevTime = e
                    }
                } else if (!this._initted) {
                    n = true
                }
            } else {
                this._totalTime = this._time = e;
                if (this._repeat !== 0) {
                    c = this._duration + this._repeatDelay;
                    this._cycle = this._totalTime / c >> 0;
                    if (this._cycle !== 0)
                        if (this._cycle === this._totalTime / c) {
                            this._cycle--
                        } this._time = this._totalTime - this._cycle * c;
                    if (this._yoyo)
                        if ((this._cycle & 1) !== 0) {
                            this._time = this._duration - this._time
                        } if (this._time > this._duration) {
                        this._time = this._duration
                    } else if (this._time < 0) {
                        this._time = 0
                    }
                }
                if (this._easeType) {
                    h = this._time / this._duration;
                    p = this._easeType;
                    d = this._easePower;
                    if (p === 1 || p === 3 && h >= .5) {
                        h = 1 - h
                    }
                    if (p === 3) {
                        h *= 2
                    }
                    if (d === 1) {
                        h *= h
                    } else if (d === 2) {
                        h *= h * h
                    } else if (d === 3) {
                        h *= h * h * h
                    } else if (d === 4) {
                        h *= h * h * h * h
                    }
                    if (p === 1) {
                        this.ratio = 1 - h
                    } else if (p === 2) {
                        this.ratio = h
                    } else if (this._time / this._duration < .5) {
                        this.ratio = h / 2
                    } else {
                        this.ratio = 1 - h / 2
                    }
                } else {
                    this.ratio = this._ease.getRatio(this._time / this._duration)
                }
            }
            if (i === this._time && !n) {
                if (s !== this._totalTime)
                    if (this._onUpdate)
                        if (!t) {
                            this._onUpdate.apply(this.vars.onUpdateScope || this, this.vars.onUpdateParams || u)
                        } return
            } else if (!this._initted) {
                this._init();
                if (!this._initted) {
                    return
                }
                if (this._time && !a) {
                    this.ratio = this._ease.getRatio(this._time / this._duration)
                } else if (a && this._ease._calcEnd) {
                    this.ratio = this._ease.getRatio(this._time === 0 ? 0 : 1)
                }
            }
            if (!this._active)
                if (!this._paused) {
                    this._active = true
                } if (s === 0) {
                if (this._startAt) {
                    if (e >= 0) {
                        this._startAt.render(e, t, n)
                    } else if (!f) {
                        f = "_dummyGS"
                    }
                }
                if (this.vars.onStart)
                    if (this._totalTime !== 0 || this._duration === 0)
                        if (!t) {
                            this.vars.onStart.apply(this.vars.onStartScope || this, this.vars.onStartParams || u)
                        }
            }
            l = this._firstPT;
            while (l) {
                if (l.f) {
                    l.t[l.p](l.c * this.ratio + l.s)
                } else {
                    var v = l.c * this.ratio + l.s;
                    if (l.p == "x") {
                        l.t.setX(v)
                    } else if (l.p == "y") {
                        l.t.setY(v)
                    } else if (l.p == "z") {
                        l.t.setZ(v)
                    } else if (l.p == "w") {
                        l.t.setWidth(v)
                    } else if (l.p == "h") {
                        l.t.setHeight(v)
                    } else if (l.p == "alpha") {
                        l.t.setAlpha(v)
                    } else if (l.p == "scale") {
                        l.t.setScale(v)
                    } else {
                        l.t[l.p] = v
                    }
                }
                l = l._next
            }
            if (this._onUpdate) {
                if (e < 0)
                    if (this._startAt) {
                        this._startAt.render(e, t, n)
                    } if (!t) {
                    this._onUpdate.apply(this.vars.onUpdateScope || this, this.vars.onUpdateParams || u)
                }
            }
            if (this._cycle !== o)
                if (!t)
                    if (!this._gc)
                        if (this.vars.onRepeat) {
                            this.vars.onRepeat.apply(this.vars.onRepeatScope || this, this.vars.onRepeatParams || u)
                        } if (f)
                if (!this._gc) {
                    if (e < 0 && this._startAt && !this._onUpdate) {
                        this._startAt.render(e, t, n)
                    }
                    if (a) {
                        if (this._timeline.autoRemoveChildren) {
                            this._enabled(false, false)
                        }
                        this._active = false
                    }
                    if (!t && this.vars[f]) {
                        this.vars[f].apply(this.vars[f + "Scope"] || this, this.vars[f + "Params"] || u)
                    }
                }
        };
        i.to = function(e, t, n) {
            return new i(e, t, n)
        };
        i.from = function(e, t, n) {
            n.runBackwards = true;
            n.immediateRender = n.immediateRender != false;
            return new i(e, t, n)
        };
        i.fromTo = function(e, t, n, r) {
            r.startAt = n;
            r.immediateRender = r.immediateRender != false && n.immediateRender != false;
            return new i(e, t, r)
        };
        i.staggerTo = i.allTo = function(e, t, o, a, f, l, c) {
            a = a || 0;
            var h = o.delay || 0,
                p = [],
                d = function() {
                    if (o.onComplete) {
                        o.onComplete.apply(o.onCompleteScope || this, o.onCompleteParams || u)
                    }
                    f.apply(c || this, l || u)
                },
                v, m, g, y;
            if (!(e instanceof Array)) {
                if (typeof e === "string") {
                    e = n.selector(e) || e
                }
                if (s(e)) {
                    e = r.call(e, 0)
                }
            }
            v = e.length;
            for (g = 0; g < v; g++) {
                m = {};
                for (y in o) {
                    m[y] = o[y]
                }
                m.delay = h;
                if (g === v - 1 && f) {
                    m.onComplete = d
                }
                p[g] = new i(e[g], t, m);
                h += a
            }
            return p
        };
        i.staggerFrom = i.allFrom = function(e, t, n, r, s, o, u) {
            n.runBackwards = true;
            n.immediateRender = n.immediateRender != false;
            return i.staggerTo(e, t, n, r, s, o, u)
        };
        i.staggerFromTo = i.allFromTo = function(e, t, n, r, s, o, u, a) {
            r.startAt = n;
            r.immediateRender = r.immediateRender != false && n.immediateRender != false;
            return i.staggerTo(e, t, r, s, o, u, a)
        };
        i.delayedCall = function(e, t, n, r, s) {
            return new i(t, 0, {
                delay: e,
                onComplete: t,
                onCompleteParams: n,
                onCompleteScope: r,
                onReverseComplete: t,
                onReverseCompleteParams: n,
                onReverseCompleteScope: r,
                immediateRender: false,
                useFrames: s,
                overwrite: 0
            })
        };
        i.set = function(e, t) {
            return new i(e, 0, t)
        };
        i.isTweening = function(e) {
            var t = n.getTweensOf(e),
                r = t.length,
                i;
            while (--r > -1) {
                i = t[r];
                if (i._active || i._startTime === i._timeline._time && i._timeline._active) {
                    return true
                }
            }
            return false
        };
        var a = function(e, t) {
                var r = [],
                    i = 0,
                    s = e._first;
                while (s) {
                    if (s instanceof n) {
                        r[i++] = s
                    } else {
                        if (t) {
                            r[i++] = s
                        }
                        r = r.concat(a(s, t));
                        i = r.length
                    }
                    s = s._next
                }
                return r
            },
            f = i.getAllTweens = function(t) {
                return a(e._rootTimeline, t).concat(a(e._rootFramesTimeline, t))
            };
        i.killAll = function(e, n, r, i) {
            if (n == null) {
                n = true
            }
            if (r == null) {
                r = true
            }
            var s = f(i != false),
                o = s.length,
                u = n && r && i,
                a, l, c;
            for (c = 0; c < o; c++) {
                l = s[c];
                if (u || l instanceof t || (a = l.target === l.vars.onComplete) && r || n && !a) {
                    if (e) {
                        l.totalTime(l.totalDuration())
                    } else {
                        l._enabled(false, false)
                    }
                }
            }
        };
        i.killChildTweensOf = function(e, t) {
            if (e == null) {
                return
            }
            var o = n._tweenLookup,
                u, a, f, l, c;
            if (typeof e === "string") {
                e = n.selector(e) || e
            }
            if (s(e)) {
                e = r(e, 0)
            }
            if (e instanceof Array) {
                l = e.length;
                while (--l > -1) {
                    i.killChildTweensOf(e[l], t)
                }
                return
            }
            u = [];
            for (f in o) {
                a = o[f].target.parentNode;
                while (a) {
                    if (a === e) {
                        u = u.concat(o[f].tweens)
                    }
                    a = a.parentNode
                }
            }
            c = u.length;
            for (l = 0; l < c; l++) {
                if (t) {
                    u[l].totalTime(u[l].totalDuration())
                }
                u[l]._enabled(false, false)
            }
        };
        var l = function(e, n, r, i) {
            if (n === undefined) {
                n = true
            }
            if (r === undefined) {
                r = true
            }
            var s = f(i),
                o = n && r && i,
                u = s.length,
                a, l;
            while (--u > -1) {
                l = s[u];
                if (o || l instanceof t || (a = l.target === l.vars.onComplete) && r || n && !a) {
                    l.paused(e)
                }
            }
        };
        i.pauseAll = function(e, t, n) {
            l(true, e, t, n)
        };
        i.resumeAll = function(e, t, n) {
            l(false, e, t, n)
        };
        o.progress = function(e) {
            return !arguments.length ? this._time / this.duration() : this.totalTime(this.duration() * (this._yoyo && (this._cycle & 1) !== 0 ? 1 - e : e) + this._cycle * (this._duration + this._repeatDelay), false)
        };
        o.totalProgress = function(e) {
            return !arguments.length ? this._totalTime / this.totalDuration() : this.totalTime(this.totalDuration() * e, false)
        };
        o.time = function(e, t) {
            if (!arguments.length) {
                return this._time
            }
            if (this._dirty) {
                this.totalDuration()
            }
            if (e > this._duration) {
                e = this._duration
            }
            if (this._yoyo && (this._cycle & 1) !== 0) {
                e = this._duration - e + this._cycle * (this._duration + this._repeatDelay)
            } else if (this._repeat !== 0) {
                e += this._cycle * (this._duration + this._repeatDelay)
            }
            return this.totalTime(e, t)
        };
        o.duration = function(t) {
            if (!arguments.length) {
                return this._duration
            }
            return e.prototype.duration.call(this, t)
        };
        o.totalDuration = function(e) {
            if (!arguments.length) {
                if (this._dirty) {
                    this._totalDuration = this._repeat === -1 ? 999999999999 : this._duration * (this._repeat + 1) + this._repeatDelay * this._repeat;
                    this._dirty = false
                }
                return this._totalDuration
            }
            return this._repeat === -1 ? this : this.duration((e - this._repeat * this._repeatDelay) / (this._repeat + 1))
        };
        o.repeat = function(e) {
            if (!arguments.length) {
                return this._repeat
            }
            this._repeat = e;
            return this._uncache(true)
        };
        o.repeatDelay = function(e) {
            if (!arguments.length) {
                return this._repeatDelay
            }
            this._repeatDelay = e;
            return this._uncache(true)
        };
        o.yoyo = function(e) {
            if (!arguments.length) {
                return this._yoyo
            }
            this._yoyo = e;
            return this
        };
        return i
    }, true);
    window._gsDefine("TimelineLite", ["core.Animation", "core.SimpleTimeline", "TweenLite"], function(e, t, n) {
        var r = function(e) {
                t.call(this, e);
                this._labels = {};
                this.autoRemoveChildren = this.vars.autoRemoveChildren === true;
                this.smoothChildTiming = this.vars.smoothChildTiming === true;
                this._sortChildren = true;
                this._onUpdate = this.vars.onUpdate;
                var n = this.vars,
                    r = i.length,
                    s, o;
                while (--r > -1) {
                    o = n[i[r]];
                    if (o) {
                        s = o.length;
                        while (--s > -1) {
                            if (o[s] === "{self}") {
                                o = n[i[r]] = o.concat();
                                o[s] = this
                            }
                        }
                    }
                }
                if (n.tweens instanceof Array) {
                    this.add(n.tweens, 0, n.align, n.stagger)
                }
            },
            i = ["onStartParams", "onUpdateParams", "onCompleteParams", "onReverseCompleteParams", "onRepeatParams"],
            s = [],
            o = function(e) {
                var t = {},
                    n;
                for (n in e) {
                    t[n] = e[n]
                }
                return t
            },
            u = s.slice,
            a = r.prototype = new t;
        r.version = "1.9.7";
        a.constructor = r;
        a.kill()._gc = false;
        a.to = function(e, t, r, i) {
            return t ? this.add(new n(e, t, r), i) : this.set(e, r, i)
        };
        a.from = function(e, t, r, i) {
            return this.add(n.from(e, t, r), i)
        };
        a.fromTo = function(e, t, r, i, s) {
            return t ? this.add(n.fromTo(e, t, r, i), s) : this.set(e, i, s)
        };
        a.staggerTo = function(e, t, i, s, a, f, l, c) {
            var h = new r({
                    onComplete: f,
                    onCompleteParams: l,
                    onCompleteScope: c
                }),
                p;
            if (typeof e === "string") {
                e = n.selector(e) || e
            }
            if (!(e instanceof Array) && e.length && e[0] && e[0].nodeType && e[0].style) {
                e = u.call(e, 0)
            }
            s = s || 0;
            for (p = 0; p < e.length; p++) {
                if (i.startAt) {
                    i.startAt = o(i.startAt)
                }
                h.to(e[p], t, o(i), p * s)
            }
            return this.add(h, a)
        };
        a.staggerFrom = function(e, t, n, r, i, s, o, u) {
            n.immediateRender = n.immediateRender != false;
            n.runBackwards = true;
            return this.staggerTo(e, t, n, r, i, s, o, u)
        };
        a.staggerFromTo = function(e, t, n, r, i, s, o, u, a) {
            r.startAt = n;
            r.immediateRender = r.immediateRender != false && n.immediateRender != false;
            return this.staggerTo(e, t, r, i, s, o, u, a)
        };
        a.call = function(e, t, r, i) {
            return this.add(n.delayedCall(0, e, t, r), i)
        };
        a.set = function(e, t, r) {
            r = this._parseTimeOrLabel(r, 0, true);
            if (t.immediateRender == null) {
                t.immediateRender = r === this._time && !this._paused
            }
            return this.add(new n(e, 0, t), r)
        };
        r.exportRoot = function(e, t) {
            e = e || {};
            if (e.smoothChildTiming == null) {
                e.smoothChildTiming = true
            }
            var i = new r(e),
                s = i._timeline,
                o, u;
            if (t == null) {
                t = true
            }
            s._remove(i, true);
            i._startTime = 0;
            i._rawPrevTime = i._time = i._totalTime = s._time;
            o = s._first;
            while (o) {
                u = o._next;
                if (!t || !(o instanceof n && o.target === o.vars.onComplete)) {
                    i.add(o, o._startTime - o._delay)
                }
                o = u
            }
            s.add(i, 0);
            return i
        };
        a.add = function(i, s, o, u) {
            var a, f, l, c, h;
            if (typeof s !== "number") {
                s = this._parseTimeOrLabel(s, 0, true, i)
            }
            if (!(i instanceof e)) {
                if (i instanceof Array) {
                    o = o || "normal";
                    u = u || 0;
                    a = s;
                    f = i.length;
                    for (l = 0; l < f; l++) {
                        if ((c = i[l]) instanceof Array) {
                            c = new r({
                                tweens: c
                            })
                        }
                        this.add(c, a);
                        if (typeof c !== "string" && typeof c !== "function") {
                            if (o === "sequence") {
                                a = c._startTime + c.totalDuration() / c._timeScale
                            } else if (o === "start") {
                                c._startTime -= c.delay()
                            }
                        }
                        a += u
                    }
                    return this._uncache(true)
                } else if (typeof i === "string") {
                    return this.addLabel(i, s)
                } else if (typeof i === "function") {
                    i = n.delayedCall(0, i)
                } else {
                    throw "Cannot add " + i + " into the timeline; it is neither a tween, timeline, function, nor a string."
                }
            }
            t.prototype.add.call(this, i, s);
            if (this._gc)
                if (!this._paused)
                    if (this._time === this._duration)
                        if (this._time < this.duration()) {
                            h = this;
                            while (h._gc && h._timeline) {
                                if (h._timeline.smoothChildTiming) {
                                    h.totalTime(h._totalTime, true)
                                } else {
                                    h._enabled(true, false)
                                }
                                h = h._timeline
                            }
                        } return this
        };
        a.remove = function(t) {
            if (t instanceof e) {
                return this._remove(t, false)
            } else if (t instanceof Array) {
                var n = t.length;
                while (--n > -1) {
                    this.remove(t[n])
                }
                return this
            } else if (typeof t === "string") {
                return this.removeLabel(t)
            }
            return this.kill(null, t)
        };
        a.append = function(e, t) {
            return this.add(e, this._parseTimeOrLabel(null, t, true, e))
        };
        a.insert = a.insertMultiple = function(e, t, n, r) {
            return this.add(e, t || 0, n, r)
        };
        a.appendMultiple = function(e, t, n, r) {
            return this.add(e, this._parseTimeOrLabel(null, t, true, e), n, r)
        };
        a.addLabel = function(e, t) {
            this._labels[e] = this._parseTimeOrLabel(t);
            return this
        };
        a.removeLabel = function(e) {
            delete this._labels[e];
            return this
        };
        a.getLabelTime = function(e) {
            return this._labels[e] != null ? this._labels[e] : -1
        };
        a._parseTimeOrLabel = function(t, n, r, i) {
            var s;
            if (i instanceof e && i.timeline === this) {
                this.remove(i)
            } else if (i instanceof Array) {
                s = i.length;
                while (--s > -1) {
                    if (i[s] instanceof e && i[s].timeline === this) {
                        this.remove(i[s])
                    }
                }
            }
            if (typeof n === "string") {
                return this._parseTimeOrLabel(n, r && typeof t === "number" && this._labels[n] == null ? t - this.duration() : 0, r)
            }
            n = n || 0;
            if (typeof t === "string" && (isNaN(t) || this._labels[t] != null)) {
                s = t.indexOf("=");
                if (s === -1) {
                    if (this._labels[t] == null) {
                        return r ? this._labels[t] = this.duration() + n : n
                    }
                    return this._labels[t] + n
                }
                n = parseInt(t.charAt(s - 1) + "1", 10) * Number(t.substr(s + 1));
                t = s > 1 ? this._parseTimeOrLabel(t.substr(0, s - 1), 0, r) : this.duration()
            } else if (t == null) {
                t = this.duration()
            }
            return Number(t) + n
        };
        a.seek = function(e, t) {
            return this.totalTime(typeof e === "number" ? e : this._parseTimeOrLabel(e), t !== false)
        };
        a.stop = function() {
            return this.paused(true)
        };
        a.gotoAndPlay = function(e, t) {
            return this.play(e, t)
        };
        a.gotoAndStop = function(e, t) {
            return this.pause(e, t)
        };
        a.render = function(e, t, n) {
            if (this._gc) {
                this._enabled(true, false)
            }
            this._active = !this._paused;
            var r = !this._dirty ? this._totalDuration : this.totalDuration(),
                i = this._time,
                o = this._startTime,
                u = this._timeScale,
                a = this._paused,
                f, l, c, h, p;
            if (e >= r) {
                this._totalTime = this._time = r;
                if (!this._reversed)
                    if (!this._hasPausedChild()) {
                        l = true;
                        h = "onComplete";
                        if (this._duration === 0)
                            if (e === 0 || this._rawPrevTime < 0)
                                if (this._rawPrevTime !== e && this._first) {
                                    p = true;
                                    if (this._rawPrevTime > 0) {
                                        h = "onReverseComplete"
                                    }
                                }
                    } this._rawPrevTime = e;
                e = r + 1e-6
            } else if (e < 1e-7) {
                this._totalTime = this._time = 0;
                if (i !== 0 || this._duration === 0 && this._rawPrevTime > 0) {
                    h = "onReverseComplete";
                    l = this._reversed
                }
                if (e < 0) {
                    this._active = false;
                    if (this._duration === 0)
                        if (this._rawPrevTime >= 0 && this._first) {
                            p = true
                        }
                } else if (!this._initted) {
                    p = true
                }
                this._rawPrevTime = e;
                e = 0
            } else {
                this._totalTime = this._time = this._rawPrevTime = e
            }
            if ((this._time === i || !this._first) && !n && !p) {
                return
            } else if (!this._initted) {
                this._initted = true
            }
            if (i === 0)
                if (this.vars.onStart)
                    if (this._time !== 0)
                        if (!t) {
                            this.vars.onStart.apply(this.vars.onStartScope || this, this.vars.onStartParams || s)
                        } if (this._time >= i) {
                f = this._first;
                while (f) {
                    c = f._next;
                    if (this._paused && !a) {
                        break
                    } else if (f._active || f._startTime <= this._time && !f._paused && !f._gc) {
                        if (!f._reversed) {
                            f.render((e - f._startTime) * f._timeScale, t, n)
                        } else {
                            f.render((!f._dirty ? f._totalDuration : f.totalDuration()) - (e - f._startTime) * f._timeScale, t, n)
                        }
                    }
                    f = c
                }
            } else {
                f = this._last;
                while (f) {
                    c = f._prev;
                    if (this._paused && !a) {
                        break
                    } else if (f._active || f._startTime <= i && !f._paused && !f._gc) {
                        if (!f._reversed) {
                            f.render((e - f._startTime) * f._timeScale, t, n)
                        } else {
                            f.render((!f._dirty ? f._totalDuration : f.totalDuration()) - (e - f._startTime) * f._timeScale, t, n)
                        }
                    }
                    f = c
                }
            }
            if (this._onUpdate)
                if (!t) {
                    this._onUpdate.apply(this.vars.onUpdateScope || this, this.vars.onUpdateParams || s)
                } if (h)
                if (!this._gc)
                    if (o === this._startTime || u !== this._timeScale)
                        if (this._time === 0 || r >= this.totalDuration()) {
                            if (l) {
                                if (this._timeline.autoRemoveChildren) {
                                    this._enabled(false, false)
                                }
                                this._active = false
                            }
                            if (!t && this.vars[h]) {
                                this.vars[h].apply(this.vars[h + "Scope"] || this, this.vars[h + "Params"] || s)
                            }
                        }
        };
        a._hasPausedChild = function() {
            var e = this._first;
            while (e) {
                if (e._paused || e instanceof r && e._hasPausedChild()) {
                    return true
                }
                e = e._next
            }
            return false
        };
        a.getChildren = function(e, t, r, i) {
            i = i || -9999999999;
            var s = [],
                o = this._first,
                u = 0;
            while (o) {
                if (o._startTime < i) {} else if (o instanceof n) {
                    if (t !== false) {
                        s[u++] = o
                    }
                } else {
                    if (r !== false) {
                        s[u++] = o
                    }
                    if (e !== false) {
                        s = s.concat(o.getChildren(true, t, r));
                        u = s.length
                    }
                }
                o = o._next
            }
            return s
        };
        a.getTweensOf = function(e, t) {
            var r = n.getTweensOf(e),
                i = r.length,
                s = [],
                o = 0;
            while (--i > -1) {
                if (r[i].timeline === this || t && this._contains(r[i])) {
                    s[o++] = r[i]
                }
            }
            return s
        };
        a._contains = function(e) {
            var t = e.timeline;
            while (t) {
                if (t === this) {
                    return true
                }
                t = t.timeline
            }
            return false
        };
        a.shiftChildren = function(e, t, n) {
            n = n || 0;
            var r = this._first,
                i = this._labels,
                s;
            while (r) {
                if (r._startTime >= n) {
                    r._startTime += e
                }
                r = r._next
            }
            if (t) {
                for (s in i) {
                    if (i[s] >= n) {
                        i[s] += e
                    }
                }
            }
            return this._uncache(true)
        };
        a._kill = function(e, t) {
            if (!e && !t) {
                return this._enabled(false, false)
            }
            var n = !t ? this.getChildren(true, true, false) : this.getTweensOf(t),
                r = n.length,
                i = false;
            while (--r > -1) {
                if (n[r]._kill(e, t)) {
                    i = true
                }
            }
            return i
        };
        a.clear = function(e) {
            var t = this.getChildren(false, true, true),
                n = t.length;
            this._time = this._totalTime = 0;
            while (--n > -1) {
                t[n]._enabled(false, false)
            }
            if (e !== false) {
                this._labels = {}
            }
            return this._uncache(true)
        };
        a.invalidate = function() {
            var e = this._first;
            while (e) {
                e.invalidate();
                e = e._next
            }
            return this
        };
        a._enabled = function(e, n) {
            if (e === this._gc) {
                var r = this._first;
                while (r) {
                    r._enabled(e, true);
                    r = r._next
                }
            }
            return t.prototype._enabled.call(this, e, n)
        };
        a.progress = function(e) {
            return !arguments.length ? this._time / this.duration() : this.totalTime(this.duration() * e, false)
        };
        a.duration = function(e) {
            if (!arguments.length) {
                if (this._dirty) {
                    this.totalDuration()
                }
                return this._duration
            }
            if (this.duration() !== 0 && e !== 0) {
                this.timeScale(this._duration / e)
            }
            return this
        };
        a.totalDuration = function(e) {
            if (!arguments.length) {
                if (this._dirty) {
                    var t = 0,
                        n = this._last,
                        r = 999999999999,
                        i, s;
                    while (n) {
                        i = n._prev;
                        if (n._dirty) {
                            n.totalDuration()
                        }
                        if (n._startTime > r && this._sortChildren && !n._paused) {
                            this.add(n, n._startTime - n._delay)
                        } else {
                            r = n._startTime
                        }
                        if (n._startTime < 0 && !n._paused) {
                            t -= n._startTime;
                            if (this._timeline.smoothChildTiming) {
                                this._startTime += n._startTime / this._timeScale
                            }
                            this.shiftChildren(-n._startTime, false, -9999999999);
                            r = 0
                        }
                        s = n._startTime + n._totalDuration / n._timeScale;
                        if (s > t) {
                            t = s
                        }
                        n = i
                    }
                    this._duration = this._totalDuration = t;
                    this._dirty = false
                }
                return this._totalDuration
            }
            if (this.totalDuration() !== 0)
                if (e !== 0) {
                    this.timeScale(this._totalDuration / e)
                } return this
        };
        a.usesFrames = function() {
            var t = this._timeline;
            while (t._timeline) {
                t = t._timeline
            }
            return t === e._rootFramesTimeline
        };
        a.rawTime = function() {
            return this._paused || this._totalTime !== 0 && this._totalTime !== this._totalDuration ? this._totalTime : (this._timeline.rawTime() - this._startTime) * this._timeScale
        };
        return r
    }, true);
    window._gsDefine("TimelineMax", ["TimelineLite", "TweenLite", "easing.Ease"], function(e, t, n) {
        var r = function(t) {
                e.call(this, t);
                this._repeat = this.vars.repeat || 0;
                this._repeatDelay = this.vars.repeatDelay || 0;
                this._cycle = 0;
                this._yoyo = this.vars.yoyo === true;
                this._dirty = true
            },
            i = [],
            s = new n(null, null, 1, 0),
            o = function(e) {
                while (e) {
                    if (e._paused) {
                        return true
                    }
                    e = e._timeline
                }
                return false
            },
            u = r.prototype = new e;
        u.constructor = r;
        u.kill()._gc = false;
        r.version = "1.9.7";
        u.invalidate = function() {
            this._yoyo = this.vars.yoyo === true;
            this._repeat = this.vars.repeat || 0;
            this._repeatDelay = this.vars.repeatDelay || 0;
            this._uncache(true);
            return e.prototype.invalidate.call(this)
        };
        u.addCallback = function(e, n, r, i) {
            return this.add(t.delayedCall(0, e, r, i), n)
        };
        u.removeCallback = function(e, t) {
            if (t == null) {
                this._kill(null, e)
            } else {
                var n = this.getTweensOf(e, false),
                    r = n.length,
                    i = this._parseTimeOrLabel(t);
                while (--r > -1) {
                    if (n[r]._startTime === i) {
                        n[r]._enabled(false, false)
                    }
                }
            }
            return this
        };
        u.tweenTo = function(e, n) {
            n = n || {};
            var r = {
                    ease: s,
                    overwrite: 2,
                    useFrames: this.usesFrames(),
                    immediateRender: false
                },
                o, u;
            for (o in n) {
                r[o] = n[o]
            }
            r.time = this._parseTimeOrLabel(e);
            u = new t(this, Math.abs(Number(r.time) - this._time) / this._timeScale || .001, r);
            r.onStart = function() {
                u.target.paused(true);
                if (u.vars.time !== u.target.time()) {
                    u.duration(Math.abs(u.vars.time - u.target.time()) / u.target._timeScale)
                }
                if (n.onStart) {
                    n.onStart.apply(n.onStartScope || u, n.onStartParams || i)
                }
            };
            return u
        };
        u.tweenFromTo = function(e, t, n) {
            n = n || {};
            e = this._parseTimeOrLabel(e);
            n.startAt = {
                onComplete: this.seek,
                onCompleteParams: [e],
                onCompleteScope: this
            };
            n.immediateRender = n.immediateRender !== false;
            var r = this.tweenTo(t, n);
            return r.duration(Math.abs(r.vars.time - e) / this._timeScale || .001)
        };
        u.render = function(e, t, n) {
            if (this._gc) {
                this._enabled(true, false)
            }
            this._active = !this._paused;
            var r = !this._dirty ? this._totalDuration : this.totalDuration(),
                s = this._duration,
                o = this._time,
                u = this._totalTime,
                a = this._startTime,
                f = this._timeScale,
                l = this._rawPrevTime,
                c = this._paused,
                h = this._cycle,
                p, d, v, m, g, y;
            if (e >= r) {
                if (!this._locked) {
                    this._totalTime = r;
                    this._cycle = this._repeat
                }
                if (!this._reversed)
                    if (!this._hasPausedChild()) {
                        d = true;
                        m = "onComplete";
                        if (s === 0)
                            if (e === 0 || this._rawPrevTime < 0)
                                if (this._rawPrevTime !== e && this._first) {
                                    g = true;
                                    if (this._rawPrevTime > 0) {
                                        m = "onReverseComplete"
                                    }
                                }
                    } this._rawPrevTime = e;
                if (this._yoyo && (this._cycle & 1) !== 0) {
                    this._time = e = 0
                } else {
                    this._time = s;
                    e = s + 1e-6
                }
            } else if (e < 1e-7) {
                if (!this._locked) {
                    this._totalTime = this._cycle = 0
                }
                this._time = 0;
                if (o !== 0 || s === 0 && this._rawPrevTime > 0 && !this._locked) {
                    m = "onReverseComplete";
                    d = this._reversed
                }
                if (e < 0) {
                    this._active = false;
                    if (s === 0)
                        if (this._rawPrevTime >= 0 && this._first) {
                            g = true
                        }
                } else if (!this._initted) {
                    g = true
                }
                this._rawPrevTime = e;
                e = 0
            } else {
                this._time = this._rawPrevTime = e;
                if (!this._locked) {
                    this._totalTime = e;
                    if (this._repeat !== 0) {
                        y = s + this._repeatDelay;
                        this._cycle = this._totalTime / y >> 0;
                        if (this._cycle !== 0)
                            if (this._cycle === this._totalTime / y) {
                                this._cycle--
                            } this._time = this._totalTime - this._cycle * y;
                        if (this._yoyo)
                            if ((this._cycle & 1) !== 0) {
                                this._time = s - this._time
                            } if (this._time > s) {
                            this._time = s;
                            e = s + 1e-6
                        } else if (this._time < 0) {
                            this._time = e = 0
                        } else {
                            e = this._time
                        }
                    }
                }
            }
            if (this._cycle !== h)
                if (!this._locked) {
                    var b = this._yoyo && (h & 1) !== 0,
                        w = b === (this._yoyo && (this._cycle & 1) !== 0),
                        E = this._totalTime,
                        S = this._cycle,
                        x = this._rawPrevTime,
                        T = this._time;
                    this._totalTime = h * s;
                    if (this._cycle < h) {
                        b = !b
                    } else {
                        this._totalTime += s
                    }
                    this._time = o;
                    this._rawPrevTime = s === 0 ? l - 1e-5 : l;
                    this._cycle = h;
                    this._locked = true;
                    o = b ? 0 : s;
                    this.render(o, t, s === 0);
                    if (!t)
                        if (!this._gc) {
                            if (this.vars.onRepeat) {
                                this.vars.onRepeat.apply(this.vars.onRepeatScope || this, this.vars.onRepeatParams || i)
                            }
                        } if (w) {
                        o = b ? s + 1e-6 : -1e-6;
                        this.render(o, true, false)
                    }
                    this._time = T;
                    this._totalTime = E;
                    this._cycle = S;
                    this._rawPrevTime = x;
                    this._locked = false
                } if ((this._time === o || !this._first) && !n && !g) {
                if (u !== this._totalTime)
                    if (this._onUpdate)
                        if (!t) {
                            this._onUpdate.apply(this.vars.onUpdateScope || this, this.vars.onUpdateParams || i)
                        } return
            } else if (!this._initted) {
                this._initted = true
            }
            if (u === 0)
                if (this.vars.onStart)
                    if (this._totalTime !== 0)
                        if (!t) {
                            this.vars.onStart.apply(this.vars.onStartScope || this, this.vars.onStartParams || i)
                        } if (this._time >= o) {
                p = this._first;
                while (p) {
                    v = p._next;
                    if (this._paused && !c) {
                        break
                    } else if (p._active || p._startTime <= this._time && !p._paused && !p._gc) {
                        if (!p._reversed) {
                            p.render((e - p._startTime) * p._timeScale, t, n)
                        } else {
                            p.render((!p._dirty ? p._totalDuration : p.totalDuration()) - (e - p._startTime) * p._timeScale, t, n)
                        }
                    }
                    p = v
                }
            } else {
                p = this._last;
                while (p) {
                    v = p._prev;
                    if (this._paused && !c) {
                        break
                    } else if (p._active || p._startTime <= o && !p._paused && !p._gc) {
                        if (!p._reversed) {
                            p.render((e - p._startTime) * p._timeScale, t, n)
                        } else {
                            p.render((!p._dirty ? p._totalDuration : p.totalDuration()) - (e - p._startTime) * p._timeScale, t, n)
                        }
                    }
                    p = v
                }
            }
            if (this._onUpdate)
                if (!t) {
                    this._onUpdate.apply(this.vars.onUpdateScope || this, this.vars.onUpdateParams || i)
                } if (m)
                if (!this._locked)
                    if (!this._gc)
                        if (a === this._startTime || f !== this._timeScale)
                            if (this._time === 0 || r >= this.totalDuration()) {
                                if (d) {
                                    if (this._timeline.autoRemoveChildren) {
                                        this._enabled(false, false)
                                    }
                                    this._active = false
                                }
                                if (!t && this.vars[m]) {
                                    this.vars[m].apply(this.vars[m + "Scope"] || this, this.vars[m + "Params"] || i)
                                }
                            }
        };
        u.getActive = function(e, t, n) {
            if (e == null) {
                e = true
            }
            if (t == null) {
                t = true
            }
            if (n == null) {
                n = false
            }
            var r = [],
                i = this.getChildren(e, t, n),
                s = 0,
                u = i.length,
                a, f;
            for (a = 0; a < u; a++) {
                f = i[a];
                if (!f._paused)
                    if (f._timeline._time >= f._startTime)
                        if (f._timeline._time < f._startTime + f._totalDuration / f._timeScale)
                            if (!o(f._timeline)) {
                                r[s++] = f
                            }
            }
            return r
        };
        u.getLabelAfter = function(e) {
            if (!e)
                if (e !== 0) {
                    e = this._time
                } var t = this.getLabelsArray(),
                n = t.length,
                r;
            for (r = 0; r < n; r++) {
                if (t[r].time > e) {
                    return t[r].name
                }
            }
            return null
        };
        u.getLabelBefore = function(e) {
            if (e == null) {
                e = this._time
            }
            var t = this.getLabelsArray(),
                n = t.length;
            while (--n > -1) {
                if (t[n].time < e) {
                    return t[n].name
                }
            }
            return null
        };
        u.getLabelsArray = function() {
            var e = [],
                t = 0,
                n;
            for (n in this._labels) {
                e[t++] = {
                    time: this._labels[n],
                    name: n
                }
            }
            e.sort(function(e, t) {
                return e.time - t.time
            });
            return e
        };
        u.progress = function(e) {
            return !arguments.length ? this._time / this.duration() : this.totalTime(this.duration() * (this._yoyo && (this._cycle & 1) !== 0 ? 1 - e : e) + this._cycle * (this._duration + this._repeatDelay), false)
        };
        u.totalProgress = function(e) {
            return !arguments.length ? this._totalTime / this.totalDuration() : this.totalTime(this.totalDuration() * e, false)
        };
        u.totalDuration = function(t) {
            if (!arguments.length) {
                if (this._dirty) {
                    e.prototype.totalDuration.call(this);
                    this._totalDuration = this._repeat === -1 ? 999999999999 : this._duration * (this._repeat + 1) + this._repeatDelay * this._repeat
                }
                return this._totalDuration
            }
            return this._repeat === -1 ? this : this.duration((t - this._repeat * this._repeatDelay) / (this._repeat + 1))
        };
        u.time = function(e, t) {
            if (!arguments.length) {
                return this._time
            }
            if (this._dirty) {
                this.totalDuration()
            }
            if (e > this._duration) {
                e = this._duration
            }
            if (this._yoyo && (this._cycle & 1) !== 0) {
                e = this._duration - e + this._cycle * (this._duration + this._repeatDelay)
            } else if (this._repeat !== 0) {
                e += this._cycle * (this._duration + this._repeatDelay)
            }
            return this.totalTime(e, t)
        };
        u.repeat = function(e) {
            if (!arguments.length) {
                return this._repeat
            }
            this._repeat = e;
            return this._uncache(true)
        };
        u.repeatDelay = function(e) {
            if (!arguments.length) {
                return this._repeatDelay
            }
            this._repeatDelay = e;
            return this._uncache(true)
        };
        u.yoyo = function(e) {
            if (!arguments.length) {
                return this._yoyo
            }
            this._yoyo = e;
            return this
        };
        u.currentLabel = function(e) {
            if (!arguments.length) {
                return this.getLabelBefore(this._time + 1e-8)
            }
            return this.seek(e, true)
        };
        return r
    }, true);
    (function() {
        var e = 180 / Math.PI,
            t = Math.PI / 180,
            n = [],
            r = [],
            i = [],
            s = {},
            o = function(e, t, n, r) {
                this.a = e;
                this.b = t;
                this.c = n;
                this.d = r;
                this.da = r - e;
                this.ca = n - e;
                this.ba = t - e
            },
            u = ",x,y,z,left,top,right,bottom,marginTop,marginLeft,marginRight,marginBottom,paddingLeft,paddingTop,paddingRight,paddingBottom,backgroundPosition,backgroundPosition_y,",
            a = function(e, t, n, r) {
                var i = {
                        a: e
                    },
                    s = {},
                    o = {},
                    u = {
                        c: r
                    },
                    a = (e + t) / 2,
                    f = (t + n) / 2,
                    l = (n + r) / 2,
                    c = (a + f) / 2,
                    h = (f + l) / 2,
                    p = (h - c) / 8;
                i.b = a + (e - a) / 4;
                s.b = c + p;
                i.c = s.a = (i.b + s.b) / 2;
                s.c = o.a = (c + h) / 2;
                o.b = h - p;
                u.b = l + (r - l) / 4;
                o.c = u.a = (o.b + u.b) / 2;
                return [i, s, o, u]
            },
            f = function(e, t, s, o, u) {
                var f = e.length - 1,
                    l = 0,
                    c = e[0].a,
                    h, p, d, v, m, g, y, b, w, E, S, x, T;
                for (h = 0; h < f; h++) {
                    m = e[l];
                    p = m.a;
                    d = m.d;
                    v = e[l + 1].d;
                    if (u) {
                        S = n[h];
                        x = r[h];
                        T = (x + S) * t * .25 / (o ? .5 : i[h] || .5);
                        g = d - (d - p) * (o ? t * .5 : S !== 0 ? T / S : 0);
                        y = d + (v - d) * (o ? t * .5 : x !== 0 ? T / x : 0);
                        b = d - (g + ((y - g) * (S * 3 / (S + x) + .5) / 4 || 0))
                    } else {
                        g = d - (d - p) * t * .5;
                        y = d + (v - d) * t * .5;
                        b = d - (g + y) / 2
                    }
                    g += b;
                    y += b;
                    m.c = w = g;
                    if (h !== 0) {
                        m.b = c
                    } else {
                        m.b = c = m.a + (m.c - m.a) * .6
                    }
                    m.da = d - p;
                    m.ca = w - p;
                    m.ba = c - p;
                    if (s) {
                        E = a(p, c, w, d);
                        e.splice(l, 1, E[0], E[1], E[2], E[3]);
                        l += 4
                    } else {
                        l++
                    }
                    c = y
                }
                m = e[l];
                m.b = c;
                m.c = c + (m.d - c) * .4;
                m.da = m.d - m.a;
                m.ca = m.c - m.a;
                m.ba = c - m.a;
                if (s) {
                    E = a(m.a, c, m.c, m.d);
                    e.splice(l, 1, E[0], E[1], E[2], E[3])
                }
            },
            l = function(e, t, i, s) {
                var u = [],
                    a, f, l, c, h, p;
                if (s) {
                    e = [s].concat(e);
                    f = e.length;
                    while (--f > -1) {
                        if (typeof(p = e[f][t]) === "string")
                            if (p.charAt(1) === "=") {
                                e[f][t] = s[t] + Number(p.charAt(0) + p.substr(2))
                            }
                    }
                }
                a = e.length - 2;
                if (a < 0) {
                    u[0] = new o(e[0][t], 0, 0, e[a < -1 ? 0 : 1][t]);
                    return u
                }
                for (f = 0; f < a; f++) {
                    l = e[f][t];
                    c = e[f + 1][t];
                    u[f] = new o(l, 0, 0, c);
                    if (i) {
                        h = e[f + 2][t];
                        n[f] = (n[f] || 0) + (c - l) * (c - l);
                        r[f] = (r[f] || 0) + (h - c) * (h - c)
                    }
                }
                u[f] = new o(e[f][t], 0, 0, e[f + 1][t]);
                return u
            },
            c = function(e, t, o, a, c, h) {
                var p = {},
                    d = [],
                    v = h || e[0],
                    m, g, y, b, w, E, S, x;
                c = typeof c === "string" ? "," + c + "," : u;
                if (t == null) {
                    t = 1
                }
                for (g in e[0]) {
                    d.push(g)
                }
                if (e.length > 1) {
                    x = e[e.length - 1];
                    S = true;
                    m = d.length;
                    while (--m > -1) {
                        g = d[m];
                        if (Math.abs(v[g] - x[g]) > .05) {
                            S = false;
                            break
                        }
                    }
                    if (S) {
                        e = e.concat();
                        if (h) {
                            e.unshift(h)
                        }
                        e.push(e[1]);
                        h = e[e.length - 3]
                    }
                }
                n.length = r.length = i.length = 0;
                m = d.length;
                while (--m > -1) {
                    g = d[m];
                    s[g] = c.indexOf("," + g + ",") !== -1;
                    p[g] = l(e, g, s[g], h)
                }
                m = n.length;
                while (--m > -1) {
                    n[m] = Math.sqrt(n[m]);
                    r[m] = Math.sqrt(r[m])
                }
                if (!a) {
                    m = d.length;
                    while (--m > -1) {
                        if (s[g]) {
                            y = p[d[m]];
                            E = y.length - 1;
                            for (b = 0; b < E; b++) {
                                w = y[b + 1].da / r[b] + y[b].da / n[b];
                                i[b] = (i[b] || 0) + w * w
                            }
                        }
                    }
                    m = i.length;
                    while (--m > -1) {
                        i[m] = Math.sqrt(i[m])
                    }
                }
                m = d.length;
                b = o ? 4 : 1;
                while (--m > -1) {
                    g = d[m];
                    y = p[g];
                    f(y, t, o, a, s[g]);
                    if (S) {
                        y.splice(0, b);
                        y.splice(y.length - b, b)
                    }
                }
                return p
            },
            h = function(e, t, n) {
                t = t || "soft";
                var r = {},
                    i = t === "cubic" ? 3 : 2,
                    s = t === "soft",
                    u = [],
                    a, f, l, c, h, p, d, v, m, g, y;
                if (s && n) {
                    e = [n].concat(e)
                }
                if (e == null || e.length < i + 1) {
                    throw "invalid Bezier data"
                }
                for (m in e[0]) {
                    u.push(m)
                }
                p = u.length;
                while (--p > -1) {
                    m = u[p];
                    r[m] = h = [];
                    g = 0;
                    v = e.length;
                    for (d = 0; d < v; d++) {
                        a = n == null ? e[d][m] : typeof(y = e[d][m]) === "string" && y.charAt(1) === "=" ? n[m] + Number(y.charAt(0) + y.substr(2)) : Number(y);
                        if (s)
                            if (d > 1)
                                if (d < v - 1) {
                                    h[g++] = (a + h[g - 2]) / 2
                                } h[g++] = a
                    }
                    v = g - i + 1;
                    g = 0;
                    for (d = 0; d < v; d += i) {
                        a = h[d];
                        f = h[d + 1];
                        l = h[d + 2];
                        c = i === 2 ? 0 : h[d + 3];
                        h[g++] = y = i === 3 ? new o(a, f, l, c) : new o(a, (2 * f + a) / 3, (2 * f + l) / 3, l)
                    }
                    h.length = g
                }
                return r
            },
            p = function(e, t, n) {
                var r = 1 / n,
                    i = e.length,
                    s, o, u, a, f, l, c, h, p, d, v;
                while (--i > -1) {
                    d = e[i];
                    u = d.a;
                    a = d.d - u;
                    f = d.c - u;
                    l = d.b - u;
                    s = o = 0;
                    for (h = 1; h <= n; h++) {
                        c = r * h;
                        p = 1 - c;
                        s = o - (o = (c * c * a + 3 * p * (c * f + p * l)) * c);
                        v = i * n + h - 1;
                        t[v] = (t[v] || 0) + s * s
                    }
                }
            },
            d = function(e, t) {
                t = t >> 0 || 6;
                var n = [],
                    r = [],
                    i = 0,
                    s = 0,
                    o = t - 1,
                    u = [],
                    a = [],
                    f, l, c, h;
                for (f in e) {
                    p(e[f], n, t)
                }
                c = n.length;
                for (l = 0; l < c; l++) {
                    i += Math.sqrt(n[l]);
                    h = l % t;
                    a[h] = i;
                    if (h === o) {
                        s += i;
                        h = l / t >> 0;
                        u[h] = a;
                        r[h] = s;
                        i = 0;
                        a = []
                    }
                }
                return {
                    length: s,
                    lengths: r,
                    segments: u
                }
            },
            v = window._gsDefine.plugin({
                propName: "bezier",
                priority: -1,
                API: 2,
                global: true,
                init: function(e, t, n) {
                    this._target = e;
                    if (t instanceof Array) {
                        t = {
                            values: t
                        }
                    }
                    this._func = {};
                    this._round = {};
                    this._props = [];
                    this._timeRes = t.timeResolution == null ? 6 : parseInt(t.timeResolution, 10);
                    var r = t.values || [],
                        i = {},
                        s = r[0],
                        o = t.autoRotate || n.vars.orientToBezier,
                        u, a, f, l, p;
                    this._autoRotate = o ? o instanceof Array ? o : [
                        ["x", "y", "rotation", o === true ? 0 : Number(o) || 0]
                    ] : null;
                    for (u in s) {
                        this._props.push(u)
                    }
                    f = this._props.length;
                    while (--f > -1) {
                        u = this._props[f];
                        this._overwriteProps.push(u);
                        a = this._func[u] = typeof e[u] === "function";
                        i[u] = !a ? parseFloat(e[u]) : e[u.indexOf("set") || typeof e["get" + u.substr(3)] !== "function" ? u : "get" + u.substr(3)]();
                        if (!p)
                            if (i[u] !== r[0][u]) {
                                p = i
                            }
                    }
                    this._beziers = t.type !== "cubic" && t.type !== "quadratic" && t.type !== "soft" ? c(r, isNaN(t.curviness) ? 1 : t.curviness, false, t.type === "thruBasic", t.correlate, p) : h(r, t.type, i);
                    this._segCount = this._beziers[u].length;
                    if (this._timeRes) {
                        var v = d(this._beziers, this._timeRes);
                        this._length = v.length;
                        this._lengths = v.lengths;
                        this._segments = v.segments;
                        this._l1 = this._li = this._s1 = this._si = 0;
                        this._l2 = this._lengths[0];
                        this._curSeg = this._segments[0];
                        this._s2 = this._curSeg[0];
                        this._prec = 1 / this._curSeg.length
                    }
                    if (o = this._autoRotate) {
                        if (!(o[0] instanceof Array)) {
                            this._autoRotate = o = [o]
                        }
                        f = o.length;
                        while (--f > -1) {
                            for (l = 0; l < 3; l++) {
                                u = o[f][l];
                                this._func[u] = typeof e[u] === "function" ? e[u.indexOf("set") || typeof e["get" + u.substr(3)] !== "function" ? u : "get" + u.substr(3)] : false
                            }
                        }
                    }
                    return true
                },
                set: function(t) {
                    var n = this._segCount,
                        r = this._func,
                        i = this._target,
                        s, o, u, a, f, l, c, h, p, d;
                    if (!this._timeRes) {
                        s = t < 0 ? 0 : t >= 1 ? n - 1 : n * t >> 0;
                        l = (t - s * (1 / n)) * n
                    } else {
                        p = this._lengths;
                        d = this._curSeg;
                        t *= this._length;
                        u = this._li;
                        if (t > this._l2 && u < n - 1) {
                            h = n - 1;
                            while (u < h && (this._l2 = p[++u]) <= t) {}
                            this._l1 = p[u - 1];
                            this._li = u;
                            this._curSeg = d = this._segments[u];
                            this._s2 = d[this._s1 = this._si = 0]
                        } else if (t < this._l1 && u > 0) {
                            while (u > 0 && (this._l1 = p[--u]) >= t) {}
                            if (u === 0 && t < this._l1) {
                                this._l1 = 0
                            } else {
                                u++
                            }
                            this._l2 = p[u];
                            this._li = u;
                            this._curSeg = d = this._segments[u];
                            this._s1 = d[(this._si = d.length - 1) - 1] || 0;
                            this._s2 = d[this._si]
                        }
                        s = u;
                        t -= this._l1;
                        u = this._si;
                        if (t > this._s2 && u < d.length - 1) {
                            h = d.length - 1;
                            while (u < h && (this._s2 = d[++u]) <= t) {}
                            this._s1 = d[u - 1];
                            this._si = u
                        } else if (t < this._s1 && u > 0) {
                            while (u > 0 && (this._s1 = d[--u]) >= t) {}
                            if (u === 0 && t < this._s1) {
                                this._s1 = 0
                            } else {
                                u++
                            }
                            this._s2 = d[u];
                            this._si = u
                        }
                        l = (u + (t - this._s1) / (this._s2 - this._s1)) * this._prec
                    }
                    o = 1 - l;
                    u = this._props.length;
                    while (--u > -1) {
                        a = this._props[u];
                        f = this._beziers[a][s];
                        c = (l * l * f.da + 3 * o * (l * f.ca + o * f.ba)) * l + f.a;
                        if (this._round[a]) {
                            c = c + (c > 0 ? .5 : -.5) >> 0
                        }
                        if (r[a]) {
                            i[a](c)
                        } else {
                            if (a == "x") {
                                i.setX(c)
                            } else if (a == "y") {
                                i.setY(c)
                            } else if (a == "z") {
                                i.setZ(c)
                            } else if (a == "angleX") {
                                i.setAngleX(c)
                            } else if (a == "angleY") {
                                i.setAngleY(c)
                            } else if (a == "angleZ") {
                                i.setAngleZ(c)
                            } else if (a == "w") {
                                i.setWidth(c)
                            } else if (a == "h") {
                                i.setHeight(c)
                            } else if (a == "alpha") {
                                i.setAlpha(c)
                            } else if (a == "scale") {
                                i.setScale2(c)
                            } else {
                                i[a] = c
                            }
                        }
                    }
                    if (this._autoRotate) {
                        var v = this._autoRotate,
                            m, g, y, b, w, E, S;
                        u = v.length;
                        while (--u > -1) {
                            a = v[u][2];
                            E = v[u][3] || 0;
                            S = v[u][4] === true ? 1 : e;
                            f = this._beziers[v[u][0]];
                            m = this._beziers[v[u][1]];
                            if (f && m) {
                                f = f[s];
                                m = m[s];
                                g = f.a + (f.b - f.a) * l;
                                b = f.b + (f.c - f.b) * l;
                                g += (b - g) * l;
                                b += (f.c + (f.d - f.c) * l - b) * l;
                                y = m.a + (m.b - m.a) * l;
                                w = m.b + (m.c - m.b) * l;
                                y += (w - y) * l;
                                w += (m.c + (m.d - m.c) * l - w) * l;
                                c = Math.atan2(w - y, b - g) * S + E;
                                if (r[a]) {
                                    i[a](c)
                                } else {
                                    i[a] = c
                                }
                            }
                        }
                    }
                }
            }),
            m = v.prototype;
        v.bezierThrough = c;
        v.cubicToQuadratic = a;
        v._autoCSS = true;
        v.quadraticToCubic = function(e, t, n) {
            return new o(e, (2 * t + e) / 3, (2 * t + n) / 3, n)
        };
        v._cssRegister = function() {
            var e = window._gsDefine.globals.CSSPlugin;
            if (!e) {
                return
            }
            var n = e._internals,
                r = n._parseToProxy,
                i = n._setPluginRatio,
                s = n.CSSPropTween;
            n._registerComplexSpecialProp("bezier", {
                parser: function(e, n, o, u, a, f) {
                    if (n instanceof Array) {
                        n = {
                            values: n
                        }
                    }
                    f = new v;
                    var l = n.values,
                        c = l.length - 1,
                        h = [],
                        p = {},
                        d, m, g;
                    if (c < 0) {
                        return a
                    }
                    for (d = 0; d <= c; d++) {
                        g = r(e, l[d], u, a, f, c !== d);
                        h[d] = g.end
                    }
                    for (m in n) {
                        p[m] = n[m]
                    }
                    p.values = h;
                    a = new s(e, "bezier", 0, 0, g.pt, 2);
                    a.data = g;
                    a.plugin = f;
                    a.setRatio = i;
                    if (p.autoRotate === 0) {
                        p.autoRotate = true
                    }
                    if (p.autoRotate && !(p.autoRotate instanceof Array)) {
                        d = p.autoRotate === true ? 0 : Number(p.autoRotate) * t;
                        p.autoRotate = g.end.left != null ? [
                            ["left", "top", "rotation", d, true]
                        ] : g.end.x != null ? [
                            ["x", "y", "rotation", d, true]
                        ] : false
                    }
                    if (p.autoRotate) {
                        if (!u._transform) {
                            u._enableTransforms(false)
                        }
                        g.autoRotate = u._target._gsTransform
                    }
                    f._onInitTween(g.proxy, p, u._tween);
                    return a
                }
            })
        };
        m._roundProps = function(e, t) {
            var n = this._overwriteProps,
                r = n.length;
            while (--r > -1) {
                if (e[n[r]] || e.bezier || e.bezierThrough) {
                    this._round[n[r]] = t
                }
            }
        };
        m._kill = function(e) {
            var t = this._props,
                n, r;
            for (n in this._beziers) {
                if (n in e) {
                    delete this._beziers[n];
                    delete this._func[n];
                    r = t.length;
                    while (--r > -1) {
                        if (t[r] === n) {
                            t.splice(r, 1)
                        }
                    }
                }
            }
            return this._super._kill.call(this, e)
        }
    })();
    window._gsDefine("plugins.CSSPlugin", ["plugins.TweenPlugin", "TweenLite"], function(e, t) {
        var n = function() {
                e.call(this, "css");
                this._overwriteProps.length = 0
            },
            r, i, s, o, u = {},
            a = n.prototype = new e("css");
        a.constructor = n;
        n.version = "1.9.7";
        n.API = 2;
        n.defaultTransformPerspective = 0;
        a = "px";
        n.suffixMap = {
            top: a,
            right: a,
            bottom: a,
            left: a,
            width: a,
            height: a,
            fontSize: a,
            padding: a,
            margin: a,
            perspective: a
        };
        var f = /(?:\d|\-\d|\.\d|\-\.\d)+/g,
            l = /(?:\d|\-\d|\.\d|\-\.\d|\+=\d|\-=\d|\+=.\d|\-=\.\d)+/g,
            c = /(?:\+=|\-=|\-|\b)[\d\-\.]+[a-zA-Z0-9]*(?:%|\b)/gi,
            h = /[^\d\-\.]/g,
            p = /(?:\d|\-|\+|=|#|\.)*/g,
            d = /opacity *= *([^)]*)/,
            v = /opacity:([^;]*)/,
            m = /alpha\(opacity *=.+?\)/i,
            g = /^(rgb|hsl)/,
            y = /([A-Z])/g,
            b = /-([a-z])/gi,
            w = /(^(?:url\(\"|url\())|(?:(\"\))$|\)$)/gi,
            E = function(e, t) {
                return t.toUpperCase()
            },
            S = /(?:Left|Right|Width)/i,
            x = /(M11|M12|M21|M22)=[\d\-\.e]+/gi,
            T = /progid\:DXImageTransform\.Microsoft\.Matrix\(.+?\)/i,
            N = /,(?=[^\)]*(?:\(|$))/gi,
            C = Math.PI / 180,
            k = 180 / Math.PI,
            L = {},
            A = document,
            O = A.createElement("div"),
            M = A.createElement("img"),
            _ = n._internals = {
                _specialProps: u
            },
            D = navigator.userAgent,
            P, H, B, j, F, I, q = function() {
                var e = D.indexOf("Android"),
                    t = A.createElement("div"),
                    n;
                B = D.indexOf("Safari") !== -1 && D.indexOf("Chrome") === -1 && (e === -1 || Number(D.substr(e + 8, 1)) > 3);
                F = B && Number(D.substr(D.indexOf("Version/") + 8, 1)) < 6;
                j = D.indexOf("Firefox") !== -1;
                /MSIE ([0-9]{1,}[\.0-9]{0,})/.exec(D);
                I = parseFloat(RegExp.$1);
                t.innerHTML = "<a style='top:1px;opacity:.55;'>a</a>";
                n = t.getElementsByTagName("a")[0];
                return n ? /^0.55/.test(n.style.opacity) : false
            }(),
            R = function(e) {
                return d.test(typeof e === "string" ? e : (e.currentStyle ? e.currentStyle.filter : e.style.filter) || "") ? parseFloat(RegExp.$1) / 100 : 1
            },
            U = function(e) {
                if (window.console) {
                    console.log(e)
                }
            },
            z = "",
            W = "",
            X = function(e, t) {
                t = t || O;
                var n = t.style,
                    r, i;
                if (n[e] !== undefined) {
                    return e
                }
                e = e.charAt(0).toUpperCase() + e.substr(1);
                r = ["O", "Moz", "ms", "Ms", "Webkit"];
                i = 5;
                while (--i > -1 && n[r[i] + e] === undefined) {}
                if (i >= 0) {
                    W = i === 3 ? "ms" : r[i];
                    z = "-" + W.toLowerCase() + "-";
                    return W + e
                }
                return null
            },
            V = A.defaultView ? A.defaultView.getComputedStyle : function() {},
            $ = n.getStyle = function(e, t, n, r, i) {
                var s;
                if (!q)
                    if (t === "opacity") {
                        return R(e)
                    } if (!r && e.style[t]) {
                    s = e.style[t]
                } else if (n = n || V(e, null)) {
                    e = n.getPropertyValue(t.replace(y, "-$1").toLowerCase());
                    s = e || n.length ? e : n[t]
                } else if (e.currentStyle) {
                    n = e.currentStyle;
                    s = n[t]
                }
                return i != null && (!s || s === "none" || s === "auto" || s === "auto auto") ? i : s
            },
            J = function(e, t, n, r, i) {
                if (r === "px" || !r) {
                    return n
                }
                if (r === "auto" || !n) {
                    return 0
                }
                var s = S.test(t),
                    o = e,
                    u = O.style,
                    a = n < 0,
                    f;
                if (a) {
                    n = -n
                }
                if (r === "%" && t.indexOf("border") !== -1) {
                    f = n / 100 * (s ? e.clientWidth : e.clientHeight)
                } else {
                    u.cssText = "border-style:solid; border-width:0; position:absolute; line-height:0;";
                    if (r === "%" || !o.appendChild) {
                        o = e.parentNode || A.body;
                        u[s ? "width" : "height"] = n + r
                    } else {
                        u[s ? "borderLeftWidth" : "borderTopWidth"] = n + r
                    }
                    o.appendChild(O);
                    f = parseFloat(O[s ? "offsetWidth" : "offsetHeight"]);
                    o.removeChild(O);
                    if (f === 0 && !i) {
                        f = J(e, t, n, r, true)
                    }
                }
                return a ? -f : f
            },
            K = function(e, t, n) {
                if ($(e, "position", n) !== "absolute") {
                    return 0
                }
                var r = t === "left" ? "Left" : "Top",
                    i = $(e, "margin" + r, n);
                return e["offset" + r] - (J(e, t, parseFloat(i), i.replace(p, "")) || 0)
            },
            Q = function(e, t) {
                var n = {},
                    r, i;
                if (t = t || V(e, null)) {
                    if (r = t.length) {
                        while (--r > -1) {
                            n[t[r].replace(b, E)] = t.getPropertyValue(t[r])
                        }
                    } else {
                        for (r in t) {
                            n[r] = t[r]
                        }
                    }
                } else if (t = e.currentStyle || e.style) {
                    for (r in t) {
                        n[r.replace(b, E)] = t[r]
                    }
                }
                if (!q) {
                    n.opacity = R(e)
                }
                i = Nt(e, t, false);
                n.rotation = i.rotation * k;
                n.skewX = i.skewX * k;
                n.scaleX = i.scaleX;
                n.scaleY = i.scaleY;
                n.x = i.x;
                n.y = i.y;
                if (Tt) {
                    n.z = i.z;
                    n.rotationX = i.rotationX * k;
                    n.rotationY = i.rotationY * k;
                    n.scaleZ = i.scaleZ
                }
                if (n.filters) {
                    delete n.filters
                }
                return n
            },
            G = function(e, t, n, r, i) {
                var s = {},
                    o = e.style,
                    u, a, f;
                for (a in n) {
                    if (a !== "cssText")
                        if (a !== "length")
                            if (isNaN(a))
                                if (t[a] !== (u = n[a]) || i && i[a])
                                    if (a.indexOf("Origin") === -1)
                                        if (typeof u === "number" || typeof u === "string") {
                                            s[a] = u === "auto" && (a === "left" || a === "top") ? K(e, a) : (u === "" || u === "auto" || u === "none") && typeof t[a] === "string" && t[a].replace(h, "") !== "" ? 0 : u;
                                            if (o[a] !== undefined) {
                                                f = new ht(o, a, o[a], f)
                                            }
                                        }
                }
                if (r) {
                    for (a in r) {
                        if (a !== "className") {
                            s[a] = r[a]
                        }
                    }
                }
                return {
                    difs: s,
                    firstMPT: f
                }
            },
            Y = {
                width: ["Left", "Right"],
                height: ["Top", "Bottom"]
            },
            Z = ["marginLeft", "marginRight", "marginTop", "marginBottom"],
            et = function(e, t, n) {
                var r = parseFloat(t === "width" ? e.offsetWidth : e.offsetHeight),
                    i = Y[t],
                    s = i.length;
                n = n || V(e, null);
                while (--s > -1) {
                    r -= parseFloat($(e, "padding" + i[s], n, true)) || 0;
                    r -= parseFloat($(e, "border" + i[s] + "Width", n, true)) || 0
                }
                return r
            },
            tt = function(e, t) {
                if (e == null || e === "" || e === "auto" || e === "auto auto") {
                    e = "0 0"
                }
                var n = e.split(" "),
                    r = e.indexOf("left") !== -1 ? "0%" : e.indexOf("right") !== -1 ? "100%" : n[0],
                    i = e.indexOf("top") !== -1 ? "0%" : e.indexOf("bottom") !== -1 ? "100%" : n[1];
                if (i == null) {
                    i = "0"
                } else if (i === "center") {
                    i = "50%"
                }
                if (r === "center" || isNaN(parseFloat(r))) {
                    r = "50%"
                }
                if (t) {
                    t.oxp = r.indexOf("%") !== -1;
                    t.oyp = i.indexOf("%") !== -1;
                    t.oxr = r.charAt(1) === "=";
                    t.oyr = i.charAt(1) === "=";
                    t.ox = parseFloat(r.replace(h, ""));
                    t.oy = parseFloat(i.replace(h, ""))
                }
                return r + " " + i + (n.length > 2 ? " " + n[2] : "")
            },
            nt = function(e, t) {
                return typeof e === "string" && e.charAt(1) === "=" ? parseInt(e.charAt(0) + "1", 10) * parseFloat(e.substr(2)) : parseFloat(e) - parseFloat(t)
            },
            rt = function(e, t) {
                return e == null ? t : typeof e === "string" && e.charAt(1) === "=" ? parseInt(e.charAt(0) + "1", 10) * Number(e.substr(2)) + t : parseFloat(e)
            },
            it = function(e, t, n, r) {
                var i = 1e-6,
                    s, o, u, a;
                if (e == null) {
                    a = t
                } else if (typeof e === "number") {
                    a = e * C
                } else {
                    s = Math.PI * 2;
                    o = e.split("_");
                    u = Number(o[0].replace(h, "")) * (e.indexOf("rad") === -1 ? C : 1) - (e.charAt(1) === "=" ? 0 : t);
                    if (o.length) {
                        if (r) {
                            r[n] = t + u
                        }
                        if (e.indexOf("short") !== -1) {
                            u = u % s;
                            if (u !== u % (s / 2)) {
                                u = u < 0 ? u + s : u - s
                            }
                        }
                        if (e.indexOf("_cw") !== -1 && u < 0) {
                            u = (u + s * 9999999999) % s - (u / s | 0) * s
                        } else if (e.indexOf("ccw") !== -1 && u > 0) {
                            u = (u - s * 9999999999) % s - (u / s | 0) * s
                        }
                    }
                    a = t + u
                }
                if (a < i && a > -i) {
                    a = 0
                }
                return a
            },
            st = {
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
            ot = function(e, t, n) {
                e = e < 0 ? e + 1 : e > 1 ? e - 1 : e;
                return (e * 6 < 1 ? t + (n - t) * e * 6 : e < .5 ? n : e * 3 < 2 ? t + (n - t) * (2 / 3 - e) * 6 : t) * 255 + .5 | 0
            },
            ut = function(e) {
                var t, n, r, i, s, o;
                if (!e || e === "") {
                    return st.black
                }
                if (typeof e === "number") {
                    return [e >> 16, e >> 8 & 255, e & 255]
                }
                if (e.charAt(e.length - 1) === ",") {
                    e = e.substr(0, e.length - 1)
                }
                if (st[e]) {
                    return st[e]
                }
                if (e.charAt(0) === "#") {
                    if (e.length === 4) {
                        t = e.charAt(1), n = e.charAt(2), r = e.charAt(3);
                        e = "#" + t + t + n + n + r + r
                    }
                    e = parseInt(e.substr(1), 16);
                    return [e >> 16, e >> 8 & 255, e & 255]
                }
                if (e.substr(0, 3) === "hsl") {
                    e = e.match(f);
                    i = Number(e[0]) % 360 / 360;
                    s = Number(e[1]) / 100;
                    o = Number(e[2]) / 100;
                    n = o <= .5 ? o * (s + 1) : o + s - o * s;
                    t = o * 2 - n;
                    if (e.length > 3) {
                        e[3] = Number(e[3])
                    }
                    e[0] = ot(i + 1 / 3, t, n);
                    e[1] = ot(i, t, n);
                    e[2] = ot(i - 1 / 3, t, n);
                    return e
                }
                e = e.match(f) || st.transparent;
                e[0] = Number(e[0]);
                e[1] = Number(e[1]);
                e[2] = Number(e[2]);
                if (e.length > 3) {
                    e[3] = Number(e[3])
                }
                return e
            },
            at = "(?:\\b(?:(?:rgb|rgba|hsl|hsla)\\(.+?\\))|\\B#.+?\\b";
        for (a in st) {
            at += "|" + a + "\\b"
        }
        at = new RegExp(at + ")", "gi");
        var ft = function(e, t, n, r) {
                if (e == null) {
                    return function(e) {
                        return e
                    }
                }
                var i = t ? (e.match(at) || [""])[0] : "",
                    s = e.split(i).join("").match(c) || [],
                    o = e.substr(0, e.indexOf(s[0])),
                    u = e.charAt(e.length - 1) === ")" ? ")" : "",
                    a = e.indexOf(" ") !== -1 ? " " : ",",
                    l = s.length,
                    h = l > 0 ? s[0].replace(f, "") : "",
                    p;
                if (!l) {
                    return function(e) {
                        return e
                    }
                }
                if (t) {
                    p = function(e) {
                        var t, f, d, v;
                        if (typeof e === "number") {
                            e += h
                        } else if (r && N.test(e)) {
                            v = e.replace(N, "|").split("|");
                            for (d = 0; d < v.length; d++) {
                                v[d] = p(v[d])
                            }
                            return v.join(",")
                        }
                        t = (e.match(at) || [i])[0];
                        f = e.split(t).join("").match(c) || [];
                        d = f.length;
                        if (l > d--) {
                            while (++d < l) {
                                f[d] = n ? f[(d - 1) / 2 | 0] : s[d]
                            }
                        }
                        return o + f.join(a) + a + t + u + (e.indexOf("inset") !== -1 ? " inset" : "")
                    };
                    return p
                }
                p = function(e) {
                    var t, i, f;
                    if (typeof e === "number") {
                        e += h
                    } else if (r && N.test(e)) {
                        i = e.replace(N, "|").split("|");
                        for (f = 0; f < i.length; f++) {
                            i[f] = p(i[f])
                        }
                        return i.join(",")
                    }
                    t = e.match(c) || [];
                    f = t.length;
                    if (l > f--) {
                        while (++f < l) {
                            t[f] = n ? t[(f - 1) / 2 | 0] : s[f]
                        }
                    }
                    return o + t.join(a) + u
                };
                return p
            },
            lt = function(e) {
                e = e.split(",");
                return function(t, n, r, i, s, o, u) {
                    var a = (n + "").split(" "),
                        f;
                    u = {};
                    for (f = 0; f < 4; f++) {
                        u[e[f]] = a[f] = a[f] || a[(f - 1) / 2 >> 0]
                    }
                    return i.parse(t, u, s, o)
                }
            },
            ct = _._setPluginRatio = function(e) {
                this.plugin.setRatio(e);
                var t = this.data,
                    n = t.proxy,
                    r = t.firstMPT,
                    i = 1e-6,
                    s, o, u, a;
                while (r) {
                    s = n[r.v];
                    if (r.r) {
                        s = s > 0 ? s + .5 | 0 : s - .5 | 0
                    } else if (s < i && s > -i) {
                        s = 0
                    }
                    r.t[r.p] = s;
                    r = r._next
                }
                if (t.autoRotate) {
                    t.autoRotate.rotation = n.rotation
                }
                if (e === 1) {
                    r = t.firstMPT;
                    while (r) {
                        o = r.t;
                        if (!o.type) {
                            o.e = o.s + o.xs0
                        } else if (o.type === 1) {
                            a = o.xs0 + o.s + o.xs1;
                            for (u = 1; u < o.l; u++) {
                                a += o["xn" + u] + o["xs" + (u + 1)]
                            }
                            o.e = a
                        }
                        r = r._next
                    }
                }
            },
            ht = function(e, t, n, r, i) {
                this.t = e;
                this.p = t;
                this.v = n;
                this.r = i;
                if (r) {
                    r._prev = this;
                    this._next = r
                }
            },
            pt = _._parseToProxy = function(e, t, n, r, i, s) {
                var o = r,
                    u = {},
                    a = {},
                    f = n._transform,
                    l = L,
                    c, h, p, d, v;
                n._transform = null;
                L = t;
                r = v = n.parse(e, t, r, i);
                L = l;
                if (s) {
                    n._transform = f;
                    if (o) {
                        o._prev = null;
                        if (o._prev) {
                            o._prev._next = null
                        }
                    }
                }
                while (r && r !== o) {
                    if (r.type <= 1) {
                        h = r.p;
                        a[h] = r.s + r.c;
                        u[h] = r.s;
                        if (!s) {
                            d = new ht(r, "s", h, d, r.r);
                            r.c = 0
                        }
                        if (r.type === 1) {
                            c = r.l;
                            while (--c > 0) {
                                p = "xn" + c;
                                h = r.p + "_" + p;
                                a[h] = r.data[p];
                                u[h] = r[p];
                                if (!s) {
                                    d = new ht(r, p, h, d, r.rxp[p])
                                }
                            }
                        }
                    }
                    r = r._next
                }
                return {
                    proxy: u,
                    end: a,
                    firstMPT: d,
                    pt: v
                }
            },
            dt = _.CSSPropTween = function(e, t, n, i, s, u, a, f, l, c, h) {
                this.t = e;
                this.p = t;
                this.s = n;
                this.c = i;
                this.n = a || "css_" + t;
                if (!(e instanceof dt)) {
                    o.push(this.n)
                }
                this.r = f;
                this.type = u || 0;
                if (l) {
                    this.pr = l;
                    r = true
                }
                this.b = c === undefined ? n : c;
                this.e = h === undefined ? n + i : h;
                if (s) {
                    this._next = s;
                    s._prev = this
                }
            },
            vt = n.parseComplex = function(e, t, n, r, i, s, o, u, a, c) {
                n = n || s || "";
                o = new dt(e, t, 0, 0, o, c ? 2 : 1, null, false, u, n, r);
                r += "";
                var h = n.split(", ").join(",").split(" "),
                    p = r.split(", ").join(",").split(" "),
                    d = h.length,
                    v = P !== false,
                    m, y, b, w, E, S, x, T, C, k, L, A;
                if (r.indexOf(",") !== -1 || n.indexOf(",") !== -1) {
                    h = h.join(" ").replace(N, ", ").split(" ");
                    p = p.join(" ").replace(N, ", ").split(" ");
                    d = h.length
                }
                if (d !== p.length) {
                    h = (s || "").split(" ");
                    d = h.length
                }
                o.plugin = a;
                o.setRatio = c;
                for (m = 0; m < d; m++) {
                    w = h[m];
                    E = p[m];
                    T = parseFloat(w);
                    if (T || T === 0) {
                        o.appendXtra("", T, nt(E, T), E.replace(l, ""), v && E.indexOf("px") !== -1, true)
                    } else if (i && (w.charAt(0) === "#" || st[w] || g.test(w))) {
                        A = E.charAt(E.length - 1) === "," ? ")," : ")";
                        w = ut(w);
                        E = ut(E);
                        C = w.length + E.length > 6;
                        if (C && !q && E[3] === 0) {
                            o["xs" + o.l] += o.l ? " transparent" : "transparent";
                            o.e = o.e.split(p[m]).join("transparent")
                        } else {
                            if (!q) {
                                C = false
                            }
                            o.appendXtra(C ? "rgba(" : "rgb(", w[0], E[0] - w[0], ",", true, true).appendXtra("", w[1], E[1] - w[1], ",", true).appendXtra("", w[2], E[2] - w[2], C ? "," : A, true);
                            if (C) {
                                w = w.length < 4 ? 1 : w[3];
                                o.appendXtra("", w, (E.length < 4 ? 1 : E[3]) - w, A, false)
                            }
                        }
                    } else {
                        S = w.match(f);
                        if (!S) {
                            o["xs" + o.l] += o.l ? " " + w : w
                        } else {
                            x = E.match(l);
                            if (!x || x.length !== S.length) {
                                return o
                            }
                            b = 0;
                            for (y = 0; y < S.length; y++) {
                                L = S[y];
                                k = w.indexOf(L, b);
                                o.appendXtra(w.substr(b, k - b), Number(L), nt(x[y], L), "", v && w.substr(k + L.length, 2) === "px", y === 0);
                                b = k + L.length
                            }
                            o["xs" + o.l] += w.substr(b)
                        }
                    }
                }
                if (r.indexOf("=") !== -1)
                    if (o.data) {
                        A = o.xs0 + o.data.s;
                        for (m = 1; m < o.l; m++) {
                            A += o["xs" + m] + o.data["xn" + m]
                        }
                        o.e = A + o["xs" + m]
                    } if (!o.l) {
                    o.type = -1;
                    o.xs0 = o.e
                }
                return o.xfirst || o
            },
            mt = 9;
        a = dt.prototype;
        a.l = a.pr = 0;
        while (--mt > 0) {
            a["xn" + mt] = 0;
            a["xs" + mt] = ""
        }
        a.xs0 = "";
        a._next = a._prev = a.xfirst = a.data = a.plugin = a.setRatio = a.rxp = null;
        a.appendXtra = function(e, t, n, r, i, s) {
            var o = this,
                u = o.l;
            o["xs" + u] += s && u ? " " + e : e || "";
            if (!n)
                if (u !== 0 && !o.plugin) {
                    o["xs" + u] += t + (r || "");
                    return o
                } o.l++;
            o.type = o.setRatio ? 2 : 1;
            o["xs" + o.l] = r || "";
            if (u > 0) {
                o.data["xn" + u] = t + n;
                o.rxp["xn" + u] = i;
                o["xn" + u] = t;
                if (!o.plugin) {
                    o.xfirst = new dt(o, "xn" + u, t, n, o.xfirst || o, 0, o.n, i, o.pr);
                    o.xfirst.xs0 = 0
                }
                return o
            }
            o.data = {
                s: t + n
            };
            o.rxp = {};
            o.s = t;
            o.c = n;
            o.r = i;
            return o
        };
        var gt = function(e, t) {
                t = t || {};
                this.p = t.prefix ? X(e) || e : e;
                u[e] = u[this.p] = this;
                this.format = t.formatter || ft(t.defaultValue, t.color, t.collapsible, t.multi);
                if (t.parser) {
                    this.parse = t.parser
                }
                this.clrs = t.color;
                this.multi = t.multi;
                this.keyword = t.keyword;
                this.dflt = t.defaultValue;
                this.pr = t.priority || 0
            },
            yt = _._registerComplexSpecialProp = function(e, t, n) {
                if (typeof t !== "object") {
                    t = {
                        parser: n
                    }
                }
                var r = e.split(","),
                    i = t.defaultValue,
                    s, o;
                n = n || [i];
                for (s = 0; s < r.length; s++) {
                    t.prefix = s === 0 && t.prefix;
                    t.defaultValue = n[s] || i;
                    o = new gt(r[s], t)
                }
            },
            bt = function(e) {
                if (!u[e]) {
                    var t = e.charAt(0).toUpperCase() + e.substr(1) + "Plugin";
                    yt(e, {
                        parser: function(e, n, r, i, s, o, a) {
                            var f = (window.GreenSockGlobals || window).com.greensock.plugins[t];
                            if (!f) {
                                U("Error: " + t + " js file not loaded.");
                                return s
                            }
                            f._cssRegister();
                            return u[r].parse(e, n, r, i, s, o, a)
                        }
                    })
                }
            };
        a = gt.prototype;
        a.parseComplex = function(e, t, n, r, i, s) {
            var o = this.keyword,
                u, a, f, l, c, h;
            if (this.multi)
                if (N.test(n) || N.test(t)) {
                    a = t.replace(N, "|").split("|");
                    f = n.replace(N, "|").split("|")
                } else if (o) {
                a = [t];
                f = [n]
            }
            if (f) {
                l = f.length > a.length ? f.length : a.length;
                for (u = 0; u < l; u++) {
                    t = a[u] = a[u] || this.dflt;
                    n = f[u] = f[u] || this.dflt;
                    if (o) {
                        c = t.indexOf(o);
                        h = n.indexOf(o);
                        if (c !== h) {
                            n = h === -1 ? f : a;
                            n[u] += " " + o
                        }
                    }
                }
                t = a.join(", ");
                n = f.join(", ")
            }
            return vt(e, this.p, t, n, this.clrs, this.dflt, r, this.pr, i, s)
        };
        a.parse = function(e, t, n, r, i, o, u) {
            return this.parseComplex(e.style, this.format($(e, this.p, s, false, this.dflt)), this.format(t), i, o)
        };
        n.registerSpecialProp = function(e, t, n) {
            yt(e, {
                parser: function(e, r, i, s, o, u, a) {
                    var f = new dt(e, i, 0, 0, o, 2, i, false, n);
                    f.plugin = u;
                    f.setRatio = t(e, r, s._tween, i);
                    return f
                },
                priority: n
            })
        };
        var wt = "scaleX,scaleY,scaleZ,x,y,z,skewX,rotation,rotationX,rotationY,perspective".split(","),
            Et = X("transform"),
            St = z + "transform",
            xt = X("transformOrigin"),
            Tt = X("perspective") !== null,
            Nt = function(e, t, r) {
                var i = r ? e._gsTransform || {
                        skewY: 0
                    } : {
                        skewY: 0
                    },
                    s = i.scaleX < 0,
                    o = 2e-5,
                    u = 1e5,
                    a = -Math.PI + 1e-4,
                    f = Math.PI - 1e-4,
                    l = Tt ? parseFloat($(e, xt, t, false, "0 0 0").split(" ")[2]) || i.zOrigin || 0 : 0,
                    c, h, p, d, v, m, g, y, b, w, E, S, T;
                if (Et) {
                    c = $(e, St, t, true)
                } else if (e.currentStyle) {
                    c = e.currentStyle.filter.match(x);
                    if (c && c.length === 4) {
                        c = [c[0].substr(4), Number(c[2].substr(4)), Number(c[1].substr(4)), c[3].substr(4), i.x || 0, i.y || 0].join(",")
                    } else if (i.x != null) {
                        return i
                    } else {
                        c = ""
                    }
                }
                h = (c || "").match(/(?:\-|\b)[\d\-\.e]+\b/gi) || [];
                p = h.length;
                while (--p > -1) {
                    d = Number(h[p]);
                    h[p] = (v = d - (d |= 0)) ? (v * u + (v < 0 ? -.5 : .5) | 0) / u + d : d
                }
                if (h.length === 16) {
                    var N = h[8],
                        C = h[9],
                        k = h[10],
                        L = h[12],
                        A = h[13],
                        O = h[14];
                    if (i.zOrigin) {
                        O = -i.zOrigin;
                        L = N * O - h[12];
                        A = C * O - h[13];
                        O = k * O + i.zOrigin - h[14]
                    }
                    if (!r || i.rotationX == null) {
                        var M = h[0],
                            _ = h[1],
                            D = h[2],
                            P = h[3],
                            H = h[4],
                            B = h[5],
                            j = h[6],
                            F = h[7],
                            I = h[11],
                            q = i.rotationX = Math.atan2(j, k),
                            R = q < a || q > f,
                            U, z, W, X, V, J, K;
                        if (q) {
                            X = Math.cos(-q);
                            V = Math.sin(-q);
                            U = H * X + N * V;
                            z = B * X + C * V;
                            W = j * X + k * V;
                            N = H * -V + N * X;
                            C = B * -V + C * X;
                            k = j * -V + k * X;
                            I = F * -V + I * X;
                            H = U;
                            B = z;
                            j = W
                        }
                        q = i.rotationY = Math.atan2(N, M);
                        if (q) {
                            J = q < a || q > f;
                            X = Math.cos(-q);
                            V = Math.sin(-q);
                            U = M * X - N * V;
                            z = _ * X - C * V;
                            W = D * X - k * V;
                            C = _ * V + C * X;
                            k = D * V + k * X;
                            I = P * V + I * X;
                            M = U;
                            _ = z;
                            D = W
                        }
                        q = i.rotation = Math.atan2(_, B);
                        if (q) {
                            K = q < a || q > f;
                            X = Math.cos(-q);
                            V = Math.sin(-q);
                            M = M * X + H * V;
                            z = _ * X + B * V;
                            B = _ * -V + B * X;
                            j = D * -V + j * X;
                            _ = z
                        }
                        if (K && R) {
                            i.rotation = i.rotationX = 0
                        } else if (K && J) {
                            i.rotation = i.rotationY = 0
                        } else if (J && R) {
                            i.rotationY = i.rotationX = 0
                        }
                        i.scaleX = (Math.sqrt(M * M + _ * _) * u + .5 | 0) / u;
                        i.scaleY = (Math.sqrt(B * B + C * C) * u + .5 | 0) / u;
                        i.scaleZ = (Math.sqrt(j * j + k * k) * u + .5 | 0) / u;
                        i.skewX = 0;
                        i.perspective = I ? 1 / (I < 0 ? -I : I) : 0;
                        i.x = L;
                        i.y = A;
                        i.z = O
                    }
                } else if ((!Tt || h.length === 0 || i.x !== h[4] || i.y !== h[5] || !i.rotationX && !i.rotationY) && !(i.x !== undefined && $(e, "display", t) === "none")) {
                    var Q = h.length >= 6,
                        G = Q ? h[0] : 1,
                        Y = h[1] || 0,
                        Z = h[2] || 0,
                        et = Q ? h[3] : 1;
                    i.x = h[4] || 0;
                    i.y = h[5] || 0;
                    m = Math.sqrt(G * G + Y * Y);
                    g = Math.sqrt(et * et + Z * Z);
                    y = G || Y ? Math.atan2(Y, G) : i.rotation || 0;
                    b = Z || et ? Math.atan2(Z, et) + y : i.skewX || 0;
                    w = m - Math.abs(i.scaleX || 0);
                    E = g - Math.abs(i.scaleY || 0);
                    if (Math.abs(b) > Math.PI / 2 && Math.abs(b) < Math.PI * 1.5) {
                        if (s) {
                            m *= -1;
                            b += y <= 0 ? Math.PI : -Math.PI;
                            y += y <= 0 ? Math.PI : -Math.PI
                        } else {
                            g *= -1;
                            b += b <= 0 ? Math.PI : -Math.PI
                        }
                    }
                    S = (y - i.rotation) % Math.PI;
                    T = (b - i.skewX) % Math.PI;
                    if (i.skewX === undefined || w > o || w < -o || E > o || E < -o || S > a && S < f && S * u | 0 !== 0 || T > a && T < f && T * u | 0 !== 0) {
                        i.scaleX = m;
                        i.scaleY = g;
                        i.rotation = y;
                        i.skewX = b
                    }
                    if (Tt) {
                        i.rotationX = i.rotationY = i.z = 0;
                        i.perspective = parseFloat(n.defaultTransformPerspective) || 0;
                        i.scaleZ = 1
                    }
                }
                i.zOrigin = l;
                for (p in i) {
                    if (i[p] < o)
                        if (i[p] > -o) {
                            i[p] = 0
                        }
                }
                if (r) {
                    e._gsTransform = i
                }
                return i
            },
            Ct = function(e) {
                var t = this.data,
                    n = -t.rotation,
                    r = n + t.skewX,
                    i = 1e5,
                    s = (Math.cos(n) * t.scaleX * i | 0) / i,
                    o = (Math.sin(n) * t.scaleX * i | 0) / i,
                    u = (Math.sin(r) * -t.scaleY * i | 0) / i,
                    a = (Math.cos(r) * t.scaleY * i | 0) / i,
                    f = this.t.style,
                    l = this.t.currentStyle,
                    c, h;
                if (!l) {
                    return
                }
                h = o;
                o = -u;
                u = -h;
                c = l.filter;
                f.filter = "";
                var v = this.t.offsetWidth,
                    m = this.t.offsetHeight,
                    g = l.position !== "absolute",
                    y = "progid:DXImageTransform.Microsoft.Matrix(M11=" + s + ", M12=" + o + ", M21=" + u + ", M22=" + a,
                    b = t.x,
                    w = t.y,
                    E, S;
                if (t.ox != null) {
                    E = (t.oxp ? v * t.ox * .01 : t.ox) - v / 2;
                    S = (t.oyp ? m * t.oy * .01 : t.oy) - m / 2;
                    b += E - (E * s + S * o);
                    w += S - (E * u + S * a)
                }
                if (!g) {
                    var x = I < 8 ? 1 : -1,
                        N, C, k;
                    E = t.ieOffsetX || 0;
                    S = t.ieOffsetY || 0;
                    t.ieOffsetX = Math.round((v - ((s < 0 ? -s : s) * v + (o < 0 ? -o : o) * m)) / 2 + b);
                    t.ieOffsetY = Math.round((m - ((a < 0 ? -a : a) * m + (u < 0 ? -u : u) * v)) / 2 + w);
                    for (mt = 0; mt < 4; mt++) {
                        C = Z[mt];
                        N = l[C];
                        h = N.indexOf("px") !== -1 ? parseFloat(N) : J(this.t, C, parseFloat(N), N.replace(p, "")) || 0;
                        if (h !== t[C]) {
                            k = mt < 2 ? -t.ieOffsetX : -t.ieOffsetY
                        } else {
                            k = mt < 2 ? E - t.ieOffsetX : S - t.ieOffsetY
                        }
                        f[C] = (t[C] = Math.round(h - k * (mt === 0 || mt === 2 ? 1 : x))) + "px"
                    }
                    y += ", sizingMethod='auto expand')"
                } else {
                    E = v / 2;
                    S = m / 2;
                    y += ", Dx=" + (E - (E * s + S * o) + b) + ", Dy=" + (S - (E * u + S * a) + w) + ")"
                }
                if (c.indexOf("DXImageTransform.Microsoft.Matrix(") !== -1) {
                    f.filter = c.replace(T, y)
                } else {
                    f.filter = y + " " + c
                }
                if (e === 0 || e === 1)
                    if (s === 1)
                        if (o === 0)
                            if (u === 0)
                                if (a === 1)
                                    if (!g || y.indexOf("Dx=0, Dy=0") !== -1)
                                        if (!d.test(c) || parseFloat(RegExp.$1) === 100)
                                            if (c.indexOf("gradient(") === -1) {
                                                f.removeAttribute("filter")
                                            }
            },
            kt = function(e) {
                var t = this.data,
                    n = this.t.style,
                    r = t.perspective,
                    i = t.scaleX,
                    s = 0,
                    o = 0,
                    u = 0,
                    a = 0,
                    f = t.scaleY,
                    l = 0,
                    c = 0,
                    h = 0,
                    p = 0,
                    d = t.scaleZ,
                    v = 0,
                    m = 0,
                    g = 0,
                    y = r ? -1 / r : 0,
                    b = t.rotation,
                    w = t.zOrigin,
                    E = 1e5,
                    S, x, T, N, C, k, L, A, O;
                if (j) {
                    L = n.top ? "top" : n.bottom ? "bottom" : parseFloat($(this.t, "top", null, false)) ? "bottom" : "top";
                    T = $(this.t, L, null, false);
                    A = parseFloat(T) || 0;
                    O = T.substr((A + "").length) || "px";
                    t._ffFix = !t._ffFix;
                    n[L] = (t._ffFix ? A + .05 : A - .05) + O
                }
                if (b || t.skewX) {
                    T = i * Math.cos(b);
                    N = f * Math.sin(b);
                    b -= t.skewX;
                    s = i * -Math.sin(b);
                    f = f * Math.cos(b);
                    i = T;
                    a = N
                }
                b = t.rotationY;
                if (b) {
                    S = Math.cos(b);
                    x = Math.sin(b);
                    T = i * S;
                    N = a * S;
                    C = d * -x;
                    k = y * -x;
                    o = i * x;
                    l = a * x;
                    d = d * S;
                    y *= S;
                    i = T;
                    a = N;
                    h = C;
                    m = k
                }
                b = t.rotationX;
                if (b) {
                    S = Math.cos(b);
                    x = Math.sin(b);
                    T = s * S + o * x;
                    N = f * S + l * x;
                    C = p * S + d * x;
                    k = g * S + y * x;
                    o = s * -x + o * S;
                    l = f * -x + l * S;
                    d = p * -x + d * S;
                    y = g * -x + y * S;
                    s = T;
                    f = N;
                    p = C;
                    g = k
                }
                if (w) {
                    v -= w;
                    u = o * v;
                    c = l * v;
                    v = d * v + w
                }
                u = (T = (u += t.x) - (u |= 0)) ? (T * E + (T < 0 ? -.5 : .5) | 0) / E + u : u;
                c = (T = (c += t.y) - (c |= 0)) ? (T * E + (T < 0 ? -.5 : .5) | 0) / E + c : c;
                v = (T = (v += t.z) - (v |= 0)) ? (T * E + (T < 0 ? -.5 : .5) | 0) / E + v : v;
                n[Et] = "matrix3d(" + [(i * E | 0) / E, (a * E | 0) / E, (h * E | 0) / E, (m * E | 0) / E, (s * E | 0) / E, (f * E | 0) / E, (p * E | 0) / E, (g * E | 0) / E, (o * E | 0) / E, (l * E | 0) / E, (d * E | 0) / E, (y * E | 0) / E, u, c, v, r ? 1 + -v / r : 1].join(",") + ")"
            },
            Lt = function(e) {
                var t = this.data,
                    n = this.t,
                    r = n.style,
                    i, s, o, u, a, f, l, c, h;
                if (j) {
                    i = r.top ? "top" : r.bottom ? "bottom" : parseFloat($(n, "top", null, false)) ? "bottom" : "top";
                    s = $(n, i, null, false);
                    o = parseFloat(s) || 0;
                    u = s.substr((o + "").length) || "px";
                    t._ffFix = !t._ffFix;
                    r[i] = (t._ffFix ? o + .05 : o - .05) + u
                }
                if (!t.rotation && !t.skewX) {
                    r[Et] = "matrix(" + t.scaleX + ",0,0," + t.scaleY + "," + t.x + "," + t.y + ")"
                } else {
                    a = t.rotation;
                    f = a - t.skewX;
                    l = 1e5;
                    c = t.scaleX * l;
                    h = t.scaleY * l;
                    r[Et] = "matrix(" + (Math.cos(a) * c | 0) / l + "," + (Math.sin(a) * c | 0) / l + "," + (Math.sin(f) * -h | 0) / l + "," + (Math.cos(f) * h | 0) / l + "," + t.x + "," + t.y + ")"
                }
            };
        yt("transform,scale,scaleX,scaleY,scaleZ,x,y,z,rotation,rotationX,rotationY,rotationZ,skewX,skewY,shortRotation,shortRotationX,shortRotationY,shortRotationZ,transformOrigin,transformPerspective,directionalRotation", {
            parser: function(e, t, n, r, i, o, u) {
                if (r._transform) {
                    return i
                }
                var a = r._transform = Nt(e, s, true),
                    f = e.style,
                    l = 1e-6,
                    c = wt.length,
                    h = u,
                    p = {},
                    d, v, m, g, y, b, w;
                if (typeof h.transform === "string" && Et) {
                    m = f.cssText;
                    f[Et] = h.transform;
                    f.display = "block";
                    d = Nt(e, null, false);
                    f.cssText = m
                } else if (typeof h === "object") {
                    d = {
                        scaleX: rt(h.scaleX != null ? h.scaleX : h.scale, a.scaleX),
                        scaleY: rt(h.scaleY != null ? h.scaleY : h.scale, a.scaleY),
                        scaleZ: rt(h.scaleZ != null ? h.scaleZ : h.scale, a.scaleZ),
                        x: rt(h.x, a.x),
                        y: rt(h.y, a.y),
                        z: rt(h.z, a.z),
                        perspective: rt(h.transformPerspective, a.perspective)
                    };
                    w = h.directionalRotation;
                    if (w != null) {
                        if (typeof w === "object") {
                            for (m in w) {
                                h[m] = w[m]
                            }
                        } else {
                            h.rotation = w
                        }
                    }
                    d.rotation = it("rotation" in h ? h.rotation : "shortRotation" in h ? h.shortRotation + "_short" : "rotationZ" in h ? h.rotationZ : a.rotation * k, a.rotation, "rotation", p);
                    if (Tt) {
                        d.rotationX = it("rotationX" in h ? h.rotationX : "shortRotationX" in h ? h.shortRotationX + "_short" : a.rotationX * k || 0, a.rotationX, "rotationX", p);
                        d.rotationY = it("rotationY" in h ? h.rotationY : "shortRotationY" in h ? h.shortRotationY + "_short" : a.rotationY * k || 0, a.rotationY, "rotationY", p)
                    }
                    d.skewX = h.skewX == null ? a.skewX : it(h.skewX, a.skewX);
                    d.skewY = h.skewY == null ? a.skewY : it(h.skewY, a.skewY);
                    if (v = d.skewY - a.skewY) {
                        d.skewX += v;
                        d.rotation += v
                    }
                }
                y = a.z || a.rotationX || a.rotationY || d.z || d.rotationX || d.rotationY || d.perspective;
                if (!y && h.scale != null) {
                    d.scaleZ = 1
                }
                while (--c > -1) {
                    n = wt[c];
                    g = d[n] - a[n];
                    if (g > l || g < -l || L[n] != null) {
                        b = true;
                        i = new dt(a, n, a[n], g, i);
                        if (n in p) {
                            i.e = p[n]
                        }
                        i.xs0 = 0;
                        i.plugin = o;
                        r._overwriteProps.push(i.n)
                    }
                }
                g = h.transformOrigin;
                if (g || Tt && y && a.zOrigin) {
                    if (Et) {
                        b = true;
                        g = (g || $(e, n, s, false, "50% 50%")) + "";
                        n = xt;
                        i = new dt(f, n, 0, 0, i, -1, "css_transformOrigin");
                        i.b = f[n];
                        i.plugin = o;
                        if (Tt) {
                            m = a.zOrigin;
                            g = g.split(" ");
                            a.zOrigin = (g.length > 2 ? parseFloat(g[2]) : m) || 0;
                            i.xs0 = i.e = f[n] = g[0] + " " + (g[1] || "50%") + " 0px";
                            i = new dt(a, "zOrigin", 0, 0, i, -1, i.n);
                            i.b = m;
                            i.xs0 = i.e = a.zOrigin
                        } else {
                            i.xs0 = i.e = f[n] = g
                        }
                    } else {
                        tt(g + "", a)
                    }
                }
                if (b) {
                    r._transformType = y || this._transformType === 3 ? 3 : 2
                }
                return i
            },
            prefix: true
        });
        yt("boxShadow", {
            defaultValue: "0px 0px 0px 0px #999",
            prefix: true,
            color: true,
            multi: true,
            keyword: "inset"
        });
        yt("borderRadius", {
            defaultValue: "0px",
            parser: function(e, t, n, r, o, u) {
                t = this.format(t);
                var a = ["borderTopLeftRadius", "borderTopRightRadius", "borderBottomRightRadius", "borderBottomLeftRadius"],
                    f = e.style,
                    l, c, h, p, d, v, m, g, y, b, w, E, S, x, T, N;
                y = parseFloat(e.offsetWidth);
                b = parseFloat(e.offsetHeight);
                l = t.split(" ");
                for (c = 0; c < a.length; c++) {
                    if (this.p.indexOf("border")) {
                        a[c] = X(a[c])
                    }
                    d = p = $(e, a[c], s, false, "0px");
                    if (d.indexOf(" ") !== -1) {
                        p = d.split(" ");
                        d = p[0];
                        p = p[1]
                    }
                    v = h = l[c];
                    m = parseFloat(d);
                    E = d.substr((m + "").length);
                    S = v.charAt(1) === "=";
                    if (S) {
                        g = parseInt(v.charAt(0) + "1", 10);
                        v = v.substr(2);
                        g *= parseFloat(v);
                        w = v.substr((g + "").length - (g < 0 ? 1 : 0)) || ""
                    } else {
                        g = parseFloat(v);
                        w = v.substr((g + "").length)
                    }
                    if (w === "") {
                        w = i[n] || E
                    }
                    if (w !== E) {
                        x = J(e, "borderLeft", m, E);
                        T = J(e, "borderTop", m, E);
                        if (w === "%") {
                            d = x / y * 100 + "%";
                            p = T / b * 100 + "%"
                        } else if (w === "em") {
                            N = J(e, "borderLeft", 1, "em");
                            d = x / N + "em";
                            p = T / N + "em"
                        } else {
                            d = x + "px";
                            p = T + "px"
                        }
                        if (S) {
                            v = parseFloat(d) + g + w;
                            h = parseFloat(p) + g + w
                        }
                    }
                    o = vt(f, a[c], d + " " + p, v + " " + h, false, "0px", o)
                }
                return o
            },
            prefix: true,
            formatter: ft("0px 0px 0px 0px", false, true)
        });
        yt("backgroundPosition", {
            defaultValue: "0 0",
            parser: function(e, t, n, r, i, o) {
                var u = "background-position",
                    a = s || V(e, null),
                    f = this.format((a ? I ? a.getPropertyValue(u + "-x") + " " + a.getPropertyValue(u + "-y") : a.getPropertyValue(u) : e.currentStyle.backgroundPositionX + " " + e.currentStyle.backgroundPositionY) || "0 0"),
                    l = this.format(t),
                    c, h, p, d, v, m;
                if (f.indexOf("%") !== -1 !== (l.indexOf("%") !== -1)) {
                    m = $(e, "backgroundImage").replace(w, "");
                    if (m && m !== "none") {
                        c = f.split(" ");
                        h = l.split(" ");
                        M.setAttribute("src", m);
                        p = 2;
                        while (--p > -1) {
                            f = c[p];
                            d = f.indexOf("%") !== -1;
                            if (d !== (h[p].indexOf("%") !== -1)) {
                                v = p === 0 ? e.offsetWidth - M.width : e.offsetHeight - M.height;
                                c[p] = d ? parseFloat(f) / 100 * v + "px" : parseFloat(f) / v * 100 + "%"
                            }
                        }
                        f = c.join(" ")
                    }
                }
                return this.parseComplex(e.style, f, l, i, o)
            },
            formatter: tt
        });
        yt("backgroundSize", {
            defaultValue: "0 0",
            formatter: tt
        });
        yt("perspective", {
            defaultValue: "0px",
            prefix: true
        });
        yt("perspectiveOrigin", {
            defaultValue: "50% 50%",
            prefix: true
        });
        yt("transformStyle", {
            prefix: true
        });
        yt("backfaceVisibility", {
            prefix: true
        });
        yt("margin", {
            parser: lt("marginTop,marginRight,marginBottom,marginLeft")
        });
        yt("padding", {
            parser: lt("paddingTop,paddingRight,paddingBottom,paddingLeft")
        });
        yt("clip", {
            defaultValue: "rect(0px,0px,0px,0px)",
            parser: function(e, t, n, r, i, o) {
                var u, a, f;
                if (I < 9) {
                    a = e.currentStyle;
                    f = I < 8 ? " " : ",";
                    u = "rect(" + a.clipTop + f + a.clipRight + f + a.clipBottom + f + a.clipLeft + ")";
                    t = this.format(t).split(",").join(f)
                } else {
                    u = this.format($(e, this.p, s, false, this.dflt));
                    t = this.format(t)
                }
                return this.parseComplex(e.style, u, t, i, o)
            }
        });
        yt("textShadow", {
            defaultValue: "0px 0px 0px #999",
            color: true,
            multi: true
        });
        yt("autoRound,strictUnits", {
            parser: function(e, t, n, r, i) {
                return i
            }
        });
        yt("border", {
            defaultValue: "0px solid #000",
            parser: function(e, t, n, r, i, o) {
                return this.parseComplex(e.style, this.format($(e, "borderTopWidth", s, false, "0px") + " " + $(e, "borderTopStyle", s, false, "solid") + " " + $(e, "borderTopColor", s, false, "#000")), this.format(t), i, o)
            },
            color: true,
            formatter: function(e) {
                var t = e.split(" ");
                return t[0] + " " + (t[1] || "solid") + " " + (e.match(at) || ["#000"])[0]
            }
        });
        yt("float,cssFloat,styleFloat", {
            parser: function(e, t, n, r, i, s) {
                var o = e.style,
                    u = "cssFloat" in o ? "cssFloat" : "styleFloat";
                return new dt(o, u, 0, 0, i, -1, n, false, 0, o[u], t)
            }
        });
        var At = function(e) {
            var t = this.t,
                n = t.filter,
                r = this.s + this.c * e | 0,
                i;
            if (r === 100) {
                if (n.indexOf("atrix(") === -1 && n.indexOf("radient(") === -1) {
                    t.removeAttribute("filter");
                    i = !$(this.data, "filter")
                } else {
                    t.filter = n.replace(m, "");
                    i = true
                }
            }
            if (!i) {
                if (this.xn1) {
                    t.filter = n = n || "alpha(opacity=100)"
                }
                if (n.indexOf("opacity") === -1) {
                    t.filter += " alpha(opacity=" + r + ")"
                } else {
                    t.filter = n.replace(d, "opacity=" + r)
                }
            }
        };
        yt("opacity,alpha,autoAlpha", {
            defaultValue: "1",
            parser: function(e, t, n, r, i, o) {
                var u = parseFloat($(e, "opacity", s, false, "1")),
                    a = e.style,
                    f;
                t = parseFloat(t);
                if (n === "autoAlpha") {
                    f = $(e, "visibility", s);
                    if (u === 1 && f === "hidden" && t !== 0) {
                        u = 0
                    }
                    i = new dt(a, "visibility", 0, 0, i, -1, null, false, 0, u !== 0 ? "visible" : "hidden", t === 0 ? "hidden" : "visible");
                    i.xs0 = "visible";
                    r._overwriteProps.push(i.n)
                }
                if (q) {
                    i = new dt(a, "opacity", u, t - u, i)
                } else {
                    i = new dt(a, "opacity", u * 100, (t - u) * 100, i);
                    i.xn1 = n === "autoAlpha" ? 1 : 0;
                    a.zoom = 1;
                    i.type = 2;
                    i.b = "alpha(opacity=" + i.s + ")";
                    i.e = "alpha(opacity=" + (i.s + i.c) + ")";
                    i.data = e;
                    i.plugin = o;
                    i.setRatio = At
                }
                return i
            }
        });
        var Ot = function(e, t) {
                if (t) {
                    if (e.removeProperty) {
                        e.removeProperty(t.replace(y, "-$1").toLowerCase())
                    } else {
                        e.removeAttribute(t)
                    }
                }
            },
            Mt = function(e) {
                this.t._gsClassPT = this;
                if (e === 1 || e === 0) {
                    this.t.className = e === 0 ? this.b : this.e;
                    var t = this.data,
                        n = this.t.style;
                    while (t) {
                        if (!t.v) {
                            Ot(n, t.p)
                        } else {
                            n[t.p] = t.v
                        }
                        t = t._next
                    }
                    if (e === 1 && this.t._gsClassPT === this) {
                        this.t._gsClassPT = null
                    }
                } else if (this.t.className !== this.e) {
                    this.t.className = this.e
                }
            };
        yt("className", {
            parser: function(e, t, n, i, o, u, a) {
                var f = e.className,
                    l = e.style.cssText,
                    c, h, p, d, v;
                o = i._classNamePT = new dt(e, n, 0, 0, o, 2);
                o.setRatio = Mt;
                o.pr = -11;
                r = true;
                o.b = f;
                h = Q(e, s);
                p = e._gsClassPT;
                if (p) {
                    d = {};
                    v = p.data;
                    while (v) {
                        d[v.p] = 1;
                        v = v._next
                    }
                    p.setRatio(1)
                }
                e._gsClassPT = o;
                o.e = t.charAt(1) !== "=" ? t : f.replace(new RegExp("\\s*\\b" + t.substr(2) + "\\b"), "") + (t.charAt(0) === "+" ? " " + t.substr(2) : "");
                if (i._tween._duration) {
                    e.className = o.e;
                    c = G(e, h, Q(e), a, d);
                    e.className = f;
                    o.data = c.firstMPT;
                    e.style.cssText = l;
                    o = o.xfirst = i.parse(e, c.difs, o, u)
                }
                return o
            }
        });
        var _t = function(e) {
            if (e === 1 || e === 0)
                if (this.data._totalTime === this.data._totalDuration) {
                    var t = this.e === "all",
                        n = this.t.style,
                        r = t ? n.cssText.split(";") : this.e.split(","),
                        i = r.length,
                        s = u.transform.parse,
                        o;
                    while (--i > -1) {
                        o = r[i];
                        if (t) {
                            o = o.substr(0, o.indexOf(":")).split(" ").join("")
                        }
                        if (u[o]) {
                            o = u[o].parse === s ? Et : u[o].p
                        }
                        Ot(n, o)
                    }
                }
        };
        yt("clearProps", {
            parser: function(e, t, n, i, s) {
                s = new dt(e, n, 0, 0, s, 2);
                s.setRatio = _t;
                s.e = t;
                s.pr = -10;
                s.data = i._tween;
                r = true;
                return s
            }
        });
        a = "bezier,throwProps,physicsProps,physics2D".split(",");
        mt = a.length;
        while (mt--) {
            bt(a[mt])
        }
        a = n.prototype;
        a._firstPT = null;
        a._onInitTween = function(e, t, u) {
            if (!e.nodeType) {
                return false
            }
            this._target = e;
            this._tween = u;
            this._vars = t;
            P = t.autoRound;
            r = false;
            i = t.suffixMap || n.suffixMap;
            s = V(e, "");
            o = this._overwriteProps;
            var a = e.style,
                f, l, c, h, p, d, m, g, y;
            if (H)
                if (a.zIndex === "") {
                    f = $(e, "zIndex", s);
                    if (f === "auto" || f === "") {
                        a.zIndex = 0
                    }
                } if (typeof t === "string") {
                h = a.cssText;
                f = Q(e, s);
                a.cssText = h + ";" + t;
                f = G(e, f, Q(e)).difs;
                if (!q && v.test(t)) {
                    f.opacity = parseFloat(RegExp.$1)
                }
                t = f;
                a.cssText = h
            }
            this._firstPT = l = this.parse(e, t, null);
            if (this._transformType) {
                y = this._transformType === 3;
                if (!Et) {
                    a.zoom = 1
                } else if (B) {
                    H = true;
                    if (a.zIndex === "") {
                        m = $(e, "zIndex", s);
                        if (m === "auto" || m === "") {
                            a.zIndex = 0
                        }
                    }
                    if (F) {
                        a.WebkitBackfaceVisibility = this._vars.WebkitBackfaceVisibility || (y ? "visible" : "hidden")
                    }
                }
                c = l;
                while (c && c._next) {
                    c = c._next
                }
                g = new dt(e, "transform", 0, 0, null, 2);
                this._linkCSSP(g, null, c);
                g.setRatio = y && Tt ? kt : Et ? Lt : Ct;
                g.data = this._transform || Nt(e, s, true);
                o.pop()
            }
            if (r) {
                while (l) {
                    d = l._next;
                    c = h;
                    while (c && c.pr > l.pr) {
                        c = c._next
                    }
                    if (l._prev = c ? c._prev : p) {
                        l._prev._next = l
                    } else {
                        h = l
                    }
                    if (l._next = c) {
                        c._prev = l
                    } else {
                        p = l
                    }
                    l = d
                }
                this._firstPT = h
            }
            return true
        };
        a.parse = function(e, t, n, r) {
            var o = e.style,
                a, f, l, c, h, d, v, m, y, b;
            for (a in t) {
                d = t[a];
                f = u[a];
                if (f) {
                    n = f.parse(e, d, a, this, n, r, t)
                } else {
                    h = $(e, a, s) + "";
                    y = typeof d === "string";
                    if (a === "color" || a === "fill" || a === "stroke" || a.indexOf("Color") !== -1 || y && g.test(d)) {
                        if (!y) {
                            d = ut(d);
                            d = (d.length > 3 ? "rgba(" : "rgb(") + d.join(",") + ")"
                        }
                        n = vt(o, a, h, d, true, "transparent", n, 0, r)
                    } else if (y && (d.indexOf(" ") !== -1 || d.indexOf(",") !== -1)) {
                        n = vt(o, a, h, d, true, null, n, 0, r)
                    } else {
                        l = parseFloat(h);
                        v = l || l === 0 ? h.substr((l + "").length) : "";
                        if (h === "" || h === "auto") {
                            if (a === "width" || a === "height") {
                                l = et(e, a, s);
                                v = "px"
                            } else if (a === "left" || a === "top") {
                                l = K(e, a, s);
                                v = "px"
                            } else {
                                l = a !== "opacity" ? 0 : 1;
                                v = ""
                            }
                        }
                        b = y && d.charAt(1) === "=";
                        if (b) {
                            c = parseInt(d.charAt(0) + "1", 10);
                            d = d.substr(2);
                            c *= parseFloat(d);
                            m = d.replace(p, "")
                        } else {
                            c = parseFloat(d);
                            m = y ? d.substr((c + "").length) || "" : ""
                        }
                        if (m === "") {
                            m = i[a] || v
                        }
                        d = c || c === 0 ? (b ? c + l : c) + m : t[a];
                        if (v !== m)
                            if (m !== "")
                                if (c || c === 0)
                                    if (l || l === 0) {
                                        l = J(e, a, l, v);
                                        if (m === "%") {
                                            l /= J(e, a, 100, "%") / 100;
                                            if (l > 100) {
                                                l = 100
                                            }
                                            if (t.strictUnits !== true) {
                                                h = l + "%"
                                            }
                                        } else if (m === "em") {
                                            l /= J(e, a, 1, "em")
                                        } else {
                                            c = J(e, a, c, m);
                                            m = "px"
                                        }
                                        if (b)
                                            if (c || c === 0) {
                                                d = c + l + m
                                            }
                                    } if (b) {
                            c += l
                        }
                        if ((l || l === 0) && (c || c === 0)) {
                            n = new dt(o, a, l, c - l, n, 0, "css_" + a, P !== false && (m === "px" || a === "zIndex"), 0, h, d);
                            n.xs0 = m
                        } else if (o[a] === undefined || !d && (d + "" === "NaN" || d == null)) {
                            U("invalid " + a + " tween value: " + t[a])
                        } else {
                            n = new dt(o, a, c || l || 0, 0, n, -1, "css_" + a, false, 0, h, d);
                            n.xs0 = d === "none" && (a === "display" || a.indexOf("Style") !== -1) ? h : d
                        }
                    }
                }
                if (r)
                    if (n && !n.plugin) {
                        n.plugin = r
                    }
            }
            return n
        };
        a.setRatio = function(e) {
            var t = this._firstPT,
                n = 1e-6,
                r, i, s;
            if (e === 1 && (this._tween._time === this._tween._duration || this._tween._time === 0)) {
                while (t) {
                    if (t.type !== 2) {
                        t.t[t.p] = t.e
                    } else {
                        t.setRatio(e)
                    }
                    t = t._next
                }
            } else if (e || !(this._tween._time === this._tween._duration || this._tween._time === 0) || this._tween._rawPrevTime === -1e-6) {
                while (t) {
                    r = t.c * e + t.s;
                    if (t.r) {
                        r = r > 0 ? r + .5 | 0 : r - .5 | 0
                    } else if (r < n)
                        if (r > -n) {
                            r = 0
                        } if (!t.type) {
                        t.t[t.p] = r + t.xs0
                    } else if (t.type === 1) {
                        s = t.l;
                        if (s === 2) {
                            t.t[t.p] = t.xs0 + r + t.xs1 + t.xn1 + t.xs2
                        } else if (s === 3) {
                            t.t[t.p] = t.xs0 + r + t.xs1 + t.xn1 + t.xs2 + t.xn2 + t.xs3
                        } else if (s === 4) {
                            t.t[t.p] = t.xs0 + r + t.xs1 + t.xn1 + t.xs2 + t.xn2 + t.xs3 + t.xn3 + t.xs4
                        } else if (s === 5) {
                            t.t[t.p] = t.xs0 + r + t.xs1 + t.xn1 + t.xs2 + t.xn2 + t.xs3 + t.xn3 + t.xs4 + t.xn4 + t.xs5
                        } else {
                            i = t.xs0 + r + t.xs1;
                            for (s = 1; s < t.l; s++) {
                                i += t["xn" + s] + t["xs" + (s + 1)]
                            }
                            t.t[t.p] = i
                        }
                    } else if (t.type === -1) {
                        t.t[t.p] = t.xs0
                    } else if (t.setRatio) {
                        t.setRatio(e)
                    }
                    t = t._next
                }
            } else {
                while (t) {
                    if (t.type !== 2) {
                        t.t[t.p] = t.b
                    } else {
                        t.setRatio(e)
                    }
                    t = t._next
                }
            }
        };
        a._enableTransforms = function(e) {
            this._transformType = e || this._transformType === 3 ? 3 : 2
        };
        a._linkCSSP = function(e, t, n, r) {
            if (e) {
                if (t) {
                    t._prev = e
                }
                if (e._next) {
                    e._next._prev = e._prev
                }
                if (n) {
                    n._next = e
                } else if (!r && this._firstPT === null) {
                    this._firstPT = e
                }
                if (e._prev) {
                    e._prev._next = e._next
                } else if (this._firstPT === e) {
                    this._firstPT = e._next
                }
                e._next = t;
                e._prev = n
            }
            return e
        };
        a._kill = function(t) {
            var n = t,
                r, i, s;
            if (t.css_autoAlpha || t.css_alpha) {
                n = {};
                for (i in t) {
                    n[i] = t[i]
                }
                n.css_opacity = 1;
                if (n.css_autoAlpha) {
                    n.css_visibility = 1
                }
            }
            if (t.css_className && (r = this._classNamePT)) {
                s = r.xfirst;
                if (s && s._prev) {
                    this._linkCSSP(s._prev, r._next, s._prev._prev)
                } else if (s === this._firstPT) {
                    this._firstPT = r._next
                }
                if (r._next) {
                    this._linkCSSP(r._next, r._next._next, s._prev)
                }
                this._classNamePT = null
            }
            return e.prototype._kill.call(this, n)
        };
        var Dt = function(e, t, n) {
            var r, i, s, o;
            if (e.slice) {
                i = e.length;
                while (--i > -1) {
                    Dt(e[i], t, n)
                }
                return
            }
            r = e.childNodes;
            i = r.length;
            while (--i > -1) {
                s = r[i];
                o = s.type;
                if (s.style) {
                    t.push(Q(s));
                    if (n) {
                        n.push(s)
                    }
                }
                if ((o === 1 || o === 9 || o === 11) && s.childNodes.length) {
                    Dt(s, t, n)
                }
            }
        };
        n.cascadeTo = function(e, n, r) {
            var i = t.to(e, n, r),
                s = [i],
                o = [],
                u = [],
                a = [],
                f = t._internals.reservedProps,
                l, c, h;
            e = i._targets || i.target;
            Dt(e, o, a);
            i.render(n, true);
            Dt(e, u);
            i.render(0, true);
            i._enabled(true);
            l = a.length;
            while (--l > -1) {
                c = G(a[l], o[l], u[l]);
                if (c.firstMPT) {
                    c = c.difs;
                    for (h in r) {
                        if (f[h]) {
                            c[h] = r[h]
                        }
                    }
                    s.push(t.to(a[l], n, c))
                }
            }
            return s
        };
        e.activate([n]);
        return n
    }, true);
    (function() {
        var e = window._gsDefine.plugin({
                propName: "roundProps",
                priority: -1,
                API: 2,
                init: function(e, t, n) {
                    this._tween = n;
                    return true
                }
            }),
            t = e.prototype;
        t._onInitAllProps = function() {
            var e = this._tween,
                t = e.vars.roundProps instanceof Array ? e.vars.roundProps : e.vars.roundProps.split(","),
                n = t.length,
                r = {},
                i = e._propLookup.roundProps,
                s, o, u;
            while (--n > -1) {
                r[t[n]] = 1
            }
            n = t.length;
            while (--n > -1) {
                s = t[n];
                o = e._firstPT;
                while (o) {
                    u = o._next;
                    if (o.pg) {
                        o.t._roundProps(r, true)
                    } else if (o.n === s) {
                        this._add(o.t, s, o.s, o.c);
                        if (u) {
                            u._prev = o._prev
                        }
                        if (o._prev) {
                            o._prev._next = u
                        } else if (e._firstPT === o) {
                            e._firstPT = u
                        }
                        o._next = o._prev = null;
                        e._propLookup[s] = i
                    }
                    o = u
                }
            }
            return false
        };
        t._add = function(e, t, n, r) {
            this._addTween(e, t, n, n + r, t, true);
            this._overwriteProps.push(t)
        }
    })();
    window._gsDefine.plugin({
        propName: "attr",
        API: 2,
        init: function(e, t, n) {
            var r;
            if (typeof e.setAttribute !== "function") {
                return false
            }
            this._target = e;
            this._proxy = {};
            for (r in t) {
                this._addTween(this._proxy, r, parseFloat(e.getAttribute(r)), t[r], r);
                this._overwriteProps.push(r)
            }
            return true
        },
        set: function(e) {
            this._super.setRatio.call(this, e);
            var t = this._overwriteProps,
                n = t.length,
                r;
            while (--n > -1) {
                r = t[n];
                this._target.setAttribute(r, this._proxy[r] + "")
            }
        }
    });
    window._gsDefine.plugin({
        propName: "directionalRotation",
        API: 2,
        init: function(e, t, n) {
            if (typeof t !== "object") {
                t = {
                    rotation: t
                }
            }
            this.finals = {};
            var r = t.useRadians === true ? Math.PI * 2 : 360,
                i = 1e-6,
                s, o, u, a, f, l;
            for (s in t) {
                if (s !== "useRadians") {
                    l = (t[s] + "").split("_");
                    o = l[0];
                    u = parseFloat(typeof e[s] !== "function" ? e[s] : e[s.indexOf("set") || typeof e["get" + s.substr(3)] !== "function" ? s : "get" + s.substr(3)]());
                    a = this.finals[s] = typeof o === "string" && o.charAt(1) === "=" ? u + parseInt(o.charAt(0) + "1", 10) * Number(o.substr(2)) : Number(o) || 0;
                    f = a - u;
                    if (l.length) {
                        o = l.join("_");
                        if (o.indexOf("short") !== -1) {
                            f = f % r;
                            if (f !== f % (r / 2)) {
                                f = f < 0 ? f + r : f - r
                            }
                        }
                        if (o.indexOf("_cw") !== -1 && f < 0) {
                            f = (f + r * 9999999999) % r - (f / r | 0) * r
                        } else if (o.indexOf("ccw") !== -1 && f > 0) {
                            f = (f - r * 9999999999) % r - (f / r | 0) * r
                        }
                    }
                    if (f > i || f < -i) {
                        this._addTween(e, s, u, u + f, s);
                        this._overwriteProps.push(s)
                    }
                }
            }
            return true
        },
        set: function(e) {
            var t;
            if (e !== 1) {
                this._super.setRatio.call(this, e)
            } else {
                t = this._firstPT;
                while (t) {
                    if (t.f) {
                        t.t[t.p](this.finals[t.p])
                    } else {
                        t.t[t.p] = this.finals[t.p]
                    }
                    t = t._next
                }
            }
        }
    })._autoCSS = true;
    window._gsDefine("easing.Back", ["easing.Ease"], function(e) {
        var t = window.GreenSockGlobals || window,
            n = t.com.greensock,
            r = Math.PI * 2,
            i = Math.PI / 2,
            s = n._class,
            o = function(t, n) {
                var r = s("easing." + t, function() {}, true),
                    i = r.prototype = new e;
                i.constructor = r;
                i.getRatio = n;
                return r
            },
            u = e.register || function() {},
            a = function(e, t, n, r, i) {
                var o = s("easing." + e, {
                    easeOut: new t,
                    easeIn: new n,
                    easeInOut: new r
                }, true);
                u(o, e);
                return o
            },
            f = function(e, t, n) {
                this.t = e;
                this.v = t;
                if (n) {
                    this.next = n;
                    n.prev = this;
                    this.c = n.v - t;
                    this.gap = n.t - e
                }
            },
            l = function(t, n) {
                var r = s("easing." + t, function(e) {
                        this._p1 = e || e === 0 ? e : 1.70158;
                        this._p2 = this._p1 * 1.525
                    }, true),
                    i = r.prototype = new e;
                i.constructor = r;
                i.getRatio = n;
                i.config = function(e) {
                    return new r(e)
                };
                return r
            },
            c = a("Back", l("BackOut", function(e) {
                return (e = e - 1) * e * ((this._p1 + 1) * e + this._p1) + 1
            }), l("BackIn", function(e) {
                return e * e * ((this._p1 + 1) * e - this._p1)
            }), l("BackInOut", function(e) {
                return (e *= 2) < 1 ? .5 * e * e * ((this._p2 + 1) * e - this._p2) : .5 * ((e -= 2) * e * ((this._p2 + 1) * e + this._p2) + 2)
            })),
            h = s("easing.SlowMo", function(e, t, n) {
                t = t || t === 0 ? t : .7;
                if (e == null) {
                    e = .7
                } else if (e > 1) {
                    e = 1
                }
                this._p = e !== 1 ? t : 0;
                this._p1 = (1 - e) / 2;
                this._p2 = e;
                this._p3 = this._p1 + this._p2;
                this._calcEnd = n === true
            }, true),
            p = h.prototype = new e,
            d, v, m;
        p.constructor = h;
        p.getRatio = function(e) {
            var t = e + (.5 - e) * this._p;
            if (e < this._p1) {
                return this._calcEnd ? 1 - (e = 1 - e / this._p1) * e : t - (e = 1 - e / this._p1) * e * e * e * t
            } else if (e > this._p3) {
                return this._calcEnd ? 1 - (e = (e - this._p3) / this._p1) * e : t + (e - t) * (e = (e - this._p3) / this._p1) * e * e * e
            }
            return this._calcEnd ? 1 : t
        };
        h.ease = new h(.7, .7);
        p.config = h.config = function(e, t, n) {
            return new h(e, t, n)
        };
        d = s("easing.SteppedEase", function(e) {
            e = e || 1;
            this._p1 = 1 / e;
            this._p2 = e + 1
        }, true);
        p = d.prototype = new e;
        p.constructor = d;
        p.getRatio = function(e) {
            if (e < 0) {
                e = 0
            } else if (e >= 1) {
                e = .999999999
            }
            return (this._p2 * e >> 0) * this._p1
        };
        p.config = d.config = function(e) {
            return new d(e)
        };
        v = s("easing.RoughEase", function(t) {
            t = t || {};
            var n = t.taper || "none",
                r = [],
                i = 0,
                s = (t.points || 20) | 0,
                o = s,
                u = t.randomize !== false,
                a = t.clamp === true,
                l = t.template instanceof e ? t.template : null,
                c = typeof t.strength === "number" ? t.strength * .4 : .4,
                h, p, d, v, m, g;
            while (--o > -1) {
                h = u ? Math.random() : 1 / s * o;
                p = l ? l.getRatio(h) : h;
                if (n === "none") {
                    d = c
                } else if (n === "out") {
                    v = 1 - h;
                    d = v * v * c
                } else if (n === "in") {
                    d = h * h * c
                } else if (h < .5) {
                    v = h * 2;
                    d = v * v * .5 * c
                } else {
                    v = (1 - h) * 2;
                    d = v * v * .5 * c
                }
                if (u) {
                    p += Math.random() * d - d * .5
                } else if (o % 2) {
                    p += d * .5
                } else {
                    p -= d * .5
                }
                if (a) {
                    if (p > 1) {
                        p = 1
                    } else if (p < 0) {
                        p = 0
                    }
                }
                r[i++] = {
                    x: h,
                    y: p
                }
            }
            r.sort(function(e, t) {
                return e.x - t.x
            });
            g = new f(1, 1, null);
            o = s;
            while (--o > -1) {
                m = r[o];
                g = new f(m.x, m.y, g)
            }
            this._prev = new f(0, 0, g.t !== 0 ? g : g.next)
        }, true);
        p = v.prototype = new e;
        p.constructor = v;
        p.getRatio = function(e) {
            var t = this._prev;
            if (e > t.t) {
                while (t.next && e >= t.t) {
                    t = t.next
                }
                t = t.prev
            } else {
                while (t.prev && e <= t.t) {
                    t = t.prev
                }
            }
            this._prev = t;
            return t.v + (e - t.t) / t.gap * t.c
        };
        p.config = function(e) {
            return new v(e)
        };
        v.ease = new v;
        a("Bounce", o("BounceOut", function(e) {
            if (e < 1 / 2.75) {
                return 7.5625 * e * e
            } else if (e < 2 / 2.75) {
                return 7.5625 * (e -= 1.5 / 2.75) * e + .75
            } else if (e < 2.5 / 2.75) {
                return 7.5625 * (e -= 2.25 / 2.75) * e + .9375
            }
            return 7.5625 * (e -= 2.625 / 2.75) * e + .984375
        }), o("BounceIn", function(e) {
            if ((e = 1 - e) < 1 / 2.75) {
                return 1 - 7.5625 * e * e
            } else if (e < 2 / 2.75) {
                return 1 - (7.5625 * (e -= 1.5 / 2.75) * e + .75)
            } else if (e < 2.5 / 2.75) {
                return 1 - (7.5625 * (e -= 2.25 / 2.75) * e + .9375)
            }
            return 1 - (7.5625 * (e -= 2.625 / 2.75) * e + .984375)
        }), o("BounceInOut", function(e) {
            var t = e < .5;
            if (t) {
                e = 1 - e * 2
            } else {
                e = e * 2 - 1
            }
            if (e < 1 / 2.75) {
                e = 7.5625 * e * e
            } else if (e < 2 / 2.75) {
                e = 7.5625 * (e -= 1.5 / 2.75) * e + .75
            } else if (e < 2.5 / 2.75) {
                e = 7.5625 * (e -= 2.25 / 2.75) * e + .9375
            } else {
                e = 7.5625 * (e -= 2.625 / 2.75) * e + .984375
            }
            return t ? (1 - e) * .5 : e * .5 + .5
        }));
        a("Circ", o("CircOut", function(e) {
            return Math.sqrt(1 - (e = e - 1) * e)
        }), o("CircIn", function(e) {
            return -(Math.sqrt(1 - e * e) - 1)
        }), o("CircInOut", function(e) {
            return (e *= 2) < 1 ? -.5 * (Math.sqrt(1 - e * e) - 1) : .5 * (Math.sqrt(1 - (e -= 2) * e) + 1)
        }));
        m = function(t, n, i) {
            var o = s("easing." + t, function(e, t) {
                    this._p1 = e || 1;
                    this._p2 = t || i;
                    this._p3 = this._p2 / r * (Math.asin(1 / this._p1) || 0)
                }, true),
                u = o.prototype = new e;
            u.constructor = o;
            u.getRatio = n;
            u.config = function(e, t) {
                return new o(e, t)
            };
            return o
        };
        a("Elastic", m("ElasticOut", function(e) {
            return this._p1 * Math.pow(2, -10 * e) * Math.sin((e - this._p3) * r / this._p2) + 1
        }, .3), m("ElasticIn", function(e) {
            return -(this._p1 * Math.pow(2, 10 * (e -= 1)) * Math.sin((e - this._p3) * r / this._p2))
        }, .3), m("ElasticInOut", function(e) {
            return (e *= 2) < 1 ? -.5 * this._p1 * Math.pow(2, 10 * (e -= 1)) * Math.sin((e - this._p3) * r / this._p2) : this._p1 * Math.pow(2, -10 * (e -= 1)) * Math.sin((e - this._p3) * r / this._p2) * .5 + 1
        }, .45));
        a("Expo", o("ExpoOut", function(e) {
            return 1 - Math.pow(2, -10 * e)
        }), o("ExpoIn", function(e) {
            return Math.pow(2, 10 * (e - 1)) - .001
        }), o("ExpoInOut", function(e) {
            return (e *= 2) < 1 ? .5 * Math.pow(2, 10 * (e - 1)) : .5 * (2 - Math.pow(2, -10 * (e - 1)))
        }));
        a("Sine", o("SineOut", function(e) {
            return Math.sin(e * i)
        }), o("SineIn", function(e) {
            return -Math.cos(e * i) + 1
        }), o("SineInOut", function(e) {
            return -.5 * (Math.cos(Math.PI * e) - 1)
        }));
        s("easing.EaseLookup", {
            find: function(t) {
                return e.map[t]
            }
        }, true);
        u(t.SlowMo, "SlowMo", "ease,");
        u(v, "RoughEase", "ease,");
        u(d, "SteppedEase", "ease,");
        return c
    }, true)
});
