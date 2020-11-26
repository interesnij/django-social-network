!function(e){if("object"==typeof exports&&"undefined"!=typeof module)module.exports=e();else if("function"==typeof define&&define.amd)define([],e);else{("undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:this).channels=e()}}(function(){return function i(c,s,a){function u(o,e){if(!s[o]){if(!c[o]){var n="function"==typeof require&&require;if(!e&&n)return n(o,!0);if(f)return f(o,!0);var t=new Error("Cannot find module '"+o+"'");throw t.code="MODULE_NOT_FOUND",t}var r=s[o]={exports:{}};c[o][0].call(r.exports,function(e){var n=c[o][1][e];return u(n||e)},r,r.exports,i,c,s,a)}return s[o].exports}for(var f="function"==typeof require&&require,e=0;e<a.length;e++)u(a[e]);return u}({1:[function(e,n,o){"use strict";function f(e){return e&&2===e.CLOSING}function h(){return{constructor:"undefined"!=typeof WebSocket&&f(WebSocket)?WebSocket:null,maxReconnectionDelay:1e4,minReconnectionDelay:1500,reconnectionDelayGrowFactor:1.3,connectionTimeout:4e3,maxRetries:1/0,debug:!1}}function b(n,e,o){Object.defineProperty(e,o,{get:function(){return n[o]},set:function(e){n[o]=e},enumerable:!0,configurable:!0})}function w(e){return e.minReconnectionDelay+Math.random()*e.minReconnectionDelay}var E=["onopen","onclose","onmessage","onerror"],k=function(o,t,n){var l,r,i=this;void 0===n&&(n={});var d=0,c=0,v=!0,y=null,p={};if(!(this instanceof k))throw new TypeError("Failed to construct 'ReconnectingWebSocket': Please use the 'new' operator");var s=h();if(Object.keys(s).filter(function(e){return n.hasOwnProperty(e)}).forEach(function(e){return s[e]=n[e]}),!f(s.constructor))throw new TypeError("Invalid WebSocket constructor. Set `options.constructor`");function a(e,o){return setTimeout(function(){var n=new Error(o);n.code=e,Array.isArray(p.error)&&p.error.forEach(function(e){return(0,e[0])(n)}),l.onerror&&l.onerror(n)},0)}function m(){u("close"),u("retries count:",++c),c>s.maxRetries?a("EHOSTDOWN","Too many failed connection attempts"):(d=d?function(e,n){var o=n*e.reconnectionDelayGrowFactor;return o>e.maxReconnectionDelay?e.maxReconnectionDelay:o}(s,d):w(s),u("reconnectDelay:",d),v&&setTimeout(e,d))}var u=s.debug?function(){for(var e=[],n=0;n<arguments.length;n++)e[n-0]=arguments[n];return console.log.apply(console,["RWS:"].concat(e))}:function(){},e=function(){u("connect");var e=l;for(var n in l=new s.constructor(o,t),r=setTimeout(function(){u("timeout"),l.close(),a("ETIMEDOUT","Connection timeout")},s.connectionTimeout),u("bypass properties"),l)["addEventListener","removeEventListener","close","send"].indexOf(n)<0&&b(l,i,n);l.addEventListener("open",function(){clearTimeout(r),u("open"),d=w(s),u("reconnectDelay:",d),c=0}),l.addEventListener("close",m),function(r,n,e){Object.keys(e).forEach(function(t){e[t].forEach(function(e){var n=e[0],o=e[1];r.addEventListener(t,n,o)})}),n&&E.forEach(function(e){r[e]=n[e]})}(l,e,p),l.onclose=l.onclose||y,y=null};u("init"),e(),this.close=function(e,n,o){void 0===e&&(e=1e3),void 0===n&&(n="");var t=void 0===o?{}:o,r=t.keepClosed,i=void 0!==r&&r,c=t.fastClose,s=void 0===c||c,a=t.delay,u=void 0===a?0:a;if(u&&(d=u),v=!i,l.close(e,n),s){var f={code:e,reason:n,wasClean:!0};m(),l.removeEventListener("close",m),Array.isArray(p.close)&&p.close.forEach(function(e){var n=e[0],o=e[1];n(f),l.removeEventListener("close",n,o)}),l.onclose&&(y=l.onclose,l.onclose(f),l.onclose=null)}},this.send=function(e){l.send(e)},this.addEventListener=function(e,n,o){Array.isArray(p[e])?p[e].some(function(e){return e[0]===n})||p[e].push([n,o]):p[e]=[[n,o]],l.addEventListener(e,n,o)},this.removeEventListener=function(e,n,o){Array.isArray(p[e])&&(p[e]=p[e].filter(function(e){return e[0]!==n})),l.removeEventListener(e,n,o)}};n.exports=k},{}],2:[function(e,n,o){"use strict";Object.defineProperty(o,"__esModule",{value:!0}),o.WebSocketBridge=void 0;var t=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var o=arguments[n];for(var t in o)Object.prototype.hasOwnProperty.call(o,t)&&(e[t]=o[t])}return e},r=function(e,n,o){return n&&i(e.prototype,n),o&&i(e,o),e};function i(e,n){for(var o=0;o<n.length;o++){var t=n[o];t.enumerable=t.enumerable||!1,t.configurable=!0,"value"in t&&(t.writable=!0),Object.defineProperty(e,t.key,t)}}var c,s=e("reconnecting-websocket"),a=(c=s)&&c.__esModule?c:{default:c};var u=(r(f,[{key:"connect",value:function(e,n,o){var t=void 0,r=("https:"===window.location.protocol?"wss":"ws")+"://"+window.location.host;t=void 0===e?r:"/"==e[0]?r+e:e,this.socket=new a.default(t,n,o)}},{key:"listen",value:function(e){var i=this;this.default_cb=e,this.socket.onmessage=function(e){var n=JSON.parse(e.data),o=void 0,t=void 0;if(void 0!==n.stream){o=n.payload,t=n.stream;var r=i.streams[t];r&&r(o,t)}else o=n,t=null,i.default_cb&&i.default_cb(o,t)}}},{key:"demultiplex",value:function(e,n){this.streams[e]=n}},{key:"send",value:function(e){this.socket.send(JSON.stringify(e))}},{key:"stream",value:function(o){var t=this;return{send:function(e){var n={stream:o,payload:e};t.socket.send(JSON.stringify(n))}}}}]),f);function f(e){!function(e,n){if(!(e instanceof n))throw new TypeError("Cannot call a class as a function")}(this,f),this.socket=null,this.streams={},this.default_cb=null,this.options=t({},e)}o.WebSocketBridge=u},{"reconnecting-websocket":1}]},{},[2])(2)});

request_user_id = document.body.querySelector(".userpic").getAttribute("data-pk");
notify = document.body.querySelector(".new_unread_notify");
notify.querySelector(".tab_badge") ? (notify_count = notify.querySelector(".tab_badge").innerHTML.replace(/\s+/g, ''), notify_count = notify_count*1) : notify_count = 0;

ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
ws_path = ws_scheme + '://' + "раса.рус:8002" + "/notify/";
webSocket = new channels.WebSocketBridge();
webSocket.connect(ws_path);


webSocket.socket.onmessage = function(e){ console.log(e.data); };
webSocket.socket.onopen = function () {
  console.log("Соединение установлено!");
};

webSocket.socket.onclose = function () {
  console.log("Соединение прервано...");
};
tab_span = document.createElement("span");
tab_span.classList.add("tab_badge", "badge-danger");


function case_user_notify() {
  console.log('case_user_notify');
  new Audio('/static/audio/new_event.mp3').play();
}
function case_post_notify(uuid) {
    if (document.body.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' )){
      post = document.body.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' );
       post_update_votes(document.body.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' ), uuid);
       soundPlayer.play('/static/audio/new_event.mp3')
       var audioElement;
       if(!audioElement) {
         audioElement = document.createElement('audio');
         audioElement.innerHTML = '<source src="' + '/static/audio/new_event.mp3'+ '" type="audio/mpeg" />'
       }
       audioElement.play();
    }
}


webSocket.listen(function (event) {
  switch (event.key) {
      case "notification":
        console.log("notification");
        if (event.recipient_id == request_user_id){

          if (event.name == "user_notify"){ case_user_notify() }
          else if (event.name == "post_notify"){ case_post_notify(event.post_id) }

          notify_count = notify_count * 1;
          notify_count += 1;
          tab_span.innerHTML = notify_count;
          notify.innerHTML = "";
          notify.append(tab_span);
        }
        break;

      case "create_item":
        console.log("create_item");
        if (event.creator_id != request_user_id){
          if (event.name == "post_create"){
            case_post_create(request_user_id, event.post_id)
          }
          else {
            console.log("not post_create")
          }
        }
        break;

    case "message":
      if (event.creator_id === request_user_id) {
        console.log("Вы создатель сообщения")
      };
      console.log(event.reseiver_ids);
      console.log(event.message_id);
      break;

    default:
      console.log('error: ', event);
      break;
  }
})
